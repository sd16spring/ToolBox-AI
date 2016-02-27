def explanations(image_name, description):
	return "{}: \n{}\n".format(image_name, description)

print explanations("Advantages of A* over BFS and DFS", "A* picks the node that looks most promising first, instead of randomly choosing the next node like in a BFS or a DFS. (A DFS blindly guesses at the next node, and a BFS examines all of the nodes before choosing one. In contrast, A* generates all the possible point values for all the nodes surrounding the current one and chooses the best one first.)")
print explanations("self_f_cost", "Calculates the total number of points, and prints this value on ALL of the tiles. (f = g + h)")
print explanations("self_g_cost", "Calculates the number of points it took to get to a given node, and prints the current point value on each of the tiles.")
print explanations("self_h_cost", "Calculates the number of points starting from the end, and prints the current point value on each of the tiles. (h is a guess as to how many points it will take to reach the end.)")
print explanations("diagonal", "This image shows that every time Paul moves diagonally, the score increases by 3.")
print explanations("hopping", "This image shows that every time Paul hops over lava, the score increases by 8.")
print explanations("swamp", "This image shows that when Paul moves through a swamp tile, the score increases by 4 (or 3 more than if he had moved through a regular tile). Furthermore, when Paul moves diagonally through a swamp tile, the score increases by 6 (again, 3 more than if he had moved diagonally through regular tiles).")
print explanations("just_for_funsies", "This image shows the code in action. I generated a somewhat complex maze and the code calculated displayed the shortest path through my maze to the end.")