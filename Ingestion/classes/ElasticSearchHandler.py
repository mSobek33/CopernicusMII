import requests, json, collections
from elasticsearch import Elasticsearch

class ElasticSearchHandler:
    def __init__(self, logger, username, password):
        self.logger = logger
        self.username = username
        self.password = password
        self.es = Elasticsearch(['http://localhost:9200'], http_auth=(self.username, self.password))

    def indexData(self, index, doc_type, iId, item):
        r = requests.get('http://localhost:9200', auth=(self.username,self.password))
        #print(r.content)
        #print(es.get(index='copernicus', doc_type='metadata', id='4a86fdb1-3ef6-4a6e-bc02-3f37e1c74015'))
        self.es.index(index=index, doc_type=doc_type, id=iId, body=item)

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


    def updateIndexWithCodeDe(self, esID, cdeEntryLinks):
        res = self.es.get(index="copernicus", doc_type='metadata', id=esID)
        json_result = json.loads(json.dumps(res))
        #print(json_result['_source']['id'])
        #print("old: "+ str(json_result['_source']))

        # TODO neue Struktur bauen (nested Update not possible)
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
                "AcquisitionInformation": json_result['_source']['properties']['AcquisitionInformation'],
                "productInformation": json_result['_source']['properties']['productInformation'],
                "links": {
                    "openAccessHub": json_result['_source']['properties']['links']['openAccessHub'],
                    "codeDE": cdeEntryLinks
                }
            }
        }
        newStructure = json.loads(json.dumps(newStructure))

        self.es.index(index="copernicus", doc_type='metadata', id=esID, body=newStructure)

        #print("new: " + str(newStructure))

