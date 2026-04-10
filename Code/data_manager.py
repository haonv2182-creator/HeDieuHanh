import csv ## 
import os


def validate_process(pid, arrival, burst, priority): ## Kiểm tra tính hợp lệ của một tiến trình
    pid = str(pid).strip()
    if not pid:
        raise ValueError("Mã tiến trình không được để trống.")

    try:
        arrival = int(arrival)
        burst = int(burst)
        priority = int(priority)
    except ValueError:
        raise ValueError("Thời điểm đến, thời gian chạy và độ ưu tiên phải là số nguyên.")

    if arrival < 0:
        raise ValueError("Thời điểm đến phải >= 0.")

    if burst <= 0:
        raise ValueError("Thời gian chạy phải > 0.")

    return {
        "pid": pid,
        "arrival_time": arrival,
        "burst_time": burst,
        "priority": priority
    }


def sample_processes(): ##Hàm tạo dữ liệu mẫu để thử nghiệm, kiểm tra các thuật toán.
    return [
        {"pid": "P1", "arrival_time": 0, "burst_time": 5, "priority": 2},
        {"pid": "P2", "arrival_time": 1, "burst_time": 3, "priority": 1},
        {"pid": "P3", "arrival_time": 2, "burst_time": 2, "priority": 3},
        {"pid": "P4", "arrival_time": 4, "burst_time": 1, "priority": 2},
    ]


def load_processes_from_csv(file_path): ## Hàm đọc dữ liệu tiến trình từ file CVS
    processes = []

    with open(file_path, mode="r", encoding="utf-8-sig", newline="") as file:
        reader = csv.DictReader(file)

        if not reader.fieldnames:
            raise ValueError("File CSV không có tiêu đề cột.")

        headers = [h.strip() for h in reader.fieldnames]
        required_headers = ["pid", "arrival_time", "burst_time", "priority"]

        for header in required_headers:
            if header not in headers:
                raise ValueError(
                    "CSV phải có đủ các cột: pid, arrival_time, burst_time, priority."
                )

        for row in reader:
            normalized_row = {k.strip(): v for k, v in row.items()}

            process = validate_process(
                normalized_row.get("pid", ""),
                normalized_row.get("arrival_time", ""),
                normalized_row.get("burst_time", ""),
                normalized_row.get("priority", "")
            )
            processes.append(process)

    return processes


def export_results_to_csv(results, algorithm_name="algorithm"): ## Hàm ghi các kết quả ra file CVS
    safe_name = (
        str(algorithm_name)
        .strip()
        .replace(" ", "_")
        .replace("(", "")
        .replace(")", "")
    )

    output_folder = r"E:\HeDieuHanh\BaoCaoHeDieuHanh\HeDieuHanh\Extra\data_manager"
    os.makedirs(output_folder, exist_ok=True)

    file_name = f"ket_qua_{safe_name}.csv"
    file_path = os.path.join(output_folder, file_name)

    with open(file_path, mode="w", encoding="utf-8-sig", newline="") as file:
        writer = csv.writer(file)

        writer.writerow([
            "pid",
            "arrival_time",
            "burst_time",
            "priority",
            "start_time",
            "completion_time",
            "waiting_time",
            "turnaround_time"
        ])

        for r in results:
            writer.writerow([
                r.get("pid", ""),
                r.get("arrival_time", ""),
                r.get("burst_time", ""),
                r.get("priority", ""),
                r.get("start_time", ""),
                r.get("completion_time", ""),
                r.get("waiting_time", ""),
                r.get("turnaround_time", "")
            ])

    return file_path