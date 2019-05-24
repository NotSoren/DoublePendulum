# DoublePendulum
Renders something to do with the double pendulum experiment. X axis is the first pendulum's start position, Y axis is the second one. 

Installation:
Run 

`git clone https://github.com/NotSoren/DoublePendulum`

`cd DoublePendulum`

`sudo install.sh`

Then you can run the `imgGenMPv4.py` or `imgGenZoom.py` scripts as normal user. Please note that the first argument is the resolution to the map, the second argument is a multiplier for how long it will simulate before skipping that spot and moving on (defaults to 1 if not specified), and the third argument is the number of processing threads to use (defaults to `multiprocessing.cpu_count()*4` if not specified). arg 4 is optional. 0 gives no output, 1 outputs to the folder named outputs, and 2 outputs directly into the folder the program is run from. 

`imgGenMPv4.py` is an experimental modular version where we are continuing to try to reduce the use of numPy to allow use with pypy, speeding up the execution process. It currently DOES NOT fully eliminate numPy, but will probably just avoid using it for the `LR()` and `calcPix()` functions. In my testing, it is between 2 and 5 times faster than `imgGenMPv5.py` on cpython3.6, and several orders of magnitude faster when using pypy3.6.0. 

`imgGenMPv2.py` is an old and now deprecated revision. It has limited threading support and other features need some work. I recommend not using it. 

`imgGenMPv3.py` is another deprecated version. It's not pooled, and only processes one row at a time. 

tl;dr: use `imgGenMPv4.py dimension depth threads output` with pypy (recommended), or cpython3 (slower). If you want to zoom in, use imgGenZoom.py. You can choose the areas to zoom into at lines 132-135
