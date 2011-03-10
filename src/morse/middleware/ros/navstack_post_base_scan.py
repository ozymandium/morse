import roslib; roslib.load_manifest('roscpp'); roslib.load_manifest('rospy'); roslib.load_manifest('sensor_msgs'); roslib.load_manifest('rosgraph_msgs')  
import rospy
import time
import math
import std_msgs
from sensor_msgs.msg import LaserScan
from sensor_msgs.msg import PointCloud
from sensor_msgs.msg import PointCloud2

def init_extra_module(self, component_instance, function, mw_data):
    """ Setup the middleware connection with this data

    Prepare the middleware to handle the serialised data as necessary.
    """
    # Add the new method to the component
    component_instance.output_functions.append(function)
    if mw_data[1] == "post_2DLaserScan": 
        self._topics.append(rospy.Publisher("/base_scan", LaserScan))
    else:
        self._topics.append(rospy.Publisher("/base_scan", PointCloud))

#Note: posting 2D Laserscans is still experimental!
def post_2DLaserScan(self, component_instance):
        """ Publish the data on the rostopic
		"""
        laserHeader = std_msgs.msg.Header()
        laserHeader.stamp = rospy.Time.now()
        laserHeader.frame_id = '/base_laser_link'
        num_readings = component_instance.blender_obj['scan_window'] * component_instance.blender_obj['resolution']
        max_angle = component_instance.blender_obj['scan_window'] * ( math.pi / 360 )
        min_angle = max_angle * (-1)
        angle_incr = ((component_instance.blender_obj['scan_window'] / num_readings) * (math.pi / 180)) 
        laser_maxrange =  component_instance.blender_obj['laser_range']

        # Note: Scan time and laser frequency are chosen as standard values        
        laser_frequency = 40
        laserscan = LaserScan(header = laserHeader, angle_min = min_angle, angle_max = max_angle, angle_increment = angle_incr, time_increment = ((1 / laser_frequency) / (num_readings)), scan_time = 1.0, range_min = 0.3, range_max = laser_maxrange, ranges = component_instance.local_data['range_list'])
       
        for topic in self._topics: 
            message = laserscan
            # publish the message on the correct topic    
            if str(topic.name) == str("/base_scan"):
                topic.publish(laserscan)
                
#Note: posting 2D Laserscans is still experimental!
#WARNING: Posting 2D pointclouds does NOT work at the moment!!!
def post_2DPointCloud(self, component_instance):
        """ Publish the data on the rostopic
		"""
        pcHeader = std_msgs.msg.Header()
        pcHeader.stamp = rospy.Time.now()
        pcHeader.frame_id = '/base_laser_link'
        
        pointcloud = PointCloud(header = pcHeader, points = component_instance.local_data['point_list'])
        for topic in self._topics: 
            # publish the message on the correct topic    
            if str(topic.name) == str("/base_scan"):
                topic.publish(pointcloud)