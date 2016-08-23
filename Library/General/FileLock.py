"""
A file lock implementation that tries to avoid platform specific
issues. It is inspired by a whole bunch of different implementations
listed below.
 - https://bitbucket.org/jaraco/yg.lockfile/src/6c448dcbf6e5/yg/lockfile/__init__.py
 - http://svn.zope.org/zc.lockfile/trunk/src/zc/lockfile/__init__.py?rev=121133&view=markup
 - http://stackoverflow.com/questions/489861/locking-a-file-in-python
 - http://www.evanfosmark.com/2009/01/cross-platform-file-locking-support-in-python/
 - http://packages.python.org/lockfile/lockfile.html
There are some tests below and a blog posting conceptually the
problems I wanted to try and solve. The tests reflect these ideas.
 - http://ionrock.wordpress.com/2012/06/28/file-locking-in-python/
I'm not advocating using this package. But if you do happen to try it
out and have suggestions please let me know.
"""
import os
import time


class FileLocked(Exception): pass


class FileLock(object):

    def __init__(self, fname, timeout=None, force=False):
        self.fname = fname
        self.lockfname = '%s.lock' % self.fname
        self.timeout = timeout
        self.force = force
        self.fh = None

        self.flags = os.O_CREAT | os.O_RDWR
        try:
            # *nix flags
            self.flags = self.flags | os.O_EXLOCK
        except AttributeError:
            # windows flags (not sure this is correct)
            self.flags = self.flags | os.O_NOINHERIT

    def valid_lock(self):
        """
        See if the lock exists and is left over from an old process.
        """

        if not os.path.exists(self.lockfname):
            return False

        my_pid = os.getpid()
        lock_pid = int(open(self.lockfname).read())

        # this is our process
        if my_pid == lock_pid:
            return True

        # it is/was another process
        # see if it is running
        try:
            os.kill(lock_pid, 0)
        except OSError:
            os.remove(self.lockfname)
            return False

        # it is running
        return True

    def is_locked(self, force=False):
        # We aren't locked
        if not self.valid_lock():
            return False

        # We are locked, but we want to force it without waiting
        if not self.timeout:
            if self.force:
                self.release()
                return False
            else:
                # We're not waiting or forcing the lock
                raise FileLocked()

        # Locked, but want to wait for an unlock
        interval = .1
        intervals = int(self.timeout / interval)

        while intervals:
            if self.valid_lock():
                intervals -= 1
                time.sleep(interval)
                print('stopping %s' % intervals)
            else:
                return True

        # check one last time
        if self.valid_lock():
            if self.force:
                self.release()
            else:
                # still locked :(
                raise FileLocked()

    def acquire(self):
        self.fh = os.open(self.lockfname, self.flags)
        os.write(self.fh, str(os.getpid()))

    def release(self):
        if self.fh:
            os.close(self.fh)
        os.remove(self.lockfname)

    def __enter__(self):
        if not self.is_locked():
            self.acquire()
        return self

    def __exit__(self, type, value, traceback):
        self.release()


class TestProcessKilled(object):

    def test_process_killed_force_unlock(self):
        lockfile = 'test.txt.lock'
        with open(lockfile, 'w+') as f:
            f.write('9999999')
        assert os.path.exists(lockfile)
        with FileLock('test.txt'):
            assert True

    def test_force_unlock_in_same_process(self):
        lockfile = 'test.txt.lock'
        with open(lockfile, 'w+') as f:
            f.write(str(os.getpid()))

        with FileLock('test.txt', force=True):
            assert True

    def test_exception_after_timeout(self):
        lockfile = 'test.txt.lock'
        with open(lockfile, 'w+') as f:
            f.write(str(os.getpid()))

        try:
            with FileLock('test.txt', timeout=1):
                assert False
        except FileLocked:
            assert True

    def test_force_after_timeout(self):
        lockfile = 'test.txt.lock'
        with open(lockfile, 'w+') as f:
            f.write(str(os.getpid()))

        timeout = 1
        start = time.time()
        with FileLock('test.txt', timeout=timeout, force=True):
            assert True
        end = time.time()
        assert end - start > timeout