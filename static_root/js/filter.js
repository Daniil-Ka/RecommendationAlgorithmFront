$(document).ready(function () {
    let AllSelectedOptions = []

    // отправка данных фильтра
    $('#submit-button').click(function () {
        const selectedTime = $("#time-select").val();
        const excludeProfanity = $("#profanity").is(":checked");
        const excludeRestricted = $("#exclude-restricted").is(":checked");

        console.log($("#search-input1").tokenInput("get"))

        $.ajax({
            url: "/send-data",
            type: 'POST',
            contentType: 'application/json',
            data: JSON.stringify({
                filters: AllSelectedOptions,
                time: selectedTime,
                profanity: excludeProfanity,
                exclude_restricted: excludeRestricted
            }),
            success: function(data) {
            console.log("Ответ от сервера:", data);
            },
            error: function() {
            console.error("Error");
            }
        });
    });

    $('.filter').each(function (index) {
        var $filter = $(this);
        var $searchInput = $filter.find('.search-input');
        var $filterOptions = $filter.find('.filter-options');
        var options = filters[index]; // Получаем список элементов для текущего фильтра

        var allOptions = options.slice(); // Создаем копию исходного списка
        var selectedOptions = []; // Массив для хранения выбранных элементов
        AllSelectedOptions.push({filter: $filter.find('.filter-title').text(), selected: selectedOptions})

        function addOptionToFilter(optionText) {
            var optionElement = $('<div class="option">' + optionText + '</div>');
            optionElement.click(function () {
                var selectedOption = $(this).text();
                var selectedOptionElement = $('<div class="option selected-option">' + selectedOption + '</div>');

                selectedOptionElement.click(function () {
                    var unselectedOption = $(this).text();
                    $(this).remove(); // Удаляем выбранный элемент при клике на него
                    selectedOptions = selectedOptions.filter(function (item) {
                        return item !== unselectedOption;
                    });
                    restartSearch();
                });

                $filterOptions.prepend(selectedOptionElement);
                selectedOptions.unshift(selectedOption);
                $(this).remove(); // Удаляем элемент из списка выбранных при клике на него
            });
            $filterOptions.append(optionElement);
        }

        function displaySelectedOptions() {
            $filterOptions.empty(); // Очищаем список выбранных элементов перед обновлением
            $.each(selectedOptions, function (index, value) {
                var selectedOptionElement = $('<div class="option selected-option">' + value + '</div>');
                selectedOptionElement.click(function () {
                    var unselectedOption = $(this).text();
                    $(this).remove(); // Удаляем выбранный элемент при клике на него
                    selectedOptions = selectedOptions.filter(function (item) {
                        return item !== unselectedOption;
                    });
                    restartSearch();
                });
                $filterOptions.append(selectedOptionElement);
            });
        }

        function restartSearch() {
            var searchText = $searchInput.val().trim().toLowerCase();
            $filterOptions.empty(); // Очищаем список перед обновлением
            displaySelectedOptions();

            // Фильтруем элементы на основе введенного текста
            $.each(allOptions, function (index, option) {
                if (option.toLowerCase().includes(searchText) && searchText && !selectedOptions.includes(option)) {
                    addOptionToFilter(option);
                }
            });
        }

        $searchInput.on('input', function () {
            restartSearch();
        });

        // Инициализируем список фильтрации при загрузке страницы
        $.each(allOptions, function (index, option) {
            addOptionToFilter(option);
        });
        displaySelectedOptions();
    });

    $('.andor-button').click(function () {
        $(this).toggleClass('active')
    });
});

// =================================


$(document).ready(function () {
    $("#search-input1").tokenInput([
    { id: 0, name: "english" },
    { id: 1, name: "spanish" },
    { id: 2, name: "french" }
    // Добавьте другие варианты языков по вашему усмотрению
  ], {
        theme: "facebook",
        hintText: "Поиск...",
        searchingText: "Поиск...",
        noResultsText: "Ничего не найдено",
        resultsLimit: 10,
        preventDuplicates: true,
        tokenLimit: 5,

        onResult: function(results) {
              // Фильтрация уже выбранных языков из результатов
            var filteredResults = results.filter(function(result) {
                var selectedLanguages = $('#search-input1').val() || [];
                return !selectedLanguages.includes(result.id);
            });
            return filteredResults;
        }
    }
    );
    //$("#filter1").tokenInput("/users/autocomplete");
});