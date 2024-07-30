from flask import Flask, render_template, request, redirect, url_for, session
from flask_socketio import SocketIO, emit
import time

#TODO
# display username at frontend
# write algorithm for guess box
# scoring system based on time
# display timer
# generate words


app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
ROOM_PASSWORD = 'lalaland'
socketio = SocketIO(app)

# List to keep track of connected users
connected_users = []
current_drawer_index = 0  # Index to track which user is drawing
game_started = False  # Flag to check if the game has started


@app.route('/', methods=['GET', 'POST'])
def home():
    session.clear()  # Clear the session to ask for credentials each time
    error = None  # Initialize the error variable

    if request.method == 'POST':
        # Get the username and password from the form
        username = request.form.get('username')
        entered_password = request.form.get('password')

        if entered_password == ROOM_PASSWORD:
            # Password is correct, store the username in the session
            session['username'] = username
            # Redirect to the index page
            return redirect(url_for('index'))
        else:
            # Password is incorrect, set an error message
            error = 'Invalid password, please try again.'

    # Render the password page with an error message if applicable
    return render_template('password.html', error=error)


@app.route('/index')
def index():
    username = session.get('username', 'Guest')  # Retrieve the username from the session
    return render_template('index.html', username=username)


@socketio.on('new_user')
def handle_new_user(username):
    if username not in connected_users:
        connected_users.append(username)
    emit('user_list', connected_users, broadcast=True)


@socketio.on('disconnect_user')
def handle_disconnect_user(username):
    if username in connected_users:
        connected_users.remove(username)
    emit('user_list', connected_users, broadcast=True)


@socketio.on('disconnect')
def handle_disconnect():
    username = session.get('username', 'Guest')
    handle_disconnect_user(username)


@socketio.on('start_game')
def handle_start_game():
    global game_started
    if not game_started and connected_users:
        game_started = True
        start_game_turns()


"""
def start_game_turns():
    global current_drawer_index, game_started
    for i in range(10):
        current_drawer_index %= len(connected_users)
        current_drawer = connected_users[current_drawer_index]
        print(f"Current drawer: {current_drawer}")  # Debug line
        #socketio.emit('turn', {'currentDrawer': current_drawer, 'timer': i}, to='/')
        emit('turn', current_drawer, broadcast=True)
        current_drawer_index += 1
        socketio.sleep(1)
"""

def start_game_turns():
    global current_drawer_index, game_started
    while game_started:
        current_drawer_index %= len(connected_users)
        current_drawer = connected_users[current_drawer_index]
        print(f"Current drawer: {current_drawer}")  # Debug line
        # Additional data you want to send
        # Countdown loop
        for countdown in range(10):
            emit('turn', {'currentDrawer': current_drawer, 'countdown': countdown}, broadcast=True)
            #time.sleep(1)  # Wait for 1 second
            socketio.sleep(1)
        # Emit the turn event with multiple pieces of data
        #emit('turn', {'currentDrawer': current_drawer, 'countdown': countdown_time}, broadcast=True)
        current_drawer_index += 1

            #socketio.sleep(10)

@socketio.on('draw')
def handle_draw(data):
    emit('draw', data, broadcast=True)


@socketio.on('chat')
def handle_chat(data):
    # Emit the chat message along with the username
    emit('chat', data, broadcast=True)


if __name__ == '__main__':
    # Start the server using socketio.run()
    socketio.run(app, host="0.0.0.0", debug=True, port=8001)
