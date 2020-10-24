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
    const alertForm = enrollFormBG.querySelector(".alert-form");
    const yesBtn = alertForm.querySelector('.yes-btn');

    const inputmovieId = enrollForm.querySelector("#movie-id")
    const inputmovieSeq = enrollForm.querySelector("#movie-seq")

    let movieTitle, movieId, movieSeq;

    $('.enrollForm').submit(function (e) {
        e.preventDefault();
        $.ajax({
            type: 'POST',
            url: 'submit.php',
            data: $(this).serialize(),
            error: function () {
                alert("Request Failed");
            },
            success: function (response) {
                //EXECUTE ANIMATION HERE
            } // this was missing
        });

    })

    cancelBtn.addEventListener("click", (e) => {
        e.preventDefault();
        enableScroll();
        enrollFormBG.style.display = 'none';
    })
    cancelBtn.addEventListener("submit", (e) => {
        e.preventDefault();

    })

    enrollBtns.forEach(enrollBtn => {
        enrollBtn.addEventListener("click", (e) => {
            e.preventDefault();
            console.log(e.target.parentNode.parentNode);
            disableScroll();
            enrollForm.style.display = 'flex';
            console.log(enrollForm);
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
        e.preventDefault();
        enrollForm.style.display = 'none';
        alertForm.style.display = 'flex';

        inputmovieId.value = movieId;
        inputmovieSeq.value = movieSeq;

        var res = enrollForm.submit();
        console.log(res);
    })
    confirmBtn.addEventListener('submit', (e) => {})
    yesBtn.addEventListener('click', (e) => {
        e.preventDefault();
        enrollFormBG.style.display = 'none';
        alertForm.style.display = 'none';
    })
});