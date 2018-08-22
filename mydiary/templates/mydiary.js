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
        } else if(data["message"] == "This user already exists!") {
            document.getElementById('regmessage').innerHTML = data["message"];
        }
    })
}

function loginmessage() {
    let usermessage = sessionStorage.getItem("usermessage")
    document.getElementById("logmessage").innerHTML = usermessage;
    sessionStorage.removeItem("usermessage")
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
        if(data["message"] == "Login successful") {
            let Token = data["access_token"]
            sessionStorage.setItem("token", Token);
            sessionStorage.setItem("usermessage", "You have been logged in!");
            window.location.href='./home.html'
        } else if(data["message"] == "Sorry, incorrect credentials") {
            document.getElementById('logmessage').innerHTML = data["message"];
        }
    })
}

function getUserEntries(){
    let Token = sessionStorage.getItem("token");
    let usermessage = sessionStorage.getItem("usermessage");
    document.getElementById("homemessage").innerHTML = usermessage;
    fetch('http://127.0.0.1:5000/api/v1/entries', {
        method:'GET',
        headers:{
            'Authorization': 'Bearer ' + Token,
            'Content-type':'application/json'
        },
    })
    .then((res) => res.json())
    .then ((data) => {
        var myTable = document.getElementById("entriesList");
        data.entries.forEach(function(entry) {
            let output = document.createElement("tr");
            output.innerHTML = `
            <th>${entry.title}</th>
            <th>${entry.date}</th>
            <th>
                <button id="${entry.entry_id}" type="submit" class="button-edit" onclick="edit(${entry.entry_id})">Edit</button>
                <input type="button" class="button-delete" onclick="" value="Delete">
            </th>
            `;
            myTable.appendChild(output)
            
        });
        sessionStorage.removeItem("usermessage")
    })
}

function getOneEntry(){
    sessionStorage.setItem("addoredit", "edit");
    let Token = sessionStorage.getItem("token");
    let entry_ID = sessionStorage.getItem("entry_ID");
    fetch('http://127.0.0.1:5000/api/v1/entries/'+ entry_ID, {
        method:'GET',
        headers:{
            'Authorization': 'Bearer ' + Token,
            'Content-type':'application/json'
        },
    })
    .then((res) => res.json())
    .then ((data) => {
        document.getElementById('entryTitle').value = data.getEntry.title;
        document.getElementById('entryDate').innerHTML = data.getEntry.date;
        document.getElementById('entryText').value = data.getEntry.data;
    })
}

function edit(entryID){
    sessionStorage.setItem("entry_ID", entryID);
    sessionStorage.setItem("addoredit", "edit");
    window.location.href='./edit.html'
}

function add(){
    sessionStorage.setItem("addoredit", "add");
    window.location.href='./edit.html'
}

function addOrEdit() {
    let addoredit = sessionStorage.getItem("addoredit");
    if(addoredit == "add") {
        document.getElementById('entryTitle').value = "";
        document.getElementById('entryDate').innerHTML = "";
        document.getElementById('entryText').value = "";
    } else if(addoredit == "edit") {
        getOneEntry()
    }
}

function newOrUpdate() {
    let addoredit = sessionStorage.getItem("addoredit");
    if(addoredit == "add") {
        addEntry()
    } else if(addoredit == "edit") {
        editEntry()
    }
}

function addEntry() {
    let Token = sessionStorage.getItem("token");
    let entrytitle = document.getElementById("entryTitle").value;
    let entrydata = document.getElementById('entryText').value;
    fetch('http://127.0.0.1:5000/api/v1/entries', {
        method:'POST',
        headers: {
            'Authorization': 'Bearer ' + Token,
            'Accept': 'application/json',
            'Content-type':'application/json'
        },
        body:JSON.stringify({"entrytitle": entrytitle, "entrydata": entrydata})
    })
    .then((res) => res.json())
    .then(function (data) {
        if(data["message"] == "Null entry field") {
            document.getElementById('editmessage').innerHTML = "Sorry! The entry cannot be left";
        } else if(data["message"] == "Entry already exists") {
            document.getElementById('editmessage').innerHTML = data["message"]
        } else if(data["message"] == "Entry added successfully") {
            usermessage = "Your thought titled, '" + entrytitle + "' has been added"
            sessionStorage.setItem("usermessage", usermessage)
            window.location.href='./home.html'
        } 
    })
}

function editEntry() {
    let Token = sessionStorage.getItem("token");
    let entrytitle = document.getElementById("entryTitle").value;
    let entrydata = document.getElementById('entryText').value;
    console.log("edit::  title: " + entrytitle + ", " + "data: " + entrydata)
    let entry_ID = sessionStorage.getItem("entry_ID");
    fetch('http://127.0.0.1:5000/api/v1/entries/'+ entry_ID, {
        method:'PUT',
        headers: {
            'Authorization': 'Bearer ' + Token,
            'Accept': 'application/json',
            'Content-type':'application/json'
        },
        body:JSON.stringify({"entrytitle": entrytitle, "entrydata": entrydata})
    })
    .then((res) => res.json())
    .then(function (data) {
        if(data["message"] == "Null entry field") {
            document.getElementById('editmessage').innerHTML = "The entry cannot be left blank. Write a note to future you!";
        } else if(data["message"] == "Sorry, cannot edit entries made before today") {
            document.getElementById('editmessage').innerHTML = data["message"]
        } else if(data["message"] == "Entry edited") {
            usermessage = "Your thought, '" + entrytitle + "' has just been updated"
            sessionStorage.setItem("usermessage", usermessage)
            window.location.href='./home.html'
        } 
    })
}

function logout() {
    let Token = sessionStorage.getItem("token");
    fetch('http://127.0.0.1:5000/logout', {
        method:'GET',
        headers: {
            'Authorization': 'Bearer ' + Token,
            'Content-type':'application/json'
        },
    })
    .then((res) => res.json())
    .then(function (data) {
        console.log("Show something")
        if(data["msg"] == "Successfully logged out") {
            sessionStorage.removeItem('token');
            sessionStorage.removeItem('entry_ID');
            sessionStorage.removeItem('addoredit');
            sessionStorage.setItem("usermessage", data["msg"]);
            window.location.href='./login.html'
        }
    })
}

// function redirect(page) {
//     pages = {
//         "login": './login.html',
//         "register": './registration.html'

//     }
// }