document.addEventListener('DOMContentLoaded', function() {
    const slider = document.querySelector('.slider');
    const images = document.querySelectorAll('.slider img');
    let currentIndex = 0;
    const intervalTime = 3000; // 3 секунды

    // Клонируем первую картинку и добавляем её в конец
    const firstImageClone = images[0].cloneNode(true);
    slider.appendChild(firstImageClone);

    function nextSlide() {
        currentIndex++;
        slider.style.transition = 'transform 0.5s ease';
        slider.style.transform = `translateX(-${currentIndex * 100}%)`;

        // Если дошли до клонированной картинки (последний слайд + 1)
        if (currentIndex === images.length) {
            setTimeout(() => {
                slider.style.transition = 'none'; // Отключаем анимацию
                currentIndex = 0;
                slider.style.transform = 'translateX(0)';
            }, 500); // Ждём окончания анимации (0.5s)
        }
    }

    setInterval(nextSlide, intervalTime);
});