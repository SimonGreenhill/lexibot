# coding=utf-8
import os
import logging
import subprocess
from pathlib import Path

import git


class Lexibot:
    def __init__(self, path):
        self.path = Path(path)
        
        if not self.path.exists():
            raise IOError("%s is not found" % self.path)
        
        self.log = logging.getLogger(path.stem)
        
        try:
            self.repo = git.Repo(path)
        except git.InvalidGitRepositoryError:
            self.repo = None
            
        self.dirty = False
        self.errors = []
        
    def __repr__(self):
        return "<Lexibot: %s>" % self.id

    @property
    def id(self):
        return self.path.stem
        
    @property
    def virtualenv(self):
        """Where the virtualenv is"""
        return (self.path.parent / ("%s.env" % str(self.path.name))).resolve()

    @property
    def python(self):
        """Path to the python 3 interpreter"""
        return self.virtualenv / 'bin' / 'python3'

    def get_env_vars(self):
        """Variables needed for virtualenv environment"""
        return {
            "VIRTUAL_ENV": str(self.virtualenv),
            "PATH": "%s%s%s" % (self.virtualenv / 'bin', os.pathsep, os.environ.get('PATH', ''))
        }

    def run(self):
        """Does everything"""
        self.update_repository()
        self.install_virtualenv()
        
        if self.dirty:  # rebuild!
            self.make_cldf()
        
        # check
        invalids = self.validate()
        warnings = self.lexibank_checks()
        differences = self.compare_cldf()
        
        if invalids or differences or warnings:
            self.notify(invalids, differences, warnings)
        
    def update_repository(self):
        """Update git repository"""
        # if not a git repository, skip
        if not self.repo:
            return
        
        # check we're on branch master
        if self.repo.active_branch.name != 'master':
            self.log.warn('Not on git branch master, in %s' % self.repo.active_branch.name)
            self.repo.heads.master.checkout()
        
        current = self.repo.head.object.hexsha
        self.log.debug('Current git hash = %s' % current)
        incoming = self.repo.head.object.hexsha
        self.log.debug('Current remote git hash = %s' % incoming)
        
        if current != incoming:
            self.log.info('Current git hash is outdated %s < %s -- setting dirty' % (current, incoming))
            self.dirty = True
            self.repo.remotes.origin.pull()
    
    def install_virtualenv(self):
        if not self.virtualenv.exists():
            self.log.info('creating virtualenv in %s' % self.virtualenv)
            subprocess.run(
                ["python", "-m", "venv", str(self.virtualenv)],
                check=True, capture_output=True
            )
            self.dirty = True  # first run, make it dirty
        
        # run dataset/setup.py
        self.log.debug('installing dataset in %s' % self.virtualenv)
        subprocess.run(
            [self.python, 'setup.py', "develop"],
            check=True, capture_output=True,
            cwd=self.path, env=self.get_env_vars()
        )
        
        # TODO: how to check that we have the latest pacakges?
        self.dirty = True
        
        
    def make_cldf(self):
        """Make the CLDF dataset"""
        self.log.debug('running make_cldf')
        p = subprocess.run(
            ["cldfbench", "lexibank.makecldf", self.id],
            # TODO specify glottolog and concepticon versions explicitly?
            check=True, capture_output=True,
            cwd=self.path, env=self.get_env_vars()
        )
        if p.stderr:
            return p.stderr.decode('utf8').split("\n")
        return
        
    def validate(self):
        """Run CLDF validate"""
        self.log.debug('running cldf validate')
        p = subprocess.run(
            ["cldf", "validate", "cldf/cldf-metadata.json"],
            check=True, capture_output=True,
            cwd=self.path, env=self.get_env_vars()
        )
        if p.stderr:
            return p.stderr.decode('utf8').split("\n")
        return
        
    def lexibank_checks(self):
        """Run the checks defined in pylexibank"""
        # TODO fails for now as checks are not yet in released version
        # p = subprocess.run(
        #     ["cldfbench", "--log-level", "WARN", "lexibank.check", self.id],
        #     check=True, capture_output=True,
        #     cwd=self.path, env=self.get_env_vars()
        # )
        # if p.stderr:
        #     return p.stderr.split("\n")
        return

    def compare_cldf(self):
        pass
    
    def notify(self, invalids, differences, warnings):
        for error in (invalids, differences, warnings):
            print(error)
        
