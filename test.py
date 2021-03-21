from TikTokApi import TikTokApi
import pandas as pd
import json
from tqdm import tqdm 

verifyFp = "verify_kmeyrnv7_Uzdyy0Nv_PLmB_45mB_9aXW_VZyRutybEpD8"
N_HASHTAGS = 20
N_USERS = 50

# find suggested hashtags -> find top users in each hashtag

# Tiktok api
api = TikTokApi.get_instance(custom_verifyFp=verifyFp, use_test_endpoints=True)

# Find hashtags
hashtags = api.get_suggested_hashtags_by_id(custom_verifyFp=verifyFp, count=N_HASHTAGS)
hashtags = [h['title'].replace('#', '') for h in hashtags]

dict_tt = {}

print(hashtags)

# Find top N users in hashtag
for h in hashtags:
    tiktoks = api.by_hashtag(h, count=N_USERS)
    for j in range(len(tiktoks)):
        user = tiktoks[j]['author']['id']
        if user in dict_tt:
            dict_tt[user][h] = dict_tt[user].get(h, 0) + 1 
        else:
            dict_tt[user] = {h : 1}

with open('users.json', 'w') as json_file:
    json.dump(dict_tt, json_file)