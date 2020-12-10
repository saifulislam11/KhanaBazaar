//loading the DOM
document.addEventListener('DOMContentLoaded',function(){

    const loginPopup = document.querySelector(".login-popup");
    const status = document.querySelector(".status");
    const redirect = document.querySelector(".redirect");
    const foodman_status = document.querySelector(".foodman-status");
    const foodman_phone = document.querySelector("#foodman_phn");
    const foodman_contact = document.querySelector(".foodman-contact");
    const foodman_image = document.querySelector(".foodman-image");
    const location_map = document.querySelector(".location-map");
    const location_summary = document.querySelector(".location-summary");

    const foodman_name = document.querySelector("#foodman_name");
    const place_name = document.querySelector(".place-name");
    const order_id = document.querySelector("#order_id");
    const verify = document.querySelector("#verify");
    const close = document.querySelector(".close");
    let x =0;
    //---------------location vars--------------//
    const latlng_buet = {'lat': 23.7265768, 'lng': 90.3926623};
    var loction = document.getElementById('location');
    var foodman_location = document.getElementById('foodman_location');
    var foodman_location2 = document.getElementById('foodman_location2');
    
    //--------------end of location vars-------------//
    ///init state
    redirect.disabled = true;
    window.addEventListener("load",function(){
        console.log(order_id);
        var check = verify.value;
        console.log(check);
        if(check==0)
        {
            location_summary.style.display = "block";
            location_map.style.display = "none";
            foodman_image.style.display = "none";
            foodman_location.value = "23.7265768,90.3926623";
            setInterval("window.location.reload()",10000);
        }
        else{
            location_summary.style.display = "none";
            location_map.style.display = "flex";
            foodman_image.style.display = "block";
            status.innerHTML = "Estimated Delivery time:Within 2 hours";
            redirect.disabled = false;
            foodman_status.innerHTML = "FOODMAN AVAILABLE NOW";
            foodman_contact.innerHTML = "CONTACT:".concat(foodman_phone.value);
            place_name.innerHTML = "Foodman:".concat(foodman_name.value).concat(" Has picked your Order");
            foodman_location.value = foodman_location2.value;
            swal({
                title:"Hey,Your order has been picked" ,
                text: "Food'll be delivered soon",
                icon: "info",
                button: "ok",
              });


        }
        

    })
    ///---------------location--------------///
    

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
    var foodman_loc_marker = L.marker(splitter(foodman_location.value)).addTo(map);
    //loction.value = ""
    cur_loc_marker.bindPopup("Your current Location").openPopup();
    foodman_loc_marker.bindPopup("Foodman location").openPopup();
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
        console.log(loction.value);
        console.log(foodman_location.value);
        console.log('map created with current location');
        var check2 = verify.value;
        if(check2!=0)
        {
            L.Routing.control({
                waypoints: [
                    
                    foodman_loc_marker.getLatLng(),
                    cur_loc_marker.getLatLng()
                ]
              }).addTo(map);
        }
        
        
        foodman_loc_marker.setLatLng(splitter(foodman_location.value));
    }
    

    map.on('locationfound', onLocationFound);
    
    /*L.Routing.control({
      waypoints: [
          
          foodman_loc_marker.getLatLng(),
          cur_loc_marker.getLatLng()
      ]
    }).addTo(map);
    console.log('kajj kore nah vai ')*/

    ///---------------end of location--------------//
    

    function showPopup(){
            const timeLimit = 0 // seconds;
            let i=0;
            const timer = setInterval(function(){
            if(i == timeLimit){
            clearInterval(timer);
            loginPopup.classList.add("show");
            }
            i++; 
            console.log(i)
            },1000);
    }
})