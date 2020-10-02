from .util import *

class ServiceManager:
    '''A ServiceManager is the main object that will control things like startup, and basically all logic.
    scandirs should be the list of directories to load services from, if doing so.'''
    def __init__(self, scandirs=["./tests/scandir_services"]):
        self.scandirs = scandirs
        self.services = []

    def run_from_dir_nocheck():
        '''Runs all services found in directories listed in self.scandirs without checking for requirements, dependencies, etc.'''
        for i in self.scandirs:
            for j in os.scandir(i):
                self.services.append(create_service(f"{i}/{j}"))
        for k in self.services:
            k.start()