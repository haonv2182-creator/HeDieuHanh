def priority_non_preemptive(processes):
    # Tạo bản sao để không làm thay đổi dữ liệu gốc
    copied_processes = [p.copy() for p in processes]

    n = len(copied_processes)
    visited = [False] * n
    completed = 0
    current_time = 0
    result = []

    while completed < n:
        idx = -1

        for i in range(n):
            if not visited[i] and copied_processes[i]["arrival_time"] <= current_time:
                if idx == -1:
                    idx = i
                else:
                    # Tie-break:
                    # 1. priority nhỏ hơn
                    # 2. arrival_time nhỏ hơn
                    # 3. pid nhỏ hơn
                    if copied_processes[i]["priority"] < copied_processes[idx]["priority"]:
                        idx = i
                    elif copied_processes[i]["priority"] == copied_processes[idx]["priority"]:
                        if copied_processes[i]["arrival_time"] < copied_processes[idx]["arrival_time"]:
                            idx = i
                        elif copied_processes[i]["arrival_time"] == copied_processes[idx]["arrival_time"]:
                            if str(copied_processes[i]["pid"]) < str(copied_processes[idx]["pid"]):
                                idx = i

        # Nếu chưa có process nào đến thì CPU rảnh
        if idx == -1:
            current_time += 1
            continue

        p = copied_processes[idx]

        p["start_time"] = current_time
        p["completion_time"] = p["start_time"] + p["burst_time"]
        p["turnaround_time"] = p["completion_time"] - p["arrival_time"]
        p["waiting_time"] = p["start_time"] - p["arrival_time"]

        current_time = p["completion_time"]
        visited[idx] = True
        completed += 1
        result.append(p)

    return result


if __name__ == "__main__":
    test_processes = [
        {"pid": "P1", "arrival_time": 0, "burst_time": 4, "priority": 2},
        {"pid": "P2", "arrival_time": 1, "burst_time": 3, "priority": 1},
        {"pid": "P3", "arrival_time": 2, "burst_time": 1, "priority": 3},
        {"pid": "P4", "arrival_time": 3, "burst_time": 2, "priority": 2},
    ]

    result = priority_non_preemptive(test_processes)

    print("PID AT BT PR ST CT WT TAT")
    for p in result:
        print(
            f"{p['pid']:>3} {p['arrival_time']:>2} {p['burst_time']:>2} {p['priority']:>2} "
            f"{p['start_time']:>2} {p['completion_time']:>2} {p['waiting_time']:>2} {p['turnaround_time']:>3}"
        )