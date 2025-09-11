const steps = document.querySelectorAll(".form-step");
const nextBtns = document.querySelectorAll(".next");
const prevBtns = document.querySelectorAll(".prev");
const progress = document.getElementById("progress");

let formSteps = 0;

nextBtns.forEach(btn => {
  btn.addEventListener("click", () => {
    if (formSteps < steps.length - 1) {
      steps[formSteps].classList.remove("active");
      formSteps++;
      steps[formSteps].classList.add("active");
      progress.style.width = ((formSteps) / (steps.length - 1)) * 100 + "%";
    }
  });
});

prevBtns.forEach(btn => {
  btn.addEventListener("click", () => {
    if (formSteps > 0) {
      steps[formSteps].classList.remove("active");
      formSteps--;
      steps[formSteps].classList.add("active");
      progress.style.width = ((formSteps) / (steps.length - 1)) * 100 + "%";
    }
  });
});
