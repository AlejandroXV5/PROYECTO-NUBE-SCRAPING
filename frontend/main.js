fetch("http://localhost:5000/api/productos")
  .then(res => res.json())
  .then(data => {
    const contenedor = document.getElementById("productos");
    contenedor.innerHTML = ""; // Limpia antes de cargar

    if (!data.length) {
      contenedor.innerHTML = "<p>No hay productos disponibles.</p>";
      return;
    }

    data.forEach(item => {
      const div = document.createElement("div");
      div.className = "producto";

      div.innerHTML = `
        <h3>${item.titulo}</h3>
        <p><span>${item.precio}</span></p>
        <p>Origen: ${item.url}</p>
        <p>Fecha: ${item.fecha_registro}</p>
      `;

      contenedor.appendChild(div);
    });
  })
  .catch(err => {
    console.error("❌ Error al cargar los productos:", err);
    document.getElementById("productos").innerHTML =
      "<p style='color:red'>❌ Error cargando productos</p>";
  });
