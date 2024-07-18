#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist, Pose
import math

class GoalControllerNode(Node):

    def _init_(self):
        super()._init_("goals_score")
        
        self.cmd_vel_pub_= self.create_publisher(Twist, '/turtle1/cmd_vel', 10)
        self.pose_sub_= self.create_subscription(Pose, '/turtle1/pose', self.pose_callback, 10)

        self.goal_pos= [[1.5, 8.5], [8.5, 8.5], [5.197, 5.197], [1.5, 1.5], [8.5, 1.5], [5.197, 5.197]]
        self.count= 0
        self.curr_goal = self.goal_pos[self.count]
        
        

    def pose_callback(self, pose:Pose):
        cmd=Twist()
        
        if self.count<6 :
            x=self.goal_pos[self.i][0]
            y=self.goal_pos[self.i][1]
        
            distance=math.sqrt((pose.x-x)*2 +(pose.y-y)*2)
            px= x-pose.x
            py= y-pose.y
            
            if distance<0.0001:
                self.get_logger().info(f"Reached goal_point :({x},{y})")
                self.count +=1
            else:
                cmd.linear.x= px*2
                cmd.linear.y= py*2
                
        elif self.pos ==6:
            self.get_logger().info("Task_2 DONE")
            cmd.linear.x= 0.0
            cmd.linear.y= 0.0
            
        self.cmd.vel_pub_.publish(cmd)
            
            
def main(args=None):
    rclpy.init(args=args)
    goals = GoalControllerNode()
    rclpy.spin(goals)
    rclpy.shutdown()

if __name__ == '_main_':
    main()