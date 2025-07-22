fetch("data/results.json")
  .then(res => res.json())
  .then(data => {
    const contenedor = document.getElementById("productos");
    contenedor.innerHTML = ""; // Limpiar antes de cargar

    if (!data.length) {
      contenedor.innerHTML = "<p>No se han encontrado productos.</p>";
      return;
    }

    // Crear los elementos de productos
    data.forEach(item => {
      const div = document.createElement("div");
      div.className = "producto";

      div.innerHTML = `
        <div class="producto-item">
          <h3><strong>${item.titulo}</strong></h3>
          <p><span class="precio">${item.precio}</span></p>
          <p><strong>Origen:</strong> ${item.origen}</p>
          <p><strong>Fecha de publicación:</strong> ${item.fecha}</p>
        </div>
        <hr>
      `;

      contenedor.appendChild(div);
    });
  })
  .catch(err => {
    console.error("❌ Error cargando productos:", err);
    document.getElementById("productos").innerHTML =
      "<p style='color:red'>❌ Error cargando productos</p>";
  });
