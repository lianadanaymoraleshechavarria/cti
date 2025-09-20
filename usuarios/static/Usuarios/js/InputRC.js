
var email = document.getElementById("email");
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
          email.value = email.value.trim();
        }

const c = (e)=>{
        let validador = /^\w+([.-_+]?\w+)*@\w+([.-]?\w+)*(\.\w{2,10})+$/
        let mensaje = ""
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
        if (mensaje) {
          errorContainer.innerHTML += createMessage(mensaje)
        }
        }
        
        email.addEventListener("input",validate_space_trim);
        boton.addEventListener("click", c, false)
           




