import json
import os

from aiogram.types import User
from brawlstats import Client

from decouple import config

bw_token = config('BRAWL_STARS_TOKEN')

client = Client(bw_token)

FILE_BASE = 'base.json'
if not os.path.exists(FILE_BASE):
    with open(FILE_BASE, 'w') as f:
        json.dump([], f, indent=4, ensure_ascii=False)
    

all_users = json.load(open(FILE_BASE))


def crete_user(data, user: User):
    user_data = {
        'id': user.id,
        'tag_bw': data['tag'],
        'name': data['name'],
        'birthday': data['birthday'],
        'phone': data['phone'],
        'location': dict(data['location']),
        'email': data['email'],
        'gems': 599,
    }
    all_users.append(user_data)
    with open(FILE_BASE, 'w', encoding='utf-8') as f:
        json.dump(all_users, f, indent=4, ensure_ascii=False)
    return user_data

def get_user(user: User):
    for user_data in all_users:
        if user_data['id'] == user.id:
            return user_data
    return None


def bw_info_by_nickname(nickname):
    try:
        player = client.get_player(nickname)
        return player
    except:
        return None
        
def check_email(email):
    from re import fullmatch
    return fullmatch(r"[^@]+@[^@]+\.[^@]+", email) is not None
    
def gen_code_gem():
    from string import ascii_uppercase, digits
    from random import choice
    return ''.join(choice(ascii_uppercase + digits) for _ in range(10))


# if __name__ == '__main__':
#     print(bw_info_by_nickname('28j9ur9q2').items())
#     print(bw_info_by_nickname('28j9ur9q2').trophies)