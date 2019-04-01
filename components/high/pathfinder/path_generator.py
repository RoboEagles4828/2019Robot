import sys
import os
import pickle
import pathfinder


class PathGenerator:
    @staticmethod
    def generate(path,
                 dt=0.02,
                 max_velocity=1.7,
                 max_acceleration=2.0,
                 max_jerk=60.0):
        return pathfinder.generate(
            path,
            pathfinder.FIT_HERMITE_CUBIC,
            pathfinder.SAMPLES_HIGH,
            dt=dt,
            max_velocity=max_velocity,
            max_acceleration=max_acceleration,
            max_jerk=max_jerk)[1]

    @staticmethod
    def set(name, trajectory):
        with open(
                sys.path[0] + ("/../" if os.getcwd()[-5:-1] == "test" else "/")
                + "%s.pickle" % name, "wb") as f:
            pickle.dump(trajectory, f)

    @staticmethod
    def get(name):
        with open(
                sys.path[0] + ("/../" if os.getcwd()[-5:-1] == "test" else "/")
                + "%s.pickle" % name, "rb") as f:
            return pickle.load(f)
