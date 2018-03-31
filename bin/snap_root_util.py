#!/usr/bin/env python3
#This script will restore the snapshot /dev/system/snap-root back to the disk,
#and Reboot the host, so that it's clean for the next set of tests
#Usage:   python3 lv.py         ------    To Create lvsnap
#         python3 lv.py -r      ------    To Restore snap-root to disk


import subprocess
import argparse
def get_lv_size():
    lv_getsize_cmd = ["sudo", "lvs", "/dev/mapper/system-root", "--no-headings", "-o", "LV_SIZE", "--nosuffix"]
    try:
        result = subprocess.run(lv_getsize_cmd, stdout=subprocess.PIPE)
        size = "-L{}".format(result.stdout.decode('utf-8').upper().strip())
        print("Setting snapshot size to {}".format(size))
        return size
    except Exception as e:
        print("lv_getsize has failed")
        print(e)

def lvcreate():
    lvcreate_cmd = ["sudo", "lvcreate", get_lv_size(), "-s", "-n", "snap-root", "/dev/system/root"]
    try:
        subprocess.run(lvcreate_cmd)
        return True
    except Exception as e:
        print("lvcreate has failed")
        print(e)

def lvrestore():
    lvrestore_cmd = ["sudo", "-i", "lvconvert", "--merge", "/dev/system/snap-root"]
    try:
        subprocess.run(lvrestore_cmd)
        return True
    except Exception as e:
        print("lvrestore has failed")
        print(e)

parser = argparse.ArgumentParser()

parser.add_argument('-r', '--restore',
                    help="restore snap-root",
                    required=False,
                    action='store_true')
args = parser.parse_args()


if args.restore is not True:
    lvcreate()
else:
    lvrestore()
    subprocess.run(["sudo", "reboot"])
