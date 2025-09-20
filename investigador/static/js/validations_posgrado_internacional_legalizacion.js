var nombre = document.getElementById("name");
var apellidos = document.getElementById("lastName");
var organismo = document.getElementById("organismo");
var motivo = document.getElementById("motivo");
var funcionario = document.getElementById("funcionario");
var ci = document.getElementById("ci");
var email = document.getElementById("email");
var telefono = document.getElementById("tel");
var year = document.getElementById("year");
var folio = document.getElementById("folio");
var tomo = document.getElementById("tomo");
var numero = document.getElementById("numero");
var archivo = document.getElementById("arhivo");

var tipo_estudio = document.getElementById("tipoestudio");
var uso = document.getElementById("uso");


var nombre_programa = document.getElementById("nombre_programa");
var organismo_op = document.getElementById("organismo_op");
var intereses = document.getElementById("intereses");
var programa_academico = document.getElementById("programa_academico");

var boton =  document.getElementById("boton");

document.addEventListener("DOMContentLoaded", function() {
    // Función para manejar el cambio en los radio buttons de Intereses
    function handleInterestChange() {
      var selectedInterest = document.querySelector(`input[id="id_intereses"]:checked`).value;
      var organismoOp = document.getElementById('prueba');
      var organismo = document.getElementById('id_organismo');
      var motivo = document.getElementById('id_motivo');
      console.log("selectedInterest")
      if (selectedInterest === 'Particular') {
        organismoOp.style = 'display:block;';
        organismo.style = 'display:none;';
        motivo.style = 'display:none;';
      } else if (selectedInterest === 'Estatal') {
        organismoOp.style = 'display:none;';
        organismo.style = 'display:block;';
        motivo.style = 'display:block;';
      }
    }
    
    document.querySelector("#id_intereses").checked = true

    handleInterestChange()
    
    // Actualiza los campos al cambiar la selección de Intereses
    document.querySelectorAll("#id_intereses").forEach(input => {
      input.addEventListener('change', handleInterestChange);
    });
    



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
            function cleanInput(inputField) {
                var regex = /^[A-Za-z\s]*$/; // Expresión regular para permitir solo letras y espacios
                var inputValue = inputField.value;
                var cleanedValue = inputValue.replace(/[^A-Za-z\s]/g, ''); // Reemplaza todos los caracteres no deseados
                inputField.value = cleanedValue; // Actualiza el valor del campo con el contenido limpio
                return cleanedValue.length > 0; // Retorna verdadero si el valor limpio tiene longitud mayor a 0
            }
            
            // Modificar el controlador de eventos para los campos específicos
            ['name', 'lastName', 'organismo', 'funcionario', 'nombre_programa'].forEach((id) => {
                var field = document.getElementById(id);
                if (field) {
                    field.addEventListener('input', function() {
                        this.value = capitalizeFirstLetter(cleanInput(this));
                    });
                }
            });
    
    function capitalizeFirstLetter(string) {
        return string.charAt(0).toUpperCase() + string.slice(1);
    }
    
    ['name', 'lastName', 'organismo', 'motivo', 'funcionario', 'nombre_programa'].forEach((id) => {
                var field = document.getElementById(id);
                if (field) {
                    field.addEventListener('input', function() {
                        this.value = capitalizeFirstLetter(this.value);
                    });
                }
            });
    
            
            function cleanNumericInput(inputField) {
                var regex = /^\d*$/; // Expresión regular para permitir solo dígitos
                var inputValue = inputField.value;
                var cleanedValue = inputValue.replace(/\D/g, ''); // Reemplaza todos los caracteres no numéricos
                inputField.value = cleanedValue; // Actualiza el valor del campo con el contenido limpio
            }
            
            // Aplicar la función a los campos específicos
            ['tomo', 'folio', 'numero', 'ci', 'tel'].forEach((id) => {
                var field = document.getElementById(id);
                if (field) {
                    field.addEventListener('input', function() {
                        cleanNumericInput(this); // Limpia el campo de entrada
                    });
                }
            });
        const c = (e)=>{
            let mensaje = ""
            let validador = /^\w+([.-_+]?\w+)*@\w+([.-]?\w+)*(\.\w{2,10})+$/
            
            if(nombre.value == ""){
                nombre.style = "border:solid 2px #212d57;"
                mensaje += `Campo 'Nombre' en blanco <br>`
                e.preventDefault()
            }else{ 
                nombre.style = "border:solid 2px white;"
            }
    
            if(apellidos.value == ""){
                apellidos.style = "border:solid 2px #212d57;"
                mensaje += `Campo 'Apellidos' en blanco <br>`
                e.preventDefault()
            }else{ 
                apellidos.style = "border:solid 2px white;"
            }
            if(ci.value == "" || isNaN(ci.value) || ci.value.length != 11 ){
                ci.style = "border:solid 2px #212d57;"
                mensaje += `Campo 'Carnet' es incorrecto debe tener 11 dígitos <br>`
                e.preventDefault()
            }
            else{
                ci.style = "border:solid 2px white;"
            }
      
            if(email.value == ""){
                email.style = "border:solid 2px #212d57;"
                mensaje += `Campo 'Email' en blanco <br>`
                e.preventDefault()
            }
            else{ 
                email.style = "border:solid 2px white;"
            }
            if (!validador.test(email.value)) {
                email.style = "border:solid 2px #212d57;"
                mensaje += `Campo 'Email' no es válido <br>`
                e.preventDefault()  
            }
            else{ 
                email.style = "border:solid 2px white;"
            }
            if(telefono.value == "" ||isNaN(telefono.value) || telefono.value.length != 8 ){
                telefono.style = "border:solid 2px #212d57;"
                mensaje += `Campo 'Teléfono' es incorrecto debe tener 8 dígitos <br>`
                e.preventDefault()
            }
            else{
                telefono.style = "border:solid 2px white;"
            }
    
            if(tipo_estudio.value == ""){
                tipo_estudio.style = "border:solid 2px #212d57;"
                mensaje += `Campo 'Tipo Estudio' en blanco <br>`
                e.preventDefault()
            }else{ 
                tipo_estudio.style = "border:solid 2px white;"
            }
            if(uso.value == ""){
                uso.style = "border:solid 2px #212d57;"
                mensaje += `Campo 'Uso' en blanco <br>`
                e.preventDefault()
            }else{ 
                uso.style = "border:solid 2px white;"
            }
            if(archivo.files.length === 0){
                archivo.style = "border:solid 2px #212d57;";
                mensaje += `Campo 'Fotocopia del Título(Solo en PDF)' en blanco <br>`;
                e.preventDefault();
            }else{ 
                archivo.style = "border:solid 2px white;";
            }
            var selectedInterest = document.querySelector(`input[id="id_intereses"]:checked`).value;
            // Verifica si el interés seleccionado es 'Estatal'
            if (selectedInterest === 'Estatal') {
                if (motivo.value == "") {
                    motivo.style = "border:solid 2px #212d57;";
                    mensaje += `Campo 'Motivo' en blanco <br>`;
                    e.preventDefault();
                }
                if (organismo.value == "") {
                    organismo.style = "border:solid 2px #212d57;";
                    mensaje += `Campo 'Organismo' en blanco <br>`;
                    e.preventDefault();
                }
            } else {
                motivo.style = "border:solid 2px white;";
            }
            
            if(funcionario.value == ""){
                funcionario.style = "border:solid 2px #212d57;"
                mensaje += `Campo 'Funcionario' en blanco <br>`
                e.preventDefault()
            }else{ 
                funcionario.style = "border:solid 2px white;"
            }
    
            if(year.value == ""){
                year.style = "border:solid 2px #212d57;"
                mensaje += `Campo 'Año' en blanco <br>`
                e.preventDefault()
            }else{ 
                year.style = "border:solid 2px white;"
            }
            if(nombre_programa.value == ""){
                nombre_programa.style = "border:solid 2px #212d57;"
                mensaje += `Campo 'Nombre del Programa' en blanco <br>`
                e.preventDefault()
            }else{ 
                nombre_programa.style = "border:solid 2px white;"
            }

            if(programa_academico.value == ""){
                programa_academico.style = "border:solid 2px #212d57;"
                mensaje += `Campo 'Programa Académico' en blanco <br>`
                e.preventDefault()
            }else{ 
                programa_academico.style = "border:solid 2px white;"
            }

            if(tomo.value == "" || isNaN(tomo.value) || tomo.value.length != 4 ){
                tomo.style = "border:solid 2px #212d57;"
                mensaje += `Campo 'Tomo' es incorrecto debe tener 4 dígitos <br>`
                e.preventDefault()
            }
            else{
                tomo.style = "border:solid 2px white;"
            }

            if(folio.value == "" || isNaN(folio.value) || folio.value.length != 4 ){
                folio.style = "border:solid 2px #212d57;"
                mensaje += `Campo 'Folio' es incorrecto debe tener 4 dígitos <br>`
                e.preventDefault()
            }
            else{
                folio.style = "border:solid 2px white;"
            }
            if(numero.value == "" || isNaN(numero.value) || numero.value.length != 4 ){
                numero.style = "border:solid 2px #212d57;"
                mensaje += `Campo 'Número' es incorrecto debe tener 4 dígitos <br>`
                e.preventDefault()
            }
            else{
                numero.style = "border:solid 2px white;"
            }

            if (mensaje) {
                errorContainer.innerHTML += createMessage(mensaje)
            }

            }
            
            boton.addEventListener("click", c, false)
               
        });
