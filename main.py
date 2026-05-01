from fastapi import FastAPI, Query
from functions import home_page, items, search_result
from typing import Annotated, Optional

app = FastAPI()

@app.get('/')   
def homepage():
    return 'all good'

@app.get('/all_products/')
async def main_page():
    data =  await home_page()
    return  data

@app.get('/product/{cluster}')
async def return_item(cluster : int) :
    out = await items(cluster)
    return out

@app.get('/product_search/')
async def searching(text : Annotated[str, Query(max_length=10, min_length=3)]) :
    
    out = await search_result(text) 
    
    return out

