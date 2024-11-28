document.addEventListener('DOMContentLoaded', function () {
    const searchInput = document.getElementById('searchInput');
    const searchIcon = document.querySelector('.search-input .bi-search');
    const dropdownButton = document.querySelector('.categories-dropdown');
    const modal = document.querySelector('.modal');

    searchInput.addEventListener('input', function () {
        if (searchInput.value.trim() !== '') {
            searchIcon.style.opacity = '0';
        } else {
            searchIcon.style.opacity = '1';
        }
    });

    dropdownButton.addEventListener('click', function (event) {
        event.stopPropagation();
        modal.style.display = 'flex';
    });

    document.addEventListener('keydown', function (e) {
        if (e.key === 'Escape' && modal.style.display !== 'none') {
            modal.style.display = 'none';
        }
    });

    document.addEventListener('click', function (event) {
        if (!modal.contains(event.target) && modal.style.display === 'flex') {
            modal.style.display = 'none';
        }
    });
});
