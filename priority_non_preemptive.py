class Process:
    def __init__(self, pid, arrival, burst, priority):
        self.pid = pid
        self.arrival = arrival
        self.burst = burst
        self.priority = priority

        self.start = 0
        self.completion = 0
        self.waiting = 0
        self.turnaround = 0


def priority_non_preemptive(processes):
    n = len(processes)
    time = 0
    completed = 0
    visited = [False] * n

    result = []

    while completed < n:
        idx = -1
        best_priority = float('inf')

        for i in range(n):
            if (not visited[i]) and processes[i].arrival <= time:
                if processes[i].priority < best_priority:
                    best_priority = processes[i].priority
                    idx = i

        # Nếu không có process nào đến → CPU rảnh
        if idx == -1:
            time += 1
            continue

        p = processes[idx]

        p.start = time
        p.completion = time + p.burst
        p.turnaround = p.completion - p.arrival
        p.waiting = p.start - p.arrival

        time = p.completion
        visited[idx] = True
        completed += 1

        result.append(p)

    return result

#test file 
if __name__ == "__main__":
    print("=== TEST PRIORITY NON-PREEMPTIVE ===")

    processes = [
        Process("P1", 0, 4, 2),
        Process("P2", 1, 3, 1),
        Process("P3", 2, 1, 3),
        Process("P4", 3, 2, 2),
    ]

    result = priority_non_preemptive(processes)

    print("\nPID | AT | BT | PR | ST | CT | WT | TAT")
    print("----------------------------------------")

    for p in result:
        print(f"{p.pid:>3} | {p.arrival:>2} | {p.burst:>2} | {p.priority:>2} | "
              f"{p.start:>2} | {p.completion:>2} | {p.waiting:>2} | {p.turnaround:>3}")