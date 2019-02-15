# TowerGame


Tower-Defense Game in Python


Tower-Defense Game made in Python 3.6 and pygame 1.9.3., for a course at university.

Select towers with left click in the menu on the right and set them with left click on a foundation. 
Some towers boost other towers range or attack power. Boost with right click. 

Sounds made with sfxr.



main.py : main loop, input handling and gamestate management(Intro, Run, Restart, Pause), run to start game
update.py : game logic
model.py : data-types and asset loading
tower.py : more data-types
towerscript.py : builds towerData.py
towerData.py : game-related data, e.g. range and attack-power of towers

Run:
Go to /src,
python towerscript.py               to build towerData 
python main.py                      to run


![Alt text](game1.gif?raw=true)
