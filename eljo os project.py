import tkinter as tk
from tkinter import ttk, messagebox

class Process:
    def __init__(self, pid, arrival, burst, priority):
        self.pid = pid
        self.arrival = arrival
        self.burst = burst
        self.priority = priority
        self.remaining = burst
        self.completion = 0
         self.start = -1

class SchedulerSimulator:
    def __init__(self, root):
        self.root = root
        self.root.title("Intelligent CPU Scheduler Simulator")

        self.processes = []
        self.create_widgets()

    def create_widgets(self):
        # Input Frame
        input_frame = ttk.LabelFrame(self.root, text="Add Process")
        input_frame.pack(fill="x", padx=10, pady=5)

        ttk.Label(input_frame, text="PID").grid(row=0, column=0)
        self.pid_entry = ttk.Entry(input_frame, width=10)
        self.pid_entry.grid(row=0, column=1)

        ttk.Label(input_frame, text="Arrival Time").grid(row=0, column=2)
        self.arrival_entry = ttk.Entry(input_frame, width=10)
        self.arrival_entry.grid(row=0, column=3)

        ttk.Label(input_frame, text="Burst Time").grid(row=0, column=4)
        self.burst_entry = ttk.Entry(input_frame, width=10)
        self.burst_entry.grid(row=0, column=5)

        ttk.Label(input_frame, text="Priority").grid(row=0, column=6)
        self.priority_entry = ttk.Entry(input_frame, width=10)
        self.priority_entry.grid(row=0, column=7)

        ttk.Button(input_frame, text="Add", command=self.add_process).grid(row=0, column=8, padx=10)

        # Process Table Frame
        self.process_table = ttk.Treeview(self.root, columns=("PID", "Arrival", "Burst", "Priority"), show='headings')
        self.process_table.heading("PID", text="PID")
        self.process_table.heading("Arrival", text="Arrival Time")
        self.process_table.heading("Burst", text="Burst Time")
        self.process_table.heading("Priority", text="Priority")
        self.process_table.pack(fill="x", padx=10, pady=5)

        # Selection & Simulation Frame
        sim_frame = ttk.LabelFrame(self.root, text="Simulation")
        sim_frame.pack(fill="x", padx=10, pady=5)

        ttk.Label(sim_frame, text="Select Algorithm:").grid(row=0, column=0)
        self.alg_var = tk.StringVar()
        self.alg_combo = ttk.Combobox(sim_frame, textvariable=self.alg_var)
        self.alg_combo['values'] = ("FCFS", "SJF", "Priority", "Round Robin")
        self.alg_combo.grid(row=0, column=1)
        self.alg_combo.current(0)
        self.alg_combo.bind("<<ComboboxSelected>>", self.toggle_priority_input)

        ttk.Label(sim_frame, text="Time Quantum (for RR):").grid(row=0, column=2)
        self.quantum_entry = ttk.Entry(sim_frame, width=10)
        self.quantum_entry.grid(row=0, column=3)

        ttk.Button(sim_frame, text="Run Simulation", command=self.run_simulation).grid(row=0, column=4, padx=10)

        # Output Frame
        self.output = tk.Text(self.root, height=15)
        self.output.pack(fill="both", padx=10, pady=5)

        # Disable priority entry initially
        self.priority_entry.config(state='disabled')

    def toggle_priority_input(self, event=None):
        if self.alg_var.get() == "Priority":
            self.priority_entry.config(state='normal')
        else:
            self.priority_entry.config(state='disabled')

    def add_process(self):
        try:
            pid = self.pid_entry.get()
            arrival = int(self.arrival_entry.get())
            burst = int(self.burst_entry.get())
            priority = int(self.priority_entry.get()) if self.priority_entry['state'] == 'normal' else 0
            self.processes.append(Process(pid, arrival, burst, priority))
            self.process_table.insert('', 'end', values=(pid, arrival, burst, priority))
            messagebox.showinfo("Added", f"Process {pid} added.")
        except ValueError:
            messagebox.showerror("Error", "Invalid input.")

    def run_simulation(self):
        if not self.processes:
            messagebox.showerror("Error", "No processes to schedule.")
            return

        alg = self.alg_var.get()
        if alg == "FCFS":
            result = self.fcfs()
        elif alg == "SJF":
            result = self.sjf()
        elif alg == "Priority":
            result = self.priority()
        elif alg == "Round Robin":
            try:
                quantum = int(self.quantum_entry.get())
                result = self.round_robin(quantum)
            except:
                messagebox.showerror("Error", "Invalid quantum.")
                return

        self.output.delete("1.0", tk.END)
        self.output.insert(tk.END, result)

        # Reset the process list and entries after simulation
        self.reset_processes()

    def reset_processes(self):
        # Clear the process list and the treeview table
        self.processes.clear()
        for item in self.process_table.get_children():
            self.process_table.delete(item)

        # Clear the entries
        self.pid_entry.delete(0, tk.END)
        self.arrival_entry.delete(0, tk.END)
        self.burst_entry.delete(0, tk.END)
        self.priority_entry.delete(0, tk.END)

        # Reset the combobox and quantum entry
        self.alg_combo.current(0)
        self.quantum_entry.delete(0, tk.END)

        # Disable priority entry again
        self.priority_entry.config(state='disabled')

    def fcfs(self):
        proc = sorted(self.processes, key=lambda x: x.arrival)
        time = 0
        result = "\nFCFS Scheduling Result:\n"
        total_wait = 0
        total_turn = 0
        for p in proc:
            if time < p.arrival:
                time = p.arrival
            wait = time - p.arrival
            time += p.burst
            turn = time - p.arrival
            total_wait += wait
            total_turn += turn
            result += f"Process {p.pid}: Waiting Time={wait}, Turnaround Time={turn}\n"
        result += f"\nAverage Waiting Time: {total_wait/len(proc):.2f}\n"
        result += f"Average Turnaround Time: {total_turn/len(proc):.2f}\n"
        return result

    def sjf(self):
        proc = sorted(self.processes, key=lambda x: (x.arrival, x.burst))
        time = 0
        result = "\nSJF Scheduling Result:\n"
        total_wait = 0
        total_turn = 0
        while proc:
            ready = [p for p in proc if p.arrival <= time]
            if not ready:
                time += 1
                continue
            p = min(ready, key=lambda x: x.burst)
            proc.remove(p)
            wait = time - p.arrival
            time += p.burst
            turn = time - p.arrival
            total_wait += wait
            total_turn += turn
            result += f"Process {p.pid}: Waiting Time={wait}, Turnaround Time={turn}\n"
        result += f"\nAverage Waiting Time: {total_wait/len(self.processes):.2f}\n"
        result += f"Average Turnaround Time: {total_turn/len(self.processes):.2f}\n"
        return result

    def priority(self):
        proc = sorted(self.processes, key=lambda x: (x.arrival, x.priority))
        time = 0
        result = "\nPriority Scheduling Result:\n"
        total_wait = 0
        total_turn = 0
        while proc:
            ready = [p for p in proc if p.arrival <= time]
            if not ready:
                time += 1
                continue
            p = min(ready, key=lambda x: x.priority)
            proc.remove(p)
            wait = time - p.arrival
            time += p.burst
            turn = time - p.arrival
            total_wait += wait
            total_turn += turn
            result += f"Process {p.pid}: Waiting Time={wait}, Turnaround Time={turn}\n"
        result += f"\nAverage Waiting Time: {total_wait/len(self.processes):.2f}\n"
        result += f"Average Turnaround Time: {total_turn/len(self.processes):.2f}\n"
        return result

    def round_robin(self, quantum):
        proc = sorted(self.processes, key=lambda x: x.arrival)
        queue = []
        time = 0
        result = "\nRound Robin Scheduling Result:\n"
        total_wait = 0
        total_turn = 0
        while proc or queue:
            while proc and proc[0].arrival <= time:
                queue.append(proc.pop(0))

            if queue:
                p = queue.pop(0)
                if p.start == -1:
                    p.start = time
                run_time = min(p.remaining, quantum)
                time += run_time
                p.remaining -= run_time

                while proc and proc[0].arrival <= time:
                    queue.append(proc.pop(0))

                if p.remaining > 0:
                    queue.append(p)
                else:
                    turn = time - p.arrival
                    wait = turn - p.burst
                    total_wait += wait
                    total_turn += turn
                    result += f"Process {p.pid}: Waiting Time={wait}, Turnaround Time={turn}\n"
            else:
                time += 1

        result += f"\nAverage Waiting Time: {total_wait/len(self.processes):.2f}\n"
        result += f"Average Turnaround Time: {total_turn/len(self.processes):.2f}\n"
        return result

# Launch the GUI
if __name__ == "__main__":
    root = tk.Tk()
    app = SchedulerSimulator(root)
    root.mainloop()
