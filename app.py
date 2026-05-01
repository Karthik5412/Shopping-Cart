import streamlit as st 
import pandas as pd
import requests 

st.set_page_config(page_title= 'shopping cart recommendation', layout= 'wide', page_icon= '🛒')
response = requests.get('http://127.0.0.1:8000/all_products/')
if response.status_code == 200 :
    data = response.json()
    df = pd.DataFrame(data)

def featch_recommendations(cluster_id) :
    return df[df['clusters'] == cluster_id].reset_index(drop=True)





if 'page' not in st.session_state :
    st.session_state.page = 'home'

if 'data' not in st.session_state :
    st.session_state.data = None

grid = st.sidebar.select_slider('Grid Size', options = [3,4])

if st.session_state.page == 'home' :
    
    st.title('🛒 Shoppin Cart Recommendation System')
    
    display_limit = min(len(df), 40)
    count = 0
    for i in range(0,display_limit, grid):
        cols = st.columns(grid)
        for j in range(grid) :
            index = i + j
            if index < display_limit:
                row = df.iloc[index] 
                with cols[j] :
                    with st.container(border= True, height= 450):
                        with st.container(border= True, height=200) :
                            st.image(row['image_url'], width='stretch')
                        with st.container(height= 70, border= False) :
                            st.write(f"**{row['title']}**")
                        
                        rating, price = st.columns(2)
                        rating.subheader(f'⭐{row["rating"]}')
                        price.subheader(f'${row["price"]}')
                        
                        if st.button('open', key=f"home_{index}"):
                            st.session_state.page = 'next page'
                            st.session_state.data = row.to_dict()
                            st.rerun()
            
    
        
    
    
    
    
elif st.session_state.page == 'next page' :
    if st.button('back'):
        st.session_state.page = 'home'
        st.session_state.data = None
        st.rerun()
    
    st.subheader('Detail View')
    left , center, right = st.columns([3,4,3])
    with center :
        st.image(st.session_state.data['image_url'], width=300)
    
    col_left , col_right = st.columns(2)
    with col_left :
        st.subheader(st.session_state.data['title'])
        st.write(f"Brand: {st.session_state.data.get('brand', 'N/A')}")
    with col_right :
        st.subheader(f'⭐ {st.session_state.data["rating"]}')
        st.subheader(f'$ {st.session_state.data["price"]}')
    
    st.link_button('Check Out', st.session_state.data['product_url'], width='stretch')
    
    st.divider()
    st.title('Recommendations : ')
    
    
    df_rec = featch_recommendations(st.session_state.data['clusters'])
    
    if not df_rec.empty:
        
        for i in range(0, len(df_rec), grid):
            cols = st.columns(grid)
            for j in range(grid) :
                index = i + j
                
                if index < len(df_rec):
                    row = df_rec.iloc[index]
                    with cols[j] :
                        with st.container(border= True, height= 450):
                            with st.container(border= True, height=200) :
                                st.image(row['image_url'], width='stretch')
                            with st.container(height= 70, border= False) :
                                st.write(f"**{row['title']}**")
                            
                            r, p = st.columns(2)
                            r.write(f'⭐ {row["rating"]}')
                            p.write(f'${row["price"]}')
                            
                            
                            if st.button('view', key=f"rec_{index}"):
                                st.session_state.data = row.to_dict()
                                st.rerun()
    else:
        st.write("No recommendations found.")