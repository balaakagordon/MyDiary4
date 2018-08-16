//var Token = null;

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
            let Token = data["access_token"]
            sessionStorage.setItem("token", Token);
            window.location.href='./home.html'
        } else if(data["message"] == "Sorry, incorrect credentials") {
            document.getElementById('logmessage').innerHTML = data["message"];
        }
    })
}

//console.log("token noFunction: " + Token)

// function getUserEntries(){
//     let Token = sessionStorage.getItem("token");
//     //console.log("token getentries: " + Token)
//     fetch('http://127.0.0.1:5000/api/v1/entries', {
//         method:'GET',
//         headers:{
//             'Authorization': 'Bearer ' + Token,
//             'Content-type':'application/json'
//         },
//     })
//     .then((res) => res.json())
//     .then (function(data) {
//         // displayEntries()
//         document.getElementById('userEntries').innerHTML = JSON.stringify(data.entries);
//         // // console.log("msg: " + data["msg"])
//         // // console.log("data: " + JSON.stringify(data.entries))
//         // var newRow = document.createElement("tr");
//         // var entryCol = document.createElement("th");
//         // entryCol.textContent
//         // var dateCol = document.createElement("th");
//         // var buttonCol = document.createElement("th");

//         // var myTable = document.getElementById("entriesList");
//         // my

//     })
// }

function getUserEntries(){
    let Token = sessionStorage.getItem("token");
    //console.log("token getentries: " + Token)
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
                <a href="edit.html"><input type="button" class="button-edit" onclick="" value="Edit"></a>
                <input type="button" class="button-delete" onclick="" value="Delete">
            </th>
            `;
            myTable.appendChild(output)
            
        });
        //document.getElementById('userEntries').innerHTML = JSON.stringify(data.entries);
        
        // console.log("msg: " + data["msg"])
        // console.log("data: " + JSON.stringify(data.entries))
        

    })
}

// output += `
//                 <ul>
//                     <li>ID: ${entry.entry_id}</li>
//                     <li>Data: ${entry.data}</li>
//                     <li>Date: ${entry.date}</li>
//                 </ul>`;


//document.getElementById('userEntries').innerHTML = output;