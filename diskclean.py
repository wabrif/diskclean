#!/usr/bin/python

import os, time, sys, shutil

def disk_free(path):
    """
    path: string
    Gets the disk usage statistics about the given path.
    returns: free space, in kbytes.
    """

    st = os.statvfs(path)
    rtob = st.f_frsize / 1024
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
    
if __name__ == '__main__':
    #path = '/media/usb'
    path = '/home/camera/motion'
    minimumfreespace = 1000000
    cleanupfreespace = 5 * minimumfreespace
    if disk_free(path) <= minimumfreespace:
        while disk_free(path) <= cleanupfreespace:
            itemtodelete = oldest_directory(path)
            try:
                if itemtodelete != None:
                    shutil.rmtree(itemtodelete)
            except:
                print "Delete failed on ",itemtodelete
                raise