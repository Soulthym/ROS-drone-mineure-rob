src="~/catkin_ws/devel/setup.bash"
function extrun {
	terminator -x bash -c "source $src; $1" &
}
killall roscore
rosnode kill -a 
source "$src"
cd ~/catkin_ws/src/projet_drone/scripts/
extrun "roscore"
sleep 5
extrun "rqt"
sleep 2
extrun "roslaunch cvg_sim_gazebo ardrone_testworld.launch"
sleep 2
extrun "roslaunch ardrone_tutorials keyboard_controller_only.launch"
sleep 2
