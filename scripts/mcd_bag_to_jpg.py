import os
import argparse

import cv2

import rosbag
from sensor_msgs.msg import Image
from cv_bridge import CvBridge

bag_file     = '/media/tmn/mySataSSD2/DATASETS/MCDVIRAL/PublishedSequences/ntu_day_01/ntu_day_01_d455b.bag'
output_dirs  = ['/media/tmn/mySataSSD2/DATASETS/MCDVIRAL/PublishedSequences/ntu_day_01/ntu_day_01_d455b/cam0/data',
                '/media/tmn/mySataSSD2/DATASETS/MCDVIRAL/PublishedSequences/ntu_day_01/ntu_day_01_d455b/cam1/data']
image_topics = ['/d455b/infra1/image_rect_raw', '/d455b/infra2/image_rect_raw']

for dir in output_dirs:
    os.makedirs(dir, exist_ok=True)

bridge = CvBridge()
bag = rosbag.Bag(bag_file, "r")

count_cam = [0, 0]

pair = []

for topic_, msg_, t_ in bag.read_messages(topics=image_topics):

    if len(pair) < 2:
        pair.append((topic_, msg_, t_))
    else:
        pair.clear()
        pair.append((topic_, msg_, t_))
        continue

    if len(pair) == 2:
        
        t0 = pair[0][1].header.stamp.to_sec()
        t1 = pair[1][1].header.stamp.to_sec()
        dt = abs(t0 - t1)

        print(t0, t1, dt)

        # Check if the last two images are pair
        if dt < 0.003:

            for topic, msg, t in pair:
            
                cv_img = bridge.imgmsg_to_cv2(msg, desired_encoding="passthrough")
                idx = image_topics.index(topic)
                cv2.imwrite(os.path.join(output_dirs[idx], "%06i.jpg" % count_cam[idx]), cv_img)
                print(f'Image {count_cam[idx]:6d} of topic {image_topics[idx]:s} written to {output_dirs[idx]:s}')
            
                count_cam[idx] += 1
        else:
            print("IMAGE PAIR NOT SYNCED!: ", t0, t1, dt)
            pair.pop(0)

bag.close()