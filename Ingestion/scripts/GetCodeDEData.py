import time, logging
from elasticsearch import Elasticsearch
from Ingestion.classes import ParameterHandler
from Ingestion.classes import CodeDeRequestHandler
from Ingestion.classes import ElasticSearchHandler
from Ingestion.classes import COPlogger



log = COPlogger('CODEDEIngestionAt')
es = Elasticsearch(['http://localhost:9200'], http_auth=('elastic', 'elastic'))
paramHandler = ParameterHandler(log.logger, 'config.ini')
config = paramHandler.setConfig()

staticURLpart = 'https://catalog.code-de.org/opensearch/request/?httpAccept=application/atom%2Bxml&maximumRecords=150'
endDate = time.strftime("%Y-%m-%dT%H:%M:%S.000Z")

requestHandler = CodeDeRequestHandler(log.logger, paramHandler)

ces = ElasticSearchHandler(log.logger, 'elastic', 'elastic')


for product in requestHandler.productList:
    requestHandler.makeRequest(product, 1, endDate)
    requestHandler.generateDictFeedfromRequest()
    startFactor = requestHandler.getStartFactor()
    for count in range(startFactor):
        if count == 0:
            startRecord = 1
        else:
            startRecord = 150 * count
        print(count)
        print(startFactor)
        # letzter Durchlauf: count = startFactor-1
        #print("Requests with Parameters: product =" + str(product) + " and startrecord = " + str(startRecord))
        requestHandler.sendRequestProgress(count, startFactor)
        output = requestHandler.makeRequest(product, startRecord, endDate)
        if(product == 'EOP:CODE-DE:S3_SLSTR_L2_LST'):
            if(output.status_code == 200):
                print("Letzter erfolgreicher Request: " + endDate)
                paramHandler.updateConfig('CODE-DE','lastConnection', endDate)
                log.logger.info(output.request)
        feed = requestHandler.generateDictFeedfromRequest()
        if 'entry' in feed:
            #entries einzeln pro Seite abholen
            entries = requestHandler.getEntries(feed)
            if type(entries) is list:
                for item in entries:
                    # search ID in ES-DB
                    title = item['title'].split('/')
                    lowerTitle = title[1].lower()
                    #print(lowerTitle)
                    id = ces.findEntryinES(lowerTitle)
                    if id is not None:
                        ces.updateIndexWithCodeDe(id, item['link'])
            else:
                # das gleich ohne for schleife
                # Muss: für jeden parentIdentifier eigenen Zeitpunkt
                print("Keine Liste: " + entries)
                print(entries)

        else:
            print("Keine CODE-DE Ergebnisse")

