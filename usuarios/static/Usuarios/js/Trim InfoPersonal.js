var nombre = document.getElementById("inputName");
var apellidos = document.getElementById("inputLastName");
var carnet = document.getElementById("inputCi")
var email = document.getElementById("inputEmail")
var telefono = document.getElementById("inputNt")
var text = document.getElementById("inputText")
var boton =  document.getElementById("boton");


const validate_space_trim = () => {
  email.value = email.value.trim();
  carnet.value = carnet.value.trim();
  telefono.value = telefono.value.trim();
}
  const errorContainer = document.querySelector("#error-container")
        const createMessage = (message) => {
            return `
            <div class="alert alert-danger alert-dismissible fade show" role="alert"
            style="position: fixed; right: 20px; top: 50px; display: flex; align-items: center; padding-right: 0rem; z-index: 2000">
            ${message}
            <button style="font-size: 10px; border-bottom: none; position: relative; box-shadow: none;" type="button"
            class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
            </button>
            </div>
            `
        }
        
const c = (e)=>{
  let validador = /^\w+([.-_+]?\w+)*@\w+([.-]?\w+)*(\.\w{2,10})+$/
  let mensaje = ""
  if(nombre.value == "" || Number.isInteger(parseFloat(nombre.value))){
    nombre.style = "border:solid 2px red;"
    mensaje += `Campo 'Nombre' en blanco o esta incorrecto <br>`
    e.preventDefault()
  }
  else{
    nombre.style = "border:solid 2px green;"
  }
  if(apellidos.value == "" || Number.isInteger(parseFloat(apellidos.value))){
    apellidos.style = "border:solid 2px red;"
    mensaje += `Campo 'Apellidos' en blanco o esta incorrecto <br>`
    e.preventDefault()
  }
  else{
    apellidos.style = "border:solid 2px green;"
  }
  if(carnet.value == "" || isNaN(carnet.value) || carnet.value.length != 11 ){
    carnet.style = "border:solid 2px red;"
    mensaje += `Campo 'Carnet' en blanco o esta incorrecto <br>`
    e.preventDefault()
  }
  else{
    carnet.style = "border:solid 2px green;"
  }
  if(email.value == ""){
    email.style = "border:solid 2px red;"
    mensaje += `Campo 'Email' en blanco <br>`
    e.preventDefault()
  }
  else{ 
    email.style = "border:solid 2px green;"
  }
  if (!validador.test(email.value)) {
    email.style = "border:solid 2px red;"
    mensaje += `Campo 'Email' no es válido <br>`
    e.preventDefault()  
  }
  else{ 
    email.style = "border:solid 2px green;"
  }
  
  if(telefono.value.length != 8  ||isNaN(telefono.value) || telefono.value == ""){
    telefono.style = "border:solid 2px red;"
    mensaje += `Campo 'Teléfono' en blanco o esta incorrecto <br>`
    e.preventDefault()
  }
  else{
    telefono.style = "border:solid 2px green;"
  }
  if(text.value == ""){
    text.style = "border:solid 2px red;"
    mensaje += `Campo 'Dirección' en blanco <br>`
    e.preventDefault()
  }
  else{
    text.style = "border:solid 2px green;"
  }
  if (mensaje) {
    errorContainer.innerHTML += createMessage(mensaje)
  }
  }
email.addEventListener("input",validate_space_trim);
carnet.addEventListener("input",validate_space_trim);
telefono.addEventListener("input",validate_space_trim);
boton.addEventListener("click", c, false)