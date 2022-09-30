from json import dumps

""" 
assumption of uniform log messages in format: 
    TIME logTYPE ORIGIN MESSAGE
    1010 ERROR aAPI This is a message

"""
class Log:
    def __init__(self, log_str):
        self.time, self.type, self.origin, self.msg = self.initializer(log_str)

    def __str__(self):
        return dumps(dict(self), ensure_ascii=False)

    def __repr__(self):
        return self.__str__()

    def __iter__(self):
        yield from {
            "time": self.time,
            "type": self.type,
            "origin": self.origin,
            "message": self.msg
        }.items()
    
    def initializer(self, str):
        logData = str.split(" ")
        time, logType, origin, msg = logData[0], logData[1], logData[2], " ".join(logData[3:])
        return time, logType.lower(), origin, msg.strip()


class Library:
    def __init__(self):
        self.errors = []
        self.infos = []
        self.warnings = []
        self.others = []
    
    def __repr__(self):
        return f"{len(self.infos)} info; {len(self.warnings)} warning; {len(self.errors)} error;"

    def ingestLog(self, log):
        if log.type == "info":
            self.infos.append(log.__dict__)
        elif log.type == "warning":
            self.warnings.append(log.__dict__)
        elif log.type == "error":
            self.errors.append(log.__dict__)
        else:
            self.others.append(log.__dict__)
    
    def ingestLogStream(self, filePath):
        cntr = 0
        with open(filePath, 'r') as f:
            for logRecord in f:
                tmp = Log(logRecord)
                self.ingestLog(tmp)
                cntr += 1
        print(f"Ingested {cntr} logs from {filePath}.")
    
    def getErrors(self):
        return self.errors