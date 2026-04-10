import tkinter as tk
from tkinter import ttk, messagebox

from fcfs import fcfs
from priority_non_preemptive import priority_non_preemptive
from data_manager import validate_process, sample_processes, export_results_to_csv


class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Mô phỏng lập lịch CPU")
        self.root.geometry("1000x700")

        self.processes = []
        self.last_results = []

        self.build_ui()

    def build_ui(self):
        # ===== Khung nhập tiến trình =====
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
        tk.Button(input_frame, text="Dữ liệu mẫu", command=self.load_sample).grid(row=1, column=5, padx=8)
        tk.Button(input_frame, text="Xóa tất cả", command=self.clear_all).grid(row=1, column=6, padx=8)

        # ===== Bảng danh sách tiến trình đã nhập =====
        process_frame = tk.LabelFrame(self.root, text="Danh sách tiến trình đã nhập", padx=10, pady=10)
        process_frame.pack(fill="x", padx=10, pady=5)

        self.process_tree = ttk.Treeview(
            process_frame,
            columns=("PID", "Arrival", "Burst", "Priority"),
            show="headings",
            height=6
        )

        for col in ("PID", "Arrival", "Burst", "Priority"):
            self.process_tree.heading(col, text=col)
            self.process_tree.column(col, width=150, anchor="center")

        self.process_tree.pack(fill="x")

        # ===== Khung thuật toán =====
        control_frame = tk.LabelFrame(self.root, text="Thuật toán", padx=10, pady=10)
        control_frame.pack(fill="x", padx=10, pady=5)

        self.algorithm = tk.StringVar(value="FCFS")
        ttk.Combobox(
            control_frame,
            textvariable=self.algorithm,
            values=["FCFS", "Priority (Non-preemptive)"],
            state="readonly",
            width=30
        ).pack(side="left", padx=10)

        tk.Button(control_frame, text="Chạy", command=self.run_algorithm).pack(side="left", padx=10)
        tk.Button(control_frame, text="Xuất CSV", command=self.export_results).pack(side="left", padx=10)

        # ===== Bảng kết quả =====
        result_frame = tk.LabelFrame(self.root, text="Kết quả", padx=10, pady=10)
        result_frame.pack(fill="both", expand=True, padx=10, pady=10)

        self.result_tree = ttk.Treeview(
            result_frame,
            columns=("PID", "Arrival", "Burst", "Priority", "Start", "Completion", "Waiting", "Turnaround"),
            show="headings",
            height=10
        )

        for col in ("PID", "Arrival", "Burst", "Priority", "Start", "Completion", "Waiting", "Turnaround"):
            self.result_tree.heading(col, text=col)
            self.result_tree.column(col, width=110, anchor="center")

        self.result_tree.pack(fill="both", expand=True)

        # ===== Thống kê =====
        self.summary_label = tk.Label(
            self.root,
            text="WT trung bình: -- | TAT trung bình: --",
            font=("Arial", 10, "bold")
        )
        self.summary_label.pack(pady=5)

    def refresh_process_tree(self):
        for item in self.process_tree.get_children():
            self.process_tree.delete(item)

        for p in self.processes:
            self.process_tree.insert(
                "",
                tk.END,
                values=(
                    p["pid"],
                    p["arrival_time"],
                    p["burst_time"],
                    p["priority"]
                )
            )

    def add_process(self):
        try:
            process = validate_process(
                self.pid_entry.get(),
                self.arrival_entry.get(),
                self.burst_entry.get(),
                self.priority_entry.get()
            )

            if any(p["pid"] == process["pid"] for p in self.processes):
                raise ValueError("Mã tiến trình đã tồn tại.")

            self.processes.append(process)
            self.refresh_process_tree()

            self.pid_entry.delete(0, tk.END)
            self.arrival_entry.delete(0, tk.END)
            self.burst_entry.delete(0, tk.END)
            self.priority_entry.delete(0, tk.END)

        except ValueError as e:
            messagebox.showerror("Lỗi", str(e))

    def load_sample(self):
        self.processes = sample_processes()
        self.last_results = []

        self.refresh_process_tree()

        for item in self.result_tree.get_children():
            self.result_tree.delete(item)

        self.summary_label.config(text="WT trung bình: -- | TAT trung bình: --")

    def clear_all(self):
        self.processes.clear()
        self.last_results.clear()

        self.pid_entry.delete(0, tk.END)
        self.arrival_entry.delete(0, tk.END)
        self.burst_entry.delete(0, tk.END)
        self.priority_entry.delete(0, tk.END)

        for item in self.process_tree.get_children():
            self.process_tree.delete(item)

        for item in self.result_tree.get_children():
            self.result_tree.delete(item)

        self.summary_label.config(text="WT trung bình: -- | TAT trung bình: --")

    def run_algorithm(self):
        if not self.processes:
            messagebox.showwarning("Cảnh báo", "Vui lòng thêm ít nhất một tiến trình.")
            return

        selected_algorithm = self.algorithm.get()

        if selected_algorithm == "FCFS":
            results = fcfs(self.processes)
        elif selected_algorithm == "Priority (Non-preemptive)":
            results = priority_non_preemptive(self.processes)
        else:
            messagebox.showerror("Lỗi", "Thuật toán không hợp lệ.")
            return

        self.last_results = results

        for item in self.result_tree.get_children():
            self.result_tree.delete(item)

        for r in results:
            self.result_tree.insert(
                "",
                tk.END,
                values=(
                    r["pid"],
                    r["arrival_time"],
                    r["burst_time"],
                    r["priority"],
                    r["start_time"],
                    r["completion_time"],
                    r["waiting_time"],
                    r["turnaround_time"]
                )
            )

        avg_wt = sum(p["waiting_time"] for p in results) / len(results)
        avg_tat = sum(p["turnaround_time"] for p in results) / len(results)

        self.summary_label.config(
            text=f"WT trung bình: {avg_wt:.2f} | TAT trung bình: {avg_tat:.2f}"
        )

    def export_results(self):
        if not self.last_results:
            messagebox.showwarning("Cảnh báo", "Chưa có kết quả để xuất.")
            return

        algorithm_name = self.algorithm.get()
        file_path = export_results_to_csv(self.last_results, algorithm_name)

        messagebox.showinfo(
            "Thành công",
            f"Đã xuất file CSV tại:\n{file_path}"
        )