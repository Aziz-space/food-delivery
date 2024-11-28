document.addEventListener('DOMContentLoaded', function () {
    const searchInput = document.getElementById('searchInput');
    const searchIcon = document.querySelector('.search-input .bi-search');

    searchInput.addEventListener('input', function() {
        if (searchInput.value.trim() !== '') {
            searchIcon.style.opacity = '0';
        } else {
            searchIcon.style.opacity = '1';
        }
    });
});
