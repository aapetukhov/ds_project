import config
import vk_api
import pandas as pd
import numpy as np

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

def get_comments(group_id, access_token, count, offset):
    


