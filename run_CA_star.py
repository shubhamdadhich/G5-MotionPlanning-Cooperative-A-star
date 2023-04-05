# original 'run_graph_search.py' script converted 
# to run CA*

import CA_star

class reservation_table(dict):
  def __init__(self):
    self = dict()
  def add(self, key, value):
    self[key] = value

# run CA* for the first robot and then update reservation table
def run_CA_star(map_path, res_table, actions=CA_star._ACTIONS):
    g = CA_star.GridMap(map_path)
    path, visited, res_table = CA_star.CA_star_search(g.init_pos, g.transition, g.is_goal, actions,g.manhattan_heuristic, res_table)
    g.display_map(path,visited)
    return path, res_table


# edit map
if __name__ == '__main__':
    # create reservation table
    res_table = reservation_table()

    # get path for robot 1 from CA*
    r1_path, res_table_1 = run_CA_star('./map0.txt', res_table)
    robot_id = 1

    print(res_table_1)

