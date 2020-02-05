from glob import glob
from instabot import Bot
import os
import sys


def save_followers_following(username, k):
    user_id = bot.get_user_id_from_username(username)
    for f in ['followers', 'followings']:
        suffix = f if 'followers' else 'following'
        bot.api.get_total_followers_or_followings(
            user_id=user_id,
            to_file=f'{output_folder}{k}_{username}_{suffix}.txt',
            usernames=True,
            which=f
        )

def gen_user_list(k):
    user_list = []
    files = glob(output_folder+str(k)+'_*')
    for file in files:
        with open(file) as f:
            lst = f.read().splitlines() 
        user_list = user_list + lst
    return user_list

def get_visited(output_folder):
    cut0 = len(output_folder) + 2
    cut1 = len('_followers.txt')
    files = glob(output_folder+'*_*')
    files = [f[cut0:-cut1] for f in files]
    return set(files)


################
    
if __name__=='__main__':
    if len(sys.argv) < 2:
        print('usage: python {} <initial user> <n levels: optional>'.format(sys.argv[0]))
        exit()
        
    user_init = sys.argv[1]
    n_levels = sys.argv[2] if len(sys.argv)==3 else 1
    output_folder = f'{user_init}/'
    
    bot = Bot()
    login_info = open('userinfo', 'r').read().splitlines()
    bot.login(username=login_info[0], password=login_info[1])
    
    if not os.path.exists(output_folder):
        os.mkdir(output_folder)
    
    k = 0
    visited = get_visited(output_folder)
    if user_init not in visited:
        save_followers_following(user_init, k)
    
    while k < n_levels:
        users = gen_user_list(k)
        k = k+1
        for u in users:
            if u not in visited:
                save_followers_following(u, k)
                visited.add(u)