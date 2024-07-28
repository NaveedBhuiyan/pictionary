from flask import Flask, render_template, request, redirect, url_for, session
from flask_socketio import SocketIO, emit

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
ROOM_PASSWORD = 'lalaland'
socketio = SocketIO(app)


@app.route('/', methods=['GET', 'POST'])
def home():
    session.clear()
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

@socketio.on('draw')
def handle_draw(data):
    emit('draw', data, broadcast=True)

@socketio.on('chat')
def handle_chat(message):
    emit('chat', message, broadcast=True)

if __name__ == '__main__':
    # Start the server using socketio.run()
    socketio.run(app, host="0.0.0.0", debug=True, port=8001)
