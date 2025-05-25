'''In this file you need to implement remote procedure call (RPC) server

* There are different RPC libraries for python, such as xmlrpclib, json-rpc. You are free to choose.
* The following functions have to be implemented and exported:
 * get_angle
 * set_angle
 * get_posture
 * execute_keyframes
 * get_transform
 * set_transform
* You can test RPC server with ipython before implementing agent_client.py
'''

# add PYTHONPATH
import os
import sys
sys.path.append(os.path.join(os.path.abspath(os.path.dirname(__file__)), '..', 'kinematics'))
import json as json
from threading import Thread

from inverse_kinematics import InverseKinematicsAgent
from xmlrpc.server import SimpleXMLRPCServer

class ServerAgent(InverseKinematicsAgent):
    '''ServerAgent provides RPC service'''

    def __init__(self):
        super(ServerAgent, self).__init__()
        self.server = SimpleXMLRPCServer(("localhost", 9999), allow_none=True, logRequests=False)

        methods = [
            "get_angle",
            "set_angle",
            "get_posture",
            "execute_keyframes",
            "get_transform",
            "set_transform"
        ]
        for method in methods:
            self.server.register_function(getattr(self, method), method)

        thread = Thread(target=self.server.serve_forever)
        thread.daemon = True
        thread.start()
        print("Started RPC ServerAgent on http://localhost:9999")

    def get_angle(self, joint_name):
        print(f"[RPC] get_angle({joint_name})")
        return self.perception.joint[joint_name]

    def set_angle(self, joint_name, angle):
        print(f"[RPC] set_angle({joint_name}, {angle})")
        self.target_joints[joint_name] = angle
        return True

    def get_posture(self):
        print("[RPC] get_posture()")
        return self.posture

    def execute_keyframes(self, keyframes):
        print("[RPC] execute_keyframes(...)")
        self.start_time = None
        self.keyframes = keyframes
        return True

    def get_transform(self, name):
        print(f"[RPC] get_transform({name})")
        return json.dumps(self.transforms[name].tolist())

    def set_transform(self, effector_name, transform):
        print(f"[RPC] set_transform({effector_name}, transform)")
        self.target_joints = self.inverse_kinematics(effector_name, json.loads(transform))
        return True
    
    
if __name__ == '__main__':
    agent = ServerAgent()
    agent.run()

