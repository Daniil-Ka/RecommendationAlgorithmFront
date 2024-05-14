$(document).ready(function () {
    $('#submit-button').click(function () {
        // Скрываем темную область
        TweenMax.to(".dim", 0.5, {opacity: 0, display: 'none', ease: Power2.easeInOut});
        // Анимация закрытия плеера
        TweenMax.to("#player", 0.5, {xPercent: 100, display: 'none', ease: Expo.easeOut});
        // Анимация закрытия навигационного меню
        TweenMax.to(".nav", 0.5, {xPercent: -100, display: 'none', ease: Power2.easeInOut})
        // Возвращение мини-плеера на место
        TweenMax.to(".mini-player", 0.5, {x: 0, ease: Expo.easeOut});
    });

    // и/или
    $('.andor-button').click(function () {
        $(this).toggleClass('active')
    });

    // фильтры
    const settings = {
        theme: "facebook",
        hintText: "Поиск...",
        searchingText: "Поиск...",
        noResultsText: "Ничего не найдено",
        resultsLimit: 10,
        preventDuplicates: true,
        tokenLimit: 5,

        onResult: function(results) {
            console.log(results)
              // Фильтрация уже выбранных языков из результатов
            return results.filter(function (result) {
                let selectedLanguages = $('#search-input1').val() || [];
                return !selectedLanguages.includes(result.id);
            });
        }
    }

    $("#search-input1").tokenInput('filters/genre', settings);
    $("#search-input2").tokenInput('filters/lang', settings);
    $("#search-input3").tokenInput('filters/mood', settings);
    $("#search-input4").tokenInput('filters/similar', settings);

    // отправка данных фильтра
    $('#submit-button').click(function () {


        const selectedTime = $("#time-select").val();
        const excludeProfanity = $("#profanity").is(":checked");
        const excludeRestricted = $("#exclude-restricted").is(":checked");

        let AllSelectedOptions = []
        $('.filter').each(function (index) {
            let $filter = $(this);
            let $searchInput = $filter.find('.search-input');
            let $filterTitle = $filter.find('.filter-title');

            let selected = $searchInput.tokenInput("get")

            AllSelectedOptions.push({filter: $filterTitle.text(), selected: selected})
        });

        $.ajax({
            url: "/algorithm/apply_filters/",
            type: 'POST',
            contentType: 'application/json',
            data: JSON.stringify({
                filters: AllSelectedOptions,
                time: selectedTime,
                profanity: excludeProfanity,
                exclude_restricted: excludeRestricted
            }),
            beforeSend: function(xhr) {
                xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
             },
            success: function(data) {
            console.log("Ответ от сервера:", data);
            },
            error: function() {
            console.error("Error");
            }
        });
    });
});

function getCookie(name) {
	var matches = document.cookie.match(new RegExp("(?:^|; )" + name.replace(/([\.$?*|{}\(\)\[\]\\\/\+^])/g, '\\$1') + "=([^;]*)"));
	return matches ? decodeURIComponent(matches[1]) : undefined;
}