import streamlit as st
from streamlit_option_menu import option_menu
import pandas as pd


class General:
    def __init__(self, dataSet):
        self.data = dataSet
        if 'recommended_movies' not in st.session_state:
            st.session_state.recommended_movies = []
    
    def all_movies(self):
        videos_link = self.data["Video Link"].values
        for i in range(0, len(videos_link) - 1, 2):
            col1, col2 = st.columns([1, 1])
            with col1:
                st.video(videos_link[i])
                like = st.checkbox("Like This Movie To Get Recommendations", key=videos_link[i])
                if like:
                    genres = self.data.loc[self.data["Video Link"] == videos_link[i], "Geners"].values[0].split(",")
                    st.session_state.recommended_movies.extend(genres)
                    st.session_state.recommended_movies = list(set(st.session_state.recommended_movies))  # Remove duplicates
            with col2:
                st.video(videos_link[i + 1])
                like = st.checkbox("Like This Movie To Get Recommendations", key=videos_link[i+1])
                if like:
                    genres = self.data.loc[self.data["Video Link"] == videos_link[i + 1], "Geners"].values[0].split(",")
                    st.session_state.recommended_movies.extend(genres)
                    st.session_state.recommended_movies = list(set(st.session_state.recommended_movies))  # Remove duplicates
    
    def search_movies(self):
        name = st.text_input("Enter the name that you wanted to search")
        word_list = name.split(" ")
        word_list = [x.lower() for x in word_list]
        new_word = "".join(word_list)
        movies_list = self.data["Names"].str.lower().tolist()
        if new_word in movies_list:
            index = movies_list.index(new_word)
            st.video(self.data.iloc[index]["Video Link"])
        else:
            html_code_snippet = f"<h5>Sorry, In Our Limited Movies Set {name} not found</h5>"
            st.markdown(html_code_snippet, unsafe_allow_html=True)
    
    def recommendations(self):
        if 'recommended_movies' in st.session_state:
            liked_genres = list(set(st.session_state.recommended_movies))
            if not liked_genres:
                st.write("You have not liked any movies yet.")
                return

        st.write("Liked Genres: ", liked_genres)
        for row in self.data['Geners'].values:
            movie_genres = row.split(",")
            common_genres = set(movie_genres).intersection(set(liked_genres))
            if len(common_genres)!=len(movie_genres):
                continue
            similarity_percentage = (len(common_genres) / len(liked_genres))*100
            if similarity_percentage>30:
                # Filter the DataFrame to get video links
                recommended_videos = self.data[self.data['Geners'] == row]['Video Link']
                for video_link in recommended_videos:
                    st.video(video_link)
                    col1, col2 = st.columns(2)
                    with col1:
                        st.write("Movie Genres: ", movie_genres)
                    with col2:
                        st.write("Similarity: ", similarity_percentage, "%")
        else:
            st.write("No recommendations yet. Like some movies to get recommendations.")


class Categories:
    def __init__(self, data_set, category):
        self.data = data_set
        self.genere = category
    
    def results(self):
        result_set = self.data[self.data["Geners"].str.contains(self.genere)]
        video_links = result_set["Video Link"].values
        for i in range(0, len(video_links) - 1, 2):
            col1, col2 = st.columns([1, 1])
            with col1:
                st.video(video_links[i])
            with col2:
                st.video(video_links[i + 1])

# Layout
with st.sidebar:
    general = option_menu("General", ["All Movies", "Search Movies", "Recommendations"],
                          icons=["film", "search", "lightbulb"], menu_icon="cast")
    categories = option_menu("Find Movies By Categories", ["Action", "Comedy", "Drama", "Horror", "Romance"])

dataSet = pd.read_csv("Movie dataset.csv")

if general == "All Movies":
    General(dataSet).all_movies()
elif general == "Search Movies":
    General(dataSet).search_movies()
elif general == "Recommendations":
    General(dataSet).recommendations()

if categories == "Action":
    Categories(dataSet, "Action").results()
elif categories == "Comedy":
    Categories(dataSet, "Comedy").results()
elif categories == "Drama":
    Categories(dataSet, "Drama").results()
elif categories == "Horror":
    Categories(dataSet, "Horror").results()
else:
    Categories(dataSet, "Romance").results()
