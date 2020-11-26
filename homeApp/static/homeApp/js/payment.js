    //------------VARIABLES FOR PAYMENT PAGE----------//

document.addEventListener('DOMContentLoaded',function(){
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
    const sel = document.querySelector('.payment-method');
    const img_pay = document.querySelector('.img_pay');

    let selected_method = sel.options[sel.selectedIndex];
    console.log(selected_method);
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
        <input type="text" id="location" name="location" placeholder="location" required>
    </div>`

       
    // get selected option in sel (reference obtained above)
    orderBTN.addEventListener("click",function(){
        console.log(selected_method.innerHTML);
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