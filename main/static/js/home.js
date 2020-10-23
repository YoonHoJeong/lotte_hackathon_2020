const handleBtnClick = (e) => {
    e.preventDefault();
    const answer = confirm("정말 삭제하시겠습니까?");
    if (answer) {
        console.log(e.target.parentNode);
        e.target.parentNode.submit();
    }
}

const handlePosterEnter = (e) => {
    const poster = e.target;
    const posterFg = poster.querySelector(".poster-fg");
    posterFg.style.display = "flex";
}
const handlePosterLeave = (e) => {
    const poster = e.target;
    const posterFg = poster.querySelector(".poster-fg");
    posterFg.style.display = "none";
}

document.addEventListener("DOMContentLoaded", () => {
    const element = document.querySelector(".vote-container");
    $("html, body").animate({
        scrollTop: $(".vote-container").position().top
    }, 700);

    const deleteBtns = document.querySelectorAll(".delete-btn");
    deleteBtns.forEach(btn => {
        btn.addEventListener("click", handleBtnClick);
    })

    const posters = document.querySelectorAll(".movie-poster");
    posters.forEach(poster => {
        poster.addEventListener("mouseenter", handlePosterEnter);
        poster.addEventListener("mouseleave", handlePosterLeave);
    })

});