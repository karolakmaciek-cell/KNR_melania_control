#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from rclpy.action import ActionServer
from control_msgs.action import FollowJointTrajectory
from trajectory_msgs.msg import JointTrajectory
from trajectory_msgs.msg import JointTrajectoryPoint



class TrajectoryServer(Node):

    def __init__(self):
        super().__init__('trajectory_server')


        self._action_server = ActionServer(self, FollowJointTrajectory, '/JointTrajectory', self.execute_callback)

    def execute_callback(self, goal_handle):
        self.get_logger().info('Executing goal...')
        trajectory = goal_handle.request.trajectory
        for idx, point in enumerate(trajectory.points):
            self.get_logger().info(f'Pozycja punktu {idx} to {str(point.positions)}')
            self.get_logger().info(f'Czas uruchomienia od startu punktu {idx} to {str(point.time_from_start.sec)}')
        goal_handle.succeed()
        result = FollowJointTrajectory.Result()
        return result




def main(args=None):
    rclpy.init(args=args)
    node = TrajectoryServer()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()