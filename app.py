import streamlit as st
import pickle 
import pandas as pd
import requests,time

movies_list=pickle.load(open('movies.pkl', 'rb'))
similarity=pickle.load(open('similarity.pkl', 'rb'))
m_list=movies_list['title'].values

# @st.cache_data(show_spinner=False)
def fetch_poster(movie_id):
    placeholder_url = "https://comodosslstore.com/resources/wp-content/uploads/2025/05/website-page-found-error-robot-character-broken-chatbot-mascot-disabled-site-technical-work_502272-1888.jpg"
    try:
        url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=c6a0b2adf8be670ba083deb51a4e95ea&language=en-US"
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36"
        }
        response = requests.get(url, headers=headers, timeout=10, verify=False)
        # response.raise_for_status()
        data = response.json()

        if 'poster_path' in data and data['poster_path']:
            return "https://image.tmdb.org/t/p/w500/" + data['poster_path']
        else:
            # st.warning(f"⚠️ Missing poster_path for movie_id={movie_id} | data={data}")
            return placeholder_url

    except requests.exceptions.RequestException as e:
        # st.error(f"❌ API error for movie_id={movie_id}: {e}")
        # st.warning(f"⚠️ Missing poster_path for movie_id={movie_id} | data={data}")
        # st.code(url, language="markdown")
        return placeholder_url
    
    time.sleep(0.5)  # Wait 500ms before next API call

    
def recommend(movie):
    movie_index=int(movies_list[movies_list['title']==movie].index[0])
    distances=similarity[movie_index]
    movie_list=sorted(list(enumerate(distances)),reverse=True,key=lambda x:x[1])[1:6]
    recom_movies=[]
    recom_movie_poster=[]
    for i in movie_list:
        movie_id=movies_list.iloc[i[0]].movie_id
        recom_movies.append(movies_list.iloc[i[0]].title)
        recom_movie_poster.append(fetch_poster(movie_id))
    return recom_movies,recom_movie_poster

st.title('Movie Recommender System')
st.write('This is a simple movie recommender system built with Streamlit.')

# Create selectbox
selected_movie = st.selectbox(
    "Choose your favorite movie:",
    m_list.tolist()
)

if st.button('Show Recommendation'):
    recommended_movie_names,recommended_movie_posters = recommend(selected_movie)
    # st.write(f"Recommendations for: {recommended_movie_posters}")
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.text(recommended_movie_names[0])
        st.image(recommended_movie_posters[0])
    with col2:
        st.text(recommended_movie_names[1])
        st.image(recommended_movie_posters[1])

    with col3:
        st.text(recommended_movie_names[2])
        st.image(recommended_movie_posters[2])
    with col4:
        st.text(recommended_movie_names[3])
        st.image(recommended_movie_posters[3])
    with col5:
        st.text(recommended_movie_names[4])
        st.image(recommended_movie_posters[4])
