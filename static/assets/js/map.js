var markers = [];
var position=[];
var ipconfig = "140.121.199.231:27018"
var center_lat;
var center_lng;
var flag = 1;

function findLocation()
{
  clearMarkers();
  flag = 1;
  var address = document.getElementById("address").value;
  var icon={
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
      center_lat = results[0].geometry.location.lat();
      center_lng = results[0].geometry.location.lng();   
      $('#findbutton').fadeIn().css('display','inline-block');
      $('#findbutton').click({lat: center_lat, lng: center_lng}, findActivity);
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
function findActivity(event){
  if(flag == 1)
  {
    const p=position.length;
    for(var i =0;i< p;i++)
    {
      position.pop(i);
    }

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
      $('#findbutton').fadeOut().css('display','none');
     
      let eventLocation=[];
      let eventName=[];
      let eventM_B=[];
      let eventM_F=[];
      for(let i =0;i<5;i++)
      {
        eventLocation.push(data[i][0]['eventLocation']);
        eventName.push(data[i][0]['eventName']);
        eventM_B.push(data[i][0]['eventM_B']);
        eventM_F.push(data[i][0]['eventM_F']);
        position.push( data[i][0]['location']);
      }
      add_ActivityToMap(position, eventLocation, eventName, eventM_B, eventM_F);
    })
    .catch(err => { throw err });
  }
  flag = 0;
}
function add_ActivityToMap(position, eventLocation, eventName, eventM_B, eventM_F)
{
  for(let i=0;i<position.length;i++)
  {
    addMarker(i, eventLocation[i], eventName[i], eventM_B[i], eventM_F[i]);
  }
}
function addMarker(e, location, name, start, end){
  var infowindow = new google.maps.InfoWindow();
  const random =Math.floor(Math.random()*10)+1;
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
        animation: google.maps.Animation.DROP
      }));
    var infoContent = "活動名稱: "+name+"<br>"+"活動地點: "+location+"<br>"+"開始時間: "+start+"<br>"+"結束時間:"+ end;
    infowindow.setContent(infoContent);
    infowindow.open(map, markers[e+1]);
    markers[e+1].addListener('click',function(){
      infowindow.open(map, markers[e+1]);
    });
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

  var submit = document.getElementById("submit");
  submit.addEventListener("click",findLocation,false);
}
window.addEventListener("load",initMap);