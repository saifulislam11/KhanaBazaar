//loading the DOM
document.addEventListener('DOMContentLoaded',function(){
    //cart modal jqueries
    function updateAmount(i){
        console.log(i);
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
    var all_buttons = document.getElementsByClassName('confirm');
    console.log(all_buttons);
    console.log(all_buttons.length);
    for(let i=0;i<all_buttons.length;i++)
    {
        let button = all_buttons[i];
        console.log(i);
        button.addEventListener('click',function(event){
            updateAmount(i);
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
    document.querySelector('#exampleInputPassword3').onkeyup = () =>{
        //checking if password is typed or not 
        if (document.querySelector('#exampleInputPassword3').value.length > 0){
            document.querySelector('#submit').disabled = false;
        } 
        else{
            document.querySelector('#submit').disabled = true;
        }
       
    }
})