import pygame
from math import sqrt
#http://www.raywenderlich.com/4946/introduction-to-a-pathfinding

class GridWorld():
    """Grid world that contains animals living in cells."""
    def __init__(self,width=10,height=10,cell_size=50):
        pygame.init()
        self.screen = pygame.display.set_mode((height*cell_size,width*cell_size))
        pygame.display.set_caption = ('Paul World')
        self.actors = {}
        self.width = width
        self.height = height
        self.cell_size = cell_size
        self._init_cells()
        self._init_paul_and_cake()
        self.add_tile_type = None

    def _draw_background(self):
        WHITE = (255,255,255)
        self.screen.fill(WHITE)

    def _init_cells(self):
        self.cells = {}
        for i in range(self.height):
            for j in range(self.width):
                self.cells[(i,j)] = Cell(self.screen,(i*self.cell_size, j*self.cell_size),(self.cell_size,self.cell_size))
    
    def _add_coords(self,a,b):
        #map: returns a list of the function applied to each element of the iterable
        #zip: returns a list of tuples [(a[0],b[0]), (a[1],b[1])]
        return tuple(map(sum,zip(a,b)))

    def _init_paul_and_cake(self):
        self.paul = Paul( (0,0), self, './images/paul.jpg' )
        self.cake = Actor( (9,9), self, './images/cake.jpg' , unremovable = True, is_obstacle = False)
        self.actors[(0,0)] = self.paul
        self.actors[(9,9)] = self.cake

    def _draw_cells(self):
        all_cells = self.cells.values()
        for cell in all_cells:
            cell.draw()

    def _draw_actors(self):
        all_actors = self.actors.values()
        for actor in all_actors:
            actor.draw()

    def _is_in_grid(self,cell_coord):
        """tells us whether cell_coord is valid and in range of the actual grid dimensions"""
        return (-1 < cell_coord[0] < self.width) and (-1 < cell_coord[1] < self.height)

    def _is_occupied(self,cell_coord):
        try:
            actor = self.actors[cell_coord]
            return actor.is_obstacle
        except:
            return False

    def _is_special(self, cell_coord):
        try:
            actor = self.actors[cell_coord]
            return actor.terrain_type
        except:
            return None

    def _add_swamp(self, mouse_pos):
        swamp_coord = (mouse_pos[0]/50, mouse_pos[1]/50)
        #is_occupied only true if unpassable!
        if self._is_special(swamp_coord)=='swamp': 
            if self.actors[swamp_coord].unremovable == False:
                self.actors.pop(swamp_coord, None)
        else:
            self.actors[swamp_coord] = ObstacleTile(swamp_coord, self, './images/swamp.jpg', is_unpassable = False, terrain_cost = 3, terrain_type = 'swamp')

    def _add_lava(self, mouse_pos):
        lava_coord = (mouse_pos[0]/50, mouse_pos[1]/50)
        if self._is_special(lava_coord)=='lava':
            if self.actors[lava_coord].unremovable == False:
                self.actors.pop(lava_coord, None)
        else:
            self.actors[lava_coord] = ObstacleTile(lava_coord, self, './images/lava.jpg', is_unpassable = True, terrain_cost = 0, terrain_type = 'lava')

    def get_terrain_cost(self, cell_coord):
        try:
            actor = self.actors[cell_coord]
            if actor.terrain_cost is not None:
                return actor.terrain_cost
            else:
                return 0
        except:
            return 0

    def main_loop(self):
        running = True
        while (running):
            self._draw_background()
            self._draw_actors()
            self._draw_cells()
            pygame.display.update()
            for event in pygame.event.get():
                if event.type is pygame.QUIT:
                    running = False
                elif event.type is pygame.MOUSEBUTTONDOWN:
                    if self.add_tile_type == 'lava':
                        self._add_lava(event.pos)
                    elif self.add_tile_type == 'swamp':
                        self._add_swamp(event.pos)
                elif event.type is pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.paul.run_astar(self.cake.cell_coordinates, self)
                        self.paul.get_path()
                    elif event.key == pygame.K_l:
                        self.add_tile_type = 'lava'
                    elif event.key == pygame.K_s:
                        self.add_tile_type = 'swamp'

class Actor(object):
    def __init__(self, cell_coordinates, world, image_loc, unremovable = False, is_obstacle = True):
        self.is_obstacle = is_obstacle
        self.unremovable = unremovable
        """takes coordinates as a tuple"""
        if world._is_occupied(cell_coordinates):
            raise Exception('%s is already occupied!'%cell_coordinates)
        self.cell_coordinates = cell_coordinates
        self.world = world
        self.image = pygame.image.load(image_loc)
        self.image_rect = self.image.get_rect()

    def draw(self):
        cells = self.world.cells
        cell = cells[self.cell_coordinates]
        x_y_coords = self.world._add_coords(cell.coordinates, (3,3) ) #add an offset so that the image will fit inside the cell border.
        rect_dim = (self.image_rect.width, self.image_rect.height)
        self.image_rect = pygame.Rect(x_y_coords, rect_dim)
        screen = self.world.screen
        screen.blit(self.image,self.image_rect)

class ObstacleTile(Actor):
    def __init__(self, cell_coordinates, world, image_loc, terrain_cost=0, is_unpassable = True, terrain_type = 'lava'):
        super(ObstacleTile, self).__init__(cell_coordinates, world, image_loc, unremovable = False, is_obstacle = is_unpassable)
        self.terrain_cost = terrain_cost
        self.terrain_type = terrain_type
        
class Cell():
    def __init__(self, draw_screen, coordinates, dimensions):
        self.draw_screen = draw_screen
        self.coordinates = coordinates
        self.dimensions = dimensions
        self.color = (0,0,0)
        self.g_cost = None
        self.h_cost = None

    @property
    def f_cost(self):
        if self.g_cost is None or self.h_cost is None:
            return None
        return self.g_cost + self.h_cost

    def draw(self):
        #COST_TO_DRAW = ''
        COST_TO_DRAW = self.g_cost
        #COST_TO_DRAW = self.h_cost
        #COST_TO_DRAW = self.f_cost
        line_width = 2
        rect = pygame.Rect((self.coordinates[0],self.coordinates[1]),(self.dimensions[0],self.dimensions[1]))
        pygame.draw.rect(self.draw_screen, self.color, rect, line_width)
        font = pygame.font.Font(None, 20)
        text = font.render(' '+str(COST_TO_DRAW) , 1, (10,10,10))
        self.draw_screen.blit(text, self.coordinates)

class Paul(Actor):
    def __init__(self, init_coordinates, world, image_loc):
        super(Paul, self).__init__(init_coordinates, world, image_loc, unremovable = True)
        self.cells = world.cells
        self.open_list = []
        self.closed_list = []

    def get_h_cost(self, coord_a,coord_b):
        """returns the h score, the manhattan distance between coord_a and the coord_b."""
        return abs(coord_a[0] - coord_b[0]) + abs(coord_a[1] - coord_b[1])

    def get_open_adj_coords(self, coords):
        """returns list of valid coords that are adjacent to the argument, open, and not in the closed list."""
        #modify directions and costs as needed
        directions = [(1,0),(0,1),(-1,0),(0,-1),(-1,-1),(1,1),(1,-1),(-1,1),(2,0),(-2,0),(0,2),(0,-2)]
        costs = [1,1,1,1,3,3,3,3,8,8,8,8]
        adj_coords = map(lambda d: self.world._add_coords(coords,d), directions)
        for i, coord in enumerate(adj_coords):
            costs[i] += self.world.get_terrain_cost(coord)
        #list of booleans
        in_bounds = [self.world._is_in_grid(c) and not self.world._is_occupied(c) and c not in self.closed_list for c in adj_coords]
        #get cooresponding coords and costs
        adj_coords = [c for (idx,c) in enumerate(adj_coords) if in_bounds[idx]]
        costs = [c for (idx,c) in enumerate(costs) if in_bounds[idx]]
        return adj_coords, costs

    def get_lowest_cost_open_coord(self):
        open_cells = self.open_list
        sorted_cells = sorted(open_cells, key = lambda s: self.cells[s].f_cost)
        costs = map(lambda c: self.cells[c].f_cost, sorted_cells)
        return sorted_cells[0]

    def reset_cell_values(self):
        self.destination_coord = None
        for cell in self.cells.values():
            cell.color = (0,0,0)
            cell.parents_coords = None
            cell.g_cost = None
            cell.h_cost = None

    def get_path(self):
        """Follows cell parents backwards until the initial cell is reached to create a path, which is the list of coordinates that paul will travel through to reach the destination."""
        coord_list = [self.destination_coord]
        print "final cost is", self.cells[coord_list[-1]].f_cost
        while self.start_coord not in coord_list:
            try:
                #attribute created in run_astar, determines which coord came before it.
                coord_list.append(self.cells[coord_list[-1]].parents_coords)
            except:
                print 'No path found to destination coord!'
                break
        for coord in coord_list:
            if coord is not None:
                self.cells[coord].color = (0,255,0)
        return coord_list

    def run_astar(self, destination_coord, world):
        """Updates cells g,h,f, and parent coordinates until the destination square is found."""
        self.reset_cell_values()
        self.start_coord = self.cell_coordinates
        self.destination_coord = destination_coord

        #start node
        coord_s = self.cell_coordinates
        cell_s = self.cells[coord_s]
        cell_s.g_cost = 0
        cell_s.h_cost = self.get_h_cost(coord_s, destination_coord)

        self.open_list = [coord_s]
        self.closed_list = []

        while len(self.open_list) > 0:
            #get smallest cost node
            coord_s = self.get_lowest_cost_open_coord()
            cell_s = self.cells[coord_s]
            self.open_list.remove(coord_s)
            self.closed_list.append(coord_s)
            walkable_open_coords, costs = self.get_open_adj_coords(coord_s)

            for idx,coord in enumerate(walkable_open_coords):
                cell = self.cells[coord]
                g_cost = cell_s.g_cost + costs[idx] 
                h_cost = self.get_h_cost(coord, destination_coord)
                f_cost = g_cost + h_cost
                if coord in self.open_list:
                    #update old cost, if necessary
                    old_f_cost = cell.f_cost
                    if f_cost < old_f_cost:
                        cell.g_cost = g_cost
                        cell.h_cost = h_cost
                        cell.parents_coords = coord_s
                else: #add to pqueue of nodes
                    self.open_list.append(coord)
                    cell.g_cost = g_cost
                    cell.h_cost = h_cost
                    cell.parents_coords = coord_s

if __name__ == "__main__":
    g = GridWorld()
    g.main_loop()
