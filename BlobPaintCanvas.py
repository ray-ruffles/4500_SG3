"""
Programming Language: Python 3.8.3

CMP_SCI-4500-001
Group Members:
- Davey Abrantes
- Jackie Herbstreit
- Joshua Culley
- Ray Rulifson
- Kendal Brown

"""


import math
import random
import pprint
import tkinter as tk
from tabulate import tabulate
import matplotlib.pyplot as plt

# Run in terminal:  "pip install tabulate"
# Run in terminal:  "pip install matplotlib"

class Canvas:
    def __init__(self, length: int, seconds: int):
        self.edge = length
        self.time = seconds
        self.current_time = 0
        self.full_canvas_shown = False

        if self.edge > 75:
            self.square_size = 7
        elif self.edge > 50:
            self.square_size = 10
        elif self.edge > 25:
            self.square_size = 15
        else:
            self.square_size = 25
        self.padding = self.square_size

        self.colors = ["Blue", "Green", "Red"]

        self.grid = {}
        self.rectangles = {}

        # Tkinter window setup
        self.root = tk.Tk()
        self.root.title("Paint Blobs Simulation")

        self.canvas = tk.Canvas(
            self.root,
            width=(self.edge * self.square_size) + (2 * self.padding),
            height=(self.edge * self.square_size) + (2 * self.padding),
            bg="white"
        )
        self.canvas.pack()

        # Create the grid data and the visible rectangles
        for b in range(1, self.edge + 1):
            for h in range(1, self.edge + 1):
                self.grid[(b, h)] = {
                    "Current Color": "White",
                    "Total Blobs": 0,
                    "Blue": 0,
                    "Green": 0,
                    "Red": 0
                }

                x1 = self.padding + (h - 1) * self.square_size
                y1 = self.padding + (b - 1) * self.square_size
                x2 = x1 + self.square_size
                y2 = y1 + self.square_size

                rect_id = self.canvas.create_rectangle(
                    x1, y1, x2, y2,
                    fill="white",
                    outline="black"
                )

                self.rectangles[(b, h)] = rect_id

    def drop_paint(self):
        x = random.randint(1, self.edge)
        y = random.randint(1, self.edge)
        color = random.choice(self.colors)

        self.grid[(x, y)]["Current Color"] = color
        self.grid[(x, y)]["Total Blobs"] += 1
        self.grid[(x, y)][color] += 1

        rect_id = self.rectangles[(x, y)]
        self.canvas.itemconfig(rect_id, fill=color.lower())

    def fill_check(self):
        for square in self.grid:
            if self.grid[square]["Total Blobs"] == 0:
                return False

        return True

    def run_animation(self):
        self.animate()
        self.root.mainloop()

    def animate(self):
        if self.time >= 60000:
            print("\n\nPlease wait while the simulation runs  . . .  \n\n")
            time_delay = 0
        else:
            time_delay = 1

        if self.current_time < self.time:
            self.drop_paint()
            self.current_time += 1

            if self.fill_check() and self.full_canvas_shown == False:
                self.full_canvas_shown = True

                print("\n\nEvery square has now been painted at least once.")
                print("Paint Blobs Dropped:", self.current_time)

                self.show_coordinates()
                self.show_statistics()

                self.root.after(5000, self.animate)
            else:
                self.root.after(time_delay, self.animate)
        else:
            print("\n\nSimulation Complete.")
            print("Paint Blobs Dropped:", self.current_time)

    def show_coordinates(self):
        headers = [
            "Coordinate",
            "Current Color",
            "Total Blobs",
            "Blue",
            "Green",
            "Red"
        ]

        table = []

        for coordinate in sorted(self.grid):
            table.append([
                coordinate,
                self.grid[coordinate]["Current Color"],
                self.grid[coordinate]["Total Blobs"],
                self.grid[coordinate]["Blue"],
                self.grid[coordinate]["Green"],
                self.grid[coordinate]["Red"]
            ])

        print(tabulate(table, headers=headers, tablefmt="fancy_grid"))

    def show_statistics(self):
        total_blobs_list = []
        one_color_squares = 0

        for coordinate in self.grid:
            total_blobs = self.grid[coordinate]["Total Blobs"]
            blue_blobs = self.grid[coordinate]["Blue"]
            green_blobs = self.grid[coordinate]["Green"]
            red_blobs = self.grid[coordinate]["Red"]

            total_blobs_list.append(total_blobs)

            colors_used = 0

            if blue_blobs > 0:
                colors_used += 1
            if green_blobs > 0:
                colors_used += 1
            if red_blobs > 0:
                colors_used += 1

            if colors_used == 1:
                one_color_squares += 1

        lowest_blobs = min(total_blobs_list)
        highest_blobs = max(total_blobs_list)
        average_blobs = sum(total_blobs_list) / len(total_blobs_list)

        print("\nCanvas Statistics:")
        print("Paint Blobs Dropped:", self.current_time)
        print("Lowest Amount of Paint Blobs on a Square:", lowest_blobs)
        print("Highest Amount of Paint Blobs on a Square:", highest_blobs)
        print("Average Amount of Paint Blobs per Square:", round(average_blobs))
        print("Number of Squares with Only One Color of Paint:", one_color_squares)

        if self.fill_check():
            print("Every square has been painted at least once.")
        else:
            print("There are still white squares on the canvas.")

    # End of Canvas Class

def change_size():
    while True:
        try:
            print("Enter a positive integer from 2 to 100.")
            n = int(input("\'n\'\t=\t"))

            if 2 <= n <= 100:
                return n
            else:
                print("INVALID INPUT.")
        except ValueError:
            print("INVALID INPUT.")


def change_supply():
    while True:
        try:
            print("Enter a positive integer from 4 to 1,000,000.")
            t = int(input("\'t\'\t=\t"))

            if 4 <= t <= 1000000:
                return t
            else:
                print("INVALID INPUT.")
        except ValueError:
            print("INVALID INPUT.")


def change_increment(increment_name):
    while True:
        try:
            print("Enter an increment of 1, 10, 100, or 1000.")
            increment = int(input(increment_name + "\t=\t"))

            if increment == 1 or increment == 10 or increment == 100 or increment == 1000:
                return increment
            else:
                print("INVALID INPUT.")
        except ValueError:
            print("INVALID INPUT.")

def run_one_nonanimated_simulation(n, max_t):
    colors = ["Blue", "Green", "Red"]
    grid = {}

    for b in range(1, n + 1):
        for h in range(1, n + 1):
            grid[(b, h)] = {
                "Current Color": "White",
                "Total Blobs": 0,
                "Blue": 0,
                "Green": 0,
                "Red": 0
            }

    for second in range(max_t):
        x = random.randint(1, n)
        y = random.randint(1, n)
        color = random.choice(colors)

        grid[(x, y)]["Current Color"] = color
        grid[(x, y)]["Total Blobs"] += 1
        grid[(x, y)][color] += 1

    total_blobs_list = []

    for coordinate in grid:
        total_blobs_list.append(grid[coordinate]["Total Blobs"])

    lowest_blobs = min(total_blobs_list)
    highest_blobs = max(total_blobs_list)
    average_blobs = sum(total_blobs_list) / len(total_blobs_list)

    return lowest_blobs, highest_blobs, average_blobs

def show_graph(x_values, lowest_values, average_values, highest_values, x_label, graph_title):
    plt.plot(x_values, lowest_values, marker="o", linestyle="None", label="Lowest")
    plt.plot(x_values, average_values, marker="s", linestyle="None", label="Average")
    plt.plot(x_values, highest_values, marker="^", linestyle="None", label="Highest")

    plt.title(graph_title)
    plt.xlabel(x_label)
    plt.ylabel("Number of Paint Blobs")
    plt.legend()
    plt.grid(True)

    plt.show()

def run_simulation(old_n: int, old_t: int):
    print("\nNow, you can run multiple non-animated simulations.")
    print("Choose one of the following options:")
    print("1. Hold \'t\' constant and change \'n\'.")
    print("2. Hold \'n\' constant and change \'t\'.")

    while True:
        try:
            choice = int(input("Choice\t=\t"))

            if choice == 1 or choice == 2:
                break
            else:
                print("INVALID INPUT.")
        except ValueError:
            print("INVALID INPUT.")

    x_values = []
    lowest_values = []
    average_values = []
    highest_values = []

    if choice == 1:
        print("\nYou chose to hold \'t\' constant and change \'n\'.")

        new_n = change_size()
        n_increment = change_increment("Nincrement")

        for simulation_number in range(10):
            current_n = new_n + (simulation_number * n_increment)

            print("\nRunning Simulation", simulation_number + 1)
            print("N:", current_n)
            print("MaxT:", old_t)

            lowest, highest, average = run_one_nonanimated_simulation(current_n, old_t)

            x_values.append(current_n)
            lowest_values.append(lowest)
            average_values.append(average)
            highest_values.append(highest)

        show_graph(
            x_values,
            lowest_values,
            average_values,
            highest_values,
            "Canvas Size, N",
            "Paint Blobs per Square while Holding MaxT Constant"
        )

    else:
        print("\nYou chose to hold \'n\' constant and change \'t\'.")

        new_t = change_supply()
        t_increment = change_increment("Tincrement")

        for simulation_number in range(10):
            current_t = new_t + (simulation_number * t_increment)

            print("\nRunning Simulation", simulation_number + 1)
            print("N:", old_n)
            print("MaxT:", current_t)

            lowest, highest, average = run_one_nonanimated_simulation(old_n, current_t)

            x_values.append(current_t)
            lowest_values.append(lowest)
            average_values.append(average)
            highest_values.append(highest)

        show_graph(
            x_values,
            lowest_values,
            average_values,
            highest_values,
            "Total Number of Paint Blobs, MaxT",
            "Paint Blobs per Square while Holding N Constant"
        )

    input("\nPress ENTER to finish the program.")

def main():
    # This is where we describe the purpose of this program;
    print("\nIn this program, we simulate the Canvas Puzzle.")
    print("Imagine you have a blank canvas to paint on.")
    print("It is a square with an edge of \'n\' inches, where \'n\' is greater than 1.")
    print("Within the square are smaller squares that are one inch in length.")
    print("Therefore, the canvas is filled with an amount of squares equal to \'n * n\'.")
    print("At each second, a blob of colored paint is dropped on a random square.")
    print("The color is either red, green, or blue.")
    print("If the square is white, the square becomes one of these three colors.")
    print("If the square already has a color, the new color is painted over the old color.")
    print("The simulation continues until every square is not white.")
    print("The program will list information about the canvas:")
    print("\t-  the total amount of paint blobs dropped in terms of \'t\', where \'t\' is time in seconds;")
    print("\t-  the lowest, highest, and average amount of paint blobs across all squares;")
    print("\t-  the amount of paint blobs of each color in each square; and")
    print("\t-  the number of squares that have only one color of paint.")
    print("\nOnce these details have been listed, the simulation continues until the absolute time limit.")
    print("At that point, the same details above will be updated and shown, then the simulation ends.")

    print("\nA sample simulation will be shown with \'n\' = 10 and \'t\' = 300.")
    davinci = Canvas(10, 300)
    davinci.run_animation()
    davinci.show_coordinates()
    davinci.show_statistics()

    print("\nNow, you pick the values for \'n\' and \'t\'.")

    while True:
        try:
            print("Enter a positive integer from 2 to 100.")
            n = int(input("\'n\'\t=\t"))
            if 2 <= n <= 100:
                break
            else:
                print("INVALID INPUT.")
        except ValueError:
            print("INVALID INPUT.")
    while True:
        try:
            print("Enter a positive integer from 4 to 1,000,000.")
            t = int(input("\'t\'\t=\t"))
            if 4 <= t <= 1000000:
                break
            else:
                print("INVALID INPUT.")
        except ValueError:
            print("INVALID INPUT.")

    davinci = Canvas(n, t)
    davinci.run_animation()
    davinci.show_coordinates()
    davinci.show_statistics()

    run_simulation(n, t)

    print("")
    # End of Main


main()
