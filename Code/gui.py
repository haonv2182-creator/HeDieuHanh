import tkinter as tk
from tkinter import ttk, messagebox, filedialog

from fcfs import fcfs
from priority_non_preemptive import priority_non_preemptive
from data_manager import (
    validate_process,
    sample_processes,
    export_results_to_csv,
    load_processes_from_csv
)


class App:
    # Hàm khởi tạo cửa sổ chính và dữ liệu ban đầu của giao diện
    def __init__(self, root):
        self.root = root
        self.root.title("Mô phỏng lập lịch CPU")
        self.root.geometry("1200x850")
        self.root.minsize(1000, 700)

        self.processes = []
        self.last_results = []

        self.build_scrollable_layout()
        self.build_ui()

    # Hàm tạo bố cục giao diện có thanh cuộn dọc cho toàn bộ cửa sổ
    def build_scrollable_layout(self):
        self.main_canvas = tk.Canvas(self.root)
        self.main_canvas.pack(side="left", fill="both", expand=True)

        self.scrollbar_y = tk.Scrollbar(self.root, orient="vertical", command=self.main_canvas.yview)
        self.scrollbar_y.pack(side="right", fill="y")

        self.main_canvas.configure(yscrollcommand=self.scrollbar_y.set)

        self.main_frame = tk.Frame(self.main_canvas)
        self.canvas_window = self.main_canvas.create_window((0, 0), window=self.main_frame, anchor="nw")

        self.main_frame.bind("<Configure>", self.on_frame_configure)
        self.main_canvas.bind("<Configure>", self.on_canvas_configure)

        self.main_canvas.bind_all("<MouseWheel>", self.on_mousewheel)

    # Hàm cập nhật vùng cuộn khi nội dung giao diện thay đổi
    def on_frame_configure(self, event):
        self.main_canvas.configure(scrollregion=self.main_canvas.bbox("all"))

    # Hàm cập nhật độ rộng vùng chứa theo độ rộng cửa sổ
    def on_canvas_configure(self, event):
        self.main_canvas.itemconfig(self.canvas_window, width=event.width)

    # Hàm hỗ trợ cuộn chuột cho giao diện
    def on_mousewheel(self, event):
        self.main_canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    # Hàm xây dựng toàn bộ giao diện chính của chương trình
    def build_ui(self):
        # ===== Khung nhập tiến trình =====
        input_frame = tk.LabelFrame(self.main_frame, text="Nhập tiến trình", padx=10, pady=10)
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
        tk.Button(input_frame, text="Nạp CSV", command=self.load_from_csv).grid(row=1, column=6, padx=8)
        tk.Button(input_frame, text="Xóa tất cả", command=self.clear_all).grid(row=1, column=7, padx=8)

        # ===== Bảng danh sách tiến trình đã nhập =====
        process_frame = tk.LabelFrame(self.main_frame, text="Danh sách tiến trình đã nhập", padx=10, pady=10)
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
        control_frame = tk.LabelFrame(self.main_frame, text="Thuật toán", padx=10, pady=10)
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
        result_frame = tk.LabelFrame(self.main_frame, text="Kết quả", padx=10, pady=10)
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
            self.main_frame,
            text="WT trung bình: -- | TAT trung bình: --",
            font=("Arial", 10, "bold")
        )
        self.summary_label.pack(pady=5)

        # ===== Khung Gantt Chart =====
        gantt_frame = tk.LabelFrame(self.main_frame, text="Gantt Chart", padx=10, pady=10)
        gantt_frame.pack(fill="x", padx=10, pady=5)

        self.gantt_canvas = tk.Canvas(gantt_frame, height=160, bg="white")
        self.gantt_canvas.pack(fill="x", expand=True)

    # Hàm cập nhật bảng hiển thị danh sách các tiến trình đã nhập
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

    # Hàm thêm một tiến trình mới từ dữ liệu người dùng nhập trên giao diện
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

    # Hàm nạp dữ liệu mẫu để phục vụ kiểm thử nhanh chương trình
    def load_sample(self):
        self.processes = sample_processes()
        self.last_results = []

        self.refresh_process_tree()

        for item in self.result_tree.get_children():
            self.result_tree.delete(item)

        self.summary_label.config(text="WT trung bình: -- | TAT trung bình: --")
        self.gantt_canvas.delete("all")

    # Hàm đọc danh sách tiến trình từ file CSV và hiển thị lên giao diện
    def load_from_csv(self):
        file_path = filedialog.askopenfilename(
            title="Chọn file CSV",
            filetypes=[("CSV files", "*.csv")]
        )

        if not file_path:
            return

        try:
            self.processes = load_processes_from_csv(file_path)
            self.last_results = []

            self.refresh_process_tree()

            for item in self.result_tree.get_children():
                self.result_tree.delete(item)

            self.summary_label.config(text="WT trung bình: -- | TAT trung bình: --")
            self.gantt_canvas.delete("all")

            messagebox.showinfo("Thành công", "Đã nạp dữ liệu từ file CSV.")
        except Exception as e:
            messagebox.showerror("Lỗi", str(e))

    # Hàm xóa toàn bộ dữ liệu đang có trên giao diện và đưa chương trình về trạng thái ban đầu
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
        self.gantt_canvas.delete("all")

    # Hàm chạy thuật toán lập lịch được chọn, sau đó hiển thị kết quả và biểu đồ Gantt
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

        self.root.update_idletasks()
        self.draw_gantt_chart(results)
        self.main_canvas.configure(scrollregion=self.main_canvas.bbox("all"))

    # Hàm xuất bảng kết quả của thuật toán ra file CSV
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

    # Hàm vẽ biểu đồ Gantt dựa trên kết quả thực thi của các tiến trình
    def draw_gantt_chart(self, results):
        self.gantt_canvas.delete("all")

        if not results:
            return

        canvas_width = self.gantt_canvas.winfo_width()
        if canvas_width <= 1:
            canvas_width = 1000

        margin_left = 40
        margin_right = 20
        top = 30
        bar_height = 40

        max_time = max(p["completion_time"] for p in results)
        if max_time == 0:
            return

        scale = (canvas_width - margin_left - margin_right) / max_time
        current_time = 0

        for p in results:
            start = p["start_time"]
            end = p["completion_time"]

            if start > current_time:
                idle_x1 = margin_left + current_time * scale
                idle_x2 = margin_left + start * scale

                self.gantt_canvas.create_rectangle(
                    idle_x1, top, idle_x2, top + bar_height,
                    fill="#dddddd", outline="black"
                )
                self.gantt_canvas.create_text(
                    (idle_x1 + idle_x2) / 2,
                    top + bar_height / 2,
                    text="Idle"
                )
                self.gantt_canvas.create_text(
                    idle_x1,
                    top + bar_height + 20,
                    text=str(current_time)
                )

                current_time = start

            x1 = margin_left + start * scale
            x2 = margin_left + end * scale

            self.gantt_canvas.create_rectangle(
                x1, top, x2, top + bar_height,
                fill="#87CEEB", outline="black"
            )
            self.gantt_canvas.create_text(
                (x1 + x2) / 2,
                top + bar_height / 2,
                text=str(p["pid"])
            )
            self.gantt_canvas.create_text(
                x1,
                top + bar_height + 20,
                text=str(start)
            )

            current_time = end

        final_x = margin_left + current_time * scale
        self.gantt_canvas.create_text(
            final_x,
            top + bar_height + 20,
            text=str(current_time)
        )