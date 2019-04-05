import sys
import os
import json
import pathfinder

from components.high.pathfinder.path_generator import PathGenerator


def test_generate_routes(robot):
    with open(sys.path[0] + ("/../" if os.getcwd()[-5:-1] == "test" else "/") +
              "config/routes.json") as f:
        routes = json.load(f)
    for name, config in routes.items():
        trajectories = []
        for path_config in config["paths"]:
            path = []
            for point in path_config:
                path.append(
                    pathfinder.Waypoint(point["x"], point["y"],
                                        pathfinder.d2r(point["angle"])))
            trajectories.append(
                PathGenerator.generate(
                    path, config["dt"], config["max_velocity"],
                    config["max_acceleration"], config["max_jerk"]))
        PathGenerator.set(name, trajectories)
