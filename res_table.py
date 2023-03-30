
# Example script for how reservation table works
# reservation table disctionary class for 
# checking if a path is taken by a previous agent
# key: (x,y,t)
# value:0 (available) or 1 (reserved)

class reservation_table(dict):
  def __init__(self):
    self = dict()
  def add(self, key, value):
    self[key] = value
 
# create reservation table
res_table = reservation_table()
# example: agent 1 path (x position, y position, time)
path = [(2,3,0),(3,4,1),(4,5,2)]

# add agent states to reservation table after path found
for state in path:
  res_table.add(str(state), 1)

# example: agent 2 is condisering its next state
state70 = (3,4,1)

# agent 2 checks if its next state is occupied by agent 1's path
print(res_table[str(state70)])