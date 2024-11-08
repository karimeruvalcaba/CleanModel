from mesa import Agent
import heapq

class Vacuum(Agent):
    def __init__(self, unique_id, model, behavior="random"):
        super().__init__(unique_id, model)
        self.direccion = 4
        self.value = 0
        self.behavior = behavior  # Determines which behavior the agent will use

    def move(self):
        if self.behavior == "random":
            self.random_move()
        elif self.behavior == "greedy":
            self.greedy_nearest_dirt()
        elif self.behavior == "a_star":
            self.a_star_to_nearest_dirt()

    def random_move(self):
        possible_steps = self.model.grid.get_neighborhood(
            self.pos,
            moore=True,
            include_center=True
        )
        self.direccion = self.random.randint(0, 8)
        
        if self.is_free(possible_steps[self.direccion]):
            self.model.grid.move_agent(self, possible_steps[self.direccion])
            self.value += 1
        self.clean_if_dirty()

    def is_free(self, pos):
        """Check if a position is free of obstacles."""
        for agent in self.model.grid.get_cell_list_contents(pos):
            if isinstance(agent, ObstacleAgent):
                return False
        return True

    def greedy_nearest_dirt(self):
        # Find all dirt positions that are still dirty
        dirt_positions = [(d.pos, self.model.get_distance(self.pos, d.pos)) 
                        for d in self.model.schedule.agents if isinstance(d, Dirt) and d.condition == 'Dirt']
        
        if dirt_positions:
            # Find the nearest dirt based on Manhattan distance
            nearest_dirt = min(dirt_positions, key=lambda x: x[1])[0]
            self.move_towards(nearest_dirt)


    def a_star_to_nearest_dirt(self):
        # Get all dirt positions in the grid that are still dirty
        dirt_positions = [d.pos for d in self.model.schedule.agents if isinstance(d, Dirt) and d.condition == 'Dirt']
        
        # If there are no dirt cells, there's nothing to search for
        if not dirt_positions:
            return
        
        # Find the closest dirt cell using Manhattan distance
        nearest_dirt = min(dirt_positions, key=lambda d: self.model.get_distance(self.pos, d))
        
        # Initialize the open set with the starting position and g and f scores
        open_set = []
        heapq.heappush(open_set, (0, self.pos))
        came_from = {}  # To reconstruct the path after finding the goal
        g_score = {self.pos: 0}  # Cost from start to each cell
        f_score = {self.pos: self.model.get_distance(self.pos, nearest_dirt)}  # Estimated cost to goal

        while open_set:
            # Get the position with the lowest f_score value
            _, current = heapq.heappop(open_set)
            
            # If we reach the nearest dirt, stop and move towards it
            if current == nearest_dirt:
                path = self.reconstruct_path(came_from, current)
                # Move to the next step in the path (not the goal itself)
                if len(path) > 1:
                    self.model.grid.move_agent(self, path[1])  # Move to the next position
                    self.value += 1  # Count the move
                return
            
            # Check each neighbor of the current cell
            for neighbor in self.model.grid.get_neighborhood(current, moore=False, include_center=False):
                # Skip if neighbor is occupied by an obstacle
                if not self.is_free(neighbor):
                    continue

                # Tentative g_score is the g_score of current + distance to neighbor (which is 1)
                tentative_g_score = g_score[current] + 1
                
                # Only consider this new path if it's better
                if neighbor not in g_score or tentative_g_score < g_score[neighbor]:
                    # Record the best path to reach this neighbor
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_g_score
                    f_score[neighbor] = tentative_g_score + self.model.get_distance(neighbor, nearest_dirt)
                    heapq.heappush(open_set, (f_score[neighbor], neighbor))

    def reconstruct_path(self, came_from, current):
        """Reconstruct the path from start to goal by tracing came_from links."""
        path = [current]
        while current in came_from:
            current = came_from[current]
            path.append(current)
        path.reverse()
        return path

    def is_free(self, pos):
        """Check if a position is free of any other agents."""
        return all(not isinstance(agent, (Vacuum, ObstacleAgent)) for agent in self.model.grid.get_cell_list_contents(pos))


    def move_towards(self, target_pos):
        """Move one step closer to the target position, ensuring the cell is empty."""
        possible_steps = self.model.grid.get_neighborhood(self.pos, moore=False, include_center=False)
        
        # Find the best step toward the target
        best_step = min(possible_steps, key=lambda pos: self.model.get_distance(pos, target_pos))
        
        # Only move if the best step is free of other agents
        if self.is_free(best_step):
            self.model.grid.move_agent(self, best_step)
            self.value += 1  # Increment movement count


    def a_star_path(self, start, goal):
        """A* search to find the shortest path from start to goal."""
        open_set = []
        heapq.heappush(open_set, (0, start))
        came_from = {}
        g_score = {start: 0}
        f_score = {start: self.model.grid.get_distance(start, goal)}

        while open_set:
            _, current = heapq.heappop(open_set)
            if current == goal:
                return self.reconstruct_path(came_from, current)

            for neighbor in self.model.grid.get_neighborhood(current, moore=True, include_center=False):
                if not self.is_free(neighbor):
                    continue
                tentative_g_score = g_score[current] + 1
                if neighbor not in g_score or tentative_g_score < g_score[neighbor]:
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_g_score
                    f_score[neighbor] = tentative_g_score + self.model.grid.get_distance(neighbor, goal)
                    heapq.heappush(open_set, (f_score[neighbor], neighbor))
        return []

    def reconstruct_path(self, came_from, current):
        path = [current]
        while current in came_from:
            current = came_from[current]
            path.append(current)
        path.reverse()
        return path

    def clean_if_dirty(self):
        for agent in self.model.grid.get_cell_list_contents(self.pos):
            if isinstance(agent, Dirt):
                self.model.grid.remove_agent(agent)

    def step(self):
        pass

    def advance(self):
        self.move()


class ObstacleAgent(Agent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)

    def step(self):
        pass

class Dirt(Agent):
    def __init__(self, pos, model, assignedValue):
        super().__init__(pos, model)
        self.pos = pos
        self.condition = assignedValue

    def step(self):
        if self.pos:
            for a in self.model.grid.get_cell_list_contents(self.pos):
                if isinstance(a, Vacuum):
                    self.condition = "clean"
