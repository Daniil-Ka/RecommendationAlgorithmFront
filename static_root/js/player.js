// ===== Открытие навигационного меню =====
$(".burger-wrapper").click(function () {

    // ===== Если меню не открыто
    if ($('.nav').css("display") === "none") {
        // Показываем темную область
        TweenMax.to(".dim", 0.5, {opacity: 1, display: 'block', ease: Power2.easeInOut});
        // Анимация открытия навигационного меню
        TweenMax.fromTo(".nav", 0.5, {xPercent: -100},
            {xPercent: 0, display: 'block', ease: Expo.easeOut});
        // Плавное появление пунктов меню
        TweenMax.staggerFrom('.nav li', 0.5, {opacity: 0, y: 20, ease: Power2.easeInOut}, 0.1);

        // Скрываем логотип
        $('.logo-text').css({'opacity': '0', 'display': 'none'});
    }
    // ===== Если меню открыто и на странице куратора
    else if ($('.nav').css("display") === "block" && $('#curator').css("display") === "block") {
        // Скрываем темную область
        TweenMax.to(".dim", 0.5, {opacity: 0, display: 'none', ease: Power2.easeInOut});
        // Анимация закрытия навигационного меню
        TweenMax.to(".nav", 0.5, {xPercent: -100, display: 'none', ease: Expo.easeOut});
        // $('.logo-text').css({'opacity': '1', 'display': 'block'});
    } else {
        // Скрываем темную область
        TweenMax.to(".dim", 0.5, {opacity: 0, display: 'none', ease: Power2.easeInOut});
        // Анимация закрытия навигационного меню
        TweenMax.to(".nav", 0.5, {xPercent: -100, display: 'none', ease: Expo.easeOut});
        // Показываем логотип
        $('.logo-text').css({'opacity': '1', 'display': 'block'});
    }

});


// ===== Открытие плеера + показ темной области =====

$(".btn-open-player, .track_info").click(function () {
    // Показываем темную область
    TweenMax.to(".dim", 0.5, {opacity: 1, display: 'block', ease: Power2.easeInOut});
    // Анимация открытия плеера
    TweenMax.fromTo("#player", 0.5, {xPercent: 100},
        {xPercent: 0, display: 'block', ease: Expo.easeOut});
    // Перемещение мини-плеера
    TweenMax.to(".mini-player", 0.5, {x: 50, ease: Expo.easeOut});
});

$('.dim').click(function () {
    // Скрываем темную область
    TweenMax.to(".dim", 0.5, {opacity: 0, display: 'none', ease: Power2.easeInOut});
    // Анимация закрытия плеера
    TweenMax.to("#player", 0.5, {xPercent: 100, display: 'none', ease: Expo.easeOut});
    // Анимация закрытия навигационного меню
    TweenMax.to(".nav", 0.5, {xPercent: -100, display: 'none', ease: Power2.easeInOut})
    // Возвращение мини-плеера на место
    TweenMax.to(".mini-player", 0.5, {x: 0, ease: Expo.easeOut});
});

// ===== Переключатель воспроизведения/паузы мини-плеера =====
var audioPlayer = new Audio();
audioPlayer.src = '/static/audio/audio.mp3';

audioPlayer.onloadedmetadata = function() {
  console.log(audioPlayer.duration);
  console.log(audioPlayer.currentTime);
};

function updateSliderPosition() {
    // Получаем общую продолжительность трека
    var duration = audioPlayer.duration;

    // Получаем текущее время трека
    var currentTime = audioPlayer.currentTime;

    // Вычисляем процент времени, прошедшего от начала трека
    var progressPercent = (currentTime / duration) * 100;

    // Устанавливаем позицию ползунка и ширину прогресса
    var handlePosition = progressPercent + '%';
    $('.slider_handle').css('left', handlePosition);
    $('.slider_progress').css('width', handlePosition);
}

audioPlayer.ontimeupdate = function() {
    // Получаем текущее время воспроизведения аудио в секундах
    const currentTime = audioPlayer.currentTime;

    // Преобразуем текущее время из секунд в формат минут:секунды
    const currentMinutes = Math.floor(currentTime / 60);
    const currentSeconds = Math.floor(currentTime % 60);

    currentTimeText = String(currentMinutes).padStart(2, "0") + ':' + String(currentSeconds).padStart(2, "0");
    $('.playback_timeline_start-time').text(currentTimeText);

    // Преобразуем текущее время из секунд в формат минут:секунды
    const duration = audioPlayer.duration;
    const durationMinutes = Math.floor(duration / 60);
    const durationSeconds = Math.floor(duration % 60);

    let durationTimeText = String(durationMinutes).padStart(2, "0") + ':' + String(durationSeconds).padStart(2, "0");
    $('.playback_timeline_end-time').text(durationTimeText);

    // Выводим текущее время воспроизведения аудио
    console.log(`Текущее время: ${currentMinutes}:${currentSeconds}`);
    updateSliderPosition();
};

$('.playback_timeline_slider').on('mousedown', function(event) {
    // Получаем ширину ползунка
    var sliderWidth = $(this).width();

    // Рассчитываем относительную позицию курсора в пределах ползунка
    var relativePosition = event.clientX - $(this).offset().left;

    // Рассчитываем новое время воспроизведения на основе относительной позиции курсора
    var newTime = (relativePosition / sliderWidth) * audioPlayer.duration;

    // Обновляем позицию элементов slider_handle и slider_progress
    var handlePosition = Math.min(Math.max(relativePosition / sliderWidth, 0), 1) * 100 + '%';
    $('.slider_handle').css('left', handlePosition);
    $('.slider_progress').css('width', handlePosition);

    // Устанавливаем новое время воспроизведения аудио
    audioPlayer.currentTime = newTime;
});

$('.btn-play').click(function () {
    // Анимация скрытия кнопки play
    TweenMax.to($('.btn-play'), 0.2, {x: 20, opacity: 0, scale: 0.3, display: 'none', ease: Power2.easeInOut});
    // Анимация появления кнопки pause
    TweenMax.fromTo($('.btn-pause'), 0.2, {x: -20, opacity: 0, scale: 0.3, display: 'none'},
        {x: 0, opacity: 1, scale: 1, display: 'block', ease: Power2.easeInOut});
    console.log('start')

    audioPlayer.play()
});

$('.btn-pause').click(function () {
    // Анимация скрытия кнопки pause
    TweenMax.to($('.btn-pause'), 0.2, {x: 20, opacity: 0, display: 'none', scale: 0.3, ease: Power2.easeInOut});
    // Анимация появления кнопки play
    TweenMax.fromTo($('.btn-play'), 0.2, {x: -20, opacity: 0, scale: 0.3, display: 'none'},
        {x: 0, opacity: 1, display: 'block', scale: 1, ease: Power2.easeInOut});
    console.log('pause')

    audioPlayer.pause()
});

$('.btn-prev').click(function () {
    console.log('prev')

    TweenMax.to($(this), 0.1, {scale: 0.8, ease: Power2.easeInOut});
    // Возвращаем кнопку в исходный размер
    TweenMax.to($(this), 0.1, {delay: 0.1, scale: 1, ease: Power2.easeInOut});
})

$('.btn-next').click(function () {
    console.log('next')

    TweenMax.to($(this), 0.15, {scale: 0.7});
    // Возвращаем кнопку в исходный размер
    TweenMax.to($(this), 0.15, {delay: 0.1, scale: 1});
})


// ===== Эффект мерцания при наведении/покидании курсора на различные элементы =====
$('.track_info').hover(function () {

        // Эффект мерцания при наведении на информацию о треке
        TweenMax.fromTo($(this), 0.5, {opacity: 0.5, ease: Power2.easeInOut},
            {opacity: 1})
    },
    function () {
        $(this).css("opacity", "1");
    });

$('.burger-wrapper, .logo-text, .back_btn').hover(function () {
        // Эффект мерцания при наведении на бургер-меню, логотип или кнопку "назад"
        TweenMax.fromTo($(this), 0.5, {opacity: 0.5, ease: Power2.easeInOut},
            {opacity: 1})
    },
    function () {
        $(this).css("opacity", "1")
    });

$('.btn-open-player').hover(function () {
        // Эффект мерцания при наведении на кнопку "Открыть плеер"
        TweenMax.fromTo($(this), 0.5, {opacity: 0.5, ease: Power2.easeInOut},
            {opacity: 1})
    },
    function () {
        $(this).css("opacity", "1")
    });

$('.nav a').hover(function () {
        // Эффект мерцания при наведении на пункты навигационного меню
        TweenMax.fromTo($(this), 0.5, {opacity: 0.5, ease: Power2.easeInOut},
            {opacity: 1})
    },
    function () {
        $(this).css("opacity", "1")
    });

// ===== Выбор элемента в списке плеера =====
$('.list_item').click(function () {
    $('.list_item').removeClass('selected');
    $(this).addClass('selected');
});


// ===== Эффект при наведении на главную кнопку плеера =====
$('.text-wrap .text').hover(function () {
        // Анимация появления обертки главной кнопки плеера
        TweenMax.to($('.main-btn_wrapper'), 0.5, {
            opacity: 1,
            display: 'block',
            position: 'absolute',
            scale: 1,
            ease: Elastic.easeOut.config(1, 0.75)
        })
    },

    function () {
        // Анимация скрытия обертки главной кнопки плеера
        TweenMax.to($('.main-btn_wrapper'), 0.5, {
            opacity: 0,
            display: 'none',
            scale: 0,
            ease: Elastic.easeOut.config(1, 0.75)
        })
    });


// ===== Страница куратора  =====
// ===== Список  =====
$('.item').hover(function () {
        // Анимация поднятия элемента списка
        TweenMax.to($(this), 0.5, {y: -30, ease: Power2.easeInOut}),
            // Добавление тени элементам списка
            $(this).children('.thumb').addClass('shadow'),
            $(this).children('.connect_btn').addClass('shadow'),

            // Плавное появление информации о треке
            TweenMax.to($(this).children('.info'), 0.5, {opacity: 1, ease: Power2.easeInOut})
    },

    function () {
        // Анимация опускания элемента списка
        TweenMax.to($(this), 0.5, {y: 0, ease: Power2.easeInOut}),
            // Удаление тени элементов списка
            $(this).children('.thumb').removeClass('shadow'),
            $(this).children('.connect_btn').removeClass('shadow'),

            // Плавное исчезновение информации о треке
            TweenMax.to($(this).children('.info'), 0.5, {opacity: 0, ease: Power2.easeInOut})
    });


// ===== Переход с главной страницы на страницу куратора  =====
// ===== Активация главной кнопки плеера =====

$('.text-wrap .text').click(function () {

    var homeToMain = new TimelineMax({});

    // Скрытие логотипа
    $('.logo-text').css('display', 'none'),
        // Анимация скрытия обертки главной кнопки плеера
        homeToMain.to($('.text-wrap'), 0.5, {display: 'none', opacity: 0, y: -20, ease: Power2.easeInOut}, 0),

        // Анимация опускания фона
        homeToMain.to($('.wave-container'), 1, {yPercent: 30, ease: Power2.easeInOut}, 0),

        // Показ страницы куратора
        $('#curator').css('display', 'block'),
        // Анимация появления кнопки "назад"
        homeToMain.fromTo($('.back_btn'), 0.8, {x: 15},
            {display: 'flex', opacity: 1, x: 0, ease: Power2.easeInOut}, 1),

        homeToMain.fromTo($('.curator_title_wrapper'), 0.8, {opacity: 0, x: 30},
            {opacity: 1, x: 0, ease: Power2.easeInOut}, 1),

        homeToMain.fromTo($('.curator_list'), 0.8, {opacity: 0, display: 'none', x: 30},
            {opacity: 1, x: 0, display: 'block', ease: Power2.easeInOut}, 1.2)

});


// ===== Переход со страницы куратора на страницу плейлиста  =====
// ===== Активация элемента списка =====

$('.item').click(function () {
    var mainToPlaylist = new TimelineMax({});

    // Скрытие страницы куратора
    mainToPlaylist.to($('#curator'), 0.8, {display: 'none', opacity: 0, scale: 1.1, ease: Power2.easeInOut}, 0)

    // mainToPlaylist.fromTo($('.curator_list'), 0.5, {opacity: 1, display: 'block', x: 0},
    //                   {opacity: 0, x: 30, display: 'none', ease: Power2.easeInOut}, 0.5),


});

// ===== Обработчик клика на кнопке "назад" =====
$('.back_btn').click(function () {
    // ===== Если на странице плейлиста (3), переход на главную (2)
    if ($('#curator').css("display") === "none") {
        var playlistToMain = new TimelineMax({});

        // Скрыть страницу плейлиста и показать главную страницу
        playlistToMain.fromTo($('#curator'), 0.8, {display: 'none', opacity: 0, scale: 1.1},
            {display: 'block', opacity: 1, scale: 1, ease: Power2.easeInOut}, 0)
    }

    // Иначе, если на главной (2), переход на домашнюю страницу (1)
    else {
        var mainToHome = new TimelineMax({});
        // Скрыть элементы страницы куратора
        mainToHome.fromTo($('.curator_title_wrapper'), 0.5, {opacity: 1, x: 0},
            {opacity: 0, x: 30, ease: Power2.easeInOut}, 0.2),

            mainToHome.fromTo($('.curator_list'), 0.5, {opacity: 1, display: 'block', x: 0},
                {opacity: 0, x: 30, display: 'none', ease: Power2.easeInOut}, 0.5),


            mainToHome.to($('.back_btn'), 0.5, {display: 'none', opacity: 0, x: 15, ease: Power2.easeInOut}, 0.5),

            mainToHome.to($('#curator'), 0, {display: 'none', ease: Power2.easeInOut}, 1),

            // Поднять фон
            mainToHome.to($('.wave-container'), 1, {yPercent: 0, ease: Power2.easeInOut}, 1),

            // Показать главную страницу
            mainToHome.to($('.text-wrap'), 0.5, {display: 'flex', opacity: 1, y: 0, ease: Power2.easeInOut}, 1.2),

            mainToHome.to($('.logo-text'), 0.5, {display: 'block', opacity: 1, y: 0, ease: Power2.easeInOut}, 1.2),

            // Принудительно перерисовать кнопку с помощью сдвига по оси Y
            mainToHome.fromTo($('.text-wrap .text'), 0.1, {y: 0.1, position: 'absolute'},
                {y: 0, position: 'relative', ease: Power2.easeInOut}, 1.3)
            // $('.text-wrap .text').css('position', 'relative');
    }
});


// ===== Плеер =====
