'''In this exercise you need to implement an angle interploation function which makes NAO executes keyframe motion

* Tasks:
    1. complete the code in `AngleInterpolationAgent.angle_interpolation`,
       you are free to use splines interploation or Bezier interploation,
       but the keyframes provided are for Bezier curves, you can simply ignore some data for splines interploation,
       please refer data format below for details.
    2. try different keyframes from `keyframes` folder

* Keyframe data format:
    keyframe := (names, times, keys)
    names := [str, ...]  # list of joint names
    times := [[float, float, ...], [float, float, ...], ...]
    # times is a matrix of floats: Each line corresponding to a joint, and column element to a key.
    keys := [[float, [int, float, float], [int, float, float]], ...]
    # keys is a list of angles in radians or an array of arrays each containing [float angle, Handle1, Handle2],
    # where Handle is [int InterpolationType, float dTime, float dAngle] describing the handle offsets relative
    # to the angle and time of the point. The first Bezier param describes the handle that controls the curve
    # preceding the point, the second describes the curve following the point.
'''


from pid import PIDAgent
from keyframes import hello


class AngleInterpolationAgent(PIDAgent):
    def __init__(self, simspark_ip='localhost',
                 simspark_port=3100,
                 teamname='DAInamite',
                 player_id=0,
                 sync_mode=True):
        super(AngleInterpolationAgent, self).__init__(simspark_ip, simspark_port, teamname, player_id, sync_mode)
        self.keyframes = ([], [], [])



      

    def think(self, perception):
        target_joints = self.angle_interpolation(self.keyframes, perception)
        target_joints['RHipYawPitch'] = target_joints['LHipYawPitch'] # copy missing joint in keyframes
        self.target_joints.update(target_joints)
        return super(AngleInterpolationAgent, self).think(perception)
    


    def angle_interpolation(self, keyframes, perception):
        target_joints = {}
        
        # YOUR CODE HERE

        if "_bezier_start_time" not in self.__dict__:
            self._bezier_start_time = perception.time

        dT = perception.time - self._bezier_start_time
        names, times, keys = keyframes

        # RHipYawPitch ist nicht in Keyframes enthalten – dupliziere LHipYawPitch
        if 'RHipYawPitch' not in names and 'LHipYawPitch' in names:
            lh_index = names.index('LHipYawPitch')
            names = names + ['RHipYawPitch']
            times = times + [times[lh_index]]
            keys = keys + [keys[lh_index]]

        for i, jName in enumerate(names):
            if jName not in self.joint_names:
                continue

            key = keys[i]
            time = times[i]

            for count, t in enumerate(time[:-1]):
                t_start = time[count]
                t_end = time[count + 1]

                if t_start < dT < t_end:
                    p0 = key[count][0]
                    p3 = key[count + 1][0]
                    h0_offset = key[count][2]
                    h1_offset = key[count + 1][1]

                    h0 = p0 + h0_offset[1] * h0_offset[2]
                    h1 = p3 + h1_offset[1] * h1_offset[2]

                    t_norm = (dT - t_start) / (t_end - t_start)

                    b = (
                        (1 - t_norm) ** 3 * p0 +
                        3 * (1 - t_norm) ** 2 * t_norm * h0 +
                        3 * (1 - t_norm) * t_norm ** 2 * h1 +
                        t_norm ** 3 * p3
                    )

                    target_joints[jName] = b
                    break

                elif time[0] > dT:
                    p0 = perception.joint[jName]
                    p3 = key[0][0]
                    h0 = p0
                    h1 = p3 + key[count][2][1] * key[count][2][2]
                    t_norm = dT / time[1]

                    b = (
                        (1 - t_norm) ** 3 * p0 +
                        3 * (1 - t_norm) ** 2 * t_norm * h0 +
                        3 * (1 - t_norm) * t_norm ** 2 * h1 +
                        t_norm ** 3 * p3
                    )

                    target_joints[jName] = b
                    break

        # Fallback: Falls keine gültige Interpolation für LHipYawPitch gemacht wurde,
        # aber der Gelenkwert existiert, nimm den aktuellen Wert
        if 'LHipYawPitch' not in target_joints and 'LHipYawPitch' in perception.joint:
            target_joints['LHipYawPitch'] = perception.joint['LHipYawPitch']

        return target_joints

if __name__ == '__main__':
    agent = AngleInterpolationAgent()
    agent.keyframes = hello()  # CHANGE DIFFERENT KEYFRAMES
    agent.run()
