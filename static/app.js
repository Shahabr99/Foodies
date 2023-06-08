"use strict";
const apiKey = 'a5f08c9f2abb42468054a03050e7a368'

const searchbar = document.querySelector('#searchbar')
const searchForm = document.querySelector('.search-form')
const mealSection = document.querySelector('.meal-section')

searchForm.addEventListener('submit', async function(e) {
    e.preventDefault()
    const val = searchbar.value
    const res = await axios.get(`https://api.spoonacular.com/recipes/complexSearch?apiKey=${apiKey}&query=${val}`)
    const mealArray = res.data.results
    mealArray.forEach(meal => function(){
        const card = document.createElement('div')
        
    })
})