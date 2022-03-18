import twint
import datetime
import os

# Configure
c = twint.Config()
c.Search = "trudeau"
c.Store_json = True

search_time = datetime.datetime(2019, 1, 1)
end_time = datetime.datetime.now()


search_time = datetime.datetime(2019, 1, 22)
end_time = datetime.datetime(2019, 2, 5)

country_name = "Canada"
language = "en"
save_folder = "raw_data"

c.Lang = language

while(search_time < end_time):
    end_time_interval = search_time + datetime.timedelta(days=7)
    c.Since = search_time.strftime("%Y-%m-%d %H:%M:%S")
    c.Until = end_time_interval.strftime("%Y-%m-%d %H:%M:%S")

    file_timestamp = search_time.strftime("%Y-%m-%d")
    file_timestamp_end = end_time_interval.strftime("%Y-%m-%d")
    filename = f"{c.Search}_{file_timestamp}_{file_timestamp_end}.json"
    c.Output = os.path.join(save_folder, filename)

    # c.Near = country_name
    # c.Geo = "56.1304,106.3468,1000km"
    twint.run.Search(c)

    search_time = end_time_interval

# c.Output = "test.json"
# c.Limit = 100
# c.Since = "2019-12-01 00:00:00"
# c.Until = "2019-12-07 00:00:00"
# c.Lang = "en"
# #c.Geo = "56.1304, 106.3468, 3700km"
# #c.Location = True
# c.Near = "Canada"

# Run
# twint.run.Search(c)
