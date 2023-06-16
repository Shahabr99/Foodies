"use strict";
const closeBtns = document.querySelectorAll(".cls-btn");
const shoppingItem = document.querySelectorAll(".shopping-list");
const checkboxs = document.querySelectorAll(".check");
const shoppingItemArr = Array.from(shoppingItem);
const checkboxsArr = Array.from(checkboxs);

let click = 0;

// Getting all the checkboxes and adding a line through to the bought items
for (let checkbox of checkboxs) {
  checkbox.addEventListener("click", function (e) {
    if (e.target.className === "check") {
      e.target.parentElement.classList.add("clicked");
      click += 1;
    }
    if (click % 2 === 0) {
      e.target.parentElement.classList.remove("clicked");
    }
  });
}

for (let closeBtn of closeBtns) {
  closeBtn.addEventListener("click", function (e) {
    if (e.target.className.includes("cls-btn")) {
      e.preventDefault();
      e.target.closest("div").style.display = "none";
    }
  });
}
