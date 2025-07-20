fetch("http://localhost:5000/api/archivos")
  .then(res => res.json())
  .then(data => {
    const contenedor = document.getElementById("archivos");
    contenedor.innerHTML = ""; // Limpia antes de cargar

    if (!data.length) {
      contenedor.innerHTML = "<p>No hay archivos descargados.</p>";
      return;
    }

    data.forEach(item => {
      const div = document.createElement("div");
      div.className = "archivo";

      div.innerHTML = `
        <p><strong>${item.nombre_archivo}</strong></p>
        <p>Hash: ${item.hash}</p>
        <p>Fecha: ${item.fecha_descarga}</p>
      `;

      contenedor.appendChild(div);
    });
  })
  .catch(err => {
    console.error("❌ Error cargando archivos:", err);
    document.getElementById("archivos").innerHTML =
      "<p style='color:red'>❌ Error cargando archivos</p>";
  });
