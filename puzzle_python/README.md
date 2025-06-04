## Game Overview

Attack15 is a puzzle game where:
• Players select panels with numbers 1-9 to make a sum of exactly 15
• Each panel resets after 15 seconds
• The game lasts for 1 minute

## Features

1. Main Menu:
   • Start button to begin the game
   • Exit button to quit the application

2. Game Mechanics:
   • 9 panels arranged in a 3x3 grid with random numbers (1-9)
   • Click panels to select/deselect them
   • When selected panels sum to 15, they're replaced with new random numbers
   • Each panel has a 15-second timer before resetting

3. Scoring System:
   • +15 points when panels summing to 15 are cleared
   • -10 points when a panel expires and resets

4. Visual Elements:
   • Color-coded panels (blue when selected)
   • Timer bar under each panel showing remaining time
   • Score and time display
   • Sum of currently selected panels

## How to Run the Game

1. Make sure you have the required dependencies:
  
   pip install -r requirements.txt
   

2. Run the game:
  
   python attack15.py
   

## Game Controls
• Click on panels to select/deselect them
• Try to find combinations that add up to 15
• Click "Back" to return to the main menu
