import os
import shutil
import fileinput
import sys

root_file = "scripts/day04.py"
def main():
    for day in range(5, 26):
        n = str(day)
        if len(n) == 1:
            n = f"0{n}"
        filename = f"scripts/day{n}.py"
        shutil.copy(root_file, filename)

        for line in fileinput.input(filename, inplace=1):
            if 'DAY_NUM =' in line:
                print(f'DAY_NUM = "{n}"', end='\n')
            else:
                print(line, end='')

    # for day in range(3, 26):
    #     n = str(day)
    #     if len(n) == 1:
    #         n = f"0{n}"
    #     os.mkdir(f"inputs/{n}")
    #     with open(f"inputs/{n}/input.txt", 'a'):
    #         os.utime(f"inputs/{n}/input.txt")
    #     with open(f"inputs/{n}/example.txt", 'a'):
    #         os.utime(f"inputs/{n}/example.txt")


if __name__ == "__main__":
    main()
