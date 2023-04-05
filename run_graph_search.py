import graph_search

def run_dfs(map_path,actions=graph_search._ACTIONS):
    g = graph_search.GridMap(map_path)
    res = graph_search.dfs(g.init_pos, g.transition, g.is_goal, actions)
    g.display_map(res[0],res[1])
    # print(f"The path is: {res[0]}")
    # print(f"The states visited are: {res[1]}")
    print(f"# states visited are: {len(res[1])}")
def run_idfs(map_path,actions=graph_search._ACTIONS):
    g = graph_search.GridMap(map_path)
    res = graph_search.idfs(g.init_pos, g.transition, g.is_goal, actions)
    g.display_map(res[0],res[1])
    print(f"# states visited are: {len(res[1])}")
def run_ucs(map_path,actions=graph_search._ACTIONS):
    g = graph_search.GridMap(map_path)
    res = graph_search.uniform_cost_search(g.init_pos, g.transition, g.is_goal, actions)
    g.display_map(res[0],res[1])
    print(f"# states visited are: {len(res[1])}")
def run_bfs(map_path,actions=graph_search._ACTIONS):
    g = graph_search.GridMap(map_path)
    res = graph_search.bfs(g.init_pos, g.transition, g.is_goal, actions)
    g.display_map(res[0],res[1])
    # print(f"The path is: {res[0]}")
    # print(f"The states visited are: {res[1]}")
    print(f"# states visited are: {len(res[1])}")
def run_As(map_path,actions=graph_search._ACTIONS):
    g = graph_search.GridMap(map_path)
    res = graph_search.a_star_search(g.init_pos, g.transition, g.is_goal, actions,g.manhattan_heuristic)
    g.display_map(res[0],res[1])
    print(f"# states visited are: {len(res[1])}")
    print(res[1])

if __name__ == '__main__':
    run_As('./map0.txt')

