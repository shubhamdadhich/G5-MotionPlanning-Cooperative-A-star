# original 'run_graph_search.py' script converted 
# to run CA*

import CA_star
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.animation import PillowWriter
import numpy as np
from visualization_multiple import animate_paths

class reservation_table(dict):
  def __init__(self):
    self = dict()
  def add(self, key, value):
    self[key] = value

# run CA* for the first robot and then update reservation table
def run_CA_star(map_path, res_table, robot_id, actions=CA_star._ACTIONS):
    g = CA_star.GridMap(map_path)
    path, visited, res_table = CA_star.CA_star_search(g.init_pos, g.transition, g.is_goal, actions,g.manhattan_heuristic, res_table, robot_id)
    g.display_map(path,visited)
    return path

# edit map
if __name__ == '__main__':

    # create reservation table
    res_table = reservation_table()

    # get path for robot 1 from CA* and update reservation table with path
    r1_path = run_CA_star('./map_col_r1.txt', res_table, robot_id = 1)

    # run CA* with next robot 
    # get path for robot 2 from CA* and update reservation table with path
    r2_path = run_CA_star('./map_col_r2.txt', res_table, robot_id = 2)

    # save video of the paths
    animate_paths(r1_path, r2_path, "video_1")

    print(res_table)



    # NOTE 
    # pseudocode for how this can be generalized with a robot class:
    # for robot in robots:
    #    robot.path = run_CA_star(robot.map, res_table, robot.robot_id)
    #    all_robots_paths.append(robot.path)
    # animate_paths(all_robots_paths, "video_1")