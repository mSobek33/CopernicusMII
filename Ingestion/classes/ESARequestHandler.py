import requests, time, sys, collections, json

class ESARequestHandler:
    def __init__(self, logger, paramHandler):
        self.logger = logger
        self.paramHandler = paramHandler
        #self.config = paramHandler.setConfig()
        self.baseURL = "https://scihub.copernicus.eu/dhus/search"
        #self.countURL = "https://scihub.copernicus.eu/dhus/api/stub/products/count"
        self.request = None
        self.pages = None


    def getPages(self, user, password):
        countURL = "https://scihub.copernicus.eu/dhus/api/stub/products/count?filter=%20%20(ingestiondate:["+self.paramHandler.config['ESA']['lastConnection']+"%20TO%20NOW])"
        self.request = requests.get(countURL, auth=(user, password))
        if(self.request.status_code == 503):
            self.logger.warning("Service is temporally not available")
            self.logger.warning("Last successful connection-date will be saved")
            self.logger.warning("Script will close")
            time.sleep(5)
            sys.exit(1)
            # exit
        else:
            self.pages = int(int(self.request.text) / 100) + (int(self.request.text) % 100 > 0)
            self.logger.info("Total data: " + self.request.text)
            self.logger.info("Pages from initial count-request: " + str(self.pages))
            print(self.pages)
            return self.pages


    def makeTimeSpanRequest(self, start, user, password):

        #url = "https://scihub.copernicus.eu/dhus/search?q=ingestiondate:["+self.paramHandler.config['ESA']['lastConnection']+"%20TO%20NOW]&format=json&rows=100"
        #self.baseURL = "https://scihub.copernicus.eu/dhus/search"
        #self.countURL = "https://scihub.copernicus.eu/dhus/api/stub/products/count?filter=%20%20(ingestiondate:["+self.paramHandler.config['ESA']['lastConnection']+"%20TO%20NOW])"

        fullURL = self.baseURL + "?q=ingestiondate:[" +self.paramHandler.config['ESA']['lastConnection']+"%20TO%20NOW]&format=json&rows=100" + '&start=' + start
        print(fullURL)
        self.request = requests.get(fullURL, auth=(user, password))
        if(self.request.status_code == 503):
            if(start != 0):
                self.paramHandler.updateConfig('lastConnection', time.strftime("%Y-%m-%dT%H:%M:%S.000Z"))
            self.logger.warning("Service is temporally not available")
            self.logger.warning("Last successful connection-date will be saved")
            self.logger.warning("Script will close")
            time.sleep(5)
            sys.exit(1)
            # exit



    def makeSingleRequest(self, id, user, password):
        #url = "https://scihub.copernicus.eu/dhus/search?q=S1B_IW_GRDH_1SDV_20180624T204058_20180624T204123_011520_0152BC_FC7C&format=json"

        fullURL = "https://scihub.copernicus.eu/dhus/search?q=" + id + "&format=json"
        #print(fullURL)
        self.request = requests.get(fullURL, auth=(user, password))
        if(self.request.status_code == 503):
            #if(start != 0):
                #self.paramHandler.updateConfig('lastConnection', time.strftime("%Y-%m-%dT%H:%M:%S.000Z"))
            #self.logger.warning("Service is temporally not available")
            #self.logger.warning("Last successful connection-date will be saved")
            #self.logger.warning("Script will close")
            time.sleep(5)
            sys.exit(1)
            # exit
        else:
            #print("Letzter erfolgreicher Request: " + time.strftime("%Y-%m-%dT%H:%M:%S.000Z"))
            self.logger.info(fullURL)
            return self.request

    def getJson(self):
        #print(self.request.content)
        json_result = json.loads(self.request.content)
        #print(json_result)
        dict1 = collections.OrderedDict(json_result)
        docs1 = dict1['feed']['entry']
        #print(docs1)
        # Items sind die einzelnen Datensätze
        return docs1