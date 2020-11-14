//loading the DOM
document.addEventListener('DOMContentLoaded',function(){
    //cart modal jqueries
    function updateAmount(i){
        //console.log(i);
        var priceElement = document.getElementsByClassName('modal-price')[i];
        
        console.log(priceElement.innerText.replace('BDT',''));
        var price = parseInt(priceElement.innerText.replace('BDT',''));
        var quantityElement = document.getElementsByClassName('count')[i];
        var quantity = quantityElement.value;
        console.log(quantity);
        total = quantity*price;
        var totalElement = document.getElementsByClassName('total-price')[i];
        totalElement.innerText = total;
        console.log(total);
    }
    
   
   

    //----update cart function-----//
    function updateCart(i,totalAmount,foodname,foodprice,foodcount){
        var priceElement = document.getElementsByClassName('modal-price')[i];
        
        ///console.log(priceElement.innerText.replace('BDT',''));
        var price = parseInt(priceElement.innerText.replace('BDT',''));
        var quantityElement = document.getElementsByClassName('count')[i];
        var quantity = parseInt(quantityElement.value);
        
        totalAmount =totalAmount+ quantity*price;
        foodprice=quantity*price;
        console.log(foodprice);
        foodcount=quantity;
        console.log(foodcount);
        //FOODNAME
        var nameOfFood = document.getElementsByClassName('modal-title')[i];
        foodname=nameOfFood;
        console.log(nameOfFood);
        
    }

    //all food-items
    var all_food_items = document.getElementsByClassName('food-item');
    var all_food_images = document.getElementsByClassName('food-image');
    var all_food_names = document.getElementsByClassName('food-name');
    console.log(all_food_items);
    //all confirm cart buttons
    var all_buttons = document.getElementsByClassName('confirm');
    //console.log(all_buttons);
    //console.log(all_buttons.length);
    for(let i=0;i<all_buttons.length;i++)
    {
        let button = all_buttons[i];
        //console.log(i);
        button.addEventListener('click',function(event){
            updateAmount(i);
        })

    }
    ///variables for cart

    const cartBTN = document.querySelector('.cart-btn');
    const closeCartBTN = document.querySelector('.close-cart');
    const clearCartBTN = document.querySelector('.clear-cart');
    const orderBTN = document.querySelector('.order');
    const cartDOM = document.querySelector('.cart');
    const cartOverlay = document.querySelector('.cart-overlay');
    const cartItems = document.querySelector('.cart-items');
    const cartTotal = document.querySelector('.cart-total');
    const cartContent = document.querySelector('.cart-content');
    const perItemCount = document.querySelector('.item-amount');
    const foodName= document.querySelector('.cart-heading');
    const perItemAmount = document.querySelector('.cart-price');

    ///form variables
    const formPrice = document.querySelector('.form-price');
    const formFoods = document.querySelector('.form-food');
    const formPrices = document.querySelector('.form-perprice');
    const formCounts = document.querySelector('.form-count');
    const Restaurant = document.querySelector('.id');
    const formRestaurant = document.querySelector('.form-restaurant');
    const formCount = document.querySelector('.form-items');
    formRestaurant.value=Restaurant.innerText;  

    //creating character values for payment page
    var foods="";
    var counts="";
    var prices="";


    //carts
    var map = new Map();
    cart=[]
    var keys =['foodname','price','count']
    //-----------getting modal elements----------------//
    const all_cart_submit = document.getElementsByClassName('cart-submit');
    const all_modal_food = document.getElementsByClassName('modal-food');
    let totalAmount =0;
    let itemTotal=0;
    ///3 variables for cart items
    var foodname='';
    var foodprice=0;
    var foodcount=0;
    function showCART(){
        cartOverlay.classList.add('transparentBcg');
        cartDOM.classList.add('showCart');
    }
    function hideCART(){
        cartOverlay.classList.remove('transparentBcg');
        cartDOM.classList.remove('showCart');
    }
    function setUP(){
        cartBTN.addEventListener('click',showCART);
        closeCartBTN.addEventListener('click',hideCART);
        
    }
    setUP();
    
    //cartlogic
    function clearCART(){
        //removing children one by one
        for(let i=0;i<all_cart_submit.length;i++){
            let button = all_cart_submit[i];
            //console.log(button);
            button.innerText="CONFIRM";
            button.disabled=false;

        }
        //removing from DOM one by one
        while(cartContent.children.length>0){
            
            cartContent.removeChild(cartContent.children[0]);
            


        }

    }
    ///find char for payment
    function findCharacters(){
        
        for(let x = 0;x<cartContent.children.length;x++){
            foods  = foods.concat(cartContent.children[x].childNodes[0].innerText,"#");
            prices=prices.concat(cartContent.children[x].childNodes[2].childNodes[1].innerText.replace('$',''),"#");
            counts=counts.concat(cartContent.children[x].childNodes[4].childNodes[3].innerText,"#");
            
            //console.log(cartContent.children);
            //cartContent.children.length


        }
        //assigning values
        formFoods.value=foods;
        formCounts.value=counts;
        formPrices.value=prices; 
        formCount.value=cartContent.children.length;
        
    }
    
    
    function cartLogic(){

        ///removing all cart
        clearCartBTN.addEventListener('click',event=>{
            clearCART();
            //UPDATING AMOUNTS TO ZERO
            itemTotal=0;
            totalAmount=0;
            cartItems.innerText=itemTotal;
            cartTotal.innerText=0;
            event.target.disabled=true;
            formPrice.value=totalAmount;
            //making all cart available again

        })
        //order
        orderBTN.addEventListener('click',event=>{
            findCharacters();
        })
        //other functionalities
        
        cartContent.addEventListener('click',event=>{
            //by this taking all elements in cartcontent
            if(event.target.classList.contains('remove-item'))
            {
                //removing cart from DOM
                let price=parseInt(event.target.parentElement.childNodes[1].innerText.replace('$',''));
                //finding name of food of removed item
                let selected_name =event.target.parentElement.parentElement.childNodes[0].innerText;
                let removetItem = event.target;
                cartContent.removeChild(removetItem.parentElement.parentElement);
                //updating values
                itemTotal=itemTotal-1;
                totalAmount=totalAmount-price;
                cartItems.innerText=itemTotal;
                cartTotal.innerText=totalAmount;
                formPrice.value=totalAmount;
               
                for(let i=0;i<all_cart_submit.length;i++){
                    button=all_cart_submit[i];
                    let fetch_name=all_cart_submit[i].parentElement.parentElement.parentElement.parentElement.childNodes[1].childNodes[1].innerText;
                    //console.log(button);
                    
                    //if names matching then activate cart button 
                    if(fetch_name==selected_name){
                        button.innerText="CONFIRM";
                        button.disabled=false;
                    }
                    
                }
                //totalAmount=totalAmount-parseInt()
            }
            
            else if(event.target.classList.contains('fa-chevron-up')){
                let price = parseInt(event.target.parentElement.parentElement.children[1].childNodes[1].innerText.replace('$',''));
                let count= parseInt(event.target.parentElement.childNodes[3].innerText);
                event.target.parentElement.childNodes[3].innerText=count+1;
                console.log(price);
                console.log(count);
                event.target.parentElement.parentElement.children[1].childNodes[1].innerText='$'+ '\n'+(price/count)*(count+1);
                //updating totalamount
                totalAmount=totalAmount-price+(price/count)*(count+1);
                cartTotal.innerText=totalAmount;
                formPrice.value=totalAmount;

            }
            else if(event.target.classList.contains('fa-chevron-down')){
                let price = parseInt(event.target.parentElement.parentElement.children[1].childNodes[1].innerText.replace('$',''));
                event.target.parentElement.parentElement.children[1].childNodes[1].innerText='$'
                let count= parseInt(event.target.parentElement.childNodes[3].innerText);
                
                console.log(price);
                console.log(count);
                if(count<=1){
                    //no change
                    event.target.parentElement.childNodes[3].innerText=count;
                    event.target.parentElement.parentElement.children[1].childNodes[1].innerText='$'+ '\n'+(price/count);
                    
                    cartTotal.innerText=totalAmount;
                    formPrice.value=totalAmount;
                }
                else{
                    event.target.parentElement.childNodes[3].innerText=count-1;
                    event.target.parentElement.parentElement.children[1].childNodes[1].innerText='$'+ '\n'+(price/count)*(count-1);
                    //updating totalamount
                    totalAmount=totalAmount-price+(price/count)*(count-1);
                    cartTotal.innerText=totalAmount;
                    formPrice.value=totalAmount;

                }
                

            }

        })
    }
    //call cartLogic
    cartLogic();
    
    
    for(let i=0;i<all_cart_submit.length;i++)
    {
        let button = all_cart_submit[i];
        //console.log(i);
        button.addEventListener('click',function(event){
            ///updateAmount(i);
            event.target.innerText="In Cart";
            event.target.disabled=true;
            //-----------steps of adding carts-------------//
            //step 1: ------get food-items-------//
            itemTotal+=1;

            //updating price & count & names
            var priceElement = document.getElementsByClassName('modal-price')[i];
            var price = parseInt(priceElement.innerText.replace('BDT',''));
            var quantityElement = document.getElementsByClassName('count')[i];
            var quantity = parseInt(quantityElement.value);
            
            totalAmount =totalAmount+ quantity*price;
            foodprice=quantity*price;
            console.log(foodprice);
            foodcount=quantity;
            console.log(foodcount);
            //FOODNAME
            var nameOfFood = document.getElementsByClassName('modal-food')[i].innerText;
            foodname=nameOfFood;
            console.log(nameOfFood);
            cartTotal.innerText=totalAmount;
            cartItems.innerText=itemTotal;
            formPrice.value=totalAmount;
            
            
            values=[foodname,foodprice,foodcount]
            //------------end of updates---------//

            //step 2:--------add food item to cart-------// 
            const div = document.createElement('div');
            div.classList.add('added-to-cart');
            div.innerHTML=`<h1 class="cart-heading">${foodname}</h1>
            
            <div>
                <h5 class="cart-price">$ ${foodprice}</h5>
                <span class="remove-item">remove</span>
            </div>
            <div>
                <i class="fa fa-chevron-up"></i>
                <h6 class="item-amount">${foodcount}</h6>
                <i class="fa fa-chevron-down"></i>
            </div>`
            
            // formFood.value=foodname;
            //console.log(formFood.value);
            cartContent.appendChild(div);
            console.log(cartContent);
            //step 5--------show cart-------//
            cartOverlay.classList.add('transparentBcg');
            cartDOM.classList.add('showCart');
            
        })

    }
    


    

    /*var all_buttons = document.getElementsByClassName('add_cart');
    console.log(all_buttons);
    console.log(all_buttons.length);
    for(let i=0;i<all_buttons.length;i++)
    {
        let button = all_buttons[i];
        ///console.log(i);
        button.addEventListener('click',function(event){
            var buttonClicked = event.target;
            console.log(i);
        })

    }*/

    /*var cart_confirm_button = document.getElementsByClassName('confirm')[0];
    ///console.log(cart_confirm_button);
    confirm_button = cart_confirm_button;
    confirm_button.addEventListener('click',function(event){
        console.log(cart_confirm_button);
        updateAmount();


    })*/
    //default submit button disabled
    document.querySelector('#submit').disabled = true;
    //onkeyup handler
    document.querySelector('#password').onkeyup = () =>{
        //checking if password is typed or not 
        if (document.querySelector('#password').value.length > 0){
            document.querySelector('#submit').disabled = false;
        } 
        else{
            document.querySelector('#submit').disabled = true;
        }
       
    }
    
})