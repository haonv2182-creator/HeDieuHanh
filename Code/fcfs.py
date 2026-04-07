def run_fcfs(processes):
    processes = sorted([dict(p) for p in processes], key=lambda x: x["arrival"])
    current_time = 0
    results = []

    for p in processes:
        start = max(current_time, p["arrival"])
        completion = start + p["burst"]
        turnaround = completion - p["arrival"]
        waiting = turnaround - p["burst"]

        results.append({
            "pid": p["pid"],
            "arrival": p["arrival"],
            "burst": p["burst"],
            "priority": p["priority"],
            "start": start,
            "completion": completion,
            "waiting": waiting,
            "turnaround": turnaround
        })

        current_time = completion

    return results
