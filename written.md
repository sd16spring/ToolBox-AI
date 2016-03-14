0. Depth-first search simply tries the next thing; it will usually take a long time and will not find the most efficient path. The advantage of A* over dfs is that A* takes into account the location of the goal. Breadth-first search works by examining each of the nodes around the position node, but still does not take into consideration the location of the goal. A* uses the distance from the start to current position and projected current position to goal to explore the most promising path.

1. When you uncomment the g_cost line, the values printed in the cells are the distance from the start point. This is because g_cost is the distance from the starting position. When you uncomment the h_cost line, the values printed in the cells are the distance from the goal. This is because h_cost is the estimated distance to the goal. When you uncomment f_cost, the values printed in the cells are the final distance, except for the very isolated cells. In all cases, the values printed in inaccessible or lava cells are None. The screenshots of the pygame windows are in a screenshots folder in this repository.

2. Paul is now capable of moving diagonally. A screenshot is included in the screenshots folder in this repository.

3. Paul is now capable of moving through swamps at four times the cost of moving to unoccupied adjacent squares. A screenshot is included in the screenshots folder in this repository (it was difficult to coerce Paul into moving through a swamp).

4. Paul is now capable of jumping lava at eight times the cost of moving to unoccupied adjacent squares. A screenshot is included in the screenshots folder in this repository.
