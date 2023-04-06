# original 'run_graph_search.py' script converted 
# to run CA*

import CA_star

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
    return path, res_table

# NOTE save sequence of path (list) to robot class

# edit map
if __name__ == '__main__':
    # create reservation table
    res_table = reservation_table()

    # get path for robot 1 from CA* and update reservation table with path
    r1_path, res_table_1 = run_CA_star('./map_col_r1.txt', res_table, robot_id = 1)

    print(res_table.keys())

    print(len(res_table_1))
    print(res_table_1)

    # run CA* with next robot 
    # get path for robot 2 from CA* and update reservation table with path
    r2_path, res_table_2 = run_CA_star('./map_col_r2.txt', res_table, robot_id = 2)

    print(len(res_table_2))
    print(res_table_2)

    # NOTE reservation table in CA* script is in progress
    # and display it better
    # and make sure heuristic is good
