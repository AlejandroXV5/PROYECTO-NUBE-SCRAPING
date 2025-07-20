document.addEventListener("DOMContentLoaded", function () {
  const calendarEl = document.getElementById("calendar");

  fetch("./data/events.json")
    .then(res => res.json())
    .then(events => {
      console.log("✅ Eventos cargados:", events);

      const calendar = new FullCalendar.Calendar(calendarEl, {
        initialView: "dayGridMonth",
        events: events,
        eventClick: function (info) {
          alert(
            `📌 ${info.event.title}\n🕒 ${info.event.start.toLocaleString()}\n📝 ${info.event.extendedProps.description}`
          );
        }
      });

      calendar.render();
    })
    .catch(err => {
      console.error("❌ Error cargando events.json:", err);
      calendarEl.innerHTML = "<p style='color:red'>❌ No se pudo cargar el calendario</p>";
    });
});
