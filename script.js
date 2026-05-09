let step = 0;

function nextStep() {
    const subtitle = document.getElementById("subtitle");
    const desc = document.getElementById("desc");
    const btn = document.getElementById("nextBtn");

    step++;

    if (step === 1) {
        subtitle.classList.remove("hidden");
        subtitle.innerText = "Turning ideas into impact through code and data";
    }

    else if (step === 2) {
        desc.classList.remove("hidden");
        desc.innerText =
            "Hey! I am Sambhav Sahoo — a developer and data enthusiast who loves building impactful solutions and constantly growing.";
    }

    else {
        btn.innerText = "Explore →";
        btn.onclick = () => window.location.href = "/projects";
    }
}

/* 🔥 BONUS: avatar follow cursor */
const avatar = document.querySelector(".avatar");

document.addEventListener("mousemove", (e) => {
    const x = (window.innerWidth / 2 - e.pageX) / 40;
    const y = (window.innerHeight / 2 - e.pageY) / 40;

    avatar.style.transform = `rotateY(${x}deg) rotateX(${y}deg)`;
});