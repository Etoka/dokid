import configparser, os, threading

class Service:
    '''The class for a dokid service. Don't use this directly, but instaed use create_service().'''
    def __init__(self, name, path, manager):
        self.name = name
        self.path = path
        self.manager = manager
        self.running = False
        self.triggers = []
        self.thread_obj = None
        self.log("creating Service object")
        self.log(f"path: {self.path}")
        self.__config = configparser.ConfigParser()
        self.__config.read(path)
        self.__bconfig = self.__config["Basic"]
        self.__reqconfig = None
        self.exe = self.__bconfig["EXEPath"]
        self.requirements = None #Only changed if requirements given in config
        if "Type" in self.__bconfig:
            self.type = self.__bconfig["Type"]
        else:
            self.type = "OnDemand"
        if "User" in self.__bconfig:
            self.run_as = self.__bconfig["User"]
        else:
            self.run_as = "root"
        if "Requirements" in self.__config:
            self.__reqconfig = self.__config["Requirements"]
            if "WaitFor" in self.__reqconfig:
                self.require_running = self.__reqconfig["WaitFor"].split(" ")
            if "RequireInstalled" in self.__reqconfig:
                self.require_installed = self.__reqconfig["RequireInstalled"].split(" ")

    def log(self, msg):
        print(f"[dokid][{self.name}] {msg}")

    def run_immediate_no_args(self):
        '''Runs the defined executable without any arguments, as the user defined by self.run_as.'''
        self.running = True
        self.log("Started running!")
        os.system(f"/bin/su {self.run_as} -c '{self.exe}'") #Change to use subprocess so we can get the output

    def check_requirements(self, log_result=True):
        '''Checks the requirements to make sure that all are satisfied. returns True if successful and false if otherwise.'''
        if not (self.__reqconfig == None):
            if "RequireInstalled" in self.__reqconfig:
                for i in self.manager.scandirs:
                    for j in self.require_installed:
                        if j in os.listdir(i):
                            break
                        else:
                            continue
                    else:
                        break
                else:
                    if log_result:
                        self.log(f"error: {self.require_installed} is required, but not installed")
                    return False
            if "WaitFor" in self.__reqconfig:
                for j in self.manager.services:
                    if (j.service_obj.name == self.require_running) and (j.service_obj.running):
                        break
                    elif j.service_obj.name in self.require_running:
                        j.service_obj.triggers.append(self)
                    else:
                        continue
                else:
                    if log_result:
                        self.log(f"error: WaitFor is set to {self.require_running} but it is not yet running")
                    return False
        return True                

class ServiceThread(threading.Thread):
    '''A subclass of threading.Thread used for Service objects. It takes one argument, the Service object.'''
    def __init__(self, service):
        super().__init__()
        self.service_obj = service
        self.service_obj.thread_obj = self

    def run(self):
        self.service_obj.run_immediate_no_args()