var baseurl = "http://mydiary4-gbalaaka.herokuapp.com"

function addUser() {
    let name = document.getElementById('uname').value;
    let email = document.getElementById('mail').value;
    let password = document.getElementById('pword').value;
    let confirmpassword = document.getElementById('pword2').value;
    fetch(baseurl + '/auth/signup', {
        method:'POST',
        headers:{
            'Accept': 'application/json',
            'Content-type':'application/json'
        },
        body:JSON.stringify({
                name: name,
                email: email,
                password: password,
                confirmpassword: confirmpassword
        })
    })
    .then((res) => res.json())
    .then(function (data) {
        if(data["message"] == "Invalid input") {
            document.getElementById('regmessage').innerHTML = data["error"];
        } else if(data["message"] == "Registered Successfully!") {
            window.location.href='/login'
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
    fetch(baseurl + '/auth/login', {
        method:'POST',
        headers:{
            'Accept': 'application/json',
            'Content-type':'application/json'
        },
        body:JSON.stringify({"email": email, "password": password})
    })
    .then((res) => res.json())
    .then (function (data) {
        if(data["message"] == "Login successful") {
            let Token = data["access_token"]
            sessionStorage.setItem("token", Token);
            sessionStorage.setItem("usermessage", "Welcome! You have been logged in, succesfully :)");
            window.location.href='/home'
        } else if(data["message"] == "Sorry, incorrect credentials") {
            document.getElementById('logmessage').innerHTML = data["message"];
        }
    })
    .catch((err) => console.log(err))
}

function userProfile() {
    let Token = sessionStorage.getItem("token");
    fetch(baseurl + '/profile', {
        method:'GET',
        headers: {
            'Authorization': 'Bearer ' + Token,
            'Content-type':'application/json'
        },
    })
    .then(function(res) {
        appStatus = res.status;
        return res.json();
    })
    .then(function (data) {
        errCatcher(data)
        document.getElementById("allentries").innerHTML = data.userdata.allEntries
        document.getElementById("currententries").innerHTML = data.userdata.currentEntries
        document.getElementById("deletedentries").innerHTML = data.userdata.deletedEntries
        document.getElementById("registered").innerHTML = data.userdata.registered
        document.getElementById("lastused").innerHTML = data.userdata.lastUsed
    })
}

function logout() {
    let Token = sessionStorage.getItem("token");
    fetch(baseurl + '/logout', {
        method:'GET',
        headers: {
            'Authorization': 'Bearer ' + Token,
            'Content-type':'application/json'
        },
    })
    .then((res) => res.json())
    .then(function (data) {
        if(data["msg"] == "Successfully logged out") {
            sessionStorage.removeItem('token');
            sessionStorage.removeItem('entry_ID');
            sessionStorage.removeItem('addoredit');
            sessionStorage.setItem("usermessage", data.msg);
            window.location.href='/login';
        }
    })
}

function getUserEntries() {
    var reminder = ""
    let Token = sessionStorage.getItem("token");
    let usermessage = sessionStorage.getItem("usermessage");
    let modal = document.getElementById('myModal');
    if (usermessage == "Welcome! You have been logged in, succesfully :)") {
        reminder = "Have you written today? Record some memories for future you! :)"
    }
    document.getElementById("homepopup").innerHTML = usermessage;
    fetch(baseurl + '/api/v1/entries', {
        method:'GET',
        headers:{
            'Authorization': 'Bearer ' + Token,
            'Content-type':'application/json'
        },
    })
    .then(function(res) {
        appStatus = res.status;
        return res.json();
    })
    .then(function (data) {
        errCatcher(data)
        let writtenToday = data.writtenToday;
        console.log("writtenToday value: " + writtenToday)
        if (writtenToday == false){
            document.getElementById("writtenToday").innerHTML = reminder;
            reminder = ""
        }
        if (usermessage == "Welcome! You have been logged in, succesfully :)") {
            modal.style.display = "block";
        }
        var myTable = document.getElementById("entriesList");
        data.entries.forEach(function(entry) {
            let output = document.createElement("tr");
            output.innerHTML = `
            <th>${entry.title}</th>
            <th>${entry.date}</th>
            <th class="flex-container">
                <button id="${entry.entry_id}" type="submit" class="button-edit" onclick="edit(${entry.entry_id})">Edit</button>
                <button id="${entry.entry_id}" type="submit" class="button-delete" onclick="del(${entry.entry_id})">Delete</button>
            </th>
            `;
            myTable.appendChild(output);

        });
        
        sessionStorage.removeItem("usermessage");
    })

}

function closeModal() {
    let modal = document.getElementById('myModal');
    modal.style.display = "none";
}

function getOneEntry() {
    sessionStorage.setItem("addoredit", "edit");
    let Token = sessionStorage.getItem("token");
    let entry_ID = sessionStorage.getItem("entry_ID");
    fetch(baseurl + '/api/v1/entries/' + entry_ID, {
        method:'GET',
        headers:{
            'Authorization': 'Bearer ' + Token,
            'Content-type':'application/json'
        },
    })
    .then(function(res) {
        appStatus = res.status;
        return res.json();
    })
    .then(function (data) {
        errCatcher(data)
        document.getElementById('entryTitle').value = data.getEntry.title;
        document.getElementById('entryDate').innerHTML = data.getEntry.date;
        document.getElementById('entryText').value = data.getEntry.data;
    })
}

function edit(entryID){
    sessionStorage.setItem("entry_ID", entryID);
    sessionStorage.setItem("addoredit", "edit");
    window.location.href='/edit'
}

function add() {
    sessionStorage.setItem("addoredit", "add");
    window.location.href='/edit'
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
    fetch(baseurl + '/api/v1/entries', {
        method:'POST',
        headers: {
            'Authorization': 'Bearer ' + Token,
            'Accept': 'application/json',
            'Content-type':'application/json'
        },
        body:JSON.stringify({"entrytitle": entrytitle, "entrydata": entrydata})
    })
    .then(function(res) {
        appStatus = res.status;
        return res.json();
    })
    .then(function (data) {
        errCatcher(data)
        if(data["message"] == "Null entry field") {
            document.getElementById('editmessage').innerHTML = "Please write down something, in the entry field, for future you!";
        } else if(data["message"] == "Entry already exists") {
            document.getElementById('editmessage').innerHTML = data["message"]
        } else if(data["message"] == "Entry added successfully") {
            if(entrytitle == ""){
                entrytitle = "..No Title.."
            }
            usermessage = "Your thought titled, '" + entrytitle + "' has been added"
            sessionStorage.setItem("usermessage", usermessage)
            window.location.href='/home'
        }
    })
    .catch((err) => console.log(err));
}

function errCatcher(data) {
    if(appStatus == 401) {
        window.location.href='/401'
    } else if(appStatus == 403) {
        window.location.href='/403'
    }
}

function editEntry() {
    let Token = sessionStorage.getItem("token");
    let entrytitle = document.getElementById("entryTitle").value;
    let entrydata = document.getElementById('entryText').value;
    let entry_ID = sessionStorage.getItem("entry_ID");
    fetch(baseurl + '/api/v1/entries/'+ entry_ID, {
        method:'PUT',
        headers: {
            'Authorization': 'Bearer ' + Token,
            'Accept': 'application/json',
            'Content-type':'application/json'
        },
        body:JSON.stringify({"entrytitle": entrytitle, "entrydata": entrydata})
    })
    // .then((res) => res.json())
    .then(function(res) {
        appStatus = res.status;
        return res.json();
    })
    .then(function (data) {
        errCatcher(data)
        if(data["message"] == "Null entry field") {
            document.getElementById('editmessage').innerHTML = "The entry cannot be left blank. Write a note to future you!";
        } else if(data["message"] == "Sorry, cannot edit entries made before today") {
            document.getElementById('editmessage').innerHTML = data["message"]
        } else if(data["message"] == "Entry edited") {
            usermessage = "Your thought, '" + entrytitle + "' has just been updated"
            sessionStorage.setItem("usermessage", usermessage)
            window.location.href='/home'
        }
    })
}

function del(entryID) {
    sessionStorage.setItem("entry_ID", entryID);
    deleteEntry();
}

function deleteEntry() {
    let Token = sessionStorage.getItem("token");
    let entry_ID = sessionStorage.getItem("entry_ID");
    fetch(baseurl + 'api/v1/entries/'+ entry_ID, {
        method:'DELETE',
        headers:{
            'Authorization': 'Bearer ' + Token,
            'Accept': 'application/json',
            'Content-type':'application/json'
        },
    })
    .then(function(res) {
        appStatus = res.status;
        return res.json();
    })
    .then(function (data) {
        errCatcher(data)
        sessionStorage.setItem("usermessage", data.message);
        window.location.href='/home';
    })
}
