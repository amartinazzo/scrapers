from glob import glob
from instabot import Bot
import json
import os
import sys
from time import sleep, time


if len(sys.argv) < 2:
    print('usage: python {} <user_list_file>'.format(sys.argv[0]))
    exit()
    

#######

output_folder = 'posts/'
user_list_file = 'restaurants.csv'    

if not os.path.exists(output_folder):
    os.makedirs(output_folder)

with open(user_list_file, 'r') as f:
    users = list(f)
users = [u.rstrip() for u in users]

files = glob('metadata_restaurants/*')

j = json.load(open(files[0], 'r'))

j['graphql']['user']['edge_owner_to_timeline_media']['count']

#get_total_user_medias

bot = Bot()
login_info = open('userinfo', 'r').read().splitlines()
bot.login(username=login_info[0], password=login_info[1])

for u in users:
    sleep(600) # 10 min
    