'''In this exercise you need to implement inverse kinematics for NAO's legs

* Tasks:
    1. solve inverse kinematics for NAO's legs by using analytical or numerical method.
       You may need documentation of NAO's leg:
       http://doc.aldebaran.com/2-1/family/nao_h21/joints_h21.html
       http://doc.aldebaran.com/2-1/family/nao_h21/links_h21.html
    2. use the results of inverse kinematics to control NAO's legs (in InverseKinematicsAgent.set_transforms)
       and test your inverse kinematics implementation.
'''


from forward_kinematics import ForwardKinematicsAgent
from numpy.matlib import identity, matrix, linalg
from math import atan2
from scipy.linalg import pinv
import numpy as np


class InverseKinematicsAgent(ForwardKinematicsAgent):
    def inverse_kinematics(self, effector_name, transform):
        '''solve the inverse kinematics

        :param str effector_name: name of end effector, e.g. LLeg, RLeg
        :param transform: 4x4 transform matrix
        :return: list of joint angles
        '''
        def make_work(t):
                return [t[-1, 0],  t[-1, 1],  t[-1, 2],  atan2(t[2, 1], t[2, 2]) ]


        #not the best but works
        lambda_ = 0.1
        max_iter = 500
        errorMargin = 1e-3
        max_step = 1

        # get all joints

        # joint_angles = {joint : 0 for joint in self.joint_names}
        # joint_angles.update( {j : self.perception.joint[j] for j in self.chains[effector_name]})
        joint_angles = {j : self.perception.joint[j] for j in self.chains[effector_name]}
        for joint in self.joint_names:
            if joint not in joint_angles:
                joint_angles[joint] = 0


        destination = make_work(transform)


        # main loop
        for i in range(max_iter):
            self.forward_kinematics(joint_angles)

            # get new values
            transformValues = [x for x in self.transforms.values()]
            transformMatrix = matrix([make_work(transformValues[-1])]).T

            # get error and fuzz
            error = destination - transformMatrix
            ind = error > max_step
            error[ind] = max_step
            ind = error < -max_step
            error[ind] = -max_step

            # break if we in very close
            if linalg.norm(error) < errorMargin:
                break

            # jacobian

            tMatrix = matrix([make_work(i) for i in transformValues[:-1]]).T
            ja = transformMatrix - tMatrix
            diff = transformMatrix - tMatrix

            # orientation fix
            for i in range(3):
                ja[i, :] = diff[2-i, :]

            ja[-1, :] = 1

            # solve
            theta = lambda_ * pinv(ja).dot(error)
            for i, j in enumerate(self.chains[effector_name]):
                joint_angles[j] += np.asarray(theta.T)[0][i]




        return [v for v in joint_angles.values()]



    def set_transforms(self, effector_name, transform):
        '''solve the inverse kinematics and control joints use the results
        '''
        # YOUR CODE HERE
        j_angles = self.inverse_kinematics(effector_name, transform)
        n = self.chains[effector_name]

        keys = [ [
                    [self.perception.joint[name], [3, 0, 0], [3, 0, 0]],
                    [j_angles[i], [3, 0, 0], [3, 0, 0]],
                ] for i, name in enumerate(n)
                ]


        time = [[2.0, 6.0]] * len(n)
        self.keyframes = (n, time, keys)  # the result joint angles have to fill in
        print(self.keyframes)


if __name__ == '__main__':
    agent = InverseKinematicsAgent()
    # test inverse kinematics
    T = identity(4)
    T[-1, 1] = 0.05
    T[-1, 2] = -0.26
    agent.set_transforms('LLeg', T)
    agent.run()
