from model import MyModel, Vacuum, ObstacleAgent, Dirt
from mesa.visualization.modules import CanvasGrid, ChartModule
from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.UserParam import UserSettableParameter

# Updated colors
COLORS = {"Dirty": "#FF5733", "Clean": "#C70039"}

def cleaningPortrayal(agent):
    if agent is None:
        return

    if isinstance(agent, Dirt):
        portrayal = {
            "Shape": "rect",
            "w": 0.7,
            "h": 0.7,
            "Color": "#FFC300",  # Changed to a bright yellow
            "Layer": 0,
            "Filled": "true"
        }

    if isinstance(agent, Vacuum):
        portrayal = {
            "Shape": "circle",
            "Color": "#1A5276",  # Changed to a deep blue
            "Layer": 1,
            "Filled": "true",
            "r": 0.5
        }

    if isinstance(agent, ObstacleAgent):
        portrayal = {
            "Shape": "circle",
            "Color": "#BFC9CA",  # Changed to light gray
            "Layer": 2,
            "Filled": "true",
            "r": 0.2
        }

    return portrayal

# Add behavior selection as a dropdown menu
model_parameters = {
    "porcentaje": UserSettableParameter("slider", "Dirt Percentage", 0.6, 0.01, 1.0, 0.1),
    "n_sliders": UserSettableParameter("number", "Number of sliders", 4, 1, 10, 1),
    "ancho": 10,
    "alto": 10,
    "tiempo": UserSettableParameter("number", "Seconds", 60, 1, 360, 5),
    "behavior": UserSettableParameter("choice", "Cleaning Behavior", value="random", choices=["random", "greedy", "a_star"])
}

# Adjusted CanvasGrid layout
grid = CanvasGrid(cleaningPortrayal, 10, 10, 600, 600)

# Updated chart colors
clean_chart = ChartModule(
    [{"Label": "Clean Tiles (in percentage)", "Color": "#16A085"}]  # Updated to teal
)

move_chart = ChartModule(
    [{"Label": "Movements", "Color": "#D35400"}]  # Changed to orange-brown
)

# Updated title and charts layout
server = ModularServer(
    MyModel,
    [grid, clean_chart, move_chart],
    "Vacuum Cleaning Simulation",
    model_parameters
)

server.port = 8521
server.launch()
