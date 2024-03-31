console.log(filters)
$(document).ready(function () {
    $('.filter').each(function (index) {
        var $filter = $(this);
        var $searchInput = $filter.find('.search-input');
        var $filterOptions = $filter.find('.filter-options');
        var options = filters[index]; // Получаем список элементов для текущего фильтра

        var allOptions = options.slice(); // Создаем копию исходного списка
        var selectedOptions = []; // Массив для хранения выбранных элементов

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
});