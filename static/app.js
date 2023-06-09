"use strict";

const searchbar = document.querySelector("#searchbar");
const searchForm = document.querySelector(".search-form");
const mealSection = document.querySelector(".meal-section");

searchForm.addEventListener("submit", async function (e) {
  e.preventDefault();
  const val = searchbar.value;
  const res = await axios.get(
    `https://api.spoonacular.com/recipes/complexSearch?apiKey=${apiKey}&query=${val}`
  );
  const mealArray = res.data.results;
  console.log(mealArray);
  mealArray.forEach(function (meal) {
    const html = `<div class="card" style="width: 18rem;">
        <img src="${meal.image}" class="card-img-top" alt="...">
        <div class="card-body">
          <h5 class="card-title">${meal.title}</h5>
          <p class="card-text">Some quick example text to build on the card title and make up the bulk of the card's content.</p>
          <a href="#" class="btn btn-primary">Select</a>
        </div>
      </div>`;
    mealSection.insertAdjacentHTML("beforeend", html);
  });
});
