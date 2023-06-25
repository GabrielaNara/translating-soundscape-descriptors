import pandas as pd
import difflib

# import csv
data = pd.read_csv('data-twitter.csv')

############################################################
############### Filtering duplicate tweets #################
############################################################
#------------------------------------------------------------------------------------
#Removing "http" from tweets
new = data["text"].str.split("http", n=1, expand=True)
data["new_tweet"] = new[0]
data["url"] = new[1]
df = data.drop_duplicates(subset='text', keep='first')
df = df.drop_duplicates(subset='new_tweet', keep='first')
df['text'] = df['new_tweet'] 
data = df
del data['new_tweet']
del data['url']
data = data.reset_index()
data = data.sort_index()
del data['index'] 

#------------------------------------------------------------------------------------
#Filtering by similarity of sentences
similarity_level = 0.8
for i in data.index:
    for distance in range(1,4):
    #for i in data.index:
        comparsion = data.text[i]
        text2 = data.text[i + distance]
        if difflib.SequenceMatcher(None,comparsion,text2).ratio() > similarity_level:
            data = data.drop([i + distance]) 
    data = data.sort_index()
    data = data.reset_index()
    del data['index'] 

#data.to_excel(("/filtered_data.xlsx"), sheet_name='dados') 
data.to_csv('data-filtered.csv')


