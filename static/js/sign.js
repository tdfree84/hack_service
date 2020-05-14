function give_me_flag() {
    // Send data to log in
    $.ajax({
            type: 'POST',
            url: '/flag_me',
            success: function(response) {
                alert(response);
            }
            });

}

function sign_in() {
    var user = document.getElementById("uname").value;
    var pass = document.getElementById("psw").value;

    // Ensure we have data
    if ((user === "") || (pass === "")) {
        alert("please fill user and pass fields");
        return;
    }

    // Send data to log in
    $.ajax({
            type: 'POST',
            data : {
                username: user,
                psw: pass
            },
            url: '/signin',
            success: function(response) {
                document.getElementById("uname").value = '';
                document.getElementById("psw").value = '';
                // reload
                window.location = '/';
            }, 
            error: function(response) {
                alert("Could not log in.");
                document.getElementById("psw").value = '';
            }
            });
}

function sign_out() {
    // Send data to log in
    $.ajax({
            type: 'POST',
            url: '/signout',
            success: function(response) {
                window.location.href = '/';
            }
            });
}

function register() {
    var user = document.getElementById("uname").value;
    var pass = document.getElementById("psw").value;

    // Ensure we have data
    if ((user === "") || (pass === "")) {
        alert("please fill user and pass fields");
        return;
    }

    // Send data to log in
    $.ajax({
            type: 'POST',
            url: '/register',
            data : {
                username: user,
                psw: pass
            },
            success: function(response) {
                alert("Registered! Now log in");
                document.getElementById("uname").value = user;
                document.getElementById("psw").value = '';
            },
            error: function(response) {
                alert("Could not register.");
                document.getElementById("uname").value = '';
                document.getElementById("psw").value = '';
            }
            });
}
