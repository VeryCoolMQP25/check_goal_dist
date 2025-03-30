import rclpy
from rclpy.node import Node
from geometry_msgs.msg import PoseStamped
from std_msgs.msg import Int32  # Import the message type to publish

class checkGoal(Node):
    def __init__(self):
        super().__init__('goal_pose_filter_node')

        # Default current & requested floor to 1

        self.current_pose = PoseStamped()
        self.goal_pose = PoseStamped()
        self.goal_reached = Int32()

        #  subscription for the current_pose

        self.floor_subscription = self.create_subscription(
            PoseStamped,  # current_floor is of type Int32
            '/amcl_pose',
            self.update_curr_pose,
            10
        )

        #  subscription for the goal_pose

        self.floor_subscription = self.create_subscription(
            PoseStamped,  # current_floor is of type Int32
            '/goal_pose',
            self.update_goal_pose,
            10
        )

        
        #  publisher for close to goal pose
        self.publisher = self.create_publisher(Int32, '/check_goal_proximity', 10)

    def update_curr_pose(self, msg):
        self.get_logger().info('Received curr pose: %s' % str(msg))
        self.current_pose = msg

        curr_pose_x = abs(self.current_pose.pose.position.x)
        curr_pose_y = abs(self.current_pose.pose.position.y)
        goal_pose_x = abs(self.goal_pose.pose.position.x)
        goal_pose_y = abs(self.goal_pose.pose.position.y)

        # If goal is close publish close to goal is true
        if abs(curr_pose_x - goal_pose_x) < 1 and abs(curr_pose_y - goal_pose_y) < 1: 
            self.get_logger().info("Close to goal!")
            self.goal_reached.data = 1
            self.publisher.publish(self.goal_reached)

    def update_goal_pose(self, msg):
        self.get_logger().info('Received goal pose: %s' % str(msg))
        self.goal_pose = msg


def main(args=None):
    rclpy.init(args=args)
    node = checkGoal()
    rclpy.spin(node)
    rclpy.shutdown()

if __name__ == '__main__':
    main()
