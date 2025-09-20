var password1 = document.getElementById("password1");
var password2 = document.getElementById("password2");
var boton =  document.getElementById("boton");

const errorContainer = document.querySelector("#error-container")
        const createMessage = (message) => {
            return `
            <div style=" position: absolute; right: 20px; top: 40px; display: flex; align-items: center; padding-right: 0rem;  z-index: 2000"
            class="alert alert-danger alert-dismissible fade show" role="alert">
            ${message}
            <button style="font-size: 10px; border-bottom: none; position: relative; box-shadow: none;" type="button"
                class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
            </button>
            </div>
            `
        }
        const validate_space_trim = () => {
          password1.value = password1.value.trim();
          password2.value = password2.value.trim();
        }

const c = (e)=>{
    let mensaje = ""
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
        password1.style = "border:solid 1px red;"
        password2.style = "border:solid 1px red;"
        mensaje += `Campo 'Contraseña' y 'Repetir contraseña' deben coincidir <br>`
        e.preventDefault()
    }
       
    if (mensaje) {
        errorContainer.innerHTML += createMessage(mensaje)
    }
    }
        
        password1.addEventListener("input",validate_space_trim);
        password2.addEventListener("input",validate_space_trim);
        boton.addEventListener("click", c, false)
           




