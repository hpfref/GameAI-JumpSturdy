# GameAI-JumpSturdy
Devoloping a symbolic AI for the 2-Player board game "Jump Sturdy".   
The game: https://www.mindsports.nl/index.php/the-pit/576-jump-sturdy

How to connect our AI to the gameserver:  
-run ./gameserver/client.py

How to simulate a game of our AI against itself on the gameserver:  
-run ./scripts/play_locally.py

How to visually simulate a whole game or position of our AI against itself:  
-set fen of game position in visuals.py  
-run ./scripts/visuals.py

How to visualize a game log:  
-move log into ./scripts/contest_logs  
-change reference in simulate_logs.py  
-run ./scripts/simulate_logs.py
