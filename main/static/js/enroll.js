document.addEventListener("DOMContentLoaded", () => {
    const enrollBtns = document.querySelectorAll(".enroll-btn");
    const enrollForm = document.querySelector(".enroll-form");
    const enrollFormBG = document.querySelector(".enroll-form-background");
    const confirmBtn = enrollForm.querySelector(".confirm-btn");
    const inputmovieId = enrollForm.querySelector("#movie-id")
    const inputmovieSeq = enrollForm.querySelector("#movie-seq")
    
    let movieTitle, movieId, movieSeq;

    enrollBtns.forEach(enrollBtn => {
        enrollBtn.addEventListener("click", (e) => {
            e.preventDefault();
            const myForm = e.target.parentNode.parentNode;
            movieTitle = myForm.querySelector(".movie-title").innerText;
            let inputs = myForm.querySelectorAll("input");
            inputs = inputs.forEach(input => {
                if (input.name === "movieId") {
                    movieId = input.value;
                }
                if (input.name === "movieSeq") {
                    movieSeq = input.value;
                }
            })
            console.log(movieTitle);
            enrollFormBG.style.display = 'flex';
            enrollForm.querySelector(".form-title").innerText = movieTitle;
        })
        enrollBtn.addEventListener("submit", (e) => {
            e.preventDefault();
            
        })
    })
    confirmBtn.addEventListener('click', (e) => {
        enrollFormBG.style.display = 'none';
        inputmovieId.value = movieId;
        inputmovieSeq.value = movieSeq;

        enrollForm.submit();
    })
});