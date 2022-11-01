import platform
import subprocess
import sys, os
import time

KB_ADDR_R = 0x1803
KB_ADDR_G = 0x1805
KB_ADDR_B = 0x1808


def set_rgb(r, g, b):
    r = rerange(r)
    g = rerange(g)
    b = rerange(b)

    write_acpi(KB_ADDR_R, r)
    write_acpi(KB_ADDR_G, g)
    write_acpi(KB_ADDR_B, b)
    return


def get_rgb():
    r = read_acpi(KB_ADDR_R)
    g = read_acpi(KB_ADDR_G)
    b = read_acpi(KB_ADDR_B)
    return (r, g, b)


def rerange(value):
    return int(value * 200 / 255)


def read_acpi(address):
    data = op_ulong(0x10000000000 + address)
    return data & 255


def write_acpi(address, value):
    return op_ulong((value << 16) + address)


def op_ulong(data):
    acpi_class = "\_SB.AMW0.WMBC"
    instance = 0
    method = 4
    return acpi_call(acpi_class, instance, method, data)


def acpi_call(acpi_class, instance, method, data):
    command = f"echo '{acpi_class} {instance} {method} {data}' | sudo tee /proc/acpi/call"

    subprocess.check_call(command, shell=True,
                          stdout=subprocess.DEVNULL)

    response = subprocess.check_output(
        "sudo cat /proc/acpi/call", shell=True)


if __name__ == '__main__':
    black = (0, 0, 0)
    white = (255, 255, 255)
    red = (255, 0, 0)
    green = (0, 128, 0)
    blue = (0, 0, 255)

    for color in (black, white, red, green, blue, black):
        print(f"Setting {color}")
        set_rgb(*color)
        time.sleep(2)
