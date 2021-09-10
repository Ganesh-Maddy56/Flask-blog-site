let id = (id)=>document.getElementById(id);

let classes = (classes)=>document.getElementsByClassName(classes);

let 
username = id("username")
email = id("email"),
form = id("form"),
password = id("password"),
errorMessage = classes("error"),
successIcon = classes("success-icon"),
failureIcon = classes("failure-icon");

form.addEventListener('submit',(e)=>{
    if (!username){
        logic(email,0,"email cannot be empty")  
        logic(password,1,"password cannot be empty")  
    }else{
        logic(username,0,"username cannot be empty") 
        logic(email,1,"email cannot be empty")  
        logic(password,2,"password cannot be empty") 
    } 
})


let logic = (id,index,message)=>{
    if (id.value.trim() === ''){
        errorMessage[index].innerHTML = message
        failureIcon[index].style.opacity = "1"
        successIcon[index].style.opacity = "0" 
    }else{
        errorMessage[index].innerHTML = '';
        failureIcon[index].style.opacity = "0"
        successIcon[index].style.opacity = "1"
    }
}


var check = document.querySelector("#check")
var box = document.querySelector(".box")
var ball = document.querySelector(".ball")

check.addEventListener('change',function(){
    if (this.checked == true){
        document.body.setAttribute('style','color:white')
        ball.setAttribute('style',"transform:translateX(100%);")
        document.body.setAttribute('style','background-color:teal')

    }
    if (check.checked == false){
        ball.setAttribute('style',"transform:translateX(0%);")
        document.body.setAttribute('style','background-color:white')


    }
})