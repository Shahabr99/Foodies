"use strict";
const shoppingItem = document.querySelectorAll(".shopping-list");
const checkboxs = document.querySelectorAll(".check");
const shoppingItemArr = Array.from(shoppingItem);
const checkboxsArr = Array.from(checkboxs);

let click = 0;

// checkbox.addEventListener("click", function (e) {
//   if (e.target === checkbox) {
//     e.target.parentElement.classList.add("clicked");
//     click += 1;
//   }
//   if (click % 2 === 0) {
//     e.target.parentElement.classList.remove("clicked");
//   }
// });

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
