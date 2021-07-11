
from flask import request, render_template
from src.Timer import Timer
from src.IpManager import IpManager

class MyLimiter(object):

    def __init__(self, arg1):
        self.time = Timer()
        self.ipManager = IpManager()
        splited = arg1.split('/')
        self.number = splited[0]
        self.unit = splited[1]
        self.unitValue = self.unitConverter()
    
    def limitedManager(self):

        try:
            int(self.number)
        except ValueError:
            return 'error in number value'

        if self.unitValue == 0:
            return 'error in unit value'

        if self.time.getTime() > int(self.number) * self.unitValue:
            self.time.reset()
            self.ipManager.removeIP(request.environ.get('HTTP_X_REAL_IP', request.remote_addr))

        if self.time.getTime() < int(self.number) * self.unitValue and self.ipManager.ipValidation(request.environ.get('HTTP_X_REAL_IP', request.remote_addr)):
            return render_template('429.html')
        return 'normal page'

    def unitConverter(self):
        if self.unit == 'second':
            return 1
        if self.unit == 'minute':
            return 60
        if self.unit == 'hour':
            return 3600
        if self.unit == 'day':
            return 86400 
        return 0

    def __call__(self, *args, **kwargs):
        def inner_func(*args, **kwargs):
            self.ipManager.saveIP(request.environ.get('HTTP_X_REAL_IP', request.remote_addr))
            if self.time.getTime() == 0:
                self.time.start()
                return 'normal page'
            return self.limitedManager()            
        return inner_func

