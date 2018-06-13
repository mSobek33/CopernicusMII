import time, requests, sys, json, collections, xmltodict

class CodeDeRequestHandler:
    def __init__(self, logger, paramHandler):
        self.logger = logger
        self.paramHandler = paramHandler
        self.staticURLpart = 'https://catalog.code-de.org/opensearch/request/?httpAccept=application/atom%2Bxml&maximumRecords=150'
        self.paramHandler = paramHandler
        self.config = self.paramHandler.setConfig()
        self.productList = [self.config['CODE-DE']['s1_grd'],
                       self.config['CODE-DE']['s1_slc'],
                       self.config['CODE-DE']['s1_ocn'],
                       self.config['CODE-DE']['s2_msi'],
                       self.config['CODE-DE']['s3_olci1'],
                       self.config['CODE-DE']['s3_olci2'],
                       self.config['CODE-DE']['s3_slstr1'],
                       self.config['CODE-DE']['s3_slstr2']]
        self.request = None
        self.actualPage = None
        self.lastPage = None


    def makeRequest(self, product, startRecord, endDate):
        productStrConf = product.replace(":","_")
        startDate = self.config['CODE-DE']['lastConnection_' + productStrConf]

        #endDate = time.strftime("%Y-%m-%dT%H:%M:%S.000Z")
        url = self.staticURLpart + "&startRecord=" + str(startRecord) + "&parentIdentifier=" + product + "&startDate=" + startDate + "&endDate=" + endDate
        #print(url)
        self.request = requests.get(url)

        if(self.request.status_code == 503):
            self.logger.warning("Service is temporally not available")
            self.logger.warning("Last successful connection-date will be saved")
            self.logger.warning("Script will close")
            time.sleep(5)
            sys.exit(1)
            # exit
        else:
            self.logger.info("Request successfull: " + url)
            # nicht bedacht: startRecord
            if(self.actualPage != None or self.lastPage != None):
                if(self.actualPage == self.lastPage-1):
                    print("Letzter erfolgreicher Request: " + endDate)
                    self.paramHandler.updateConfig('CODE-DE','lastConnection_' + productStrConf, endDate)
                    self.logger.info(self.request)
            return self.request

    def generateDictFeedfromRequest(self):
        jsonString = str(json.dumps(xmltodict.parse(self.request.content), indent=4))
        jsonObject = json.loads(jsonString)
        dict1 = collections.OrderedDict(jsonObject)
        self.docs1 = dict1['feed']
        return self.docs1

    def sendRequestProgress(self, actualPage, lastPage):
        self.actualPage = actualPage
        self.lastPage = lastPage


    def getStartFactor(self):
        startFactor = int(int(self.docs1['os:totalResults']) / 150) + (int(self.docs1['os:totalResults']) % 150 < 0)
        if(int(self.docs1['os:totalResults']) != 0):
            startFactor = startFactor + 1
        #print("Pages: " + str(pages))
        quotient = int(self.docs1['os:totalResults']) / 150
        #print(int(output['os:totalResults']) / 150)
        return startFactor

    def getEntries(self, feed):
        entries = feed['entry']
        return entries
