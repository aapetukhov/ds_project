import config
import vk_api
import pandas as pd
import numpy as np
import datetime

login = config.LOGIN
password = config.PASSWORD
token = config.TOKEN

lentach_id = '-29534144'
rbc_id = '-25232578'
gosduma_id = '-138347372'
mash_id = '-112510789'

lentach_url = f'https://api.vk.com/method/wall.get?owner_id=-29534144&fields=bdate&access_token={token}&v=5.131'
rbc_url = f'https://api.vk.com/method/wall.get?owner_id=-25232578&fields=bdate&access_token={token}&v=5.131'
gosduma_url = f'https://api.vk.com/method/wall.get?owner_id=-138347372&fields=bdate&access_token={token}2&v=5.131'
mash_url = f'https://api.vk.com/method/wall.get?owner_id=-112510789&fields=bdate&access_token={token}2&v=5.131'

session = vk_api.VkApi(token = token)
vk = session.get_api()

def get_posts_ids(group_id, access_token = token, offset = 0):
  posts_json = session.method('wall.get', {'owner_id': group_id,
                                           'offset': offset,
                                           'count': 100})
  
  posts_ids = [posts_json['items'][i]['id'] for i in range(100)]
  oldest_post_date = posts_json['items'][0]['date']
  
  return posts_ids, oldest_post_date

def get_comments_info(group_id, post_id, access_token = token, offset = 0):
    comments_json = session.method('wall.getComments', {'owner_id': group_id,
                                                        'post_id': post_id,
                                                        'offset': offset,
                                                        'count': 100})
    #получаем информацию о комментариях
    count = len(comments_json['items'])

    comments_texts = [comments_json['items'][i]['text'] for i in range(count)]
    comments_timestamps = [comments_json['items'][i]['date'] for i in range(count)]
    comments_dates = [datetime.datetime.fromtimestamp(ts).strftime('%Y/%m/%d') for ts in comments_timestamps]

    #получаем информацию об авторах комментариев

    authors_ids = [comments_json['items'][i]['id'] for i in range(count)]
    authors_info = session.method('users.get', {'user_ids': ','.join([str(num) for num in authors_ids]),
                                                   'fields': 'country, city'})
    authors_countries = []
    authors_cities = []

    for i in range(count):
      try:
        #authors_countries.append(authors_info[i]['country']['title'])
        authors_cities.append(authors_info[i]['city']['title'])
      
      except:
        #authors_countries.append(None)
        authors_cities.append(None)

    comments_info = pd.DataFrame({'authors_id': authors_ids, 
                                  'comment_text': comments_texts,
                                  'authors_city': authors_cities,
                                  'group_id': group_id}, index = comments_dates)
    return comments_info