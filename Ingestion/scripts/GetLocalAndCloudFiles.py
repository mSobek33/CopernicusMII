from Ingestion.classes import FileFinder
from Ingestion.classes import DirFileHandler
from Ingestion.classes import ESARequestHandler
from Ingestion.classes import COPlogger
from Ingestion.classes import ParameterHandler
from Ingestion.classes import ElasticSearchHandler
from Ingestion.classes import LDFormatter

import sys, json


log = COPlogger('LocalIngestionAt')
paramHandler = ParameterHandler(log.logger, 'local_config.ini')
config = paramHandler.setConfig()
requestHandler = ESARequestHandler(log.logger, paramHandler)
ces = ElasticSearchHandler(log.logger, 'elastic', 'elastic')

esaUser = sys.argv[1]
esaPassword = sys.argv[2]
user = sys.argv[3]

fileFinder = FileFinder()

#files = fileFinder.find("*." + config['COMPANY']['file'], config['COMPANY']['folder'])
files = fileFinder.findPattern("*.SAFE", config['COMPANY']['folder'])

accessPassed = False

if(ces.checkExistingIndex(config['COMPANY']['index']) == False):
    accessPassed = True
    owner = str(config['COMPANY']['owner']).split(",")
    print(owner)
    body = {
        "user": owner,
        "path": config['COMPANY']['index'] + "/" + config['COMPANY']['docType'],
        "note": config['COMPANY']['note']
    }
    ces.indexData("private", "indexes", body)

else:
    users = config['COMPANY']['owner'].split(',')
    print(users)
    for name in users:
        print(name + " " + user)
        if name == user:
            print("This Index already exists")
            accessPassed = True
            # Delete for Reindexing
            ces.es.indices.delete(index=config['COMPANY']['index'], ignore=[400, 404])
    if accessPassed == False:
        print("Access Denied")

if(accessPassed == True):
    dfh = DirFileHandler()
    for file in files:
        print(file)
        content = requestHandler.makeSingleRequest(
            dfh.getIDFromPath(file), esaUser, esaPassword).content
        doc = requestHandler.getJson()
        if(list(doc.keys())[0]=='title'):
            id = str(list(doc.values())[0])
            #print(id)
        ldFormatter = LDFormatter(log.logger)
        data = ldFormatter.createGeoJSONStructure(doc)
        data = json.loads(data)
        data["ressourceURL"] = "http://localhost:5000/index/" + id
        data["mainIndexURL"] = "http://localhost:9200/copernicus/metadata/" + id
        data["path"] = file

        ces.indexData(config['COMPANY']['index'], config['COMPANY']['docType'], data)
        #print(data)
