# DoublePendulum
Renders something to do with the double pendulum experiment... Spudzee is more of an expert on it than me. I just made it speedy and sexy. 

Installation:
Run 

git clone https://github.com/NotSoren/DoublePendulum 

cd DoublePendulum

sudo install.sh

Then you can run the imgGenMPv2.py or imgGenMPZoom.py scripts as normal user. Please note that the first argument is the resolution to the map, the second argument is a multiplier for how long it will simulate before skipping that spot and moving on (defaults to 1 if not specified), and the third argument is the number of processing threads to use (defaults to multiprocessing.cpu_count()*2 if not specified). 
