let songHistoryCounter = 0;

// Функция для сохранения истории песен в куки
function saveSongsHistory(history) {
    Cookies.set(`songsHistory${songHistoryCounter}`, JSON.stringify(history), { expires: 7 }); // Сохранение на 7 дней
    songHistoryCounter++; // Увеличиваем счетчик для следующей истории песен
}

// Функция для загрузки полной истории из куки
function loadFullSongsHistory() {
    let history = [];
    let i = 0;
    while (true) {
        const historyCookie = Cookies.get(`songsHistory${i}`);
        if (!historyCookie) break;
        history.push(JSON.parse(historyCookie));
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
