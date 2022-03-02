import os, sys, time, re

def pipeEx(inp):

    pr, pw = os.pipe()

    rc = os.fork()

    if rc < 0:
        print("fork failed, returning %d\n" % rc, file=sys.stderr)
        sys.exit(1)

    elif rc == 0:  # child

        args = [inp[0], inp[1]]

        os.close(1)  # redirect child's stdout
        os.dup(pw)
        os.set_inheritable(1, True)

        # exec 1

        for dir in re.split(":", os.environ['PATH']):  # try each directory in the path
            program = "%s/%s" % (dir, args[0])

            try:
                os.execve(program, args, os.environ)  # trying idk
            except FileNotFoundError:  # ...expected
                pass  # ...fail quietly

        os.write(2, ("%s: Command not found\n" % args[0]).encode())
        sys.exit(1)


    else:  # parent (forked ok)

        rcc = os.fork()

        if rcc < 0:
            print("fork failed, returning %d\n" % rc, file=sys.stderr)
            sys.exit(1)

        elif rcc == 0:  # child 2

            os.close(0)
            os.dup(pr)
            os.set_inheritable(0, True)

            try:
                args = [inp[3], inp[4]]

            except IndexError:
                args = [inp[3]]

            for fd in (pr, pw):
                os.close(fd)

            # print(args)

            for dir in re.split(":", os.environ['PATH']):  # try each directory in the path
                program = "%s/%s" % (dir, args[0])

                try:
                    os.execve(program, args, os.environ)  # trying idk
                except FileNotFoundError:  # ...expected
                    pass  # ...fail quietly

            os.write(2, ("%s: Command not found\n" % args[0]).encode())
            sys.exit(1)


        else:  # parent

            os.wait()
            for fd in (pr, pw):
                os.close(fd)


def redEx(inp):

    rc = os.fork()

    if rc < 0:
        sys.exit(1)

    elif rc == 0:  # child

        if  ">" in inp:
            os.close(1)  # redirect child's stdout

            temp = inp[inp.index(">") + 1: inp.index(">") + 2]

            os.open(temp[0], os.O_CREAT | os.O_WRONLY)
            os.set_inheritable(1, True)
            newinp = inp[:inp.index(">")]

        else:
            os.close(0)  # close stdin

            temp = inp[inp.index("<") + 1: inp.index("<") + 2]

            os.open(temp[0], os.O_RDONLY)  # redirect stdin
            os.set_inheritable(0, True)
            newinp = inp[:inp.index("<")]

        args = newinp
        for dir in re.split(":", os.environ['PATH']):  # try each directory in the path
            program = "%s/%s" % (dir, args[0])

            try:
                os.execve(program, args, os.environ)  # trying idk
            except FileNotFoundError:  # ...expected
                pass  # ...fail quietly

        os.write(2, ("%s: Command not found\n" % args[0]).encode())
        sys.exit(1)

    else:  # parent (forked ok)
        os.wait()



def ex(inp):

    rc = os.fork()


    if rc < 0:
        os.write(2, ("fork failed, returning %d\n" % rc).encode())
        sys.exit(1)

    elif rc == 0:  # child

        args = inp
        for dir in re.split(":", os.environ['PATH']):  # try each directory in the path
            program = "%s/%s" % (dir, args[0])

            try:
                os.execve(program, args, os.environ)  # try to exec program
            except FileNotFoundError:  # ...expected
                pass  # ...fail quietly

        os.write(2, ("%s: Command not found\n" % args[0]).encode())
        sys.exit(1)  # terminate with error

    else:  # parent (forked ok)

        os.wait()
        #os.write(1, ("Parent: Child %d terminated with exit code %d\n" % childPidCode).encode())

def chdir(dir):


    try:
        os.chdir(dir)

    except FileNotFoundError:

        os.write(0, ("Path not found\n").encode())

print("Starting shell...")

cwd = os.getcwd()
while(True):
    rawinp = str(input(cwd + "$ "))

    inp = rawinp.split()

    if (len(inp) == 0):
        continue

    elif len(inp) > 2:

        if "|" in inp:
            pipeEx(inp)
        elif "<" in inp or ">" in inp:
            redEx(inp)
        else:
            os.write(0, ("Command not found\n").encode())


    elif (inp[0] == "cd"):
        if len(inp) == 1:
            os.write(0, ("No directory specified\n").encode())
            continue

        dir = inp[1]
        chdir(dir)
        cwd = os.getcwd()
    elif (inp[0] == "exit"):
        os.write(1, ("Terminating session...").encode())
        sys.exit(0)
    else:
        ex(inp)

    cwd = os.getcwd()