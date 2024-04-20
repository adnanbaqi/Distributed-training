import subprocess
import datetime

def print_current_time():
    current_time = datetime.datetime.now()
    print(f"Current system time: {current_time}")


def check_and_sync_time():
    print("Checking initial system time:")
    print_current_time()

    try:
        subprocess.run(['sudo', 'ntpdate', 'pool.ntp.org'], check=False)
        print("Time synchronized successfully.")
    except FileNotFoundError:
        print("ntpdate is not installed. Installing now...")
        subprocess.run(['sudo', 'apt-get', 'install', '-y', 'ntpdate'])
        print("Attempting to synchronize time after installation:")
        subprocess.run(['sudo', 'ntpdate', 'pool.ntp.org'])
    except subprocess.CalledProcessError:
        print("Failed to synchronize time. Check your network connection or server availability.")

    print("Final system time after attempting synchronization:")
    print_current_time()

check_and_sync_time()
