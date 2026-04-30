from fastapi import FastAPI
from functions import preprocessing, cluster_prediction, items

app = FastAPI()

@app.get('/')   
def homepage():
    return 'all good'

@app.get('/product/{name}')
async def return_item(name : str, text : str) :
    out = await items(name , text)
    return out