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
    # g.display_map(path,visited)
    return path

# edit map
if __name__ == '__main__':
    
    # NOTE robots need to take up position up to a time step 't' once they reach the goal
    # currently the robots don't take up the goal position once they reach it, so robots can
    # pass through each other
    
    # create reservation table
    res_table = reservation_table()

    # make list of all paths, starts, ends
    all_paths = []
    all_starts = []
    all_ends = []

    maps_list = ['./t2_r1_map.txt','./t2_r2_map.txt','./t2_r3_map.txt','./t2_r4_map.txt']
    robot_ids = [1,2,3,4]

    for i in range(4):
      path = run_CA_star(maps_list[i], res_table, robot_ids[i])
      all_paths.append(path)
      all_starts.append(path[0])
      all_ends.append(path[-1])

    all_obstacles = []

    # save video of the paths
    animate_paths(all_paths, all_ends, all_obstacles,"video_4", True)