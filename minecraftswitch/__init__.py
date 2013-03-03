import os
import sys
import glob
import subprocess

MINEDIR = os.path.expanduser('~/Library/Application Support/minecraft')

# Return codes
OK = 0
ERROR = 1 # Unrecoverable errors
BADARG = 2 # Invalid user arguments
NOTINIT = 3 # 'minecraft-switch init' has not been run.
RUNNING = 4 # Minecraft is running

class SwitchError(RuntimeError):
    """Errors to report to the user encountered during switching."""
    def __init__(self, code, msg):
        RuntimeError.__init__(self, code, msg)
        self.code = code
        self.msg = msg

def usage():
    return """Usage: %s <command>

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
    """Raise a SwitchError if not is_initialised()."""
    if not is_initialised():
        raise SwitchError(
            NOTINIT, "You must run '%s init <name>' first." % sys.argv[0])

def check_minecraft_not_running():
    """Raise a SwitchError if minecraft is running."""
    ps = subprocess.Popen(['/bin/ps', 'aux'], stdout=subprocess.PIPE)
    stdout, stderr = ps.communicate()
    for line in stdout.split('\n'):
        if "Minecraft.app/Contents/MacOS/JavaApplicationStub" in line:
            raise SwitchError(
                RUNNING, "Minecraft must not be running during this command.")

def init(*args):
    """Take the existing minecraft environment and turn it into a multi-env"""
    if len(args) != 1:
        print >> sys.stderr, "Missing argument: name for first environment"
        print >> sys.stderr, usage()
        return BADARG
    if not args[0].isalnum():
        print >> sys.stderr, "environment name must contain only a-z,A-Z,0-9"
    check_minecraft_not_running()
    if is_initialised():
        print "Already initialised"
        return OK
    else:
        if not os.path.exists(MINEDIR):
            raise SwitchError(ERROR, "Minecraft not found at %s" % MINEDIR)
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
    check_minecraft_not_running()
    check_initialised()
    # create a new empty dir for the new environment
    newdir = "%s.%s" % (MINEDIR, args[0])
    if os.path.exists(newdir):
        raise SwitchError(ERROR, "Environment already exists")
    os.mkdir(newdir)
    # update symlink
    os.unlink(MINEDIR)
    os.symlink(newdir, MINEDIR)
    print "Created and switched to new environment at %s" % newdir
    print "You will need to download the game data into it."

def switch(*args):
    if len(args) != 1:
        print >> sys.stderr, "Missing argument: name of environment to switch to"
        print >> sys.stderr, usage()
        return BADARG
    check_minecraft_not_running()
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
    # get current env:
    current = os.path.realpath(MINEDIR).rsplit('.', 1)[1]
    dirs = glob.glob(MINEDIR + '.*')
    envs = [d[len(MINEDIR) + 1:] for d in dirs]
    if envs:
        print "Environments (* indicates current environment):"
        for env in envs:
            if env == current:
                print " *",
            else:
                print "  ",
            print env
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
    
    try:
        return cmd(*sys.argv[2:])
    except SwitchError, e:
        print >> sys.stderr, "Error:", e.msg
        return e.code

