import json
import os
from pandas import read_csv
import requests
from scrape import get_users
from time import sleep
import sys


def get_metadata(username, output_folder):
    response = requests.get(f'http://www.instagram.com/{username}?__a=1')
    if response.status_code != 200:
        print(f'{username} -> status code:', response.status_code)
        return None
    try:
        data = json.loads(response.content)
    except:
        print(f'{username} -> could not load json')
        return None
    with open(f'{output_folder}{username}.json', 'w', encoding='utf8') as f:
        json.dump(data, f)
    return data


def write_metadata_to_file(username, data, file):
    followed_by = data['graphql']['user']['edge_followed_by']['count']
    follow = data['graphql']['user']['edge_follow']['count']
    with open(file, 'a') as f:
        f.write(f'{username},{followed_by},{follow}\n')


################

if len(sys.argv)<2:
    print('usage: python {} <input_folder>'.format(sys.argv[0]))
    exit(1)


input_folder = sys.argv[1]

k = 0
metadata_file = 'metadata.csv'
output_folder = 'metadata/'

if not os.path.exists(output_folder):
    os.mkdir(output_folder)

users = get_users(k, input_folder)

df = read_csv(metadata_file)
users_visited = set(df['username'].values)
users = users - users_visited
del df

print("nr users", len(users))

for ix, u in enumerate(users):
    print(f'reading {u}')
    data = get_metadata(u, output_folder)
    if data is not None:
        write_metadata_to_file(u, data, metadata_file)
    sleep(1)
    if ix%100==0:
        print('################\nsleep more', ix)
        sleep(10)