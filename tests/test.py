import pandas as pd

df = pd.DataFrame({'year': [2011, 2011, 2011, 2012, 2012,
                           2012],
                   'ages': ['15-25', '26-35', '36-45', '15-25', '26-35', '36-45'],
                   'value': [30, 34, 38, 31, 32, 36],
                   'question': ['owns_dog', 'owns_dog', 'owns_dog', 'owns_dog', 'owns_dog', 'owns_dog']})

df2 = pd.DataFrame({'year': [2011, 2011, 2011, 2012, 2012,
                           2012],
                   'ages': ['15-25', '26-35', '36-45', '15-25', '26-35', '36-45'],
                   'value': [26, 32, 37, 30, 29, 37],
                   'question': ['owns_cat', 'owns_cat', 'owns_cat', 'owns_cat', 'owns_cat', 'owns_cat']})

df = pd.concat([df, df2])

df = df.pivot(index=['year', 'ages'], columns='question', values='value')

df.to_clipboard()
