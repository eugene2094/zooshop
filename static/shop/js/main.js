// Ждём загрузки всего документа
document.addEventListener('DOMContentLoaded', function () {
    // Уведомление при добавлении товара в корзину
    const cartButtons = document.querySelectorAll('.btn-outline-primary');

    cartButtons.forEach(button => {
        button.addEventListener('click', function (e) {
            if (button.innerText.includes('Корзина')) {
                alert('Перейдите в корзину для оформления заказа.');
            }
        });
    });

    const links = document.querySelectorAll('a[href^=\"#\"]');

    links.forEach(link => {
        link.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth'
                });
            }
        });
    });

    // Подсветка активного пункта меню
    const currentLocation = location.href;
    const menuItems = document.querySelectorAll('aside a');

    menuItems.forEach(item => {
        if (item.href === currentLocation) {
            item.classList.add('active');
            item.style.fontWeight = 'bold';
        }
    });
});
