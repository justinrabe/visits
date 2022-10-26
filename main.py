import pandas as pd
import json
import inflection as infl
data = []
with open('ga_sessions_20160801.json') as f:
    for line in f:
        data.append(json.loads(line))

df = pd.json_normalize(data)
print(len(df.index))
##df2 = pd.read_json('ga_sessions_20160801.json', lines = True)
##print(df.head(10))

visits = df[['fullVisitorId', 'visitId','visitNumber','visitStartTime','device.browser','geoNetwork.country']]
## Stripping normalized prefixes
visits = visits.rename(columns={"device.browser": "browser", "geoNetwork.country": "country"})
## Convert to snake case
visits.columns = [infl.underscore(x) for x in visits.columns] 
visits['primary_id'] = visits['full_visitor_id'].astype(str) + visits['visit_id'].astype(str)
##print(visits.head(10))

##print(list(df.columns.tolist()))

df2 = pd.json_normalize(data, record_path=['hits'])

##print(df2.head(10))
##print(list(df2.columns.tolist()))
hits = df2[['hitNumber', 'type', 'time', 'page.pagePath','page.pageTitle','page.hostname']]
hits['primary_id'] = visits['primary_id']
hits['hit_timestamp'] = visits['visit_start_time'] + hits['time']
hits['hit_timestamp'] = pd.to_datetime(hits['hit_timestamp'])
print(hits.head(10))
