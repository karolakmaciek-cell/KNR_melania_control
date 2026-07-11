#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from rclpy.action import ActionClient
from control_msgs.action import FollowJointTrajectory
from trajectory_msgs.msg import JointTrajectory
from trajectory_msgs.msg import JointTrajectoryPoint



class MelaniaMover(Node):

    def __init__(self):
        super().__init__('melania_mover')


        self._action_client = ActionClient(self, FollowJointTrajectory, '/joint_trajectory_controller/follow_joint_trajectory')


        goal_msg = FollowJointTrajectory.Goal()

        goal_msg.trajectory.joint_names = ['RTz', 'RTx', 'RTy', 'RSy', 'RFy', 'RFx', 'LTz', 'LTx', 'LTy', 'LSy', 'LFy', 'LFx', 'RAy', 'RAx', 'LAy', 'LAx']

        #najwazniejsza czesc czyli dajemy trajectory dla naszego wezla
        points = [[0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
                  [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -1.5708, -1.5708],
                  [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0 , 0.0, 0.0],
                  [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -1.5708, -1.5708],
                  [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]]
        
        time = [10,13,16,19,22]

        for i in range(len(points)):
            point = JointTrajectoryPoint()
            point.positions = points[i]
            point.time_from_start.sec = time[i]
            goal_msg.trajectory.points.append(point)

        
        if not self._action_client.wait_for_server(timeout_sec=2.0):
            self.get_logger().error('Nie znaleziono Action serwera')
            return
        
        self._send_goal_future = self._action_client.send_goal_async(goal_msg, feedback_callback=self.feedback_callback)
        self._send_goal_future.add_done_callback(self.goal_response_callback)
        
    def goal_response_callback(self, future):
        goal_handle = future.result()
        if not goal_handle.accepted:
            self.get_logger().warning('Cel odrzucony')
            return

        self.get_logger().info('Cel zaakceptowany')
        self._get_result_future = goal_handle.get_result_async()
        self._get_result_future.add_done_callback(self.get_result_callback) #info o zakonczeniu ruchu

    def get_result_callback(self, future): #co sie stanie jak ruch sie zakoncy na razie pomijamy opcje z result
        result = future.result().result
        self.get_logger().info(f'Ruch zakonczony')

    def feedback_callback(self, feedback_msg): #opcjonalnie jakbysmy chcieli raportowac proces ale nie jest to obowiazkowe
        pass

def main(args=None):
    rclpy.init(args=args)
    node = MelaniaMover()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
