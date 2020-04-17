#!/usr/bin/python3

#from __future__ import print_function
#from __future__ import division

import os
import time
import sys
import shutil
import argparse


def disk_free(path):
    """
    path: string
    Gets the disk usage statistics about the given path.
    returns: free space in kbytes.
    """

    st = os.statvfs(path)
    rtob = st.f_frsize // 1024
    free = st.f_bavail * rtob
    total = st.f_blocks * rtob
    used = (st.f_blocks - st.f_bfree) * rtob
    return free

def oldest_directory(path):
    """
    path: string
    Gets the oldest directory in a path
    returns: name of the oldest directory
    """

    oldesttime = time.time()
    oldestdir = None
    for fname in os.listdir(path):
        fullpath = os.path.join(path, fname)
        if os.path.isdir(fullpath) and os.path.getmtime(fullpath) <= oldesttime:
            oldesttime = os.path.getmtime(fullpath)
            oldestdir = fullpath
    return oldestdir

def oldest_file(path):
    """
    path: string
    Gets the oldest file in a path
    returns: name of the oldest file
    """

    oldesttime = time.time()
    oldestfile = None
    for (dirpath, dirnames, filenames) in os.walk(path):
        for file in filenames:
            fullpath = os.path.join(dirpath, file)
            if os.path.getmtime(fullpath) <= oldesttime:
                oldesttime = os.path.getmtime(fullpath)
                oldestfile = fullpath
    return oldestfile

def main():
    parser = argparse.ArgumentParser(description="Check the amount of free diskspace for a directory and then delete subdirectories if space gets low")
    parser.add_argument("directory", help="Path to the directory to clean up")
    parser.add_argument("-m", "--minimumfreespace", type=int, default=10000000, help="The minimum freespace to allow before starting the clean-up")
    args = parser.parse_args()
    minimumfreespace = args.minimumfreespace
    basepath = args.directory
    if not os.path.isdir(basepath):
        print(basepath," isn't a valid directory")
        exit()
    cleanupfreespace = 5 * minimumfreespace
    if disk_free(basepath) <= minimumfreespace:
        while disk_free(basepath) <= cleanupfreespace:
            itemtodelete = oldest_directory(basepath)
            if itemtodelete == None:
                print ("Can't clear up enough freespace, no more valid directories to delete")
                exit()
            try:
                shutil.rmtree(itemtodelete)
            except:
                print ("Delete failed on ",itemtodelete)
                raise

if __name__ == '__main__':
    main()
