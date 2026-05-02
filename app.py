import streamlit as st
import requests
import pandas as pd

@st.cache_data
def load_data():
    url = 'http://127.0.0.1:8000/all_products/'

    response = requests.get(url)
    if response.status_code == 200 :
        data = response.json()
        df = pd.DataFrame(data)
        
    return df

data = load_data()


def recommend_products(cluster_id, product_name) :
    output = data[data['clusters'] == cluster_id].copy()
    output = output[output['title'] != product_name].reset_index(drop=True)
    
    return pd.DataFrame(output).iloc[:600].reset_index(drop= True)
    

def search_product(text : str) :
    text = text.lower().strip()
    output = data[data['title'].str.lower().str.strip().str.contains(text)]
    
    return pd.DataFrame(output).iloc[:600].reset_index(drop= True)

st.set_page_config(page_title='Shopping Cart', page_icon= '🛒', layout= 'wide')

if 'page' not in st.session_state :
    st.session_state.page = 'home'
    
if 'data' not in st.session_state :
    st.session_state.data = None
    
if st.sidebar.button('🏘️Home') :
    st.session_state.page = 'home'
    st.session_state.data = None
    st.rerun()
    
grid = st.sidebar.select_slider('Grid Size', [3,4])
search = st.text_input(' ', width='stretch')
enter = st.button('Fetch Product')
if enter :
    st.session_state.page = 'search'
    st.rerun()

if st.session_state.page == 'home' :
    
    st.title('🛒 Shopping Cart Recommender')
    df = load_data()
    display_limit = min(len(df), 45)
    for i in range(0, display_limit, grid):
                cols = st.columns(grid)
                
                for j in range(grid):
                    index = i + j
                    
                    if index < display_limit:
                        row = df.iloc[index]
                        
                        with cols[j]:
                            with st.container(border=True, height= 400):
                                with st.container(border= True, height= 200) :
                                    st.image(row['image_url'], use_container_width=True)
                                
                                with st.container(height=25, border=False):
                                    st.write(row['title'])
                                
                                r_col, p_col = st.columns(2)
                                r_col.subheader(f"⭐{row['rating']}", text_alignment='left')
                                p_col.subheader(f"**${row['price']}**", text_alignment= 'right')
                                
                                if st.button('Open', key=f"home_{index}", use_container_width=True):
                                    st.session_state.page = 'next page'
                                    st.session_state.data = row.to_dict()
                                    st.rerun()


elif st.session_state.page == 'next page' :
    
    st.title('Details ...')
    
    lt, cen, rt = st.columns([2.5, 5, 2.5])
    with cen :
        with st.container(border= True) :
            st.image(st.session_state.data['image_url'])
            
    st.subheader(st.session_state.data['title'])
    st.markdown(st.session_state.data['brand'])
    
    la , ra = st.columns(2)
    
    with la :
        st.subheader(f'⭐ {st.session_state.data['rating']}')
        
    with ra :
        st.subheader(f'$ {st.session_state.data['price']}', text_alignment= 'right')
        
    st.link_button('Check Out', st.session_state.data['product_url'], width= 'stretch')
    
    st.title('Recommendations 🔍')
    
    rec_df = recommend_products(cluster_id= st.session_state.data['clusters'], product_name= st.session_state.data['title'])
    
    display_limit = min(len(rec_df), 45)
    for i in range(0, display_limit, grid):
                cols = st.columns(grid)
                
                for j in range(grid):
                    index = i + j
                    
                    if index < display_limit:
                        row = rec_df.iloc[index]
                        
                        with cols[j]:
                            with st.container(border=True, height= 400):
                                with st.container(border= True, height= 200) :
                                    st.image(row['image_url'], use_container_width=True)
                                
                                with st.container(height=25, border=False):
                                    st.write(row['title'])
                                
                                r_col, p_col = st.columns(2)
                                r_col.subheader(f"⭐{row['rating']}", text_alignment='left')
                                p_col.subheader(f"**${row['price']}**", text_alignment= 'right')
                                
                                if st.button('Open', key=f"home_{index}", use_container_width=True):
                                    st.session_state.page = 'next page'
                                    st.session_state.data = row.to_dict()
                                    st.rerun()

elif st.session_state.page == 'search' :
    search_df = search_product(search)
    
    data_limit = len(search_df) / 1.5
    
    for idx, row in search_df.loc[0:data_limit].iterrows() :
        with st.container(border= True, height= 300) :
            col_l , col_r = st.columns([4,6])
            
            with col_l :
                st.image(row['image_url'])
                
            with col_r :
                st.markdown(row['title'])
                st.subheader(f'⭐ {row['rating']}')
                st.subheader(f"**${row['price']}**")
                
            if st.button('Open', key=f"home_{idx}", use_container_width=True):
                st.session_state.page = 'next page'
                st.session_state.data = row.to_dict()
                st.rerun()

        