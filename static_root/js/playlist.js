const $list = $('.recommendations-list');
let activeIndex = 0; // Начальный активный элемент
let recommendationCount = 5; // Начальное количество рекомендаций

// Функция создания элемента
function createRecommendationComponent(title, artist) {
    return $(`
        <div class="recommendations_info_wrapper">
            <div class="recommendations_thumb"></div>
            <div class="recommendations_info">
                <div class="recommendations_title">${title}</div>
                <div class="recommendations_artist">${artist}</div>
            </div>
        </div>
    `);
}

const updateList = () => {
    const hideDelta = 3; // а каком удалее начинаем скрывать элементы
    const $items = $('.recommendations_info_wrapper');
    $items.removeClass('active hidden half-hidden');
    $items.eq(activeIndex).addClass('active');

    // Управляем классом 'hidden' и 'half-hidden' для элементов, находящихся близко к краю
    $items.each(function(index) {
        if (index < activeIndex - hideDelta || index > activeIndex + hideDelta) {
            $(this).addClass('hidden');
        } else if (index === activeIndex - hideDelta || index === activeIndex + hideDelta) {
            $(this).addClass('half-hidden');
        }
    });
    scrollToActive();
};

const scrollToActive = () => {
    const $activeItem = $('.recommendations_info_wrapper.active');
    const containerHeight = $list.height();
    const itemHeight = $activeItem.outerHeight(true);
    const scrollPosition = $activeItem.position().top - containerHeight / 2 + itemHeight / 2;
    const windowHeight = $(window).height();
    console.log(-scrollPosition + windowHeight / 2)
    $list.stop().animate({top: -scrollPosition + windowHeight / 2}, 500);
};

const rotateList = (direction) => {
    const $items = $('.recommendations_info_wrapper');
    const newIndex = direction === 'next' ? activeIndex + 1 : activeIndex - 1;

    // Ограничиваем значение newIndex от 0 до (длины списка - 1)
    activeIndex = Math.max(0, Math.min(newIndex, $items.length - 1));

    updateList(); // Обновляем список
};

const addRecommendation = (title, artist, photo_url, $list) => {
    const $items = $('.recommendations_info_wrapper');
    recommendationCount++;
    const $element = createRecommendationComponent(title, artist);
    $element.find('.recommendations_thumb').css('background-image', photo_url);

    $list.append($element);
    activeIndex = $list.children().length - 1;
    updateList();
};

const removeRecommendation = () => {
    const $items = $('.recommendations_info_wrapper');
    if ($items.length > 0) {
        $items.last().remove();
        if (activeIndex >= $items.length - 1) {
            activeIndex = $items.length - 2;
            if (activeIndex < 0) {
                activeIndex = 0;
            }
        }
        updateList();
    }
};

