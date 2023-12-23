import os
import sys
from KrampusBot import KrampusBot

def main():

    while True:
        KB = KrampusBot()
        KB.chat()


if __name__ == "__main__":
    main()
    os.execv(__file__, sys.argv) 