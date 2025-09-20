var username = document.getElementById("username");
var password = document.getElementById("password");
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
        const validate_space_trim = () => {
          username.value = username.value.trim();
          password.value = password.value.trim();
        }

const c = (e)=>{
        let mensaje = ""
        if(username.value == ""){
            username.style = "border:solid 2px red;"
            mensaje += `Campo 'Usuario' en blanco <br>`
            e.preventDefault()
        }else{ 
            username.style = "border:solid 2px green;"
        }
        if(password.value == ""){
            password.style = "border:solid 2px red;"
            mensaje += `Campo 'Contraseña' en blanco <br>`
            e.preventDefault()
        }else{
            password.style = "border:solid 2px green;"
        }
        if (mensaje) {
            errorContainer.innerHTML += createMessage(mensaje)
        }
    
        }
        
        username.addEventListener("input",validate_space_trim);
        password.addEventListener("input",validate_space_trim);
        boton.addEventListener("click", c, false)
           




