from mesa.time import SimultaneousActivation
from mesa.space import Grid
from mesa import Model
from mesa.datacollection import DataCollector
from agent import Vacuum, ObstacleAgent, Dirt
import time

class MyModel(Model):
    def __init__(self, n_sliders, alto, ancho, porcentaje, tiempo, behavior):
        global start_time
        start_time = time.time_ns() 
        start_time = start_time + (tiempo * 1000000000)
        print(tiempo)
        self.num_agents = n_sliders
        self.schedule = SimultaneousActivation(self)
        self.grid = Grid(alto, ancho, torus=False)
        self.time = tiempo
        self.behavior = behavior
        
        # Initialize DataCollector to track clean percentage and movement count
        self.datacollector = DataCollector(
            {
                "Clean Tiles (in percentage)": lambda m: self.count_type(m),
                "Movements": lambda m: self.count_moves(m)
            }
        )

        # Obstacle setup
        numObs = (ancho * 2) + (alto * 2 - 4)
        listaPosLimite = [(col, ren) for col in [0, ancho-1] for ren in range(alto)]
        for col in range(1, ancho-1):
            for ren in [0, alto-1]:
                listaPosLimite.append((col, ren))

        for i in range(numObs):
            a = ObstacleAgent(i + 1000, self)
            self.schedule.add(a)
            self.grid.place_agent(a, listaPosLimite[i])

        # Vacuum setup with behavior parameter
        for i in range(self.num_agents):
            a = Vacuum(i + 2000, self, behavior=self.behavior)
            self.schedule.add(a)
            
            # Find a random empty position on the grid for each vacuum
            while True:
                x = self.random.randrange(self.grid.width)
                y = self.random.randrange(self.grid.height)
                if self.grid.is_cell_empty((x, y)):
                    self.grid.place_agent(a, (x, y))
                    break


        # Dirt setup
        for (contents, x, y) in self.grid.coord_iter():
            if self.grid.is_cell_empty((x, y)) and self.random.random() < porcentaje:
                new_dirt = Dirt((x, y), self, 'Dirt')
                self.grid.place_agent(new_dirt, (x, y))
                self.schedule.add(new_dirt)

        self.running = True
        self.datacollector.collect(self)

    def step(self):
        # Step all agents
        self.schedule.step()
        self.datacollector.collect(self)

        # Ensure the number of Vacuum agents remains the same
        current_vacuum_count = sum(1 for agent in self.schedule.agents if isinstance(agent, Vacuum))
        if current_vacuum_count < self.num_agents:
            for i in range(self.num_agents - current_vacuum_count):
                # Create a new Vacuum agent with a unique ID and the selected behavior
                new_vacuum = Vacuum(2000 + current_vacuum_count + i, self, behavior=self.behavior)
                self.schedule.add(new_vacuum)
                
                # Place the new Vacuum agent in a random empty cell
                while True:
                    x = self.random.randrange(self.grid.width)
                    y = self.random.randrange(self.grid.height)
                    if self.grid.is_cell_empty((x, y)):
                        self.grid.place_agent(new_vacuum, (x, y))
                        break

        # Stop the model if time has expired
        current_time = time.time_ns()
        print(current_time - start_time)
        if current_time >= start_time:
            self.running = False

        
    @staticmethod
    def count_type(model):
        count = 0
        for agent in model.schedule.agents:
            if isinstance(agent, Dirt) and agent.condition == 'Dirt':
                count += 1
        total_cells = model.grid.width * model.grid.height
        clean_percentage = ((total_cells - count) * 100) / total_cells
        return clean_percentage

    @staticmethod
    def count_moves(model):
        total_moves = sum(agent.value for agent in model.schedule.agents if isinstance(agent, Vacuum))
        return total_moves
    
    def get_distance(self, pos1, pos2):
        """Calculate Manhattan distance between two points."""
        x1, y1 = pos1
        x2, y2 = pos2
        return abs(x1 - x2) + abs(y1 - y2)  # Manhattan distance    
