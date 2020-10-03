from .util import *

class ServiceManager:
    '''A ServiceManager is the main object that will control things like startup, and basically all logic.
    scandirs should be the list of directories to load services from, if doing so.'''
    def __init__(self, scandirs=["./tests/scandir_services"]):
        self.scandirs = scandirs
        self.services = []

    def run_from_dir(self):
        '''Runs all services found in directories listed in self.scandirs'''
        for i in self.scandirs:
            for j in os.listdir(i):
                self.services.append(create_service(f"{i}/{j}", self))
        for k in self.services:
            k.service_obj.check_requirements() #Todo: remove service from list if it has unfulfilled install requirements
            k.start()
            for l in k.service_obj.triggers:
                if not l.running:
                    l.thread_obj.start()