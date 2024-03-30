$(document).ready(function() {
  var options = [
    'Элемент 1',
    'Элемент 2',
    'Элемент 3',
  ];

  var allOptions = options.slice(); // Создаем копию исходного списка
  var selectedOptions = []; // Массив для хранения выбранных элементов

  function addOptionToFilter(optionText) {
    var optionElement = $('<div class="option">' + optionText + '</div>');
    optionElement.click(function() {
      var selectedOption = $(this).text();
      var selectedOptionElement = $('<div class="option selected-option">' + selectedOption + '</div>');
            selectedOptionElement.click(function() {
            var unselectedOption = $(this).text();

            $(this).remove(); // Удаляем выбранный элемент при клике на него

            selectedOptions = selectedOptions.filter(function(item) {
              return item !== unselectedOption;
            });

            restartSearch();
            //addOptionToFilter(unselectedOption); // Добавляем элемент обратно в список
      });

      $('.filter-options').prepend(selectedOptionElement);
      selectedOptions.unshift(selectedOption);
      $(this).remove(); // Удаляем элемент из списка выбранных при клике на него
    });
    $('.filter-options').append(optionElement);
  }

  //
  function displaySelectedOptions() {
    //$('.filter-options').empty(); // Очищаем список выбранных элементов перед обновлением
    $.each(selectedOptions, function(index, value) {
      var selectedOptionElement = $('<div class="option selected-option">' + value + '</div>');

      selectedOptionElement.click(function() {
            var unselectedOption = $(this).text();

            $(this).remove(); // Удаляем выбранный элемент при клике на него

            selectedOptions = selectedOptions.filter(function(item) {
              return item !== unselectedOption;
            });

            restartSearch();
            //addOptionToFilter(unselectedOption); // Добавляем элемент обратно в список
      });

      $('.filter-options').append(selectedOptionElement);
    });
  }

     function restartSearch() {
        var searchText = $('.search-input').val().trim().toLowerCase();
            $('.filter-options').empty(); // Очищаем список перед обновлением
        displaySelectedOptions();

        // Фильтруем элементы на основе введенного текста
        $.each(allOptions, function(index, option) {
          if (option.toLowerCase().includes(searchText) && searchText && !selectedOptions.includes(option)) {
            addOptionToFilter(option);
          }
        });
      }

  $('.search-input').on('input', function() {
    var searchText = $(this).val().trim().toLowerCase();
    $('.filter-options').empty(); // Очищаем список перед обновлением
      displaySelectedOptions();

      // Фильтруем элементы на основе введенного текста
      $.each(allOptions, function(index, option) {
        if (option.toLowerCase().includes(searchText) && searchText && !selectedOptions.includes(option)) {
          addOptionToFilter(option);
        }
      });
  });
});