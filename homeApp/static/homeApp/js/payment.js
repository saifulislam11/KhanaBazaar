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
    
});