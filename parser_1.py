import config
import vk_api
import pandas as pd
import numpy as np
import datetime
from time import sleep 

token = config.TOKEN

lentach_id = '-29534144'
rbc_id = '-25232578'
gosduma_id = '-138347372'
mash_id = '-112510789'

session = vk_api.VkApi(token = token)
vk = session.get_api()

def get_posts_ids(group_id, access_token = token, offset = 0):
  posts_json = session.method('wall.get', {'owner_id': group_id,
                                           'offset': offset,
                                           'count': 100})
  
  posts_ids = [posts_json['items'][i]['id'] for i in range(100)]
  oldest_post_date = posts_json['items'][-1]['date']
  
  return posts_ids, oldest_post_date #возвращает список id постов и даты последнего поста

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

def get_all_comments_info(group_id, post_id, access_token = token):
  offset = 0
  all_comments_df = pd.DataFrame()

  while True:
    current_comments_df = get_comments_info(group_id, post_id, access_token, offset)

    if current_comments_df.empty:
      break

    all_comments_df = pd.concat([all_comments_df, current_comments_df])
    offset += 100

  return all_comments_df

def parse_comments(group_id):
  posts_offset = 0
  ids_offset = 0
  posts_ids = []
  stop_date = 1686250527 #2021-10-06

  while True:
    sleep(1)
    posts = get_posts_ids(group_id = group_id, access_token = token, offset = posts_offset)
    oldest_date = posts[-1] #дата последнего поста
    posts_ids.extend(posts[0])

    if oldest_date < stop_date:
      break

    posts_offset += 100

  all_comments_df = pd.DataFrame()

  for id in posts_ids:
    current_comments_df = get_all_comments_info(group_id, id, access_token = token)

    all_comments_df = pd.concat([all_comments_df, current_comments_df])
    ids_offset += 100

  return all_comments_df