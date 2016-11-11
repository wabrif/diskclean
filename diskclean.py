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
    for dir in os.listdir(path):
        fullpath = path+'/'+dir
        if os.path.getmtime(fullpath) <= oldesttime:
            oldesttime= os.path.getmtime(fullpath)
            oldestdir = fullpath
    return oldestdir
    
if __name__ == '__main__':
    root = '/media/usb'
    path = '/media/usb'
    minimumfreespace = 100 * 1024
    print minimumfreespace
    cleanupfreespace = 500 * minimumfreespace
    print disk_free(root)
    if disk_free(root) <= minimumfreespace:
        while disk_free(root) <= cleanupfreespace:
            try:
                if oldest_directory(path)!= None:
                    shutil.rmtree(oldest_directory(path))
            except:
                pass
