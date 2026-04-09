def fcfs(processes):
    # Tạo bản sao để không làm thay đổi dữ liệu gốc
    sorted_processes = [p.copy() for p in processes]

    # Sắp xếp theo arrival_time, nếu trùng thì theo pid
    sorted_processes.sort(key=lambda x: (x["arrival_time"], x["pid"]))

    current_time = 0

    for p in sorted_processes:
        if current_time < p["arrival_time"]:
            current_time = p["arrival_time"]

        p["start_time"] = current_time
        p["completion_time"] = p["start_time"] + p["burst_time"]
        p["turnaround_time"] = p["completion_time"] - p["arrival_time"]
        p["waiting_time"] = p["start_time"] - p["arrival_time"]

        current_time = p["completion_time"]

    return sorted_processes


if __name__ == "__main__":
    test_processes = [
        {"pid": "P1", "arrival_time": 0, "burst_time": 5, "priority": 2},
        {"pid": "P2", "arrival_time": 1, "burst_time": 3, "priority": 1},
        {"pid": "P3", "arrival_time": 2, "burst_time": 2, "priority": 3},
    ]

    result = fcfs(test_processes)

    print("PID AT BT PR ST CT WT TAT")
    for p in result:
        print(
            f"{p['pid']:>3} {p['arrival_time']:>2} {p['burst_time']:>2} {p['priority']:>2} "
            f"{p['start_time']:>2} {p['completion_time']:>2} {p['waiting_time']:>2} {p['turnaround_time']:>3}"
        )
    # FCFS kh cần dùng priority, giữ để thống nhất dữ liệu với các thuật toán khác
     