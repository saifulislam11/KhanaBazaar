    //------------VARIABLES FOR PAYMENT PAGE----------//

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
        map.flyTo(e.latlng);
        console.log('map created with current location');
    }

    map.on('locationfound', onLocationFound);

    ///---------------end of location--------------//
    const PcartBTN = document.querySelector('.Pcart-btn');
    const PcloseCartBTN = document.querySelector('.Pclose-cart');
    const PclearCartBTN = document.querySelector('.Pclear-cart');
    const PcartDOM = document.querySelector('.Pcart');
    const PcartOverlay = document.querySelector('.Pcart-overlay');
    const PcartItems = document.querySelector('.Pcart-items');
    const PcartTotal = document.querySelector('.Pcart-total');
    const PcartContent = document.querySelector('.Pcart-content');
    console.log(PcartBTN);
    console.log(PcartBTN);


     //----------------------------login popup----------------------
     const loginPopup = document.querySelector(".login-popup");
     const order_type = document.querySelector("#delivery_type");
     const delivery_address = document.querySelector("#delivery_address");
     const del_address = document.querySelector(".del-address");
     const close = document.querySelector(".close");
     const order_pop_button = document.querySelector('#confirm_order');
     order_pop_button.addEventListener("click",function(){
        showPopup();
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
console.log(PcartBTN);


close.addEventListener("click",function(){
    loginPopup.classList.remove("show");
})


//----------------------end of login popup------------------------

    

    //------------Psetups--------------//
    function PshowCART(){
        PcartOverlay.classList.add('transparentBcg');
        PcartDOM.classList.add('showCart');
    }
    function PhideCART(){
        PcartOverlay.classList.remove('transparentBcg');
        PcartDOM.classList.remove('showCart');
    }
    function PsetUP(){
        PcartBTN.addEventListener('click',PshowCART);
        PcloseCartBTN.addEventListener('click',PhideCART);
    }
    PsetUP();
    console.log(PcartBTN);

    const gateway = document.querySelector('.gateway');
    const orderBTN = document.querySelector('#confirm_order');
    const promo_used = document.querySelector('#promo_used');
    const final_price = document.querySelector('#final_price');
    const sel = document.querySelector('.payment-method');
    const promo = document.querySelector('.promo-selected');
    const promo_table_row = document.getElementsByClassName('promo-table-row');
    const img_pay = document.querySelector('.img_pay');
    const typing = document.querySelector('.typing');
    const cart_total = document.querySelector('.Pcart-total');
    var save_price = final_price.value;

    let selected_method = sel.options[sel.selectedIndex];
    let selected_promo = promo.options[promo.selectedIndex];
    console.log(selected_method);
    console.log(selected_promo);
    promo_used.value = selected_promo.innerHTML;
    console.log(PcartBTN);
    sel.addEventListener("change",function(){
        let opt;
        for ( let i = 0, len = sel.options.length; i < len; i++ ) {
            opt = sel.options[i];
            console.log(opt);
            if ( opt.selected === true ) {
                break;
            }
        }
        selected_method = opt;
        console.log(selected_method.innerHTML);
    })
    promo.addEventListener("change",function(){
        let opt;
        for ( let i = 0, len = promo.options.length; i < len; i++ ) {
            opt = promo.options[i];
            console.log(opt);
            if ( opt.selected === true ) {
                break;
            }
        }
        
        selected_promo = opt;
        console.log(selected_promo.innerHTML);
        promo_used.value = selected_promo.innerHTML;
        console.log(promo_used.value);
        if(promo_used.value === "Not now")
        {
            swal({
                title:"No Promo Selected!!" ,
                text: "Are you sure?",
                icon: "warning",
                button: "Yes",
              });
        }
        else{
            swal({
                title:selected_promo.innerHTML.concat(" Selected!!") ,
                text: "Thanks for using the promo!",
                icon: "success",
                button: "OK!",
              });
        }
        
    })
 
    

    const div1 = document.createElement('div');
    const div2 = document.createElement('div');
    const div3 = document.createElement('div');
    const div4 = document.createElement('div');
    var img = document.createElement('img'); 
    ///img.src =  'https://www.logo.wine/a/logo/BKash/BKash-bKash-Logo.wine.svg';    for bkash
    ///https://seeklogo.com/images/D/dutch-bangla-rocket-logo-B4D1CC458D-seeklogo.com.png
    

    ///div.classList.add('added-to-cart');
    div1.innerHTML = `<div class="form-group">
    <label for="fname">Accepted Cards</label>
    <div class="form-group">
        <i class="fa fa-cc-visa" style="color:navy;"></i>
        <i class="fa fa-cc-amex" style="color:blue;"></i>
        <i class="fa fa-cc-mastercard" style="color:red;"></i>
        <i class="fa fa-cc-discover" style="color:orange;"></i>
    </div>
    <label for="cname">Name on Card</label>
    <div class="form-group">
    <input type="text" id="cname" name="cardname" placeholder="John More Doe" required>
    </div>
    <label for="ccnum">Credit card number</label>
    <div class="form-group">
    <input type="text" id="ccnum" name="cardnumber" placeholder="1111-2222-3333-4444" required>
    </div>
    
    <label for="expmonth">Exp Month</label>
    <div class="form-group">
    <input type="text" id="expmonth" name="expmonth" placeholder="September" required>
    </div>
    
    <label for="expyear">Exp Year</label>
    <div class="form-group">
        <input type="text" id="expyear" name="expyear" placeholder="2018" required>
    </div>
    <label for="cvv">CVV</label>
    <div class="form-group">
        <input type="text" id="cvv" name="cvv" placeholder="352" required>
    </div>`

    //div for Bkash
    div2.innerHTML = `<div class="form-group">
    <div class="form-group">
    </div>
    <label for="phone">Phone Number</label>
    <div class="form-group">
        <input type="text" id="phone" name="phone" placeholder="01XXXXXXXXX" required>
    </div>
    <label for="pin">PIN</label>
    <div class="form-group">
        <input type="text" id="pin" name="pin" placeholder="XXX-XXX" required>
    </div>`
    div3.innerHTML = `<div class="form-group">
    <div class="form-group">
    </div>
    <label for="phone">Phone Number</label>
    <div class="form-group">
        <input type="text" id="phone" name="phone" placeholder="01XXXXXXXXX" required>
    </div>
    <label for="pin">PIN</label>
    <div class="form-group">
        <input type="text" id="pin" name="pin" placeholder="XXX-XXX" required>
    </div>`
    div4.innerHTML = `<div class="form-group">
    <div class="form-group">
    </div>
    <label for="phone">Phone Number</label>
    <div class="form-group">
        <input type="text" id="phone" name="phone" placeholder="01XXXXXXXXX" required>
    </div>
    <label for="pin">confirm location</label>
    <div class="form-group">
        <input type="text" class="form-control form-box del-address" id="location" name="location" placeholder="location" required>
    </div>`

       
    // get selected option in sel (reference obtained above)
    orderBTN.addEventListener("click",function(){
        //initialize final_price
        final_price.value = save_price;
        delivery_address.value = del_address.value;
        order_type.value = selected_method.innerHTML;
        console.log(delivery_address.value);
        console.log(selected_method.innerHTML);
        for(let i=0;i<promo_table_row.length;i++)
        {
            //checking selected promo
            console.log('hello');
            const temp = promo_table_row[i].children[0].innerHTML;
            console.log(temp);
            
            if(promo_used.value == temp)
            {
                var temp_percent = promo_table_row[i].children[2].innerHTML;
                console.log(temp_percent);
                var temp_fixed = promo_table_row[i].children[3].innerHTML;
                console.log(temp_fixed);
                temp_fixed = temp_fixed.replace('$','');
                temp_percent = temp_percent.replace('%','');
                var remainig_promo = promo_table_row[i].children[6].innerHTML;
                
                if(Number(temp_percent) === 0){
                    if(Number(remainig_promo)===0)
                    {
                        swal({
                            title:"Promo Not Applicable!!" ,
                            text: "Thanks For your response",
                            icon: "error",
                            button: "ok",
                          });
                        ///setting promo to not now
                        promo_used.value = "Not now";
                        typing.innerHTML = "Your Total is ".concat(save_price,"TK");
                        cart_total.innerHTML = save_price;
                        final_price.value = save_price;
                    }
                    else{
                        console.log('check for fixed amount now');
                        //setting reduced price
                        final_price.value = final_price.value - Number(temp_fixed);
                        typing.innerHTML = "Your Total is ".concat(final_price.value,"TK");
                        cart_total.innerHTML = final_price.value;

                    }
                    
                }
                else{
                    var offer = Number(temp_percent);
                    var reduce = (final_price.value*offer)/100
                    
                    var max_offer = promo_table_row[i].children[5].innerHTML;
                    
                    max_offer = max_offer.replace('$','');
                    console.log(max_offer);

                    if(Number(remainig_promo)===0)
                    {
                        swal({
                            title:"Promo Not Applicable!!" ,
                            text: "Thanks For your response",
                            icon: "error",
                            button: "ok",
                          });
                        ///setting promo to not now
                        promo_used.value = "Not now";
                        typing.innerHTML = "Your Total is ".concat(save_price,"TK");
                        cart_total.innerHTML = save_price;
                        final_price.value = save_price;
                    }
                    ///if less than max discount
                    else if(Number(max_offer)>=reduce)
                    {
                        final_price.value = final_price.value - reduce ;
                        typing.innerHTML = "Your Total is ".concat(final_price.value,"TK");
                        cart_total.innerHTML = final_price.value;
                        
                    }
                    else{
                        ///setting promo to not now
                        promo_used.value = "Not now";
                        typing.innerHTML = "Your Total is ".concat(save_price,"TK");
                        cart_total.innerHTML = save_price;
                        final_price.value = save_price;
                        swal({
                            title:"Promo Not Applicable!!" ,
                            text: "Thanks For your response",
                            icon: "warning",
                            button: "ok",
                          });
                    }

                   

                }
                break;
            }
        }
        if (promo_used.value === "Not now" ){
            typing.innerHTML = "Your Total is ".concat(save_price,"TK");
            cart_total.innerHTML = save_price;
            final_price.value = save_price;
            console.log(save_price);
        }
        if(selected_method.innerHTML == 'Bkash')
        {
            while(img_pay.children.length>0){
                img_pay.removeChild(img_pay.children[0]);
            }
            while(gateway.children.length>0){
                gateway.removeChild(gateway.children[0]);
            }
            img.src =  'https://www.logo.wine/a/logo/BKash/BKash-bKash-Logo.wine.svg';
            img.width = 130;
            img_pay.appendChild(img);
            gateway.appendChild(div2);

        }
        else if(selected_method.innerHTML == 'Credit Card')
        {
            while(img_pay.children.length>0){
                img_pay.removeChild(img_pay.children[0]);
            }
            while(gateway.children.length>0){
                gateway.removeChild(gateway.children[0]);
            }
            gateway.appendChild(div1);

        }
        else if(selected_method.innerHTML == 'Rocket')
        {
            while(img_pay.children.length>0){
                img_pay.removeChild(img_pay.children[0]);
            }
            while(gateway.children.length>0){
                gateway.removeChild(gateway.children[0]);
            }
            img.src = 'https://seeklogo.com/images/D/dutch-bangla-rocket-logo-B4D1CC458D-seeklogo.com.png';
            img.width = 130;
            img_pay.appendChild(img);
            gateway.appendChild(div3);

        }
        else{
            while(img_pay.children.length>0){
                img_pay.removeChild(img_pay.children[0]);
            }
            while(gateway.children.length>0){
                gateway.removeChild(gateway.children[0]);
            }
            img.src = 'https://media3.s-nbcnews.com/j/newscms/2019_06/2746941/190208-stock-money-fanned-out-ew-317p_fa445b2f6f3e86a3ffa18707e6a8adcb.nbcnews-fp-1024-512.jpg';
            img.width = 130;
            img_pay.appendChild(img);
            gateway.appendChild(div4);
        }
    })
    
    
    
    

    
    //console.log(cartContent);

    
});