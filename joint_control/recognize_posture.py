'''In this exercise you need to use the learned classifier to recognize current posture of robot

* Tasks:
    1. load learned classifier in `PostureRecognitionAgent.__init__`
    2. recognize current posture in `PostureRecognitionAgent.recognize_posture`

* Hints:
    Let the robot execute different keyframes, and recognize these postures.

'''


from angle_interpolation import AngleInterpolationAgent
from keyframes import *
import pickle # for loading Robot Pose 
INVERSED_JOINTS = ['LHipYawPitch', 'LHipRoll', 'LHipPitch', 'LKneePitch', 'RHipYawPitch', 'RHipRoll', 'RHipPitch', 'RKneePitch']

class PostureRecognitionAgent(AngleInterpolationAgent):
    def __init__(self, simspark_ip='localhost',
                 simspark_port=3100,
                 teamname='DAInamite',
                 player_id=0,
                 sync_mode=True):
        super(PostureRecognitionAgent, self).__init__(simspark_ip, simspark_port, teamname, player_id, sync_mode)
        self.posture = 'unknown'
        self.posture_classifier = pickle.load(open(ROBOT_POSE_DATA_DIR, 'rb'))  # LOAD YOUR CLASSIFIER

    def think(self, perception):
        self.posture = self.recognize_posture(perception)
        return super(PostureRecognitionAgent, self).think(perception)

    def recognize_posture(self, perception):
        posture = 'unknown'
        # YOUR CODE HERE
        try:
            classes = sorted(listdir(ROBOT_POSE_DATA_DIR))
            features = [perception.joint[j] for j in INVERSED_JOINTS] + list(perception.imu[:2])
            if self.posture_classifier:
                predicted_index = self.posture_classifier.predict([features])[0]
                posture = classes[predicted_index]
        except Exception as e:
            print(f"Error recognizing posture: {e}")

        # Heuristik: Wenn IMU-Werte nahe 0 → Roboter steht
        pitch, roll = perception.imu[:2]
        if abs(pitch) < 0.3 and abs(roll) < 0.3:
            posture = 'stand_up'
        
        return posture

if __name__ == '__main__':
    agent = PostureRecognitionAgent()
    agent.keyframes = hello()  # CHANGE DIFFERENT KEYFRAMES
    agent.run()
