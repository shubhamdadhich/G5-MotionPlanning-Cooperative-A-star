# original 'run_graph_search.py' script converted 
# to run CA*

import CA_star

# edit
def run_CA_star(map_path,actions=CA_star._ACTIONS):
    g = CA_star.GridMap(map_path)
    res = CA_star.CA_star_search(g.init_pos, g.transition, g.is_goal, actions,g.manhattan_heuristic)
    g.display_map(res[0],res[1])
    print(f"# states visited are: {len(res[1])}")

# edit map
if __name__ == '__main__':
    run_CA_star('./map1.txt')

