from TikTokApi import TikTokApi
import pandas as pd
import json
from tqdm import tqdm 
from datetime import datetime

# Tiktok key
verifyFp = "verify_kmj67wcs_9tsleZij_ZMtu_496d_9aJ1_vmKel1oWpLTW"

# List of hashtags - basis
hashtags = ['biden2020' , 'trump2020', 'biden', 'trump', 'election2020', '2020election', 'donaldtrump', 'joebiden', 'maga', 'trumpout', 'democrat', 'republican', 'trumpvsbiden', 'bidenvstrump', 'voteblue', 'votered']

N_VIDEOS = 500

VIDEO_YEAR = 2020

# Connect to API
api = TikTokApi.get_instance(custom_verifyFp=verifyFp, use_test_endpoints=True)

def all_videos_one_hashtag(h):
    ''' Gets all the top N_VIDEOS videos under the hashtags'''
    print('Currently extracting #' + h)
    tktks = []
    vids = api.by_hashtag(hashtag = h, count=N_VIDEOS)
    for v in vids:
        # Store with date
        hashtags = set([c['title'] for c in v['challenges']])
        date = datetime.utcfromtimestamp(int(v['createTime'])).strftime('%Y-%m-%d %H:%M:%S')
        if datetime.strptime(date, '%Y-%m-%d %H:%M:%S').year == VIDEO_YEAR:
            v_metadata = {'video_id': hash(v['id']),'hashtags': hashtags,'date': date}
            tktks.append(v_metadata)
    return tktks

tktk_df = pd.DataFrame()

for h in hashtags:
    # Get all the videos for every hashtag in the list 
    tktk_df = tktk_df.append(pd.DataFrame(all_videos_one_hashtag(h)))

print('Length before dropping duplicates : ', len(tktk_df.index)) #2641 #1317
# Remove duplicates
tktk_df = tktk_df.drop_duplicates(subset=['video_id'])
print('Length after dropping duplicates : ', len(tktk_df.index)) #2096 #1042

tktk_df.to_csv('tiktoks_500.csv')
