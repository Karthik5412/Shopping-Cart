from fastapi import FastAPI
import pandas as pd
from fastapi.responses import JSONResponse
import random

async def all_products() :
    df = pd.read_csv('datasets/cleaned.csv')
    
    num = random.randint(1000, 5000)
    sample =  df.loc[num : num + 3000].reset_index(drop= True)
    
    return JSONResponse(content= sample.to_dict(orient='records'))

app = FastAPI()

@app.get('/')   
def homepage():
    return 'all good'

@app.get('/all_products/')
async def main_page():
    data =  await all_products()
    return  data

