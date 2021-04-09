from TikTokApi import TikTokApi
import pandas as pd
import json
from tqdm import tqdm 
from datetime import datetime

verifyFp = "verify_kmj67wcs_9tsleZij_ZMtu_496d_9aJ1_vmKel1oWpLTW"

hashtags = ['biden2020' , 'trump2020', 'biden', 'trump', 'election2020', '2020election', 'donaldtrump', 'joebiden', 'maga', 'trumpout', 'democrat', 'republican', 'trumpvsbiden', 'bidenvstrump', 'voteblue', 'votered']

api = TikTokApi.get_instance(custom_verifyFp=verifyFp, use_test_endpoints=True)

def all_videos_one_hashtag(h):
    print('Currently extracting #' + h)
    tktks = []
    vids = api.by_hashtag(hashtag = h, count=200)
    for v in vids:
        hashtags = set([c['title'] for c in v['challenges']])
        date = datetime.utcfromtimestamp(int(v['createTime'])).strftime('%Y-%m-%d %H:%M:%S')
        if datetime.strptime(date, '%Y-%m-%d %H:%M:%S').year == 2020:
            v_metadata = {'video_id': hash(v['id']),'hashtags': hashtags,'date': date,'user_id': hash(v['author']['id']),'n_likes':v['stats']['diggCount'], 'n_comments':v['stats']['commentCount'],'n_shared':v['stats']['shareCount'], 'sound': v['music']['title']}
            tktks.append(v_metadata)
    return tktks

tktk_df = pd.DataFrame()

for h in hashtags:
    tktk_df = tktk_df.append(pd.DataFrame(all_videos_one_hashtag(h)))

print('Length before dropping duplicates : ', len(tktk_df.index)) #2641
tktk_df = tktk_df.drop_duplicates(subset=['video_id'])
print('Length after dropping duplicates : ', len(tktk_df.index)) # 2096

tktk_df.to_csv('tiktoks.csv')
