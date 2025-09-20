document.addEventListener("DOMContentLoaded", function() {
    let elementos = document.querySelectorAll(".text");
    let elementos_aux = [];

    elementos.forEach((e) => {
        elementos_aux.push(e.innerText);
    });

    elementos.forEach((e) => {
        e.innerHTML = `${e.innerText} <a style="text-decoration: none;" href="{% url 'VisualizarNoticias' noticia.id %}"> ...leer más</a>`;
    });

});
