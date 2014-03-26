"""
A module containing tools to deal with releases

"""

import os

from fabric.api import *
import fabtools


class ReleaseManager(object):
    """
    A class to deal with releases

    """

    def __init__(self, path=None):
        self.path = path

    def list(self):
        """Return a list of releases present in self.path"""
        if not self.path:
            return []
        return sorted(run("ls -x %s" % self.path).split())

    def latest(self):
        """Return the latest release"""
        releases = self.list()
        if not releases:
            return None
        return releases[-1]

    def previous(self):
        """Return the previous release (the one before the latest)"""
        releases = self.list()
        if len(releases) < 2:
            return None
        return releases[-2]

    def create(self):
        """
        Creates a new release in self.path

        This function does all the following tasks:
         - Cloning the repository specified by env.repository on the branch
           env.git_branch
         - Setting the release metadata into the deploy.json file
        
        It returns the full path of the new release

        """
        import json
        import time
        import platform

        now = int(time.time())
        path = os.path.join(self.path, "%d" % now)
        fabtools.require.git.working_copy(env.repository, branch=env.git_branch, path=path)
        metadata = {
            'timestamp': now,
            'user': env.local_user,
            'host': platform.node()
            }
        fabtools.require.files.file(path=os.path.join(path, 'deploy.json'),
                                    contents=json.dumps(metadata, indent=4))
        return now

    def set_current(self, release):
        """
        Sets the current release to `release` by creating a symbolic link

        """
        if not release or not self.path:
            abort("Cannot set current release: imcomplete path")
        if not env.has_key('current_path'):
            abort("Cannot set current release: current_path is not defined")
        run("ln -nfs %s %s" % (os.path.join(self.path, release), env.current_path))

    def commit(self):
        """Sets the current release to the latest one"""
        return self.set_current(self.latest())

    def rollback(self):
        """Rollback to the previous release"""
        return self.set_current(self.previous())
