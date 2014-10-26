#!/usr/bin/env python

## Script that manages course content.

from git import *
import sys; import os
from time import strftime
import json
from os.path import expanduser, isfile

configFile = expanduser("~/.synccourse")

def usageAndDie():
    print '''synccourses: Syncs courses in folder specified in config file
             
    Usage: synccourse [pull|add|commit|push|sync]
    
    pull, add, commit and push correspond to their git equivalent
    sync does add + commit + push on the repos'''
    sys.exit(-1)

def noConfFileAndDie():
    print "Config file " +configFile +" not found"   
    print '''Typically contains a json object of the form:
    
    {"courseDir":"/path/to/courseDir"}
    
    The script extends the home directory (~) shortcut'''
    sys.exit(-1)

def pull(path, repo):
    repo = Repo(path, odbt=GitDB)
    repo.remotes.origin.pull()

def commit(repo):
    index = repo.index
    new_commit = index.commit("Syncing " +strftime("%m-%d %H:%M"))

def add(repo):
    index = repo.index
    index.add([diff.a_blob.path for diff in index.diff(None)])   

def main():
    if len(sys.argv) < 2:
        usageAndDie()
    if not isfile(configFile):
        noConfFileAndDie()
    json_data=open(configFile)
    data = json.load(json_data)
    courseDir = expanduser(data['courseDir'])
    json_data.close()
    intent = sys.argv[1]
    for myDir in os.listdir(courseDir):
        if os.path.isdir(courseDir +myDir):
            repo = Repo(courseDir +myDir)
            assert repo.bare == False
            repo.config_reader()
            if intent == "pull":
                pull(courseDir +myDir, repo)
            elif intent == "add":
                add()
            elif (intent == "commit") and repo.is_dirty():
                commit(repo)
            elif intent == "push":
                repo.remotes.origin.push()
            elif intent == "sync":
                add(repo)
                commit(repo)
                repo.remotes.origin.push()

main()
