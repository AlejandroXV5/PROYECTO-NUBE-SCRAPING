fetch("http://localhost:5000/api/productos")
  .then(res => res.json())
  .then(data => {
    const contenedor = document.getElementById("productos");
    contenedor.innerHTML = ""; // Limpiar antes de cargar nuevos datos

    if (!data.length) {
      contenedor.innerHTML = "<p>No hay productos disponibles.</p>";
      return;
    }

    // Crear los elementos de los productos
    data.forEach(item => {
      const div = document.createElement("div");
      div.className = "producto";

      div.innerHTML = `
        <div class="producto-item">
          <h3><strong>${item.titulo}</strong></h3>
          <p><strong>Precio:</strong> <span class="precio">${item.precio}</span></p>
          <p><strong>Origen:</strong> <a href="${item.url}" target="_blank">${item.url}</a></p>
          <p><strong>Fecha de Registro:</strong> ${new Date(item.fecha_registro).toLocaleDateString()}</p>
        </div>
        <hr>
      `;

      contenedor.appendChild(div);
    });
  })
  .catch(err => {
    console.error("❌ Error al cargar los productos:", err);
    document.getElementById("productos").innerHTML =
      "<p style='color:red'>❌ Error cargando productos</p>";
  });
