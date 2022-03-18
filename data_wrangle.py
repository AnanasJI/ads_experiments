import pandas as pd
from typing import Dict
import json
import tweepy as tw
import datetime
import os
import requests
import re


def save_tweet(tweet_json, list_to_save):
    list_to_save.append(tweet_json)


# your Twitter API key and API secret
with open("auth.json", "r") as f:
    data = json.load(f)
    api_key = data["API_K"]
    api_secret = data["API_S"]

# authenticate
auth = tw.OAuthHandler(api_key, api_secret)
api = tw.API(auth, wait_on_rate_limit=True)

country = "Canada"

# get country id from file
with open("country_ids.json", "r") as f:
    country_id = json.load(f)[country]

search_time = datetime.datetime(2019, 1, 22)
end_time = datetime.datetime.now()
end_time = datetime.datetime(2019, 2, 5)
data_folder = "raw_data"
search_term = "trudeau"
save_folder = "filtered_data"
items = 0

while(search_time < end_time):
    end_time_interval = search_time + datetime.timedelta(days=7)

    file_timestamp = search_time.strftime("%Y-%m-%d")
    file_timestamp_end = end_time_interval.strftime("%Y-%m-%d")
    filename = f"{search_term}_{file_timestamp}_{file_timestamp_end}.json"
    path_name_read = os.path.join(data_folder, filename)
    path_name_save = os.path.join(save_folder, filename)

    try:
        with open(path_name_read, "r", encoding="utf8") as f:
            raw_data = json.load(f)
    except:
        raw_data = []
        for line in open(path_name_read, "r", encoding="utf8"):
            raw_data.append(json.loads(line))

    list_filtered_results = []

    # look-up each tweet id
    for line in raw_data:
        if items >= 200:
            break

        id = line["id"]

        try:
            status = api.get_status(id, tweet_mode="extended")

            if status.lang == "en":
                if status.place and status.place.country == country:
                    save_tweet(status._json, list_filtered_results)
                elif status.geo and status.geo.place:
                    print(status.geo.place.__dict__)
                    if status.geo.place.country == country:
                        save_tweet(status._json, list_filtered_results)
                    exit(0)
                elif status.coordinates:
                    print("coordis")
                    print(status.coordinates)
                    print(type(status.coordinates))
                    exit(0)
                elif status.user.location:
                    location = status.user.location
                    for word in location.split(","):
                        if (word.lower().strip() == "usa") or ("usa" in word.lower().strip()):
                            break
                        response = requests.request(
                            "GET", f"https://www.geonames.org/search.html?q={word}&country=")
                        results = re.findall(
                            "/countries.*\.html", response.text)
                        if results:
                            found_country = results[0].strip(
                                ".html").split("/")[-1]
                            if found_country == country.lower():
                                save_tweet(status._json, list_filtered_results)
                                break
            items += 1
        except:
            pass

    with open(path_name_save, "w") as f:
        json.dump(list_filtered_results, f)

    search_time = end_time_interval
