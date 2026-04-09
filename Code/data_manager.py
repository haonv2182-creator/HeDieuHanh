def validate_process(pid, arrival, burst, priority):
    process = {
        "pid": pid.strip(),
        "arrival_time": int(arrival.strip()),
        "burst_time": int(burst.strip()),
        "priority": int(priority.strip())
    }

    if not process["pid"]:
        raise ValueError("Vui lòng nhập mã tiến trình")
    if process["arrival_time"] < 0:
        raise ValueError("Thời điểm đến phải >= 0")
    if process["burst_time"] <= 0:
        raise ValueError("Thời gian chạy phải lớn hơn 0")

    return process