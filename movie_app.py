# import libraries
import streamlit as st
import pandas as pd
import plotly.express as px

# load the dataset
df = pd.read_csv("cleaned_movies.csv")

# make sure release data is the datetime format
df["release_date"] = pd.to_datetime(df["release_date"], errors="coerce")
df["release_year"] = df["release_date"].dt.year

# add a title
st.title("Top Movies and Genre Trends")

# Add tabs for different pages
tab1, tab2, tab3 = st.tabs(["Top Movies", "Trend Analysis by Genre", "Movies Released by Genre"])

# Tab 1: Top Movies
with tab1:
    # Add a sidebar for release year filtering
    min_year = int(df['release_year'].min())
    max_year = int(df['release_year'].max())
    year_filter = st.slider(
        "Select Release Year Range:",
        min_value=min_year,
        max_value=max_year,
        value=(min_year, max_year)
    )

    # make a genre filter
    genre_filter = st.selectbox(
        label="Select Genre:",
        options=df["primary_genre"].unique(),
        index=0
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

# Tab 2: Trend Analysis by Genre
with tab2:
    # Add a sidebar for release year filtering
    min_year = int(df['release_year'].min())
    max_year = int(df['release_year'].max())
    year_filter = st.slider(
        "Select Release Year Range for Trend Analysis:",
        min_value=min_year,
        max_value=max_year,
        value=(min_year, max_year)
    )

    # make a genre filter
    genre_filter = st.selectbox(
        label="Select Genre for Trend Analysis:",
        options=df["primary_genre"].unique(),
        index=0
    )

    # Filter dataset by release year and genre
    filtered_genre_range = df[
        (df["release_year"] >= year_filter[0]) &
        (df["release_year"] <= year_filter[1]) &
        (df["primary_genre"] == genre_filter)
    ]

    # Group by genre and release year, then calculate average popularity
    trend_data_genre = filtered_genre_range.groupby(["primary_genre", "release_year"])["popularity"].mean().reset_index()

    # Create a line plot for trend analysis by genre
    fig = px.line(
        trend_data_genre,
        x="release_year",
        y="popularity",
        color="primary_genre",
        title=f"Average Popularity by Genre Over the Years ({genre_filter})",
        labels={"popularity": "Average Popularity", "release_year": "Release Year", "primary_genre": "Genre"}
    )

    st.plotly_chart(fig)

# Tab 3: Movies Released by Genre (Table)
with tab3:
    # Add a slider for selecting a specific year
    selected_year = st.slider(
        "Select Year for Movie Count by Genre:",
        min_value=min_year,
        max_value=max_year,
        value=2020
    )

    # Filter dataset by the selected year
    filtered_by_year = df[df["release_year"] == selected_year]

    # Group by genre and count the number of movies released in the selected year
    movie_count_by_genre = filtered_by_year.groupby("primary_genre").size().reset_index(name='movie_count')

    # Display the table
    st.write(f"Movies Released in {selected_year} by Genre:")
    st.dataframe(movie_count_by_genre)