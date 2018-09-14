# Readme for Table Tennis Tournament Manager

This is a unix-style program that allows for the recording of rankings in multiple table tennis leagues.

# Technologies Used
- Python
- HTML

# Features:
- Ability to create and remove leaderboards.
- Ability to alter leaderboards based on match results.
- Generate HTML file of all leaderboards.

# Installation

1) Install Python 2.7

# Usage

In terminal, cd to the directory of this project.

## Commands

```
python main.py <option> <arguments>
```

##Arguments:
```
    --help          View the help.
    --add_player    Add a player to the players table.
    --rm_player     Remove a player from the current leaderboard.
    --rm_player_all Remove a specified player from all leaderboards and players table.
    --add_board     Create a new leaderboard.
    --rm_board
    --change        Select another leaderboard.
    --result        Record the result of a match on the current leaderboard.
    --rank          View the current leaderboard.
```