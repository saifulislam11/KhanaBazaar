//loading the DOM
document.addEventListener('DOMContentLoaded',function(){
    ///---------------location--------------///
    const latlng_buet = {'lat': 23.7265768, 'lng': 90.3926623};
    var loction = document.getElementById('location');

    function splitter(ss) {
        var arr = ss.split(',');
        var a = +arr[0];
        var b = +arr[1];
        return {'lat': a, 'lng': b};
    }


    function parser_haversine(ss) {
        return {
            latitude: ss[0],
            longitude: ss[1]
        }
    }
    var map = L.map('map',
        {
            center: latlng_buet,
            enableHighAccuracy: true
        });
    var cur_loc_marker = L.marker(splitter(loction.value)).addTo(map);
    //loction.value = ""
    cur_loc_marker.bindPopup("Your current Location").openPopup();
    L.tileLayer('https://api.mapbox.com/styles/v1/{id}/tiles/{z}/{x}/{y}?access_token={accessToken}', {
        attribution: 'Map data &copy; <a href="https://www.openstreetmap.org/">OpenStreetMap</a> contributors, <a href="https://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, Imagery © <a href="https://www.mapbox.com/">Mapbox</a>',
        maxZoom: 18,
        id: 'mapbox/streets-v11',
        tileSize: 512,
        zoomOffset: -1,
        accessToken: 'pk.eyJ1Ijoidm9kcm8iLCJhIjoiY2tpMzh1ZnZ5MGRwazJyc3k1d2c2dmcxOSJ9.EeruKONlBRsXX8I77GbuPw'
    }).addTo(map);


    map.locate({
        enableHighAccuracy: true,
        watch: true,
        setView: true,
        maxZoom: 18
    });
    var restaurant_loc_marker = L.marker(splitter(" 23.7265768,90.3926623")).addTo(map);

    function onLocationFound(e) {
        /*
        var dist = haversine(cur_loc_marker.getLatLng(), e.latlng, {
            format: '{lat,lng}',
            'unit': 'meter'
        });
        if (dist > 500) {
            loction.value = e.latlng.lat + ',' + e.latlng.lng;
            console.log(dist);
            alert('Your Location is being Updated');
            update_location_form.submit()
        }*/

        cur_loc_marker.setLatLng(e.latlng);
        console.log(e.latlng);
        map.flyTo(e.latlng);
        console.log('map created with current location');
        
        restaurant_loc_marker.setLatLng({lat: 23.7265768, lng: 90.3926623});
    }
    

    map.on('locationfound', onLocationFound);
    /*L.Routing.control({
      waypoints: [
          cur_loc_marker.getLatLng(),
          restaurant_loc_marker.getLatLng()
      ]
    }).addTo(map);
    console.log('kajj kore nah vai ')*/

    ///---------------end of location--------------//
    const loginPopup = document.querySelector(".login-popup");
    const order_id = document.querySelector("#order_id");
    
    const close = document.querySelector(".close");
    window.addEventListener("load",function(){
        console.log(order_id);
    
        showPopup();
        // setTimeout(function(){
        //   loginPopup.classList.add("show");
        // },5000)
    
        })
    
    function showPopup(){
            const timeLimit = 1 // seconds;
            let i=0;
            const timer = setInterval(function(){
            i++;
            if(i == timeLimit){
            clearInterval(timer);
            loginPopup.classList.add("show");
            } 
            console.log(i)
            },1000);
    }
    
})