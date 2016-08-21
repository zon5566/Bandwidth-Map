var map, heatmap, Line;
var VLine = [], HLine = [];

var XORIGIN = 121.45278, YORIGIN = 24.95608;
var XEND = 121.65833, YEND = 25.21218;

var XMETER_SIZE = 0.001966/2, YMETER_SIZE = 0.001802/2;
var XBLOCK_SIZE = XMETER_SIZE, YBLOCK_SIZE = YMETER_SIZE; // 100m*100m

var LineCoordinate, Line;
var blocksize;

function initMap() {
  map = new google.maps.Map(document.getElementById("map"), {
    zoom: 15,
    zoomControl: true,
    scrollwheel: true,
    scaleControl: true,
    mapTypeControl: false,
    navigationControl: true,
    streetViewControl: false,
    disableDoubleClickZoom: true,
    disableDefaultUI: true,
    center: {lat:25.033, lng:121.56},
  });

  document.getElementById("zoom").innerHTML = map.getZoom();
   document.getElementById("block").innerHTML = 400;
  // --Block Lines-----------
  for(var lon_ = XORIGIN; lon_<=XEND; lon_+=XBLOCK_SIZE) {
    LineCoordinate = [
      {lat: YORIGIN, lng: lon_},
      {lat: YEND, lng: lon_},
    ];
    Line = new google.maps.Polyline({
      path: LineCoordinate,
      geodesic: true,
      strokeColor: 'gray',
      strokeOpacity: 0.5,
      stokeWeight: 1,
    });
    VLine.push(Line);
  }

  for(var lat_ = YORIGIN; lat_<=YEND; lat_+=YBLOCK_SIZE) {
    LineCoordinate = [
      {lat: lat_, lng: XORIGIN},
      {lat: lat_, lng: XEND},
    ];
    Line = new google.maps.Polyline({
      path: LineCoordinate,
      geodesic: true,
      strokeColor: 'gray',
      strokeOpacity: 0.5,
      stokeWeight: 1,
    });
    HLine.push(Line);
  }
  draw_block(map.getZoom());

  google.maps.event.addListener(map, "click", function(event){
    var Clat = event.latLng.lat();
    var Clng = event.latLng.lng();
    if(in_area(Clng, Clat)){
      var center = new google.maps.LatLng(get_center(Clng, Clat)[1], get_center(Clng, Clat)[0]);
      map.panTo(center);

      /*====================django ajax ======*/
      jQuery(document).ajaxSend(function(event, xhr, settings) {
          function getCookie(name) {
              var cookieValue = null;
              if (document.cookie && document.cookie != '') {
                  var cookies = document.cookie.split(';');
                  for (var i = 0; i < cookies.length; i++) {
                      var cookie = jQuery.trim(cookies[i]);
                      // Does this cookie string begin with the name we want?
                      if (cookie.substring(0, name.length + 1) == (name + '=')) {
                          cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                          break;
                      }
                  }
              }
              return cookieValue;
          }
          function sameOrigin(url) {
              // url could be relative or scheme relative or absolute
              var host = document.location.host; // host + port
              var protocol = document.location.protocol;
              var sr_origin = '//' + host;
              var origin = protocol + sr_origin;
              // Allow absolute or scheme relative URLs to same origin
              return (url == origin || url.slice(0, origin.length + 1) == origin + '/') ||
                  (url == sr_origin || url.slice(0, sr_origin.length + 1) == sr_origin + '/') ||
                  // or any other URL that isn't scheme relative or absolute i.e relative.
                  !(/^(\/\/|http:|https:).*/.test(url));
          }
          function safeMethod(method) {
              return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
          }

          if (!safeMethod(settings.type) && sameOrigin(settings.url)) {
              xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
          }
      });
      /*===============================django ajax end===*/
      
      blocksize = get_current_blocksize(map.getZoom(), get_center(Clng, Clat));
      $.ajax({
        method: 'POST',
        url: '',
        dataType: 'text',
        data: {
          xcenter: get_center(Clng, Clat)[0],
          ycenter: get_center(Clng, Clat)[1],
          xblocksize: blocksize[0],
          yblocksize: blocksize[1],
          carrier_select: $('#carrier_select').val(),
          hour_select: $('#hour_select').val(),
          minute_select: $('#minute_select').val(),
        },
        success: function(data) {
          console.log('pass argument success');
        },
        error: function(xhr, status, error) {
          console.log('oops something wrong:'+error);
        },
      });
    }
  });

  google.maps.event.addListener(map, 'zoom_changed', function(){
    var current_zlevel = map.getZoom();
    document.getElementById('zoom').innerHTML = current_zlevel;
    
    var degree;
    if(current_zlevel > 18) degree = 1;
    else if(current_zlevel <= 13) degree = Math.pow(2,16-current_zlevel);
    else degree = 19 - current_zlevel;
    document.getElementById('block').innerHTML = 100*degree;
    
    if(current_zlevel>18) return;
    else{
      remove_block();
      draw_block(current_zlevel);
    }
  });
}

function in_area(lng, lat){
  if(lng>XORIGIN && lng<XEND && lat>YORIGIN && lat<YEND)
    return true;
  else return false;
}

function draw_block(level){
  var degree;
  if(level>18) degree = 1;
  else if(level<=13) degree = Math.pow(2,16-level);
  else degree = 19-level;

  XBLOCK_SIZE = XMETER_SIZE*degree;
  YBLOCK_SIZE = YMETER_SIZE*degree;

  for(var i=0; i<VLine.length; i+=degree){
    VLine[i].setMap(map);
  }

  for(var j=0; j<HLine.length; j+=degree){
    HLine[j].setMap(map);
  }
}

function remove_block(){
  for(var i=0; i<VLine.length; i++){
    VLine[i].setMap(null);
  }

  for(var j=0; j<HLine.length; j++){
    HLine[j].setMap(null);
  }  
}

function get_center(lng, lat){
  var xblock = Math.floor((lng-XORIGIN)/XBLOCK_SIZE)+1;
  var yblock = Math.floor((lat-YORIGIN)/YBLOCK_SIZE)+1;
  var center_lng = XORIGIN + XBLOCK_SIZE*(xblock-0.5);
  var center_lat = YORIGIN + YBLOCK_SIZE*(yblock-0.5);
  return [center_lng, center_lat];
}

function get_current_blocksize(level, center){
  var current_lng = center[0], curent_lat = center[1];
  var Xsize, Ysize;
  if(level>18) {
    Xsize = XBLOCK_SIZE;
    Ysize = YBLOCK_SIZE;
  }
  else if(level<=13) {
    Xsize = XBLOCK_SIZE*Math.pow(2,16-level);
    Ysize = YBLOCK_SIZE*Math.pow(2,16-level);
  }
  else {
    Xsize = XBLOCK_SIZE*(19-level);
    Ysize = YBLOCK_SIZE*(19-level);    
  }
  return [Xsize, Ysize];
}