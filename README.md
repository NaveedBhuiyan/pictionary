# Pictionary Game

Welcome to the Pictionary Game! This is a real-time multiplayer game where players can draw and guess words. One player is selected as the "drawer" and draws a word on a canvas while the other players guess the word in a chat box.

## Features

- Real-time drawing and guessing
- User-friendly chat interface
- List of connected users
- Secret word for the drawer only
- Automatic recognition of the correct guess

## Technologies Used

- Flask: Backend web framework
- Flask-SocketIO: For real-time communication
- HTML, CSS, and JavaScript: Frontend development
- Socket.IO: Enables real-time bidirectional communication

## Prerequisites

- Python 3.x
- Flask
- Flask-SocketIO

## Getting Started

Follow these instructions to get a copy of the project up and running on your local machine.

### Installation

1. **Clone the repository:**

    ```bash
    git clone https://github.com/yourusername/pictionary-game.git
    cd pictionary-game
    ```

2. **Set up a virtual environment (recommended):**

    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```

3. **Install the required packages:**

    ```bash
    pip install -r requirements.txt
    ```

### Running the Application

1. **Start the Flask server:**

    ```bash
    python app.py
    ```

2. **Access the game:**

   Open a web browser and go to `http://0.0.0.0:8001`.

### How to Play

- **Starting the Game:**
  - Click on the "Start Game" button to begin.
  
- **Drawing:**
  - The designated drawer can draw on the canvas using the mouse.

- **Guessing:**
  - Players type their guesses into the chat box. If a player guesses the correct word, the game announces it in the chat.

## File Structure

- `app.py`: Main application file containing server logic.
- `templates/index.html`: Main HTML file for the game interface.
- `static/style.css`: Styles for the game interface.
- `requirements.txt`: List of Python packages required.

## Customization

- **Word List:**
  - You can customize the list of words by modifying the `WORDS` list in `app.py`.

## Contributions

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgements

- This game was developed using tutorials and resources from the Flask and Socket.IO communities.
