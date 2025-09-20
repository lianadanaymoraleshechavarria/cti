// Asegurar que el logo sea clickeable
document.addEventListener("DOMContentLoaded", () => {
    const logoLinks = document.querySelectorAll(".navbar-brand")
  
    logoLinks.forEach((link) => {
      link.addEventListener("click", function (e) {
        // Prevenir comportamiento predeterminado
        e.preventDefault()
  
        // Obtener la URL del href
        const href = this.getAttribute("href")
  
        // Redirigir a la URL
        if (href && href !== "#") {
          window.location.href = href
        }
  
        // Registrar en consola para depuración
        console.log("Logo clickeado, redirigiendo a:", href)
      })
    })
  })
  