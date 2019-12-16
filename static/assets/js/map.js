/*global $*/
var markers = [];
var position=[];
var ipconfig = "140.121.199.231:27018"

function findLocation()
{
  clearMarkers();
  const address = document.getElementById("address").value;
  var icon = {
    url: "https://cdn.pixabay.com/photo/2016/07/21/00/38/pokemon-1531648_960_720.png", // url
    scaledSize: new google.maps.Size(40,60), // scaled size
    origin: new google.maps.Point(0,0), // origin
    anchor: new google.maps.Point(0, 0) // anchor
  };

  geocoder.geocode({
    'address': address
  }, function(results, status) {
    if (status == 'OK') {
      map.setCenter(results[0].geometry.location);
      markers.push( new google.maps.Marker({
        map: map,
        position: results[0].geometry.location,
        icon:icon,
        animation: google.maps.Animation.DROP
      }));
      const center_lat = results[0].geometry.location.lat();
      const center_lng = results[0].geometry.location.lng();

      const find = document.getElementById("findbutton");
      find.style.display='inline';
      find.addEventListener("click", add(center_lat, center_lng), false);

    } else {
      console.log(status);
    }
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

function add(center_lat, center_lng)
{
  fetch('http://'+ipconfig+'/api/map/location',
  {
    method: 'POST',
    body: JSON.stringify({'lat':center_lat,'lng':center_lng}), // data can be `string` or {object}!
    headers: new Headers({
      'Content-Type': 'application/json'
    })
  })
  .then(res => res.json())
  .then((data) => {
    console.log(position);
    for(let i =0;i<3;i++)
    {
      console.log(parseFloat(data.location[i][0]),parseFloat(data.location[i][1]))
      //var location = new google.map.LatLng(parseFloat(data.location[i][0]),parseFloat(data.location[i][1]));
      var location = {lat:parseFloat(data.location[i][0]),lng:parseFloat(data.location[i][1])};
      position.push(location);
      
    }
    console.log(position);
  })
  .catch(err => { throw err });
// var position = [
//   {label:'是在',lat:25.0336962,lng:121.5643673,},
//   {label:'哈摟',lat:25.0333698,lng:121.5641564},
//   {label:'你有事',lat:25.033899,lng:121.564329},
//   {label:'哈哈',lat:25.0338407,lng:121.5645269},
//   {label:'XD',lat:25.0336377,lng:121.5645727}
// ];
  setTimeout(function(){ 
    console.log("position.length: "+position.length);   
    for (var i = 0; i < position.length; i++) 
    {
      addMarker(i);
    } 
  }, 3000);

  
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

function initMap()
{
  //設定初始位置
  geocoder = new google.maps.Geocoder();
  map = new google.maps.Map(document.getElementById('map'), {
    zoom: 17
  });

  var address = '海洋大學';

  geocoder.geocode( { 'address': address}, function(results, status) {
    if (status == 'OK') {
      map.setCenter(results[0].geometry.location);
    } else {
      console.log(status);
    }
  });

  const submit = document.getElementById("submit");
  submit.addEventListener("click",findLocation,false)
}

window.addEventListener("load",initMap);