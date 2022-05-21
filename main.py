import requests
import ratelimit
from ratelimit import sleep_and_retry
import csv
import json
import enlighten

manager = enlighten.get_manager()

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

    user_counter = manager.counter(total=len(mf_users), desc="Users".rjust(12), unit="Users", color="blue", leave=False)
    for user in mf_users:
        fetch_user_details(user)
        user_counter.update()
    manager.stop()


def process_mf_files():
    print('hi')


if __name__ == '__main__':
    print('hi')

