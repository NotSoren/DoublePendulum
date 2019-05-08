# DoublePendulum
Renders something to do with the double pendulum experiment. X axis is the first pendulum's start position, Y axis is the second one. 

Installation:
Run 

`git clone https://github.com/NotSoren/DoublePendulum`

`cd DoublePendulum`

`sudo install.sh`

Then you can run the `imgGenMPv3.py` or `imgGenZoom.py` scripts as normal user. Please note that the first argument is the resolution to the map, the second argument is a multiplier for how long it will simulate before skipping that spot and moving on (defaults to 1 if not specified), and the third argument is the number of processing threads to use (defaults to `multiprocessing.cpu_count()*2` if not specified). 

`imgGenMPv4.py` is an experimental modular version where we are continuing to try to reduce the use of numPy to allow use with pypy, speeding up the execution process. It currently DOES NOT fully eliminate numPy, nor will it in all likelihood. It will probably just avoid using it for the `LR()` and `calcPix()` functions. 

`imgGenMPv2.py` is an old and now deprecated revision. It has limited threading support and other features need some work. I recommend not using it. 
