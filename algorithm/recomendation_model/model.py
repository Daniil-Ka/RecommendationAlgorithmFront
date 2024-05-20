import pickle
import h5py
import numpy as np
import pandas as pd
import torch
from sklearn.preprocessing import LabelEncoder, StandardScaler
from torch import nn


class Model:
    model = None

    @classmethod
    def load(cls):
        data = pd.read_csv('model_files/dataset.csv', sep=';')

        cls.label_encoders = {}
        for column in ['Название', 'Артист', 'Жанр', 'Язык']:
            le = LabelEncoder()
            data[column] = le.fit_transform(data[column])
            cls.label_encoders[column] = le

        cls.scaler = StandardScaler()
        data[['Количество треков у артиста', 'Количество лайков артиста']] = cls.scaler.fit_transform(
            data[['Количество треков у артиста', 'Количество лайков артиста']])

        model = ImprovedMusicNet(data)

        # Загружаем параметры модели из HDF5 файла
        with h5py.File('model_files/model.h5', 'r') as f:
            with torch.no_grad():
                for name, param in model.named_parameters():
                    param.copy_(torch.tensor(np.array(f[name])))

        # Load state dict from pickle file
        with open('model_files/weights.pkl', 'rb') as f:
            state_dict = pickle.load(f)
            model.load_state_dict(state_dict)

        cls.model = model



    @classmethod
    def predict_unpopular_artists(cls, genres, languages, top_n=5):
        genre_enc = cls.label_encoders['Жанр'].transform(genres)
        language_enc = cls.label_encoders['Язык'].transform(languages)
        input_data = []
        for genre in genre_enc:
            for lang in language_enc:
                input_data.append([genre, lang, 0, 0])  # Dummy values for tracks and likes

        # Преобразование данных с фиктивными значениями
        input_data = np.array(input_data)
        input_data[:, 2:] = cls.scaler.transform(input_data[:, 2:])  # Нормализация только последних двух признаков
        input_data = torch.tensor(input_data, dtype=torch.float32)

        cls.model.eval()
        with torch.no_grad():
            outputs = cls.model(input_data)
            _, predicted = torch.max(outputs.data, 1)

        predicted_artists = cls.label_encoders['Артист'].inverse_transform(predicted.numpy())
        unique_artists, counts = np.unique(predicted_artists, return_counts=True)
        sorted_artists = sorted(zip(unique_artists, counts), key=lambda x: x[1])
        sorted_artists.reverse()
        sorted_artists = sorted_artists[:top_n]

        return [a[0] for a in sorted_artists]


class ImprovedMusicNet(nn.Module):
    def __init__(self, data):
        super(ImprovedMusicNet, self).__init__()
        self.fc1 = nn.Linear(4, 512)
        self.dropout1 = nn.Dropout(0.3)
        self.fc2 = nn.Linear(512, 256)
        self.dropout2 = nn.Dropout(0.3)
        self.fc3 = nn.Linear(256, 128)
        self.dropout3 = nn.Dropout(0.3)
        self.fc4 = nn.Linear(128, 64)
        self.dropout4 = nn.Dropout(0.3)
        self.fc5 = nn.Linear(64, len(data['Артист'].unique()))

    def forward(self, x):
        x = torch.relu(self.fc1(x))
        x = self.dropout1(x)
        x = torch.relu(self.fc2(x))
        x = self.dropout2(x)
        x = torch.relu(self.fc3(x))
        x = self.dropout3(x)
        x = torch.relu(self.fc4(x))
        x = self.dropout4(x)
        x = self.fc5(x)
        return x

