document.addEventListener('DOMContentLoaded', function () {
    function splitter(ss) {
        var arr = ss.split(',')
        var a = +arr[0]
        var b = +arr[1]
        return [a, b]
    }

    console.log('location is loading');
    const latlng_buet = [23.7265768, 90.3926623];
    var location = document.getElementById('location')
    var latlng_rest = splitter(location.value);
    //console.log(' restaurant location is ' + latlng_rest);
    var map = L.map('map',
        {
            center: latlng_buet,
            zoom: 18,
            enableHighAccuracy: true
        });
    if (latlng_rest == undefined) {
        latlng_rest = latlng_buet;
    }
    //var cur_loc_marker = L.marker(latlng_buet).addTo(map);
    var cur_loc_marker = L.marker(latlng_rest).addTo(map);
    var new_loc_marker = undefined;
    cur_loc_marker.bindPopup("Current restaurant Location").openPopup();
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
        // var radius = e.accuracy;
        //
        // L.marker(e.latlng).addTo(map)
        //     .bindPopup("You are within " + radius + " meters from this point").openPopup();
        //cur_loc_marker.setLatLng(e.latlng);
        //L.circle(e.latlng, radius).addTo(map);
        //console.log('current pos ' + e.latlng);
        map.flyTo(e.latlng);
    }

    map.on('locationfound', onLocationFound);

    map.on('click', function (e) {
        if (new_loc_marker == undefined) {
            new_loc_marker = L.marker(e.latlng).addTo(map);
            new_loc_marker.bindPopup('New Restarant Location').openPopup();
        } else {
            new_loc_marker.setLatLng(e.latlng)
        }
        location.value = e.latlng.lat + ',' + e.latlng.lng
        //location.setAttribute('value', location.value)
        //document.getElementById('map').value = location.value
        //console.log(location.value);
    });


    //console.log(latlng);

});