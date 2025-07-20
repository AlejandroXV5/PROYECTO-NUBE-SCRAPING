fetch("data/results.json")
  .then(res => res.json())
  .then(data => {
    const contenedor = document.getElementById("productos");
    contenedor.innerHTML = ""; // Limpia antes de cargar

    data.forEach(item => {
      const div = document.createElement("div");
      div.className = "producto";

      div.innerHTML = `
        <h3>${item.titulo}</h3>
        <p><span>${item.precio}</span></p>
        <p>Origen: ${item.origen}</p>
        <p>Fecha: ${item.fecha}</p>
      `;

      contenedor.appendChild(div);
    });
  })
  .catch(err => {
    console.error("Error al cargar productos desde results.json:", err);
  });
