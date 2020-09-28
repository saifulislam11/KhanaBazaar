//loading the DOM
document.addEventListener('DOMContentLoaded',function(){
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