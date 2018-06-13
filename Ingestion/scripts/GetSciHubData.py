import sys, time, logging
#sys.path.insert(0, '/Ingestion/classes')
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
requestHandler = ESARequestHandler(log.logger, paramHandler)

user = sys.argv[1]
password = sys.argv[2]

pages = requestHandler.getPages(user, password)
ces = ElasticSearchHandler(log.logger, 'elastic', 'elastic')

# main :
for count in range(pages):
    start = count*100
    print("Start: "+str(start))
    requestHandler.makeRequest(str(start), user, password)
    doc = requestHandler.getJson()

    for item in doc:
        if(list(item.keys())[0]=='title'):
            id = str(list(item.values())[0])
        ldFormatter = LDFormatter(item, log.logger)
        data = ldFormatter.createGeoJSONStructure()

        ces.indexData('copernicus', 'metadata', id, data)

log.logger.info("Process successfully finished")

