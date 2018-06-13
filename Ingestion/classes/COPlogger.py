import logging, time

class COPlogger:
    def __init__(self, name):
        self.logger = logging.getLogger(name)
        self.timestr = time.strftime("%Y-%m-%d-%H%M%S")
        self.hdlr = logging.FileHandler("C:/data/ScriptingCopernicusMII/Ingestion/Logging/" + name + self.timestr + ".log")
        self.formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
        self.hdlr.setFormatter(self.formatter)
        self.logger.addHandler(self.hdlr)
        self.logger.setLevel(logging.INFO)