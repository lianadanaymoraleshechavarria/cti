const inputs = document.querySelectorAll(".input");

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

/*
* Seccion de Select
*/
const selectInput = document.querySelector(".select-rol")
//const selectElements = document.querySelectorAll(".select-options .element")
const selectElements = document.querySelector(".select-options")
let selection = false

selectInput.addEventListener("click", () => {
    selectInput.classList.toggle("focused")
    if (!selection){
        selectInput.classList.toggle("focus")
        if ( Array.from(selectInput.classList).indexOf("focus") != -1 ){
            selectInput.children[1].innerText = "Selecciona un Rol"
        } else {
            selectInput.children[1].innerText = ""
        }
    }
})

selectElements.addEventListener("click", (e) => {
    if (e.target.className === "element"){
        let trueField = selectInput.children[0]
        let fakeField = selectInput.children[1]
        trueField.value = e.target.ariaValueText
        fakeField.innerText = e.target.innerText
        selection = true
        selectInput.classList.toggle("focused")
    }
})

