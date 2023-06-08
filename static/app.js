"use strict";

const searchbar = document.querySelector('#searchbar')
const searchForm = document.querySelector('.search-form')

searchForm.addEventListener('submit', function(e) {
    e.preventDefault()
    const val = searchbar.value
    const res = axios.get(`https://api.spoonacular.com/recipes/complexSearch?query=${val}`)
    console.log(res)
})