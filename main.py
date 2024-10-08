from gui import visualizer
from logic.simulation import simulate

if __name__ == "__main__":
    print("-" * 50)
    print("Welcome to the Wumpus World Simulator!")
    input = input("Do you want to run the simulation? it will take a while to run (y/n): ")
    # lower case the input
    input = input.lower()
    if input == "y":
        simulate()
    
    print("Visualizing the simulation...")
    visualizer.visualize()