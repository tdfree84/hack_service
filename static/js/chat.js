function move(room_name, up_or_down) {
    // Get move up or down
    var direction;
    if (up_or_down === 'up')
        direction = -1;
    else
        direction = 1;
    // Get the rooms as they appear on screen
    var rooms = document.getElementsByClassName("channel_container");   
    console.log(rooms);
    var new_pos; // Where the new spot will be
    var old_pos; // Where the old spot was
    var i;
    // Get where the chat room is now and assign it
    // to its new position
    for (i = 0; i < rooms.length; i++) {
        if ("channel_"+room_name === rooms[i].id) {
            new_pos = i + direction; // -1 for up, 1 for down
            old_pos = i;
            // Stay in bounds
            if (new_pos < 0)
                new_pos = 0;
            if (new_pos > rooms.length)
                new_pos = rooms.length;
        }
    }

    // Collect the current order to send to server
    var room_names = [];
    var j;
    for (j = 0; j < rooms.length; j++) {
        room_names.push(rooms[j].id.slice(8));
    }

    // Get the room in way of new one
    var temp = room_names[new_pos];
    // Place new room in new place
    room_names[new_pos] = room_names[old_pos];
    // Put vacated room in its new place
    room_names[old_pos] = temp;
    console.log(room_names);

    // Send request to leave room
    $.ajax({
            type: 'POST',
            url: '/updatechannelorder',
            dataType: "json",
            traditional: true,
            data: {
                'channels': JSON.stringify(room_names),
            },
            success: function(response) {
                window.location.href = '/';
            },
            error: function(response) {
                alert('did not update rooms');
            },
            });
}

function leave_room(room_name) {
    // Send request to leave room
    $.ajax({
            type: 'POST',
            data: {
                channel_name: room_name,
            },
            url: '/leavechannel',
            success: function(response) {
                window.location.href = '/';
            },
            error: function(response) {
                alert('did not leave room');
            },
            });

}

function new_channel() {
    document.getElementById("newroominput").disabled = true;
    var room_name = document.getElementById("newroominput").value;

    // Ensure we have data
    if (room_name === "")
        return;

    console.log(room_name);
    // Send request for new room
    $.ajax({
            type: 'POST',
            data: {
                channel_name: room_name,
            },
            url: '/newchannel',
            success: function(response) {
                document.getElementById("newroominput").value = '';
                document.getElementById("newroominput").disabled = false;
                window.location.href = '/';
            },
            error: function(response) {
                alert('did not create room');
            },
            });
}

function send_message(room_name) {
    var message = document.getElementById(room_name+"_input").value;

    // Ensure we have data
    if (message === "")
        return;

    // Send data to log in
    $.ajax({
            type: 'POST',
            data : {
                text: message,
                channel: room_name,
            },
            url: '/send',
            success: function(response) {
                document.getElementById(room_name+"_input").value = '';
                document.getElementById(room_name+"_text_box").value = response.text;
                var textarea = document.getElementById(room_name+"_text_box");
                textarea.scrollTop = textarea.scrollHeight;
            }, 
            error: function(response) {
                alert("Could not send message.");
            }
            });
}

async function get_messages() {
    var errors = 0;
    while (true) {
        let logged_in = true;
        console.log("getting...");

        // Get messages for logged in user
        $.ajax({
                type: 'GET',
                url: '/getmessages',
                success: function(response) {
                    // If the user is logged out, flag it for later
                    if (response.logged_in === false) {
                        logged_in = false;
                        console.log("saw user is logged out");
                    }
                    else {
                        // Set each chat room's messages as such received
                        for (var i = 0; i < response.channels.length; i++) {
                            document.getElementById(response.channels[i]+"_text_box").value = response[response.channels[i]];
                            var textarea = document.getElementById(response.channels[i]+"_text_box");
                            textarea.scrollTop = textarea.scrollHeight;
                        }
                        errors = 0;
                    }
                },
                error: function(response) {
                    errors = errors + 1;
                    console.log("not receiving from server.");
                }
                });
        await new Promise(r => setTimeout(r, 2000));
        console.log("errors: "+errors);
        // If logged out or server is not responding, stop the loop
        if ((logged_in === false) || (errors > 10)) {
            break; }
    }
}

