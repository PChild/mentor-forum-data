import requests
import ratelimit
from ratelimit import sleep_and_retry
import csv
import json
import enlighten
import os


@sleep_and_retry
@ratelimit.limits(calls=3, period=1)
def fetch_user_details(user):
    user_profile = "https://www.chiefdelphi.com/u/{user}.json"
    url = user_profile.format(user=user)
    try:
        profile = requests.get(url).json()
        with open('mf_users/' + user + '.json', 'w') as f:
            json.dump(profile, f)
    except:
        print("Problem:", url)


def fetch_user_files(users_csv='mf_users.csv'):
    mf_users = []
    with open(users_csv, newline='') as infile:
        for row in csv.reader(infile):
            mf_users.append(row[0])

    user_counter = enlighten.Counter(total=len(mf_users), desc="Users", unit="Users", color="blue", leave=False)
    for user in mf_users:
        fetch_user_details(user)
        user_counter.update()
    user_counter.close()


def process_mf_files(dir='mf_users/'):
    mf_data = []
    file_cnt = enlighten.Counter(total=len(os.listdir(dir)), desc="Users", unit="Users", color="blue", leave=False)
    for file in os.listdir(dir):
        try:
            user = json.load(open(dir + file))['user']
            if 'profile_hidden' in user.keys():
                mf_data.append({
                    'username': user['username'],
                    'name': user['name'],
                    'hidden': True
                })
            else:
                mf_data.append({
                    'username': user['username'],
                    'name': user['name'],
                    'hidden': False,
                    'team': user['user_fields']['1'],
                    'location': user['location'] if 'location' in user.keys() else '',
                    'rookie_year': user['user_fields']['2'],
                    'created': user['created_at'],
                    'seen': user['last_seen_at'],
                    'posted': user['last_posted_at'],
                    'level': user['trust_level'],
                    'reading_time': user['time_read'],
                    'profile_views': user['profile_view_count']
                })
        except:
            print("Problem:", file)
        file_cnt.update()

    with open('mf_data.csv', 'w', newline='') as outfile:
        dict_writer = csv.DictWriter(outfile, mf_data[0].keys())
        dict_writer.writeheader()
        dict_writer.writerows(mf_data)


if __name__ == '__main__':
    process_mf_files()

