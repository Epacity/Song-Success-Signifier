import pandas as pd
import pymongo
import sys
import warnings

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, recall_score, precision_score, f1_score
from sklearn.feature_extraction.text import TfidfVectorizer

from scraper.topic_classifier import generate_topic

from visualization import plot_boxplot, plot_heatmap, plot_histogram, plot_bar_graph

client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["songs"]

warnings.filterwarnings("ignore", category=FutureWarning)

def format_songs() -> pd.DataFrame:
    genres = db.list_collection_names()
    dataframe_dict = {"artist": [], "length": [], "genre": [], "in_top_50":[], "title":[], "lyrics":[], "topic":[], "play_count":[]}
    for genre in genres:
        docs = db[genre].find({})
        for doc in docs:
            dataframe_dict["artist"].append(doc["artist"])
            dataframe_dict["length"].append(doc["length"])
            dataframe_dict["genre"].append(doc["genre"])
            dataframe_dict["in_top_50"].append(doc["in_top_50"])
            dataframe_dict["title"].append(doc["title"])
            dataframe_dict["lyrics"].append(doc["lyrics"])
            dataframe_dict["topic"].append(doc["topic"])
            dataframe_dict["play_count"].append(doc["play_count"])

    df = pd.DataFrame(dataframe_dict)
    return df


class SongSuccessSignifier:
    def __init__(self, song_data) -> None:
        self.data = song_data

        # Features we use for prediction
        self.text_features = ['lyrics', 'topic']
        self.categorical_features = ['genre']

        # Gather all unique genres=
        self.genres = db.list_collection_names()

    """
          Prepare features for machine learning

          Parameters:
          - genre: Specific genre to filter (optional)

          Returns:
          - Preprocessed feature matrix
          - Target variable
      """

    def prepare_features(self, genre_data):
        # Text vectorization for lyrics and subject matter
        text_transformer = ColumnTransformer(
            transformers=[
                ('lyrics_tfidf', TfidfVectorizer(
                    max_features=5000,
                    stop_words='english',
                    ngram_range=(1, 2)), 'lyrics'),
                ('topic_tfidf', TfidfVectorizer(
                    max_features=5000,
                    stop_words='english',
                    ngram_range=(1, 2)), 'topic')
            ],
            remainder='drop'  # Drop all other columns
        )

        # Categorical feature encoding
        categorical_transformer = Pipeline(steps=[('onehot', OneHotEncoder(handle_unknown='ignore'))])

        preprocessor = ColumnTransformer(
            transformers=[
                ('text', text_transformer, self.text_features),
                ('categorical', categorical_transformer, self.categorical_features),
            ]
        )

        # Create the feature matrix
        X = pd.concat([
            genre_data[self.text_features],
            genre_data[self.categorical_features],
        ], axis=1)

        return preprocessor, X


    def train_genre_models(self):
        genre_models = {}
        genre_performances = {}

        for genre in self.genres:
            genre_data = self.data[self.data['genre'] == genre]
            y = (genre_data['in_top_50'] == True).astype(int)

            # Pass genre_data to prepare_features
            preprocessor, X = self.prepare_features(genre_data)


            X_train, X_test, Y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
            X_train = X_train.reset_index(drop=True)
            Y_train = Y_train.reset_index(drop=True)



            model = Pipeline(steps=[
                ('preprocessor', preprocessor),
                ('classifier', RandomForestClassifier(
                    n_estimators=100,
                    class_weight='balanced',
                    random_state=42))
            ])
            model.fit(X_train, Y_train)
            y_pred = model.predict(X_test)
            performance = {
                'accuracy': accuracy_score(y_test, y_pred),
                'precision': precision_score(y_test, y_pred, zero_division=0),
                'recall': recall_score(y_test, y_pred),
                'f1_score': f1_score(y_test, y_pred),
            }

            genre_models[genre] = model
            genre_performances[genre] = performance

        return genre_models, genre_performances

    """
    Predict the probability of a song reaching Top 50 in different genres

      Parameters:
      - song_data: Dictionary with song information
      - genre_models: Trained models for each genre

      Returns:
      - Probabilities of Top 50 success for each genre
    """
    def predict_genre_success(self, song_features, genre_models):
        input_df = pd.DataFrame([song_features])

        #input_df['combined_text'] = input_df['lyrics'] + ' ' + input_df['topic']

        genre_probabilities = {}
        for genre, model in genre_models.items():
          # Predict probability of Top 50 Success
          prob = model.predict_proba(input_df)[:, 1][0]
          genre_probabilities[genre] = prob

        return genre_probabilities


if __name__ == '__main__':
    print("Getting songs DataFrame from MongoDB...")
    songs_df = format_songs()
    predictor = SongSuccessSignifier(songs_df)
    print("Training the model...")
    genre_models, genre_performances = predictor.train_genre_models()

    print("Pulling the test song lyrics from lyrics.txt...")
    with open("lyrics.txt", "r+") as lyrics_file:
        lyrics_text = lyrics_file.read()


    print("Generating topic from the song lyrics...")
    topic, err = generate_topic(lyrics_text)
    if err:
        print(f"Could not generate song lyrics: {err}")
        sys.exit()

    print(f"Song topic: {topic}")
    song_features = {
        "lyrics":lyrics_text,
        "topic":topic,
        "genre":"Unknown"
    }
    print("Predicting the success of a sample song...")
    success_probabilities = predictor.predict_genre_success(song_features, genre_models)
    print("Here are the probabilities of this song's success in each genre:")
    for genre, probability in success_probabilities.items():

        # Filter is necessary due to too many false positives
        if genre == "Musica Mexicana":
            continue

        print(f"{genre}: {probability*100:.2f}%")

    print("Showing model visualizations...")
    plot_heatmap(genre_performances)
    plot_bar_graph(genre_performances)
    plot_histogram(genre_performances)
    plot_boxplot(genre_performances)
    print("Done!")
