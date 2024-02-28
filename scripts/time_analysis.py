from datetime import datetime

def calc_time(file_name, start_time_str, end_time_str):
    # Convert start and end time strings to datetime objects
    start_time = datetime.strptime(start_time_str, "%Y-%m-%d_%H:%M:%S")
    end_time = datetime.strptime(end_time_str, "%Y-%m-%d_%H:%M:%S")

    # Calculate the time difference
    time_difference = end_time - start_time

    # Extract hours from the time difference
    hours_between = time_difference.total_seconds() / 3600

    print(f"File: {file_name}")
    print(f"Running Time: {hours_between:.2f} hours")

def calc_file_times(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()

    blocks = [lines[i:i+4] for i in range(0, len(lines), 4)]

    for block in blocks:
        name_of_file = block[0].strip()
        start_time_str = block[2].strip()
        end_time_str = block[3].strip()
        calc_time(name_of_file, start_time_str, end_time_str)

if __name__ == '__main__':
    calc_file_times("error_logs/cpus/summary")