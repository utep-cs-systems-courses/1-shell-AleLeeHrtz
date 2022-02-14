import os
import sys
import re

# Create a child process
# using os.fork() method
print("starting pid")
pid = os.fork()
print("pid done")

# pid greater than 0 represents
# the parent process
if pid > 0:
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