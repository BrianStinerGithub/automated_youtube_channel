from shutil import rmtree
from config import *
import os

def cleanup():
    rmtree(OUTPUTPATH, ignore_errors=True)
    try:
        os.remove(OUTPUTPATH)
    except OSError as e:  ## if failed, report it back to the user ##
        print ("Error: %s - %s." % (e.filename, e.strerror))


if __name__ == "__main__":
    print("Removing temp files!")
    cleanup()
    print("Removed temp files!")