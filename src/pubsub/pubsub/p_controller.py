import rclpy
from rclpy.node import Node
from turtlesim.msg import Pose
from geometry_msgs.msg import Twist
from math import sqrt, pow, atan2

class TurtleControllerNode(Node):

    def __init__(self):
        super().__init__("p_controller")
        self.get_logger().info("node p_controller initialized")
        self.cmd_vel_publisher_ = self.create_publisher(Twist, "turtle1/cmd_vel", 10)
        self.pose_subscriber_ = self.create_subscription(Pose, "/turtle1/pose", self.pose_callback, 10)
        
        self.pose = None

        self.error=0.1
        self.Kp1=1.5
        self.Kp2=6.0
        self.goal_list= [[1.5,8.5],[8.5,8.5],[5.197,5.197],[1.5,1.5],[8.5,1.5],[5.197,5.197]]
        self.goal_variable=0
        
        self.goal=self.goal_list[self.goal_variable]
        
        
        self.get_logger().info("initialization complete")

    def pose_callback(self, msg):
        self.pose= msg
        self.pose.x = round(self.pose.x, 4)
        self.pose.y = round(self.pose.y, 4)
        self.pose.theta= round(self.pose.theta,4)
        self.get_logger().info(f"updated pose: x=" + str(self.pose.x) + "y=" + str(self.pose.y))
        self.p_controller_move()

            

    def p_controller_move(self):

        if self.pose is None:
            return
        
        
        goal_pose_x, goal_pose_y= self.goal
        distance=sqrt(pow(goal_pose_x-self.pose.x,2)+pow(goal_pose_y-self.pose.y,2))
        if distance < self.error:
            if self.goal_variable <=5:

               self.goal_variable= (self.goal_variable +1)
               self.goal=self.goal_list[self.goal_variable]
               return


        linear_vel=(self.Kp1)*distance
        angle_diff=atan2(goal_pose_y-self.pose.y,goal_pose_x-self.pose.x)
        angular_vel=(self.Kp2)*(angle_diff-self.pose.theta)

        cmd=Twist()
        cmd.linear.x=linear_vel
        cmd.angular.z=angular_vel
              
        self.get_logger().info(f"publishing velocity: x={cmd.linear.x}, z={cmd.angular.z}")
        self.cmd_vel_publisher_.publish(cmd)
           

    
def main(args=None):
    rclpy.init(args=args)
    node = TurtleControllerNode()
    node.get_logger().info("node initialized in main")
    rclpy.spin(node)   
    rclpy.shutdown()
    node.get_logger().info("node shutdown")


if __name__ == '__main__':
    main()
            
        
 