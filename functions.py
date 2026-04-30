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

df = pd.read_csv('datasets//amazon.csv')
df = df[['product_name', 'about_product', 'img_link', 'product_link']]

subset = df.sample(n=300, random_state=42)

async def preprocessing(data : str) -> str :
    try :
        stop_words = set(stopwords.words('english'))
        lematizer = WordNetLemmatizer()
        #Lower Case
        data = str(data).lower()
        
        #Remove punctuations
        data = re.sub(r'[^a-zA-z\s]', "",data)

        #Words split
        words = data.split()

        #removing stopwords
        words = [word for word in words if word not in stop_words]

        #Lematization
        words = [lematizer.lemmatize(word) for word in words]

        return ' '.join(words)
    except Exception as e:
        return e 


async def cluster_prediction(text : str) :
    
    try :
        data = await preprocessing(text)
        
        data = [data]
        
        matrix = tfidf.transform(data)
        
        cluster = model.predict(matrix)
        
        return int(cluster[0])
    except Exception as e:
        return e


async def items(name: str, text : str) :
    
    try :
        main_cluster = await cluster_prediction(name + ' ' + text)
        
        subset['text'] = subset['product_name'] + subset['about_product']
        
        clusters = []
        for text in subset['text']:
            clu = await cluster_prediction(text)
            clusters.append(clu)
        
        subset['cluster'] = clusters
        
        output = subset[subset['cluster'] == main_cluster]
        
        return output.to_dict(orient='records')
    
    except Exception as e:
        return e
    





