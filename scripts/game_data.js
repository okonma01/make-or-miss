// establish a websocket connection to the Flask app
var socket = io.connect('http://localhost:8000');

// listen for the 'game_data' event
socket.on('game_data', function (game_data) {
    // update the Jinja variables in the HTML template with the game data
    document.getElementById('team1_name').innerHTML = game_data.team1_name;
    document.getElementById('team1_score').innerHTML = game_data.team1_score;

    document.getElementById('team2_name').innerHTML = game_data.team2_name;
    document.getElementById('team2_score').innerHTML = game_data.team2_score;

    document.getElementById('time_remaining').innerHTML = game_data.time_remaining;
});