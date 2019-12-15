// Initialize and add the map
// $.getJSON( "mapStyle.json", function( json ) {
//     console.log( "JSON Data received, name is " + json.name);
// });
var map;
var geolocation = 'https://www.googleapis.com/geolocation/v1/geolocate?key=AIzaSyB1CriIa5SUuz2nx9H0N92hKSoEC4himHE';
var markers = [];
var position = [
  {label:'是在',lat:25.0336962,lng:121.5643673,},
  {label:'哈摟',lat:25.0333698,lng:121.5641564},
  {label:'你有事',lat:25.033899,lng:121.564329},
  {label:'哈哈',lat:25.0338407,lng:121.5645269},
  {label:'XD',lat:25.0336377,lng:121.5645727}
];
function drawDashedCurve(P1, P2, map) {
    var lineLength = google.maps.geometry.spherical.computeDistanceBetween(P1, P2);
    var lineHeading = google.maps.geometry.spherical.computeHeading(P1, P2);
    if (lineHeading < 0) {
      var lineHeading1 = lineHeading + 45;
      var lineHeading2 = lineHeading + 135;
    } else {
      var lineHeading1 = lineHeading + -45;
      var lineHeading2 = lineHeading + -135;
    }
    var pA = google.maps.geometry.spherical.computeOffset(P1, lineLength / 2.2, lineHeading1);
    var pB = google.maps.geometry.spherical.computeOffset(P2, lineLength / 2.2, lineHeading2);
  
    var curvedLine = new GmapsCubicBezier(P1, pA, pB, P2, 0.01, map);
  }
var style = JSON.parse(style);
console.log(style);
function initMap() {
  navigator.geolocation.watchPosition((position) => {
      console.log(position.coords);
      lat = position.coords.latitude;
      lng = position.coords.longitude;
      // 初始化地圖
      map = new google.maps.Map(document.getElementById('map'), {
          zoom: 18,
          center: { lat: lat, lng: lng }
      });
      marker = new google.maps.Marker({
          position: { lat: lat, lng: lng },
          map: map
      });
  });
}
function clearMarkers() {
  for (var i = 0; i < markers.length; i++) {
    if(markers[i]){
      markers[i].setMap(null);
    }
  }
  markers = [];
}
function add()
{
    clearMarkers();
    for (var i = 0; i < position.length; i++) 
    {
        addMarker(i);
    }
}
function addMarker(e) {
  setTimeout(function() {
    markers.push(new google.maps.Marker({
        position: {
          lat: position[e].lat,
          lng: position[e].lng
        },
        map: map,
        //label: position[e].label,
        animation: google.maps.Animation.DROP
      }));
  }, e * 150);
}
window.addEventListener("load",initMap);