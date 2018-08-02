
import logging, configparser

class ParameterHandler:
    def __init__(self, logger, config_file):
        #self.datanode = datanode
        self.logger = logger
        self.config_file = config_file
        self.config = configparser.ConfigParser()

    def setConfig(self):
        self.config.read(self.config_file)
        self.logger.info("Starting Script with configuration file: " + self.config_file)
        #if(self.config_file == 'config.ini'):
            #self.logger.info("Starting Script with configuration file: " + self.config_file)
            #self.logger.info("Last connection: " + str(self.config[self.datanode]['lastConnection']))
        #elif(self.config_file == 'data_uris.ini'):
            #self.logger.info("Starting Script with data list from file: " + self.config_file)
            #print(self.config['Sentinel-1']['id_Sentinel-1'])
            #print("Check")
        return self.config

    def updateConfig(self, datanode, parameter, value):
        self.config.set(datanode, parameter, value)
        with open('config.ini', 'w') as configfile:
            self.config.write(configfile)
