import requests, json, collections
from elasticsearch import Elasticsearch, helpers

class ElasticSearchHandler:
    def __init__(self, logger, username, password):
        self.logger = logger
        self.username = username
        self.password = password
        self.es = Elasticsearch(['http://localhost:9200'], http_auth=(self.username, self.password))

    def indexData(self, index, doc_type, item, iId=None):
        r = requests.get('http://localhost:9200', auth=(self.username,self.password))
        if(iId == None):
            self.es.index(index=index, doc_type=doc_type, body=item)
        else:
            self.es.index(index=index, doc_type=doc_type, id=iId, body=item, request_timeout=60)

    def checkExistingIndex(self, index):
        if self.es.indices.exists(index=index):
            return True
        else:
            return False

    def getTotalHits(self):
        res = self.es.search(index='copernicus', doc_type='metadata')
        return res["hits"]["total"]

    def getItemsPerPage(self, start, query=None):
        if(query == None):
            query = {
                "from": start, "size": 1000
            }
            res = self.es.search(index='copernicus', doc_type='metadata', body=query)
        else:
            query = query
            res = self.es.search(index='copernicus', body=query)

        return res

    def getAllItems(self, query=None):
        if(query == None):
            res = helpers.scan(
                client = self.es,
                scroll = '2m',
                index = "copernicus")

        else:
            res = helpers.scan(
                client = self.es,
                scroll = '2m',
                query = query,
                index = "copernicus")

        return res

    def findSharedIndexes(self, username):
        body = {
            "from": 0, "size": 100,
            "query": {
                "query_string": {
                    "query": username
                }
            }
        }
        res = self.es.search(index="private", body=body)
        #print(res)
        paths = {}

        if(res["hits"]["total"] != 0):
            for entry in res['hits']['hits']:
                paths.update({entry['_id'] : entry['_source']['path']})
            return paths
        else:
            return None

    def getValueFromPrivateIndexes(self, indexes, id):

        paths = {}

        for key, value in indexes.items():
            indexI = value.split("/")[0]
            docType = value.split("/")[1]
            mainIndexURL = "http\\:\\/\\/localhost:9200\\/copernicus\\/metadata\\/" + id
            #print(indexI)
            #print(docType)
            #print(key)
            res = self.es.search(index=indexI, body={
                "from": 0, "size": 100,
                "query": {
                    "query_string": {
                        "query": id,
                        "lowercase_expanded_terms": False
                    }
                }
            })
            #print(res)
            if(res["hits"]["total"] != 0):
                #print(res['hits']['hits'])
                for entry in res['hits']['hits']:
                    entry = str(entry['_source']['path']).replace("\\", "/")
                    paths.update({key : entry})
                #return paths

        print(paths)
        return paths


    def findEntryinES(self, id):
        #print(title)
        res = self.es.search(index="copernicus", body={
            "_source": ["title"],
            "query": {
                "match": {
                    "properties.title": id
                }
            }
        })
        jsonString = str(json.dumps(res['hits']))
        splitJ = jsonString.split('hits')
        if len(splitJ[1]) >= 10:
            resID = splitJ[1].split(',')[2].split(' ')[2].split('"')[1]
            #print("Found ID in ES-DB: " + str(resID))
            return resID
        else:
            # logging
            #print("Keine Ergebnisse gefunden")
            return None

    def getEntry(self, esID):
        res = self.es.get_source(index="copernicus", doc_type='metadata', id=esID)
        json_result = json.loads(json.dumps(res))
        return res

    def updateIndexWithPrivateInfo(self, index, doc_type, esID, updateBody):
        self.es.update(index=index, doc_type=doc_type, id=esID, body=updateBody)


    def updateIndexWithCodeDe(self, esID, cdeEntryLinks):
        res = self.es.get(index="copernicus", doc_type='metadata', id=esID)
        # remove '@'
        bCdeEntryLinks = json.loads(json.dumps(cdeEntryLinks).replace("@", ""))
        json_result = json.loads(json.dumps(res))
        #print(json_result['_source']['id'])
        #print("old: "+ str(json_result['_source']))
        print(json_result)

        # neue Struktur bauen (nested Update not possible)
        newStructure = {
            "@context": json_result['_source']['@context'],
            "type": json_result['_source']['type'],
            "id": json_result['_source']['id'],
            "bbox":
                json_result['_source']['bbox'],
            "geometry": {
                "type": json_result['_source']['geometry']['type'],
                "coordinates": json_result['_source']['geometry']['coordinates']
            },
            "properties": {
                "type": json_result['_source']['properties']['type'],
                "date": json_result['_source']['properties']['date'],
                "title": json_result['_source']['properties']['title'],
                "identifier": json_result['_source']['properties']['identifier'],
                "acquisitionInformation": json_result['_source']['properties']['acquisitionInformation'],
                "productInformation": json_result['_source']['properties']['productInformation'],
                "links": {
                    "openAccessHub": json_result['_source']['properties']['links']['openAccessHub'],
                    "codeDE": bCdeEntryLinks
                }
            }
        }
        newStructure = json.loads(json.dumps(newStructure))

        self.es.index(index="copernicus", doc_type='metadata', id=esID, body=newStructure)

        #print("new: " + str(newStructure))

