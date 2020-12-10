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

//invalid log check
const invalid = document.querySelector('#invalid_log');
const register = document.querySelector('#register_log');
console.log(invalid.value);
//------------all alert context-------------//
if(invalid.value === "Incorrect password or email!!!")
{
    swal({
        title:invalid.value ,
        text: "Try Again",
        icon: "error",
        button: "Ok",
      });
}
if(register.value === "registered successfully")
{
    swal({
        title:register.value ,
        text: "Welcome to KhanaBazaar",
        icon: "info",
        button: "continue",
      });
}
else if(register.value === "something went wrong.try again")
{
    swal({
        title:"There exists an ID using this mail" ,
        text: "Try with another mail",
        icon: "error",
        button: "Ok",
      });

}

//-----------------end of alert-----------//
    
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
        console.log()
        //checking if password is typed or not 
        if(document.querySelector('#password1').value=='' || document.querySelector('#password1').value != document.querySelector('#confirmpassword').value ){
            document.querySelector('#register').disabled = true;
        }
        else if (document.querySelector('#password1').value == document.querySelector('#confirmpassword').value){
            document.querySelector('#register').disabled = false;
        } 
        
        else{
            document.querySelector('#register').disabled = true;

        }
       
    }
    document.querySelector('#confirmpassword').onkeyup = () =>{
        console.log('pressed');
        console.log()
        //checking if password is typed or not 
        if(document.querySelector('#password1').value=='' || document.querySelector('#password1').value != document.querySelector('#confirmpassword').value ){
            document.querySelector('#register').disabled = true;
        }
        else if (document.querySelector('#password1').value == document.querySelector('#confirmpassword').value){
            document.querySelector('#register').disabled = false;
        } 
        
        else{
            document.querySelector('#register').disabled = true;

        }
       
    }
    
})