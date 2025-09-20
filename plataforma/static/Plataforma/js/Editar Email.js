var address = document.getElementById("inputEmail")
var server = document.getElementById("inputServer")
var port = document.getElementById("inputPort")
var username = document.getElementById("inputUsername")
var password = document.getElementById("inputPassword")
var boton =  document.getElementById("boton");

const errorContainer = document.querySelector("#error-container")
        const createMessage = (message) => {
            return `
            <div style="position: absolute; right: 20px; top: 40px; display: flex; align-items: center; padding-right: 0rem; z-index: 2000"
            class="alert alert-danger alert-dismissible fade show" role="alert">
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
            if(address.value == ""){
                address.style = "border:solid 2px red;"
                mensaje += `Campo 'Dirección de correo' en blanco <br>`
                e.preventDefault()
            }else{ 
                address.style = "border:solid 2px green;"
            }
            if(!validador.test(address.value)){
                address.style = "border:solid 2px red;"
                mensaje += `Campo 'Dirección de correo' no es válido <br>`
                e.preventDefault()
            }else{ 
                address.style = "border:solid 2px green;"
            }
            if(server.value == ""){
                server.style = "border:solid 2px red;"
                mensaje += `Campo 'Smtp_Server' en blanco <br>`
                e.preventDefault()
            }else{
                server.style = "border:solid 2px green;"
            }
            if(port.value == "" || isNaN(port.value)|| port.value.length != 3 ){
                port.style = "border:solid 2px red;"
                mensaje += `Campo 'Smtp_Port' en blanco <br>`
                e.preventDefault()
            }else{
                port.style = "border:solid 2px green;"
            }
            if(username.value == ""){
                username.style = "border:solid 2px red;"
                mensaje += `Campo 'Usuario de correo' en blanco <br>`
                e.preventDefault()
            }else{ 
                username.style = "border:solid 2px green;"
            }
            if(!validador.test(username.value)){
                username.style = "border:solid 2px red;"
                mensaje += `Campo 'Usuario de correo' no es válido <br>`
                e.preventDefault()
            }else{ 
                username.style = "border:solid 2px green;"
            }
            if(password.value == ""){
                password.style = "border:solid 2px red;"
                mensaje += `Campo 'Contraseña de correo' en blanco <br>`
                e.preventDefault()
            }else{
                password.style = "border:solid 2px green;"
            }
            if (mensaje) {
                errorContainer.innerHTML += createMessage(mensaje)
            }
        
            }
        
    boton.addEventListener("click", c, false)