# Birdie Quest

Birdie Quest is an interactive Flappy Bird-inspired game that utilizes face tracking for gameplay. The player's nose position is tracked via a webcam, allowing them to control the bird's height using head movements. The game is built using **Pygame**, **OpenCV**, and **MediaPipe**.

## Features

- **Face Tracking Controls**: Move your head up and down to control the bird.
- **Classic Flappy Bird Mechanics**: Navigate through obstacles to achieve a high score.
- **Dynamic Background and Sprites**: Smooth animations for an immersive experience.
- **Sound Effects and Background Music**: Engaging audio experience.
- **Score Tracking**: Saves high scores for competition.

## Installation

### Prerequisites

Ensure you have Python installed (>=3.7). Then, install the required dependencies:

```sh
pip install pygame opencv-python mediapipe
```

### Running the Game

1. Clone this repository:
   ```sh
   git clone https://github.com/your-repo/birdie-quest.git
   cd birdie-quest
   ```
2. Run the game:
   ```sh
   python main.py
   ```

### Alternative: Download the Executable

If you don't want to install Python and dependencies, you can download the executable from the [Releases](https://github.com/riandrei/birdie-quest/releases/tag/v1.0) page on our GitHub.

## Controls

- Move your **head up/down** to control the bird’s height.
- Press **Escape (ESC)** to exit.
- Use the **menu options** to restart or view scores.

## File Structure

```
📂 birdie-quest
├── 📂 assets           # Game assets (images, sounds)
├── 📂 objects          # Game object classes (Bird, Floor, Obstacle, etc.)
├── main.py            # Main game loop and logic
├── configs.py         # Game configuration settings
└── README.md          # This file
```

## License

This project is open-source under the MIT License.

Enjoy playing Birdie Quest! 🚀
