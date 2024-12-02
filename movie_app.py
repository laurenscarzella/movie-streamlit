# import libraries
import streamlit as st
import pandas as pd
import plotly.express as px

# load the dataset
df = pd.read_csv("cleaned_movies.csv")

# make sure release data is the datetime format
df["release_date"] = pd.to_datetime(df["release_date"], errors = "coerce")
df["release_year"] = df["release_date"].dt.year

# add a title
st.title("Most Popular Movies By Genre")

# add a sidebar for release year filtering
st.sidebar.header("Filter Options")
min_year = int(df['release_year'].min())
max_year = int(df['release_year'].max())
year_filter = st.sidebar.slider(
    "Select Release Year Range:",
    min_value=min_year,
    max_value=max_year,
    value=(min_year, max_year)
)

# make a genre filter
genre_filter = st.selectbox(
    label = "Select Genre:",
    options = df["primary_genre"].unique(),
    index = 0
)

# add a checkbox to show top 10 movies or top 50 movies (or as close as possible)
show_top_50 = st.checkbox("Show Top 50 Movies")

# filter dataset by genre and release year
if genre_filter:
    filtered = df[
        (df["primary_genre"] == genre_filter) &
        (df["release_year"] >= year_filter[0]) &
        (df["release_year"] <= year_filter[1])
    ]
    sorted = filtered.sort_values(by="popularity", ascending=False)

    num_to_show = 10 if not show_top_50 else min(50, len(sorted))

    # Create the figure for top movies
    if not sorted.empty:
        fig = px.bar(
            sorted.head(num_to_show),
            x="title",
            y="popularity",
            color="primary_genre",
            title=f"Top {num_to_show} Most Popular Movies in {genre_filter} Genre ({year_filter[0]}-{year_filter[1]})",
            labels={"popularity": "Popularity Score", "title": "Movie Title"},
            color_discrete_sequence=['#008080']
        )

        st.plotly_chart(fig)
    else:
        st.write("No movies found in the selected year range and genre.")

    # Add an expander to preview the filtered dataset
    with st.expander("Show Filtered Data Table"):
        st.dataframe(filtered)