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
            document.getElementById('regmessage').innerHTML = data["error"];
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
        //console.log("data: " + data)
        if(data["message"] == "Login successful") {
            console.log("token from login: " + data["access_token"])
            getUserEntries(data["access_token"])
            //window.location.href='./home.html'
        } else if(data["message"] == "Sorry, incorrect credentials") {
            document.getElementById('logmessage').innerHTML = data["message"];
        }
    })
}


function getUserEntries(token){
    //console.log("token getentries: " + token)
    fetch('http://127.0.0.1:5000/api/v1/entries', {
        method:'GET',
        headers:{
            'Authorization': 'Bearer ' + token,
            'Content-type':'application/json'
        },
    })
    .then((res) => res.json())
    .then (function (data) {
        console.log("data: " + data["msg"])
        console.log("data: " + data["entries"])
    })
}