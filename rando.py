import pandas as pd

df = pd.read_csv('world_cup_dataset.csv')
'''
df = df.drop(columns=['squad_form'])

'''
cols = list(df.columns)
cols.remove('elo_rating')
cols.insert(cols.index('confederation')+1,'elo_rating')
df = df[cols]
df = df.loc[:, ~df.columns.str.contains('^Unnamed')]
df.to_csv('world_cup_dataset.csv',index=False)
