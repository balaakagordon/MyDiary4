function addUser() {

    let name = document.getElementById('uname').value;
    let email = document.getElementById('mail').value;
    let password = document.getElementById('pword').value;
    let confirmpassword = document.getElementById('pword2').value;
    fetch('http://127.0.0.1:5000/auth/signup', {
        method:'POST',
        headers:{
            'Accept': 'application/json',
            'Content-type':'application/json'
        },
        body:JSON.stringify({name: name, email: email, password:password, confirmpassword:confirmpassword})
    })
    .then((res) => res.json())
    .then(function (data) {
        if(data["message"] == "Invalid input") {
            let errormsg = data["error"];
            document.getElementById('regmessage').innerHTML = errormsg;
        } else if(data["message"] == "Registered Successfully!") {
            window.location.href='./login.html'
            //login(email, password);
        } else if(data["message"] == "This user already exists!") {
            document.getElementById('regmessage').innerHTML = data["message"];
        }
    })
}


function login(){

    let email = document.getElementById('mail').value;
    let password = document.getElementById('pword').value;
    fetch('http://127.0.0.1:5000/auth/login', {
        method:'POST',
        headers:{
            'Accept': 'application/json',
            'Content-type':'application/json'
        },
        body:JSON.stringify({"email": email, "password":password})
    })
    .then((res) => res.json())
    .then (function (data) {
        console.log(data["message"])
        if(data["message"] == "Login successful") {
            window.location.href='./home.html'
        } else if(data["message"] == "Sorry, incorrect credentials") {
            document.getElementById('logmessage').innerHTML = errormsg;
        }
    })
}