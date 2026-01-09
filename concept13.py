import time
import streamlit as st
import pandas as pd

st.set_page_config(page_title="Caching and State")

st.header("Function with Caching and State", divider="rainbow")

#Functions in StreamLit
st.subheader("Functions in StreamLit")
def greet(name:str)->str:
    return f"Hello, {name}! Welcome to our App"

name = st.text_input("Enter your name: ")
if name:
    st.write(greet(name))

st.divider()

#Caching in StreamLit
def load_data():
    df = pd.read_csv("Assets/fetal_health.csv")
    return df

start_time = time.time()
df = load_data()
st.write(f"Time taken to load data: {time.time()-start_time} seconds")
st.dataframe(df)

st.divider()

#Session State in StreamLit
st.subheader("Session State in StreamLit")
st.write("""
Every time a user interacts with a streamlit app (like clicking a button or moving a slider), the app state is updated (The app runs from top to bottom).
This behaviour is stateless- by default, the app does'nt remember anything across runs.
Session State acts like memory for each user. It stores values and let your persist data across interactions.
E.g of usage:
- Track a Counter
- Remember a user name.preference
- Keep a score Quiz
- Toggle a theme switch
            
Without session state, all variables reset on each rerun!
""")

if "counter" not in st.session_state:
    st.session_state.counter = 0

col1, col2 = st.columns(2)

with col1:
    if st.button("Increment"):
        st.session_state.counter +=1
with col2:
    if st.button("Decrement"):
        st.session_state.counter -= 1
st.write(f"Counter: {st.session_state.counter}")

st.divider()

#Function Combination, Caching, and State
st.subheader("Combining functions, caching, and state")

st.cache_data
def load_large_dataset():
    df = pd.read_csv("Assets/tmdb_5000_movies.csv")
    return df

start_time = time.time()
df = load_large_dataset()
st.write(f"The time taken to load the dataset is {time.time() - start_time} seconds.")

if "recommend_watch" not in st.session_state:
    st.session_state.recommend_watch = df["original_title"].values[0]

st.session_state.recommend_watch = st.selectbox("Choose a movie to watch", 
df["original_title"].values)

def filter_data(df, recommend_watch):
    return df[df["original_title"] == recommend_watch]

filtered_df = filter_data(df, st.session_state.recommend_watch)
st.dataframe(filtered_df)
st.divider()

