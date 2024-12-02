# import libraries
import streamlit as st
import pandas as pd
import plotly.express as px

df = pd.read_csv("cleaned_movies.csv")

st.title("Most Popular Movies By Genre")

genre_filter = st.selectbox(
    label = "Select Genre:",
    options = df["primary_genre"].unique(),
    index = 0
)

if genre_filter:
    filtered = df[df["primary_genre"] == genre_filter]
    sorted = filtered.sort_values(by = "popularity", ascending = False)

    fig = px.bar(
        sorted.head(10),
        x = "title",
        y = "popularity",
        color = "primary_genre",
        title = f"Top 10 Most Popular Movies in {genre_filter} Genre",
        labels = {"popularity": "Popularity Score", "title": "Movie Title"},
        color_discrete_sequence = ['#008080']
    )

    st.plotly_chart(fig)