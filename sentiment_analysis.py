import os
import json
from transformers import pipeline
import datetime
import time
from typing import List, Tuple
from enum import Enum
import sys

import torch

import matplotlib.pyplot as plt


class Label(Enum):
    POSITIVE = "POSITIVE"
    NEGATIVE = "NEGATIVE"
    NEUTRAL = "NEUTRAL"


def get_classifier(model_name: str = "distilbert-base-uncased-finetuned-sst-2-english"):
    # most popular en classifier, faster + smaller version than bert
    return pipeline("sentiment-analysis", model=model_name)


def get_sentiment(tweets: List, classifier) -> float:
    # confidence threshold
    confidence_threshold = 0.7
    score = 0
    counts = 0

    results = classifier(tweets)
    for result in results:
        if result["score"] >= confidence_threshold:
            counts += 1
            match result["label"]:
                case Label.POSITIVE.value:
                    score += 1
                case Label.NEGATIVE.value:
                    score -= 1
                case _:
                    sys.exit("Invalid label: " + result["label"])
    return score / max(1, counts)


directory = "filtered_data"
save_calculation_file = "calculatied_sentiment_2.json"

sentiment_over_time = []
number_of_tweets_over_time = []
time_line = []

search_time = datetime.datetime(2019, 1, 1)
#search_time = datetime.datetime(2022, 3, 1)
end_time = datetime.datetime.now()
end_time = datetime.datetime(2022, 3, 15)
classifier = get_classifier()
search_term = "trudeau"
# iterate over files in
# that directory
start_time = time.time()

while(search_time < end_time):
    end_time_interval = search_time + datetime.timedelta(days=7)
    file_timestamp = search_time.strftime("%Y-%m-%d")
    file_timestamp_end = end_time_interval.strftime("%Y-%m-%d")
    filename = f"{search_term}_{file_timestamp}_{file_timestamp_end}.json"
    path_name = os.path.join(directory, filename)

    with open(path_name, "r") as file:
        data = json.load(file)

    texts = [tweet["full_text"] for tweet in data]
    print(search_time)
    sentiment_over_time.append(get_sentiment(texts, classifier))
    number_of_tweets_over_time.append(len(texts))
    time_line.append(search_time)

    search_time = end_time_interval

end_calculation_time = time.time()

print(end_calculation_time - start_time)

calcs_dict = {t.strftime("%Y-%m-%d"): [sentiment, counts] for (t, sentiment, counts) in zip(
    time_line, sentiment_over_time, number_of_tweets_over_time)}
with open(save_calculation_file, "a") as f:
    json.dump(calcs_dict, f)

start_plot_time = time.time()

fig, axs = plt.subplots(2, 1)
axs[0].plot(time_line, sentiment_over_time, "-bo")
axs[0].set_xlabel("time")
axs[0].set_ylabel("sentiment")
axs[0].grid(True)


axs[1].plot(time_line, number_of_tweets_over_time, "-bo")
axs[1].set_ylabel("number of tweets")
axs[1].grid(True)


fig.tight_layout()
plt.savefig("draft_2_years_time_line_2.png")

end_plot_time = time.time()
print(end_plot_time - start_plot_time)
plt.show()
