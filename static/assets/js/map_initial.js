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
      find.addEventListener("click",function(){
        add(center_lat, center_lng);
      }, false);

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
    //console.log(position);
    for(let i =0;i<5;i++)
    {
      console.log(data[i][0]['eventLocation']);
      console.log(data[i][0]['eventName']);
      console.log(data[i][0]['eventM_B']);
      console.log(data[i][0]['eventM_F']);
      console.log(data[i][0]['location']);
      
      var location = data[i][0]['location'];
      position.push(location);
      
    }
    console.log(position);
  })
  .catch(err => { throw err });

  setTimeout(function(){ 
    console.log("position.length: "+position.length);   
    for (var i = 0; i < position.length; i++) 
    {
      addMarker(i);
    } 
  }, 3000);

  
}

function addMarker(e) {
  const random =Math.floor(Math.random()*5)+1;
  var icon = {
    url: '/static/gps_images/'+random+'.png', // url
    scaledSize: new google.maps.Size(80,80), // scaled size
    origin: new google.maps.Point(0,0), // origin
    anchor: new google.maps.Point(0, 0) // anchor
  };


  setTimeout(function() {
    markers.push(new google.maps.Marker({
        position: {
          lat: position[e].lat,
          lng: position[e].lng
        },
        map: map,
        icon:icon,
        //label: position[e].label,
        animation: google.maps.Animation.DROP
      }));
      // var infowindow = new google.maps.InfoWindow({
      //   content: '哈摟你好',
      //   position: {
      //     lat: position[e].lat,
      //     lng: position[e].lng
      //   },
      //   maxWidth:200,
      //   pixelOffset: new google.maps.Size(100, -20) 
      // });
      // infowindow.open(map,markers);
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
  submit.addEventListener("click",findLocation,false);
}

window.addEventListener("load",initMap);