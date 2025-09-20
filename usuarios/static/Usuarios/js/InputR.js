var username = document.getElementById("username");
var password1 = document.getElementById("password1");
var password2 = document.getElementById("password2");
var email = document.getElementById("email");
var boton =  document.getElementById("boton");

const errorContainer = document.querySelector("#error-container")
        const createMessage = (message) => {
            return `
            <div style=" position: absolute; right: 20px; top:10px; display: flex; align-items: center; padding-right: 0rem;  z-index: 2000"
            class="alert alert-danger alert-dismissible fade show" role="alert">
            ${message}
                <button style="font-size: 10px; border-bottom: none; position: relative; box-shadow: none;" type="button"
                    class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
                </button>
            </div>
            `
        }
        const validate_space_trim = () => {
            username.value = username.value.trim();
            email.value = email.value.trim();
            password1.value = password1.value.trim();
            password2.value = password2.value.trim();
          }

const c = (e)=>{
        let validador = /^\w+([.-_+]?\w+)*@\w+([.-]?\w+)*(\.\w{2,10})+$/
        let mensaje = ""
        if(username.value == ""){
            username.style = "border:solid 2px red;"
            mensaje += `Campo 'Usuario' en blanco <br>`
            e.preventDefault()
        }else{ 
            username.style = "border:solid 2px green;"
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
        if(password1.value == ""){
            password1.style = "border:solid 2px red;"
            mensaje += `Campo 'Contraseña' en blanco <br>`
            e.preventDefault()
        }
        else{ 
            password1.style = "border:solid 2px green;"
        }
        if(password2.value == ""){
            password2.style = "border:solid 2px red;"
            mensaje += `Campo 'Repetir contraseña' en blanco <br>`
            e.preventDefault()
        }
        else{ 
            password2.style = "border:solid 2px green;"
        }
        if(password1.value != password2.value){
            password1.style = "border:solid 2px red;"
            password2.style = "border:solid 2px red;"
            mensaje += `Campo 'Contraseña' y 'Repetir contraseña' deben coincidir <br>`
            e.preventDefault()
        }
           
        if (mensaje) {
            errorContainer.innerHTML += createMessage(mensaje)
        }
        }
        username.addEventListener("input",validate_space_trim);
        email.addEventListener("input",validate_space_trim);
        password1.addEventListener("input",validate_space_trim);
        password2.addEventListener("input",validate_space_trim);
        boton.addEventListener("click", c, false)
           




