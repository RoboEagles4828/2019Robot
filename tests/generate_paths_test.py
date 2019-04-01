import sys
import os
import json
import pathfinder

from components.high.pathfinder.path_generator import PathGenerator


def test_generate_paths(robot):
    with open(sys.path[0] + ("/../" if os.getcwd()[-5:-1] == "test" else "/") +
              "config/paths.json") as f:
        paths = json.load(f)
    for name, config in paths.items():
        path = []
        for point in config["path"]:
            path.append(
                pathfinder.Waypoint(point["x"], point["y"], point["angle"]))
        PathGenerator.set(
            name,
            PathGenerator.generate(path, config["dt"], config["max_velocity"],
                                   config["max_acceleration"],
                                   config["max_jerk"]))
