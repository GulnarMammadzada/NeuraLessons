import numpy as np
import pandas as pd

df=pd.read_csv('sample_data(2).csv')

print(df.info())
print(df.describe())
print(df.isnull().sum)

print(np.nan==np.nan)

df['age']=df['age'].fillna(df['age'].mean())
print(df['age'])
df['city']=df['city'].fillna(df['city'].mode()[0])
print(df['city'])

# df=df[df['age']<100]
df.loc[df['age']>100,'age']=100
print(df['age'])


df['age_zscore']=(df['age']-df['age'].mean())/df['age'].std()
df=df[(df['age_zscore']<3) & df['age_zscore']>-3]
print(df['age_zscore'])

df=df.sort_values(by='income',ascending=False)
print(df['income'])

df['join_date']=pd.to_datetime(df['join_date'])
df['last_purchase']=pd.to_datetime(df['last_purchase'])

df['days_active']=(df['last_purchase']-df['join_date']).dt.days
print(df['days_active'])


from sklearn.preprocessing import MinMaxScaler

scaler=MinMaxScaler()

columns=['age','income']
df[columns]=scaler.fit_transform(df[columns])
print(df[columns].round(3))

df.to_csv("clean_data.csv",index=False)