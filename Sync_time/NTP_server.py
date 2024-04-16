import os
import subprocess

# Check if ntpdate is installed and synchronize time
def check_and_sync_time():
    try:
        # Try running ntpdate to check if it is installed
        subprocess.run(['ntpdate', '-q', 'pool.ntp.org'], check=True)
    except FileNotFoundError:
        # If not installed, install it (you may need to use a different package manager depending on the OS)
        print("ntpdate is not installed. Installing now...")
        subprocess.run(['sudo', 'apt-get', 'install', '-y', 'ntpdate'])
        # After installation, synchronize time
        subprocess.run(['sudo', 'ntpdate', 'pool.ntp.org'])

# Call the time synchronization function at the start
check_and_sync_time()