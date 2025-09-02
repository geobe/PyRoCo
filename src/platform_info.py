# importing module
import platform

def test_platform():
    # dictionary
    print("hello platform!")
    info = {}

    # platform details
    platform_details = platform.platform()

    # adding it to dictionary
    info["platform details"] = platform_details

    # system name
    system_name = platform.system()

    # adding it to dictionary
    info["system name"] = system_name

    # processor name
    processor_name = platform.processor()

    # adding it to dictionary
    info["processor name"] = processor_name

    # machine info
    machine_info = platform.machine()

    # adding it to dictionary
    info["machine info"] = machine_info

    # architectural detail
    architecture_details = platform.architecture()

    # adding it to dictionary
    info["architectural detail"] = architecture_details

    # printing the details
    for i, j in info.items():
        print(i, " - ", j)

    if 'aarch64' in machine_info:
        print("I'm a raspi!")
    else:
        print("Oh no, not a raspi")

if __name__ == "__main__":
    test_platform()