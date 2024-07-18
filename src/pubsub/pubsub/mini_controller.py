import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from nav_msgs.msg import Odometry
from time import*
import math
from tf_transformations import euler_from_quaternion #you will require this to get theta since odom data gives orientation in quternion form but you need the orientation in euler form, research more to get idea

class Task2BController(Node):

   def __init__(self):
        super().__init__('task2b_controller')

        # Initialze Publisher and Subscriber
        # We'll leave this for you to figure out the syntax for
        # initialising publisher and subscriber of cmd_vel and odom respectively
        self.cmd_vel_publisher_ = self.create_publisher(Twist, "cmd_vel", 10)
        self.odom_subscriber_ = self.create_subscription(Odometry, "odom", self.odom_callback, 10)

        # Declare a Twist message
        self.vel = Twist()
        # Initialise the required variables to 0

        # For maintaining control loop rate.
        self.rate = self.create_rate(100)
        # Initialise variables that may be needed for the control loop
        # For ex: x_d, y_d, theta_d (in **meters** and **radians**) for defining desired goal-pose.
        # and also Kp values for the P Controller
        self.time_period=0.1
        #self.timer=self.create_timer(self.time_period,self.timer_callback)
        self.Kp1=1.5
        self.Kp2=4.0
        self.init_pose=None
        self.init_y=None
        self.cmd = 'forward'
        self.curr_pose=None
        self.curr_y=None
        self.count=0
        self.side_length = 2.0 
        self.distance=0.0
        self.y_turned=0.0

   

   def odom_callback(self,cmd):
       self.curr_pose=cmd.pose.pose.position
       rotate=cmd.pose.pose.orientation
       _,_,self.curr_y=self.euler_from_quaternion(rotate)

       if self.init_pose is None:
            self.init_pose = self.curr_pose
            self.init_y = self.curr_y

       if self.cmd == 'forward':
            self.distance=math.sqrt(pow(self.curr_pose.x-self.init_pose.x,2)+pow(self.curr_pose.y-self.init_pose.y,2))

       elif self.cmd == 'turn':
            self.y_turned = abs(self.curr_y - self.init_y)

   def run(self):
       while rclpy.ok():
           rclpy.spin_once(self)
           cmd = Twist()
           if self.cmd == 'forward':
               self.dist_error = self.side_length - self.distance
               if self.dist_error > 0:
                    cmd.linear.x = self.Kp1* self.dist_error
               else:
                    self.cmd = 'turn'
                    self.init_y= self.curr_y
                    self.init_pose = self.curr_pose
                    cmd.linear.x = 0.0
               
           elif self.cmd == 'turn':
                self.y_error = (math.pi / 2) - self.y_turned
                if self.y_error > 0:
                    cmd.angular.z = self.Kp2* self.y_error
                else:
                    self.cmd = 'forward'
                    self.count += 1
                    self.init_pose = self.curr_pose
                    self.init_y= self.curr_y
                    cmd.angular.z = 0.0
           if self.count == 4:
                cmd.linear.x = 0.0
                cmd.angular.z = 0.0
                self.pub_.publish(cmd)
                self.get_logger().info('Square path completed.')
                break

           self.pub_.publish(cmd)

   def euler_from_quaternion(rotate):
        """
        Convert quaternion to Euler angles.
        """
        x = rotate.x
        y = rotate.y
        z = rotate.z
        w = rotate.w

        t0 = +2.0 * (w * x + y * z)
        t1 = +1.0 - 2.0 * (x * x + y * y)
        roll_x = math.atan2(t0, t1)

        t2 = +2.0 * (w * y - z * x)
        t2 = +1.0 if t2 > +1.0 else t2
        t2 = -1.0 if t2 < -1.0 else t2
        pitch_y = math.asin(t2)

        t3 = +2.0 * (w * z + x * y)
        t4 = +1.0 - 2.0 * (y * y + z * z)
        yaw_z = math.atan2(t3, t4)

        return roll_x, pitch_y, yaw_z

def main(args=None):
    rclpy.init(args=args)

    # Create an instance of the EbotController class
    mini_controller = Task2BController()
    mini_controller.run()

    # Send an initial request with the index from ebot_controller.index
    #mini_controller.send_request(mini_controller.index)
    '''
    # Main loop
    while rclpy.ok():

        # Check if the service call is done
        if : ##provide an if logic for iterating the number of indexes required to traverse
            
            #########           GOAL POSE             #########
            ##write the logic to assign goal pose
            x_goal      = 
            y_goal      = 
            theta_goal  = 
            ####################################################

            # Find error (in x, y and theta) in global frame
            # the /odom topic is giving pose of the robot in global frame
            # the desired pose is declared above and defined by you in global frame
            # therefore calculate error in global frame

            # (Calculate error in body frame)
            # But for Controller outputs robot velocity in robot_body frame, 
            # i.e. velocity are define is in x, y of the robot frame, 
            # Notice: the direction of z axis says the same in global and body frame
            # therefore the errors will have have to be calculated in body frame.
            # 
            # This is probably the crux of Task 2, figure this out and rest should be fine.

            # Finally implement a P controller 
            # to react to the error with velocities in x, y and theta.

            # Safety Check
            # make sure the velocities are within a range.
            # for now since we are in a simulator and we are not dealing with actual physical limits on the system 
            # we may get away with skipping this step. But it will be very necessary in the long run.


            #If Condition is up to you
            
            mini_controller.index += 1


        # Spin once to process callbacks
        rclpy.spin_once(mini_controller)
         '''
    # Destroy the node and shut down ROS
    mini_controller.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()