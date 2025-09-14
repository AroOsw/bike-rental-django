function decodePolyline(encoded) {
   if (typeof encoded !== 'string') {
    return [];
  }

  let points = [];
  let lat = 0;
  let lng = 0;
  let index = 0;

  while (index < encoded.length) {
    let byte = null;
    let shift = 0;
    let result = 0;

    do {
      byte = encoded.charCodeAt(index++) - 63;
      result |= (byte & 0x1f) << shift;
      shift += 5;
    } while (byte >= 0x20);

    let dlat = ((result & 1) != 0 ? ~(result >> 1) : (result >> 1));
    lat += dlat;

    shift = 0;
    result = 0;

    do {
      byte = encoded.charCodeAt(index++) - 63;
      result |= (byte & 0x1f) << shift;
      shift += 5;
    } while (byte >= 0x20);

    let dlng = ((result & 1) != 0 ? ~(result >> 1) : (result >> 1));
    lng += dlng;

    points.push([lat / 100000, lng / 100000]);
  }

  return points;
}

document.addEventListener('DOMContentLoaded', () => {
    const activities = document.querySelectorAll('.activity');
    activities.forEach(activity => {
        const mapId = activity.querySelector('div[id^="map-"]').id;
        const polylineId = activity.querySelector('input[id^="polyline-"]').id;
        const encoded = document.getElementById(polylineId).value;

        if (!encoded) {
            console.warn(`No polyline for map ${mapId}`);
            return;
        }

        const map = L.map(mapId).setView([52.2297, 21.0122], 10);
        L.tileLayer('https://tile.openstreetmap.de/{z}/{x}/{y}.png', {
            attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
        }).addTo(map);

        const coords = decodePolyline(encoded);
        if (coords.length > 0) {
            L.polyline(coords, { color: '#2575FCFF' }).addTo(map);

            const startPoint = coords[0];
            const endPoint = coords[coords.length - 1];

            L.marker(startPoint).addTo(map)
                .bindPopup("<b>Start</b>")
                .openPopup();

            L.marker(endPoint).addTo(map)
                .bindPopup("<b>Finish</b>");

            map.fitBounds(L.latLngBounds(coords));
        } else {
            console.warn(`Empty coordinates for map ${mapId}`);
        }
    });
});