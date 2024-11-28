document.addEventListener('DOMContentLoaded', function () {
    const searchInput = document.getElementById('searchInput');
    const searchIcon = document.querySelector('.search-input .bi-search');
    const dropdownButton = document.querySelector('.categories-dropdown');
    const modal = document.querySelector('.modal');
    const cartButtons = document.querySelectorAll('.add-to-cart-btn');

    searchInput.addEventListener('input', function () {
        searchIcon.style.opacity = searchInput.value.trim() ? '0' : '1';
    });

    if (dropdownButton && modal) {
        dropdownButton.addEventListener('click', function (event) {
            event.stopPropagation();
            modal.style.display = 'flex';
        });

        document.addEventListener('keydown', function (e) {
            if (e.key === 'Escape' && modal.style.display === 'flex') {
                modal.style.display = 'none';
            }
        });

        document.addEventListener('click', function (event) {
            if (!modal.contains(event.target) && modal.style.display === 'flex') {
                modal.style.display = 'none';
            }
        });
    }

    cartButtons.forEach(button => {
        button.addEventListener('click', function () {
            const cartQuantityContainer = this.closest('.cart-quantity-container');
            const quantityContainer = cartQuantityContainer.querySelector('.quantity-container');

            // Скрываем кнопку "В корзину"
            this.style.display = 'none';

            // Показываем контейнер с количеством
            quantityContainer.style.display = 'flex';

            // Устанавливаем начальное количество
            const quantityDisplay = quantityContainer.querySelector('.quantity-display');
            quantityDisplay.textContent = '1';
        });
    });

    // Обработчики для кнопок + и -
    document.querySelectorAll('.quantity-btn').forEach(btn => {
        btn.addEventListener('click', function () {
            const quantityContainer = this.closest('.quantity-container');
            const quantityDisplay = quantityContainer.querySelector('.quantity-display');
            let currentQuantity = parseInt(quantityDisplay.textContent);

            if (this.classList.contains('plus')) {
                currentQuantity++;
            } else if (this.classList.contains('minus')) {
                currentQuantity = Math.max(0, currentQuantity - 1);

                // Если количество 0, возвращаем кнопку "В корзину"
                if (currentQuantity === 0) {
                    const cartQuantityContainer = this.closest('.cart-quantity-container');
                    cartQuantityContainer.querySelector('.add-to-cart-btn').style.display = 'inline-block';

                    // Скрываем контейнер с количеством
                    quantityContainer.style.display = 'none';
                }
            }

            quantityDisplay.textContent = currentQuantity;
        });
    });
});
