'''In this file you need to implement remote procedure call (RPC) client

* The agent_server.py has to be implemented first (at least one function is implemented and exported)
* Please implement functions in ClientAgent first, which should request remote call directly
* The PostHandler can be implement in the last step, it provides non-blocking functions, e.g. agent.post.execute_keyframes
 * Hints: [threading](https://docs.python.org/2/library/threading.html) may be needed for monitoring if the task is done
'''

import weakref
import threading
import xmlrpc.client
from keyframes import hello

import weakref
import threading
import xmlrpc.client
from keyframes import hello

class PostHandler(object):
    '''The post handler wraps functions to be executed in parallel'''
    def __init__(self, obj):
        self.proxy = weakref.proxy(obj)

    def execute_keyframes(self, keyframes):
        '''Non-blocking call of ClientAgent.execute_keyframes'''
        threading.Thread(target=self.proxy.execute_keyframes, args=(keyframes,)).start()

    def set_transform(self, effector_name, transform):
        '''Non-blocking call of ClientAgent.set_transform'''
        threading.Thread(target=self.proxy.set_transform, args=(effector_name, transform)).start()

class ClientAgent(object):
    '''ClientAgent requests RPC service from remote server'''

    def __init__(self):
        self.post = PostHandler(self)
        self.server = xmlrpc.client.ServerProxy("http://localhost:9999/")

    def get_angle(self, joint_name):
        try:
            return self.server.get_angle(joint_name)
        except Exception as e:
            print("Error in get_angle:", e)
            return False

    def set_angle(self, joint_name, angle):
        try:
            return self.server.set_angle(joint_name, angle)
        except Exception as e:
            print("Error in set_angle:", e)
            return False

    def get_posture(self):
        try:
            return self.server.get_posture()
        except Exception as e:
            print("Error in get_posture:", e)
            return False

    def execute_keyframes(self, keyframes):
        try:
            return self.server.execute_keyframes(keyframes)
        except Exception as e:
            print("Error in execute_keyframes:", e)
            return False

    def get_transform(self, name):
        try:
            return self.server.get_transform(name)
        except Exception as e:
            print("Error in get_transform:", e)
            return False

    def set_transform(self, effector_name, transform):
        try:
            return self.server.set_transform(effector_name, transform)
        except Exception as e:
            print("Error in set_transform:", e)
            return False

    def attempt(self, func, *args):
        exe_str = "global res; res = self.server." + func.__name__ + "("
        for i in args:
            exe_str += "'" + str(i) + "'," if isinstance(i, str) else str(i) + ","
        exe_str = exe_str.rstrip(',') + ")"

        try:
            exec(exe_str)
            global res
            return res
        except Exception as e:
            print("Error in attempt:", exe_str, ":", e)
            return False

if __name__ == '__main__':
    agent = ClientAgent()
    # TEST CODE HERE
    print(agent.get_angle("HeadYaw"))
    print(agent.get_posture())
    print(agent.get_transform("HeadYaw"))
    keyframes = hello()
    a = agent.execute_keyframes(keyframes)
    print(a)
    a = agent.execute_keyframes(keyframes)
    print(a)


