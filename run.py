from collections import defaultdict
import datetime

import configargparse as cap
import tweepy
from tqdm import tqdm
import pandas as pd

argparser = cap.ArgParser(default_config_files=['keys.yml'])
argparser.add('-c', is_config_file=True, help='config file path')
argparser.add('--api', env_var='BOT_API')
argparser.add('--api-secret', env_var='BOT_API_SECRET')
argparser.add('--access', env_var='BOT_ACCESS')
argparser.add('--access-secret', env_var='BOT_ACCESS_SECRET')

args = argparser.parse_args()

# Authenticate to Twitter
auth = tweepy.OAuthHandler(args.api, args.api_secret)
auth.set_access_token(args.access, args.access_secret)

api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

try:
    api.verify_credentials()
    print("Authentication OK")
except:
    print("Error during authentication")

# # get current percentage
data = pd.read_csv('https://raw.githubusercontent.com/owid/covid-19-data/master/public/data/vaccinations/vaccinations.csv', parse_dates=['date'])

data_filtered = data[data.location == 'India']
data_filtered = data_filtered[data_filtered.date == data_filtered.date.max()]
# print(data_filtered.to_json())

# take last item in case dataset contains multiple items this day:
one_dose_percentage = data_filtered.iloc[-1].people_vaccinated_per_hundred
full_dose_percentage = data_filtered.iloc[-1].people_fully_vaccinated_per_hundred


one_dose_bar = tqdm(initial=one_dose_percentage, total=100., bar_format='|{bar:12}| {percentage:3.2f}% ', ascii=False)
full_dose_bar = tqdm(initial=full_dose_percentage, total=100., bar_format='|{bar:12}| {percentage:3.2f}% ', ascii=False)

one_dose_bar_string = one_dose_bar.__str__()

full_dose_bar_string = full_dose_bar.__str__()

one_dose_bar.close()
full_dose_bar.close()
tweet_string = "1st dose/100: " + one_dose_bar_string[:-7].replace(' ', '\u3000') + one_dose_bar_string[-7:] + '\n' + "2nd dose/100: " + full_dose_bar_string[:-7].replace(' ', '\u3000') + full_dose_bar_string[-7:] + '\n'

print("final string:")
print(tweet_string)
print("tweet length:", len(tweet_string))

# and update on twitter
api.update_status(tweet_string)
