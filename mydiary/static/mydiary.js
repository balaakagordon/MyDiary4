function addUser(){

    let name = document.getElementById('uname').value;
    let email = document.getElementById('mail').value;
    let password = document.getElementById('pword').value;
    let confirmpassword = document.getElementById('pword2').value;

    fetch('http://127.0.0.1:5000/auth/signup', {
        method:'POST',
        headers:{
            'Content-type':'application/json'
        },
        body:JSON.stringify({name: name, email: email, password:password, confirmpassword:confirmpassword})
    })
    .then((res) => res.json())
    .then(function (data){
        //let serverresponse = data["message"];
        if(data["message"] == "Invalid input"){
            let errormsg = data["error"];
        } else if(serverresponse == "Registered Successfully!"){
            login();
        }
        
    })

}

function regResponse(data){
    //let serverresponse = data["message"];
        if(data["message"] == "Invalid input"){
            let errormsg = data["error"];
        } else if(serverresponse == "Registered Successfully!"){
            window.location.href='./home.html'
            login();
        }

}



function login(e){
    e.preventDefault();

    let email = document.getElementById('mail').value;
    let password = document.getElementById('pword').value;

    fetch('http://127.0.0.1:5000/auth/login', {
        method:'POST',
        headers:{
            'Content-type':'application/json'
        },
        body:json.dumps({"email": email, "password":password})
    })
    //.then((res) => res.json())
    .then(regResponse(data))
}