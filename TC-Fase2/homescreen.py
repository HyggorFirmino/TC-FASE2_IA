import tkinter as tk
from tkinter import messagebox
import tsp  # Import the tsp module

# -- COLOR PALETTE --
COLOR_BG = "#1e1e1e"            # Dark Grey Background
COLOR_FG = "#ffffff"            # White Text
COLOR_ACCENT = "#007acc"        # Blue Accent
COLOR_ACCENT_HOVER = "#005f9e"  # Darker Blue
COLOR_INPUT_BG = "#2d2d2d"      # Darker Field Input
COLOR_BORDER = "#3e3e3e"        # Border Color

def start_simulation():
    try:
        # Get values from entries
        capacity = int(entry_capacity.get())
        population = int(entry_population.get())
        generations = int(entry_generations.get())
        mutation = float(entry_mutation.get())
        
        critical = entry_critical.get()
        penalty_val = float(entry_penalty.get())

        # Validate inputs
        if capacity <= 0 or population <= 0 or generations <= 0:
            raise ValueError("Values must be positive integers.")
        if not (0 <= mutation <= 1):
            raise ValueError("Mutation probability must be between 0 and 1.")

        # Disable button to prevent multiple clicks
        btn_start.config(state=tk.DISABLED, text="Running...", bg=COLOR_BORDER)
        root.update()

        # Run the simulation
        print(f"Starting... Cap={capacity}, Pop={population}, Crit={critical}")
        tsp.run_tsp_simulation(truck_capacity=capacity, 
                               population_size=population, 
                               n_generations=generations, 
                               mutation_probability=mutation,
                               critical_indices_str=critical,
                               priority_penalty=penalty_val)
        
        # Re-enable button after simulation closes
        btn_start.config(state=tk.NORMAL, text="START SIMULATION", bg=COLOR_ACCENT)

    except ValueError as e:
        messagebox.showerror("Invalid Input", f"Please check your inputs:\n{e}")
        btn_start.config(state=tk.NORMAL, text="START SIMULATION", bg=COLOR_ACCENT)
    except Exception as e:
        messagebox.showerror("Error", f"An unexpected error occurred:\n{e}")
        btn_start.config(state=tk.NORMAL, text="START SIMULATION", bg=COLOR_ACCENT)


# Create Main Window
root = tk.Tk()
root.title("TSP Genetic Solver")
root.geometry("450x550")
root.resizable(False, False)
root.configure(bg=COLOR_BG)

# -- STYLING HELPERS --
def create_label(parent, text):
    return tk.Label(parent, text=text, font=("Segoe UI", 10), bg=COLOR_BG, fg="#aaaaaa")

def create_entry(parent, default_value):
    entry = tk.Entry(parent, font=("Segoe UI", 11), bg=COLOR_INPUT_BG, 
                     fg=COLOR_FG, insertbackground=COLOR_FG, relief="flat", bd=5)
    entry.insert(0, str(default_value))
    return entry

# HEADER
frame_header = tk.Frame(root, bg=COLOR_BG)
frame_header.pack(pady=30)

lbl_title = tk.Label(frame_header, text="TSP CONFIGURATION", font=("Segoe UI", 18, "bold"), bg=COLOR_BG, fg=COLOR_FG)
lbl_title.pack()

lbl_subtitle = tk.Label(frame_header, text="Configure your Genetic Algorithm Parameters", font=("Segoe UI", 9), bg=COLOR_BG, fg="#888888")
lbl_subtitle.pack()


# INPUTS CONTAINER
frame_inputs = tk.Frame(root, bg=COLOR_BG)
frame_inputs.pack(pady=10, padx=40, fill="x")

# --- ROW 1: Capacity & Population ---
frame_row1 = tk.Frame(frame_inputs, bg=COLOR_BG)
frame_row1.pack(fill="x", pady=5)

# Capacity
frame_cap = tk.Frame(frame_row1, bg=COLOR_BG)
frame_cap.pack(side="left", expand=True, fill="x", padx=(0, 5))
create_label(frame_cap, "Truck Capacity (kg)").pack(anchor="w")
entry_capacity = create_entry(frame_cap, "80")
entry_capacity.pack(fill="x")

# Population
frame_pop = tk.Frame(frame_row1, bg=COLOR_BG)
frame_pop.pack(side="right", expand=True, fill="x", padx=(5, 0))
create_label(frame_pop, "Population Size").pack(anchor="w")
entry_population = create_entry(frame_pop, "100")
entry_population.pack(fill="x")

# --- ROW 2: Mutation & Generations ---
frame_row2 = tk.Frame(frame_inputs, bg=COLOR_BG)
frame_row2.pack(fill="x", pady=5)

# Mutation
frame_mut = tk.Frame(frame_row2, bg=COLOR_BG)
frame_mut.pack(side="left", expand=True, fill="x", padx=(0, 5))
create_label(frame_mut, "Mutation Prob (0-1)").pack(anchor="w")
entry_mutation = create_entry(frame_mut, "0.5")
entry_mutation.pack(fill="x")

# Gen
frame_gen = tk.Frame(frame_row2, bg=COLOR_BG)
frame_gen.pack(side="right", expand=True, fill="x", padx=(5, 0))
create_label(frame_gen, "Max Generations").pack(anchor="w")
entry_generations = create_entry(frame_gen, "5000")
entry_generations.pack(fill="x")

# --- DIVIDER ---
tk.Frame(frame_inputs, height=1, bg=COLOR_BORDER).pack(fill="x", pady=15)

# --- ROW 3: Priorities ---
create_label(frame_inputs, "Critical City Indices (comma separated, e.g. 10, 15, 20)").pack(anchor="w")
entry_critical = create_entry(frame_inputs, "1, 5, 12, 18, 30")
entry_critical.pack(fill="x", pady=(0, 10))

create_label(frame_inputs, "Priority Violation Penalty").pack(anchor="w")
entry_penalty = create_entry(frame_inputs, "5000")
entry_penalty.pack(fill="x")


def open_chat():
    import subprocess
    # Run chat-ia.py as a separate process
    subprocess.Popen(["python", "chat-ia.py"])

# Button Frame using grid
button_frame = tk.Frame(root, bg=COLOR_BG)
button_frame.pack(pady=20)

btn_start = tk.Button(button_frame, text="Start Simulation", command=start_simulation, 
                      bg=COLOR_ACCENT, fg="white", font=("Segoe UI", 12, "bold"), 
                      relief="flat", padx=20, pady=10)
btn_start.grid(row=0, column=0, padx=10)

btn_chat = tk.Button(button_frame, text="Chat with AI", command=open_chat, 
                     bg="#252526", fg="white", font=("Segoe UI", 12, "bold"), 
                     relief="flat", padx=20, pady=10)
btn_chat.grid(row=0, column=1, padx=10)

def on_enter(e):
    e.widget['background'] = '#005999'

def on_leave(e):
    e.widget['background'] = COLOR_ACCENT

def on_enter_chat(e):
    e.widget['background'] = '#3e3e42'

def on_leave_chat(e):
    e.widget['background'] = '#252526'

btn_start.bind("<Enter>", on_enter)
btn_start.bind("<Leave>", on_leave)

btn_chat.bind("<Enter>", on_enter_chat)
btn_chat.bind("<Leave>", on_leave_chat)

# FOOTER
lbl_footer = tk.Label(root, text="Genetic Algorithm TSP Solver v1.0", font=("Segoe UI", 8), bg=COLOR_BG, fg="#444444")
lbl_footer.pack(side="bottom", pady=10)

# Run the GUI
root.mainloop()
