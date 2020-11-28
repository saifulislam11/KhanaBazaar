//loading the DOM
document.addEventListener('DOMContentLoaded',function(){
    const loginPopup = document.querySelector(".login-popup");
    const close = document.querySelector(".close");
    window.addEventListener("load",function(){
    
    showPopup();
    setTimeout(function(){
      loginPopup.classList.add("show");
     },1000)

    })

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