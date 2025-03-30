import sys
if sys.prefix == '/usr':
    sys.real_prefix = sys.prefix
    sys.prefix = sys.exec_prefix = '/home/tori/ros2_ws/src/check_goal_dist/install/check_goal_proximity'
