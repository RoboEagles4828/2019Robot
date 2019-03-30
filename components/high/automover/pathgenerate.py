import pathfinder as pf
import os.path
import pickle
import wpilib

class PathGenerator:
    points = [1]

    def makeTrajectory(self):
        return pf.generate(self.points, pf.FIT_HERMITE_CUBIC, pf.SAMPLES_HIGH,
                                    dt=0.03,
                                    max_velocity=1.7,
                                    max_acceleration=2.0,
                                    max_jerk=60.0)

    def saveTrajectory(self, trajectory):
        # because of a quirk in pyfrc, this must be in a subdirectory
        # or the file won't get copied over to the robot
        pickle_file = os.path.join(os.path.dirname(__file__), 'trajectory.pickle')

        if wpilib.RobotBase.isSimulation():
            # generate the trajectory here

            # and then write it out
            with open(pickle_file, 'wb') as fp:
                pickle.dump(trajectory, fp)
        else:
            with open('fname', 'rb') as fp:
                trajectory = pickle.load(fp)
        return trajectory