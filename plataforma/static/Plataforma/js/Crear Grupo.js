var grupo = document.getElementById("grupo")
var permisos = document.getElementsByClassName("form-check-input")
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


        const validadorMultiple = () => {
            permisos = document.getElementsByClassName("form-check-input")
            for (let index = 0; index < Array.from(permisos).length; index++) {
                const element = permisos[index];
                if (element.checked){
                    return true
                }
            }
            return false
        }
            

        const c = (e)=>{
            let mensaje = ""
            if(grupo.value == ""){
                grupo.style = "border:solid 2px red;"
                mensaje += `Campo 'Nombre' en blanco <br>`
                e.preventDefault()
            }else{ 
                grupo.style = "border:solid 2px green;"
            }

                if(!validadorMultiple()){
                    document.getElementById("contenedor-permisos").style = "border:solid 2px red;border-radius: 10px;padding-left: 10px;"
                    mensaje += `No ha seleccionado ningun permiso <br>`
                    e.preventDefault()
                }else{
                    document.getElementById("contenedor-permisos").style = "border:solid 2px green;border-radius: 10px;padding-left: 10px;"
                }
            
            
            if (mensaje) {
                errorContainer.innerHTML += createMessage(mensaje)
            }
        
            }
        
    boton.addEventListener("click", c, false)