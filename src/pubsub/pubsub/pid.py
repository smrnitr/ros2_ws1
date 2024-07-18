import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist, Pose
import math

class GoalControllerNode(Node):

    def _init_(self):
        super()._init_('goals')
        
        self.cmd_vel_pub = self.create_publisher(Twist, '/turtle1/cmd_vel', 10)
        self.pose_sub = self.create_subscription(Pose, '/turtle1/pose', self.pose_callback, 10)

        self.goal_pos= [[1.5, 8.5], [8.5, 8.5], [5.197, 5.197], [1.5, 1.5], [8.5, 1.5], [5.197, 5.197]]
        self.curr_goal_index = 0
        self.curr_goal = self.goal_pos[self.curr_goal_index]
        
        self.goal_reach = 0.1
        self.max_v = 1.0    #speed=v
        self.max_w = 1.0    #angular_speed=w(omega)
        
        #A pinch of PID
        #pv and pw are used as prop.constants
        self.pv = 0.5   
        self.pw = 1.0

        self.curr_pose = None

    def pose_callback(self, msg):
        self.curr_pose = msg
        print(self.curr_pose.x)
        self.move_to_goal()

    def move_to_goal(self):
        if self.curr_pose is None:
            return
        
        goal_x, goal_y = self.curr_goal
        curr_x, curr_y = self.curr_pose.x, self.curr_pose.y
        
        error_x = goal_x - curr_x
        error_y = goal_y - curr_y
        
        distance_to_goal = math.sqrt(error_x*2 + error_y*2)
        
        if distance_to_goal < self.goal_reach:
            self.curr_goal_index = (self.curr_goal_index + 1) % len(self.goal_pos)
            self.curr_goal = self.goal_pos[self.curr_goal_index]
            return
        
        linear_velocity = min(self.pv * distance_to_goal, self.max_v)
        
        angle_to_goal = math.atan2(error_y, error_x)
        angular_velocity = min(self.pw* (angle_to_goal - self.curr_pose.theta), self.max_w)
        
        cmd_vel = Twist()
        cmd_vel.linear.x = linear_velocity
        cmd_vel.angular.z = angular_velocity
        
        self.cmd_vel_pub.publish(cmd_vel)

def main(args=None):
    rclpy.init(args=args)
    goals = GoalControllerNode()
    rclpy.spin(goals)
    rclpy.shutdown()

if __name__ == '_main_':
    main()