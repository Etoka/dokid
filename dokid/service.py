import configparser, os, threading

class Service:
    '''The class for a dokid service. Don't use this directly, but instaed use create_service().'''
    def __init__(self, name, path):
        self.name = name
        self.path = path
        self.__config = configparser.ConfigParser()
        self.__config.read(path)
        self.__bconfig = self.__config["Basic"]
        self.exe = self.__bconfig["EXEPath"]
        self.type = self.__bconfig["Type"]

    def run_immediate_no_args(self):
        '''Runs the defined executable without any arguments.'''
        os.system(self.exe) #Change to use subprocess so we can get the output

class ServiceThread(threading.Thread):
    '''A subclass of threading.Thread used for Service objects. It takes one argument, the Service object.'''
    def __init__(self, service):
        super().__init__()
        self.service_obj = service

    def run(self):
        self.service_obj.run_immediate_no_args()