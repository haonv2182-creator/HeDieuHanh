def fcfs(processes):
    # Sắp xếp theo arrival_time
    processes.sort(key=lambda x: (x["arrival_time"], x["pid"]))

    current_time = 0

    for p in processes:
        if current_time < p["arrival_time"]:
            current_time = p["arrival_time"]

        p["start_time"] = current_time
        p["completion_time"] = p["start_time"] + p["burst_time"]
        p["turnaround_time"] = p["completion_time"] - p["arrival_time"]
        p["waiting_time"] = p["start_time"] - p["arrival_time"]

        current_time = p["completion_time"]

    return processes


# ====== TEST ======
if __name__ == "__main__":
    processes = [
        {"pid": 1, "arrival_time": 0, "burst_time": 5, "priority": 2},
        {"pid": 2, "arrival_time": 1, "burst_time": 3, "priority": 1},
        {"pid": 3, "arrival_time": 2, "burst_time": 2, "priority": 3},
    ]
    
    result = fcfs(processes)

    print("PID AT BT PR ST CT WT TAT")
    for p in result:
        print(f"{p['pid']:>3} {p['arrival_time']:>2} {p['burst_time']:>2} {p['priority']:>2} "
              f"{p['start_time']:>2} {p['completion_time']:>2} {p['waiting_time']:>2} {p['turnaround_time']:>2}")
    