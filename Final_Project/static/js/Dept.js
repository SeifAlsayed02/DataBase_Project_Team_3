console.log("hello");

// let dept = document.querySelectorAll("input[name=department]").checked;
// let dept = document.querySelector(".department").value;
// let dept2 = document.getElementById("dept2");
let dept1 = document.getElementById("dept1");
let dept2 = document.getElementById("dept2");
let place = document.querySelector(".dept span");
let root_theme = document.querySelector(":root").checked;

console.log(dept1);
// console.log(dept2);

// if (dept1.checked == true) {
//   console.log("card");

function checkButton() {
  if (dept1.checked == true) {
    console.log("card");
  }
  if (dept2.checked == true) {
    console.log("icu");
    // place.textContent = "ICU";
    root_theme.style.setProperty("--color-primary", "#005383");
    root_theme.style.setProperty("--color-low", "#006291");
    root_theme.style.setProperty("--color-secondary", "#f85a40");
  }
}
// if (dept2.checked) {
//   console.log("icu");
// }
// if (dept.value == "dept2") {
//   place.textContent = "Cardiology";
//   console.log("card");
// } else {
//   console.log("icu");
//   place.textContent = "ICU";
//   root_theme.style.setProperty("--color-primary", "#005383");
//   root_theme.style.setProperty("--color-low", "#006291");
//   root_theme.style.setProperty("--color-secondary", "#f85a40");
// }

// dept2.addEventListener("click", () => {
//   place.textContent = "ICU";
//   root_theme.style.setProperty("--color-primary", "#005383");
//   root_theme.style.setProperty("--color-low", "#006291");
//   root_theme.style.setProperty("--color-secondary", "#f85a40");
// });

// function changeColor() {
//   const selectedColor = document.querySelector(
//     'input[name="department"]:checked'
//   ).value;
//   if (selectedColor == dept2) {
//     place.textContent = "ICU";
//     root_theme.style.setProperty("--color-primary", "#005383");
//     root_theme.style.setProperty("--color-low", "#006291");
//     root_theme.style.setProperty("--color-secondary", "#f85a40");
//   }
// }

// changeColor();

// var selectedDepartment;

// if (document.getElementById("dept1").value) {
//   selectedDepartment = "dept1";
//   console.log("in if condition");
// } else if (document.getElementById("dept2").value) {
//   console.log("in if 2condition");
//   selectedDepartment = "dept2";
// }

// if (selectedDepartment == "dept2") {
//   console.log("Reached dept2");
//   place.textContent = "ICU";
//   root_theme.style.setProperty("--color-primary", "#005383");
//   root_theme.style.setProperty("--color-low", "#006291");
//   root_theme.style.setProperty("--color-secondary", "#f85a40");
// }
