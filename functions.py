import pickle
import joblib
import pandas as pd
import re
import nltk
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords
import numpy
from sklearn.model_selection import train_test_split as tts

model = joblib.load('pickle_files//kmeans.plk')
tfidf = joblib.load('pickle_files//tfidf.plk')

df = pd.read_csv('datasets//cleaned.csv')

df = df[['product_id','brand','title','price','category','rating','image_url','product_url','clusters']].copy()

subset = df.sample(n=100, random_state=42).reset_index(drop=True)
dt = subset.to_dict(orient='records').copy()

async def home_page () :
    return subset.to_dict(orient='records')


async def items(cluster : int) :
    
    try :
        output = df[df['clusters'] == cluster].copy()
        output = output.reset_index(drop= True)
        return output.to_dict(orient='records')
    
    except Exception as e:
        return e
    

async def search_result(text : str) :
    text = text.lower().strip()
    output = []
    for row in dt :
        if text in str(row['title']).lower().strip() :
            output.append(row)
                
        if len(output) == 15 :
            
            return output
        
    return {'msg' : 'No product Found'}

