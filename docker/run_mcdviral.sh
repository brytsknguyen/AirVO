# docker pull brytsknguyen/air_vo_noetic_focal:latest

DATA_PATH=${1:-/media/tmn/mySataSSD2/DATASETS/MCDVIRAL/Experiment/AirVO/ntu_day_01_d455b}
PKG_DIR=$(rospack find air_vo)

(rviz -d $PKG_DIR/launch/mcdviral.rviz)&
rvizpid=$!

docker run -it --rm --net=host --privileged --runtime nvidia --gpus all \
               --env DISPLAY=$DISPLAY \
               --volume /tmp/.X11-unix:/tmp/.X11-unix \
               --volume $PKG_DIR:$PKG_DIR \
               --volume $DATA_PATH:$DATA_PATH \
               --workdir $PKG_DIR/../.. \
               --name air_slam \
               brytsknguyen/air_vo_noetic_focal:latest \
               /bin/bash -c "catkin build; source devel/setup.bash; roslaunch air_vo run_mcdviral.launch"