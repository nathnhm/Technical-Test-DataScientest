class IpManager(object):

    def __init__(self):
        self.array = []
    
    def saveIP(self, ip):
        if ip not in self.array:
            self.array.append(ip)
    
    def removeIP(self, ip):
        self.array.remove(ip)

    def ipValidation(self, ip):
        if ip in self.array:
            return True
        return False
    