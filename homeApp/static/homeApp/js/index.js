//loading the DOM
document.addEventListener('DOMContentLoaded',function(){
var password = document.getElementById("password1")
var confirmpassword = document.getElementById("confirmpassword");

/*function validatePassword(){
  if(password.value != confirmpassword.value) {
    console.log(password.value)
    console.log(confirmpassword.value)
    confirmpassword.setCustomValidity("Passwords Don't Match");
  }
}

password.onchange = validatePassword;
confirmpassword.onkeyup = validatePassword;*/
    
       //default submit button disabled
    document.querySelector('#submit').disabled = true;
    //onkeyup handler
    document.querySelector('#password').onkeyup = () =>{
        console.log('pressed');
        //checking if password is typed or not 
        if (document.querySelector('#password').value.length > 0){
            document.querySelector('#submit').disabled = false;
        } 
        else{
            document.querySelector('#submit').disabled = true;
        }
       
    }
    document.querySelector('#register').disabled = true;
    //onkeyup handler
    document.querySelector('#address').onkeyup = () =>{
        console.log('pressed');
        //checking if password is typed or not 
        if (document.querySelector('#password1').value == document.querySelector('#confirmpassword').value){
            document.querySelector('#register').disabled = false;
        } 
        else{
            document.querySelector('#register').disabled = true;
        }
       
    }
    
})