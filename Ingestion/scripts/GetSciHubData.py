import sys, time
from Ingestion.classes import ParameterHandler
from Ingestion.classes import ESARequestHandler
from Ingestion.classes import ElasticSearchHandler
from Ingestion.classes import LDFormatter
from Ingestion.classes import COPlogger


# Zeitformat: 2014-02-01T00:00:00.000Z
# https://scihub.copernicus.eu/dhus/search?q=ingestiondate:[2016-02-01T00:00:00.000Z%20TO%20NOW]&format=json&rows=100

#logger = setLogger()
log = COPlogger('ESAIngestionAt')
paramHandler = ParameterHandler(log.logger, 'config.ini')
config = paramHandler.setConfig()
requestHandler = ESARequestHandler(log.logger, paramHandler)
#lastCon =

user = sys.argv[1]
password = sys.argv[2]

pages = requestHandler.getPages(user, password)
ces = ElasticSearchHandler(log.logger, 'elastic', 'elastic')

# main :
for count in range(pages):
    start = count*100
    requestHandler.makeTimeSpanRequest(str(start), user, password)
    doc = requestHandler.getJson()

    for item in doc:
        if(list(item.keys())[0]=='title'):
            id = str(list(item.values())[0])
        ldFormatter = LDFormatter(log.logger)
        data = ldFormatter.createGeoJSONStructure(item)
        ces.indexData('copernicus', 'metadata', data, id)


print("Letzter erfolgreicher Request: " + time.strftime("%Y-%m-%dT%H:%M:%S.000Z"))
paramHandler.updateConfig('ESA','lastConnection', time.strftime("%Y-%m-%dT%H:%M:%S.000Z"))


log.logger.info("Process successfully finished")

