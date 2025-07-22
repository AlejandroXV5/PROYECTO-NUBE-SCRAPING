document.addEventListener("DOMContentLoaded", function () {
  const calendarEl = document.getElementById("calendar");

  // Cargar los eventos desde el archivo JSON
  fetch("/data/events.json")
    .then(res => res.json())  // Convierte la respuesta en formato JSON
    .then(events => {
      console.log("✅ Eventos cargados:", events);  // Verifica los eventos cargados

      // Inicializa el calendario FullCalendar
      const calendar = new FullCalendar.Calendar(calendarEl, {
        initialView: "dayGridMonth",  // Vista inicial del calendario
        events: events,  // Los eventos cargados desde el archivo JSON
        eventClick: function (info) {
          // Al hacer clic en un evento, muestra detalles en un alert
          alert(
            `📌 ${info.event.title}\n🕒 ${info.event.start.toLocaleString()}\n📝 ${info.event.extendedProps.description}`
          );
        }
      });

      calendar.render();  // Renderiza el calendario
    })
    .catch(err => {
      console.error("❌ Error cargando events.json:", err);
      calendarEl.innerHTML = "<p style='color:red'>❌ No se pudo cargar el calendario</p>";  // Muestra mensaje de error si no se cargan los eventos
    });
});
