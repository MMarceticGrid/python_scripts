#!/usr/bin/python3

import argparse
import platform
import psutil 
import subprocess
import os


def get_distro_info():
    name = os.name
    system = platform.system()
    release  = platform.release()
    return system,name,release


def get_memory():
    memory = psutil.virtual_memory()
    return memory.total, memory.used, memory.free


def get_cpu():
    cpu_info = {
        'model': platform.processor(),
        'cores': psutil.cpu_count(logical=False),
        'threads': psutil.cpu_count(logical=True),
        'speed': psutil.cpu_freq().max 
    }
    return cpu_info


def get_user():
    return os.getlogin()


def get_load():
    load = os.getloadavg()
    return load


def get_ip():
    try:
        result = subprocess.run(['ifconfig'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        for line in result.stdout.splitlines():
            if 'inet ' in line and not '127.0.0.1' in line:
                return line.split()[1]
    except Exception as e:
        print("Error:", e)
    return None

def main():

    parser = argparse.ArgumentParser()

    parser.add_argument('-d', '--distro', action = 'store_true', help = 'This option is showing distro info')
    parser.add_argument('-m', '--memory', action = 'store_true', help = 'This option is showing memory(total, used, free)')
    parser.add_argument('-c', '--cpu', action = 'store_true', help = 'This option is showing CPU info (model, core numbers, speed)')
    parser.add_argument('-u', '--user', action = 'store_true', help = 'This option is showing current user')
    parser.add_argument('-l', '--load', action = 'store_true', help = 'This option is showing system load average')
    parser.add_argument('-i', '--ip', action = 'store_true', help = 'This option is showing IP address')

    args = parser.parse_args()
        
    if args.distro:
        system,name,release = get_distro_info()
        print(f"Distribution info: {system} {release} {name}\n")

    if args.memory:
        total, used, free = get_memory()
        print(f"Memory Total: {total / (1024 ** 3):.2f} GB")
        print(f"Memory Used: {used / (1024 ** 3):.2f} GB")
        print(f"Memory Free: {free / (1024 ** 3):.2f} GB\n")

    if args.cpu:
        cpu_info = get_cpu()
        print(f"CPU Model: {cpu_info['model']}")
        print(f"CPU Cores: {cpu_info['cores']}")
        print(f"CPU Threads: {cpu_info['threads']}")
        print(f"CPU Max Speed: {cpu_info['speed']} MHz\n")

    if args.user:
        user = get_user()
        print(f"Current User: {user}\n")

    if args.load:
        load = get_load()
        print(f"System Load Average: {load[0]:.2f} (1 min), {load[1]:.2f} (5 min), {load[2]:.2f} (15 min)\n")

    if args.ip:
        ip = get_ip()
        print(f"IP Address: {ip}\n")


if __name__ == '__main__':
    main()
