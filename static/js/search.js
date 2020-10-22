document.addEventListener("DOMContentLoaded", () => {
    const urlParams = new URLSearchParams(window.location.search);
    const searchTerm = urlParams.get('query');
    const input = document.querySelector(".input-search");

    const searchTitle = document.querySelector(".search-term");

    searchTitle.innerText = "\"" + searchTerm + "\"";
    input.value = searchTerm;
});


