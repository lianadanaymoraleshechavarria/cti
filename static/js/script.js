const menuItemList = document.querySelectorAll('.nav-item')
const path = window.location.pathname.split("/")[1]

menuItemList.forEach(e => {
    if(e.ariaLabel === path){
        let currentlyActive = document.querySelector(".nav-item .active")
        currentlyActive.classList.toggle("active")
        e.children[0].classList.toggle("active")
    }
})