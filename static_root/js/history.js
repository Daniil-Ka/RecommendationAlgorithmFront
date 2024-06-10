let songHistoryCounter = 0;

// Функция для сохранения истории песен в локальное хранилище
function saveSongsHistory(history) {
    localStorage.setItem(`songsHistory${songHistoryCounter}`, JSON.stringify(history));
    songHistoryCounter++; // Увеличиваем счетчик для следующей истории песен
    localStorage.setItem('songHistoryCounter', songHistoryCounter); // Сохраняем текущее значение счетчика
}

// Функция для загрузки полной истории из локального хранилища
function loadFullSongsHistory() {
    let history = [];
    let i = 0;
    while (true) {
        const historyItem = localStorage.getItem(`songsHistory${i}`);
        if (!historyItem) break;
        history.push(JSON.parse(historyItem));
        i++;
    }
    return history;
}

function AddSongToHistory(jsonData) {
    saveSongsHistory(jsonData);
}

// Загрузка полной истории при загрузке страницы
let fullSongsHistory = loadFullSongsHistory();
songHistoryCounter = fullSongsHistory.length;
console.log(fullSongsHistory);