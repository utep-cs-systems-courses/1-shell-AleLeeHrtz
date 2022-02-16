import os
import sys
import re

def chdir(dir):


    try:
        os.chdir(dir)

    except FileNotFoundError:

        os.write(0, ("Path not found\n").encode())

def ls():
    list = os.listdir()
    print()

    for dir in list:
        print(dir + " ")


# Create a child process
# using os.fork() method
def ex():
    print("starting pid")
    pid = os.getpid()
    print("pid done")

    print("Forking...")
    fk = os.fork()

    # pid greater than 0 represents
    # the parent process
    if fk < 0:
        os.write(0, ("fork failed, returning...\n").encode())
        sys.exit(1)
    
    print("Forked succesfully.")

    if fk > 0:
        print("I am parent process:")
        print("Process ID:", os.getpid())
        print("Child's process ID:", pid)
        print("in parent")

    # pid equal to 0 represents
    # the created child process
    else:
        print("\nI am child process:")
        print("Process ID:", os.getpid())
        print("Parent's process ID:", os.getppid())
        print("In child")

    print("out")

    # If any error occurred while
    # using os.fork() method
    # OSError will be raised

while(True):
    rawinp = str(input("$"))

    inp = rawinp.split()

    if (inp[0] == "exit"):
        sys.exit(0)

    if (inp[0] == "ls"):
        ls()

    if (inp[0] == "cd"):
        dir = inp[1]
        chdir(dir)


