var keys = {
    37: 1,
    38: 1,
    39: 1,
    40: 1
};

function preventDefault(e) {
    e.preventDefault();
}

function preventDefaultForScrollKeys(e) {
    if (keys[e.keyCode]) {
        preventDefault(e);
        return false;
    }
}

// modern Chrome requires { passive: false } when adding event
var supportsPassive = false;
try {
    window.addEventListener("test", null, Object.defineProperty({}, 'passive', {
        get: function () {
            supportsPassive = true;
        }
    }));
} catch (e) {}

var wheelOpt = supportsPassive ? {
    passive: false
} : false;

var wheelEvent = 'onwheel' in document.createElement('div') ? 'wheel' : 'mousewheel';

// call this to Disable
function disableScroll() {
    window.addEventListener('DOMMouseScroll', preventDefault, false); // older FF
    window.addEventListener(wheelEvent, preventDefault, wheelOpt); // modern desktop
    window.addEventListener('touchmove', preventDefault, wheelOpt); // mobile
    window.addEventListener('keydown', preventDefaultForScrollKeys, false);
}

// call this to Enable
function enableScroll() {
    window.removeEventListener('DOMMouseScroll', preventDefault, false);
    window.removeEventListener(wheelEvent, preventDefault, wheelOpt);
    window.removeEventListener('touchmove', preventDefault, wheelOpt);
    window.removeEventListener('keydown', preventDefaultForScrollKeys, false);
}

document.addEventListener("DOMContentLoaded", () => {
    const enrollBtns = document.querySelectorAll(".enroll-btn");
    const enrollForm = document.querySelector(".enroll-form");
    const enrollFormBG = document.querySelector(".enroll-form-background");
    const confirmBtn = enrollForm.querySelector(".confirm-btn");
    const cancelBtn = enrollForm.querySelector(".cancel-btn");

    const inputmovieId = enrollForm.querySelector("#movie-id")
    const inputmovieSeq = enrollForm.querySelector("#movie-seq")

    let movieTitle, movieId, movieSeq;

    console.log(cancelBtn);
    cancelBtn.addEventListener("click", (e) => {
        e.preventDefault();
        enrollFormBG.style.display = 'none';
    })
    cancelBtn.addEventListener("submit", (e) => {
        e.preventDefault();
    })

    enrollBtns.forEach(enrollBtn => {
        enrollBtn.addEventListener("click", (e) => {
            e.preventDefault();
            disableScroll();

            console.log(e);

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

            enrollFormBG.style.display = 'flex';
            enrollForm.querySelector(".form-title").innerText = "\"" + movieTitle + "\"";
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