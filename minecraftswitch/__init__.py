#!/usr/bin/env python
import os
import sys
import glob

MINEDIR = os.path.expanduser('~/Library/Application Support/minecraft')

# Return codes
OK = 0
ERROR = 1
BADARG = 2
NOTINIT = 3

def usage():
    return """%s <command>

Available commands:

init <name> -- set up and create new environment name
new <name> -- create new minecraft environment
switch <name> -- switch to given minecraft environment
list -- list environments
""".strip() % (sys.argv[0])

def is_initialised():
    """Return True if the init command has been run."""
    return os.path.islink(MINEDIR)

def check_initialised():
    """Complain at the user and exit if not is_initialised()."""
    if not is_initialised():
        print >> sys.stderr, "You must run '%s init <name>' first" % sys.argv[0]
        # FIXME - don't like using sys.exit in random functions.
        sys.exit(NOTINIT)

def init(*args):
    """Take the existing minecraft environment and turn it into a multi-env"""
    if len(args) != 1:
        print >> sys.stderr, "Missing argument: name for first environment"
        print >> sys.stderr, usage()
        return BADARG
    if not args[0].isalnum():
        print >> sys.stderr, "environment name must contain only a-z,A-Z,0-9"
    if is_initialised():
        print "Already initialised"
        return OK
    else:
        if not os.path.exists(MINEDIR):
            print >> sys.stderr, "Error: Minecraft not found at %s" % MINEDIR
            return ERROR
        # move the minecraft directory to a new location
        newdir = "%s.%s" % (MINEDIR, args[0])
        os.rename(MINEDIR, newdir)
        # symlink to the new location
        os.symlink(newdir, MINEDIR)
        print "Created new environment at %s" % newdir
        return OK

def new(*args):
    if len(args) != 1:
        print >> sys.stderr, "Missing argument: name for new environment"
        print >> sys.stderr, usage()
        return BADARG
    if not args[0].isalnum():
        print >> sys.stderr, "environment name must contain only a-z,A-Z,0-9"
    check_initialised()
    # create a new empty dir for the new environment
    newdir = "%s.%s" % (MINEDIR, args[0])
    os.mkdir(newdir)
    # update symlink
    os.unlink(MINEDIR)
    os.symlink(newdir, MINEDIR)
    print "Created new environment at %s" % newdir
    print "You will need to download the game data into it."

def switch(*args):
    if len(args) != 1:
        print >> sys.stderr, "Missing argument: name of environment to switch to"
        print >> sys.stderr, usage()
        return BADARG
    check_initialised()
    # check environment exists
    newdir = "%s.%s" % (MINEDIR, args[0])
    if not os.path.isdir(newdir):
        print >> sys.stderr, "No such environment (looking for %s)" % newdir
    # update symlink
    os.unlink(MINEDIR)
    os.symlink(newdir, MINEDIR)
    print "Switched to environment at %s" % newdir

def list(*args):
    check_initialised()
    dirs = glob.glob(MINEDIR + '.*')
    envs = [d[len(MINEDIR) + 1:] for d in dirs]
    if envs:
        print "Environments:"
        for env in envs:
            print " *", env
    else:
        print "No environments set up (you need to init)."

def main():
    # TODO - use getopt
    if len(sys.argv) < 2:
        print >> sys.stderr, usage()
        return BADARG

    try:
        cmd = {
            'init': init,
            'new': new,
            'switch': switch,
            'list': list
        }[sys.argv[1]]
    except KeyError:
        print >> sys.stderr, "Invalid command."
        print >> sys.stderr, usage()
        return BADARG
    return cmd(*sys.argv[2:])

if __name__ == '__main__':
    sys.exit(main())
