import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder


class Model:
    model = None

    @classmethod
    def load(cls):
        data = pd.read_csv('model_dataset.csv', delimiter=';')
        data.dropna(inplace=True)
        data.drop_duplicates(inplace=True)
        X = data.drop(columns=['Название', 'Артист'])
        y = data['Артист']
        X = pd.get_dummies(X)
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        cls.X = pd.get_dummies(X)
        cls.model = RandomForestClassifier(random_state=42)
        cls.model = cls.model.fit(X_train, y_train)

    @classmethod
    def predict_artists(cls, genre, language, top_n=4):
        if cls.model is None:
            cls.load()
        input_data = pd.DataFrame(0, index=range(1), columns=cls.X.columns)
        input_data['Жанр_' + genre] = 1

        probabilities = cls.model.predict_proba(input_data)
        top_indices = (-probabilities[0]).argsort()[:top_n][1:]
        top_artists = [cls.model.classes_[idx] for idx in top_indices]

        return top_artists

