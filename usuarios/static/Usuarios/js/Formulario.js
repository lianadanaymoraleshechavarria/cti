const inputs = document.querySelectorAll(".input");
const selectInput = document.querySelector(".select-municipio")

function focusFunc(){
    let parent = this.parentNode;
    parent.classList.add("focus");
}
function blurFunc(){
    let parent = this.parentNode;
    if(this.value == ""){
        parent.classList.remove("focus");
    }
}

inputs.forEach(input => {
    input.addEventListener("focus",focusFunc);
    input.addEventListener("blur",blurFunc);
})

selectInput.addEventListener("click", () => {
    selectInput.children[0].classList.toggle("toggled")
})

