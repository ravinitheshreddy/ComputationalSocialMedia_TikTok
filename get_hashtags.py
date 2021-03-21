from TikTokApi import TikTokApi
import pandas as pd
import json
from tqdm import tqdm 

verifyFp = "verify_kmj67wcs_9tsleZij_ZMtu_496d_9aJ1_vmKel1oWpLTW"

# find users -> their tiktoks -> the hashtags -> top videos -> dict
api = TikTokApi.get_instance(custom_verifyFp=verifyFp, use_test_endpoints=True)

# Create list of hashtags 

# Find some popular users

N_USERS_PER_IT = 30
PAGE_SIZE = 1
FIRST_USER = '6745191554350760966'

set_users = set(FIRST_USER)

users = api.get_suggested_users_by_id(count=N_USERS_PER_IT)

users_id = set([u['id'] for u in users])
set_users = set([u['subTitle'].replace('@', '') for u in users])
set_users.update(set_users)


for uid in users_id.copy():
    users = api.get_suggested_users_by_id(userId = uid, count=N_USERS_PER_IT)
    ids = set([u['id'] for u in users])
    users_id.update(ids)
    users_names = set([u['subTitle'].replace('@', '') for u in users])
    set_users.update(users_names)

print('--- The list of users has been created')

set_hashtags = set()

count = 0

print('--- Creating the list of hashtags, takes some time ...')

for uid in tqdm(users_id):
    vids = api.get_user(uid, page_size=PAGE_SIZE)
    for i in range(len(vids['items'])):
        set_hashtags.update([t['title'] for t in vids['items'][i]['challenges']])

print('--- Number of hashtags found : ',  len(set_hashtags))

with open("hashtags.txt", "w") as fp:
    json.dump(str(set_hashtags), fp)

print('--- List of hashtags saved as hashtags.txt')