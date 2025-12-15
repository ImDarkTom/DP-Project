import pandas as pd
import json

with open('datasets/physical-activity.json', mode='r') as file:
    data = json.load(file)

column_names: list[str] = list(map(lambda x: x['name'], data['meta']['view']['columns']))

df = pd.DataFrame(data['data'], columns=column_names)
print(df.head())

# data: list[list[str | int]] = [['Alex', 10], ['Bob', 12], ['Clarke', 13]]
# df = pd.DataFrame(data, columns=['Name', 'Age'])
# print(df)