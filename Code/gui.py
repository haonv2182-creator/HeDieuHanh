import tkinter as tk
from tkinter import ttk, messagebox

from fcfs import run_fcfs
from data_manager import validate_process, sample_processes


class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Mô phỏng lập lịch CPU")
        self.root.geometry("950x600")

        self.processes = []
        self.build_ui()

    def build_ui(self):
        input_frame = tk.LabelFrame(self.root, text="Nhập tiến trình", padx=10, pady=10)
        input_frame.pack(fill="x", padx=10, pady=10)

        tk.Label(input_frame, text="Mã tiến trình").grid(row=0, column=0, padx=5, pady=5)
        tk.Label(input_frame, text="Thời điểm đến").grid(row=0, column=1, padx=5, pady=5)
        tk.Label(input_frame, text="Thời gian chạy").grid(row=0, column=2, padx=5, pady=5)
        tk.Label(input_frame, text="Độ ưu tiên").grid(row=0, column=3, padx=5, pady=5)

        self.pid_entry = tk.Entry(input_frame, width=12)
        self.arrival_entry = tk.Entry(input_frame, width=12)
        self.burst_entry = tk.Entry(input_frame, width=12)
        self.priority_entry = tk.Entry(input_frame, width=12)

        self.pid_entry.grid(row=1, column=0, padx=5, pady=5)
        self.arrival_entry.grid(row=1, column=1, padx=5, pady=5)
        self.burst_entry.grid(row=1, column=2, padx=5, pady=5)
        self.priority_entry.grid(row=1, column=3, padx=5, pady=5)

        tk.Button(input_frame, text="Thêm tiến trình", command=self.add_process).grid(row=1, column=4, padx=8)
        tk.Button(input_frame, text="Xóa tất cả", command=self.clear_all).grid(row=1, column=6, padx=8)

        control_frame = tk.LabelFrame(self.root, text="Thuật toán", padx=10, pady=10)
        control_frame.pack(fill="x", padx=10, pady=5)

        self.algorithm = tk.StringVar(value="FCFS")
        ttk.Combobox(
            control_frame,
            textvariable=self.algorithm,
            values=["FCFS", "Ưu tiên (Không độc quyền)"],
            state="readonly",
            width=30
        ).pack(side="left", padx=10)

        tk.Button(control_frame, text="Chạy", command=self.run_algorithm).pack(side="left", padx=10)

        self.result_tree = ttk.Treeview(
            self.root,
            columns=("PID", "Arrival", "Burst", "Priority", "Start", "Completion", "Waiting", "Turnaround"),
            show="headings",
            height=10
        )
        for col in ("PID", "Arrival", "Burst", "Priority", "Start", "Completion", "Waiting", "Turnaround"):
            self.result_tree.heading(col, text=col)
            self.result_tree.column(col, width=110, anchor="center")
        self.result_tree.pack(fill="both", expand=True, padx=10, pady=10)

    def add_process(self):
        try:
            process = validate_process(
                self.pid_entry.get(),
                self.arrival_entry.get(),
                self.burst_entry.get(),
                self.priority_entry.get()
            )
            self.processes.append(process)

            self.pid_entry.delete(0, tk.END)
            self.arrival_entry.delete(0, tk.END)
            self.burst_entry.delete(0, tk.END)
            self.priority_entry.delete(0, tk.END)

        except ValueError as e:
            messagebox.showerror("Lỗi", str(e))

    def load_sample(self):
        self.processes = sample_processes()

    def clear_all(self):
        self.processes.clear()
        for item in self.result_tree.get_children():
            self.result_tree.delete(item)

    def run_algorithm(self):
        if not self.processes:
            messagebox.showwarning("Cảnh báo", "Vui lòng thêm ít nhất một tiến trình.")
            return

        if self.algorithm.get() != "FCFS":
            messagebox.showinfo("Thông báo", "Priority sẽ hoàn thiện ở tuần sau.")
            return

        results = run_fcfs(self.processes)

        for item in self.result_tree.get_children():
            self.result_tree.delete(item)

        for r in results:
            self.result_tree.insert(
                "",
                tk.END,
                values=(
                    r["pid"], r["arrival"], r["burst"], r["priority"],
                    r["start"], r["completion"], r["waiting"], r["turnaround"]
                )
            )
