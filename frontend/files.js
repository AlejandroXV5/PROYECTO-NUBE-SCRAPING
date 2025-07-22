// Llamada a la API o al archivo para obtener los archivos descargados
fetch("http://localhost:5000/api/archivos")
  .then(res => res.json())  // Asegúrate de que la respuesta sea JSON
  .then(data => {
    const contenedor = document.getElementById("files-container");
    contenedor.innerHTML = ""; // Limpiar antes de cargar nuevos archivos

    if (!data.length) {
      contenedor.innerHTML = "<p>No hay archivos descargados.</p>";
      return;
    }

    // Crear los elementos de archivos
    data.forEach(item => {
      const div = document.createElement("div");
      div.className = "archivo";

      div.innerHTML = `
        <div class="archivo-item">
          <p><strong>Nombre del archivo:</strong> ${item.nombre_archivo}</p>
          <p><strong>Hash:</strong> ${item.hash}</p>
          <p><strong>Fecha de descarga:</strong> ${new Date(item.fecha_descarga).toLocaleString()}</p>
        </div>
        <hr>
      `;

      contenedor.appendChild(div);
    });
  })
  .catch(err => {
    console.error("❌ Error cargando archivos:", err);
    document.getElementById("files-container").innerHTML =
      "<p style='color:red'>❌ Error cargando archivos</p>";
  });
