import json, collections, datetime, geocoder
import numpy as np
from UliEngineering.Math.Coordinates import BoundingBox
from Ingestion.classes import ParameterHandler

class LDFormatter:
    def __init__(self, jsonEntry, logger):
        self.jsonEntry = jsonEntry
        self.logger = logger
        self.structure = ""
        self.dataHandler = ParameterHandler(self.logger, 'data_uris.ini')
        self.dataList = self.dataHandler.setConfig()

    def updateContext(self):
        None

    def createGeoJSONStructure(self):

        # value for GeoJSON attr 'id'
        if(list(self.jsonEntry.keys())[0]=='title'):
            id = "http://localhost:9200/copernicus/metadata/" + str(list(self.jsonEntry.values())[0])
            print(id)
        # value for GeoJSON attr 'type'
        type = "Feature"

        # values for GeoJSON attr 'geometry' and 'bbox'
        for value in self.jsonEntry['str']:
            if(value['name'] == 'footprint'):
                #print(str(str(value).split("(")[0].split("'")[7]))
                if(str(str(value).split("(")[0].split("'")[7]) == "POLYGON "):
                    gType = "Polygon"
                    strCoordinates = str(value).split("(")[2].split(")")[0].split(",")
                else:
                    gType = "Multipolygon"
                    strCoordinates = str(value).split("(")[3].split(")")[0].split(",")
                coords = np.asarray(strCoordinates)
                n2Coords = list()
                geomCoordinatesStr = list()
                for coord in coords:
                    sCoord = coord.split(" ")
                    # if MULTIPOLYGON
                    if(sCoord[0] == ''):
                        sCoord = [str for str in sCoord if str]

                    for coord2 in sCoord:
                        geomCoordinatesStr.append(coord2)
                    n2Coords.append(sCoord)#
                # if MULTIPOLYGON
                if(geomCoordinatesStr[2] == ''):
                    geomCoordinatesStr = [str for str in geomCoordinatesStr if str]
                geomCoordinates = list(map(float, geomCoordinatesStr))
                aN2Coords = np.asarray(n2Coords, np.float)
                bbox = [BoundingBox(aN2Coords).minx, BoundingBox(aN2Coords).miny, BoundingBox(aN2Coords).maxx, BoundingBox(aN2Coords).maxy]

                #g = geocoder.google([0.278970,51.683979], method='reverse')

                #print(g.city)

        def createContext(self, mission):
            if(mission == "Sentinel-1"):
                context = {
                        "id": "@id",
                        "type": "@type",
                        "gj": "https://purl.org/geojson/vocab#",
                        "eop": "http://www.opengis.net/eo-geojson/1.0/",
                        "dc": "http://purl.org/dc/terms/",
                        "openAccessHub": "https://scihub.copernicus.eu/",
                        "codeDE": "https://code-de.org/",
                        "bbox": "gj:bbox",
                        "geometry": "gj:geometry",
                        "properties": "gj:properties",
                        "Properties": "gj:Properties",
                        "coordinates": "gj:coordinates",
                        "AcquisitionInformation": "eop:AcquisitionInformation",
                        "acquisitionInformation": "eop:acquisitionInformation",
                        "date": "dc:date",
                        "title": "dc:title",
                        "identifier": "dc:identifier",
                        "platform": "eop:platform",
                        "Platform": "eop:Platform",
                        "instrument": "eop:instrument",
                        "Instrument": "eop:Instrument",
                        "instrumentShortName": "eop:instrumentShortName",
                        "polarisationChannels": "eop:polarisationChannels",
                        "acquisitionParameters": "eop:acquisitionParameters",
                        "AcquisitionParameters": "eop:AcquisitionParameters",
                        "operationalMode": "eop:operationalMode",
                        "orbitDirection": "eop:orbitDirection",
                        "orbitNumber": "eop:orbitNumber",
                        "DESCENDING": "eop:DESCENDING",
                        "ASCENDING": "eop:ASCENDING",
                        "ProductInformation": "eop:ProductInformation",
                        "productInformation": "eop:productInformation",
                        "productType": "eop:productType",
                        "size": "eop:size",
                        "links": "eop:Links"
                    }
                return context
            elif(mission == "Sentinel-2"):
                context = {
                              "id": "@id",
                              "type": "@type",
                              "gj": "https://purl.org/geojson/vocab#",
                              "eop": "http://www.opengis.net/eo-geojson/1.0/",
                              "dc": "http://purl.org/dc/terms/",
                              "openAccessHub": "https://scihub.copernicus.eu/",
                              "codeDE": "https://code-de.org/",
                              "bbox": "gj:bbox",
                              "geometry": "gj:geometry",
                              "properties": "gj:properties",
                              "Properties": "gj:Properties",
                              "coordinates": "gj:coordinates",
                              "AcquisitionInformation": "eop:AcquisitionInformation",
                              "acquisitionInformation": "eop:acquisitionInformation",
                              "date": "dc:date",
                              "title": "dc:title",
                              "identifier": "dc:identifier",
                              "platform": "eop:platform",
                              "Platform": "eop:Platform",
                              "platformSerialIdentifier": "eop:platformSerialIdentifier",
                              "instrument": "eop:instrument",
                              "Instrument": "eop:Instrument",
                              "instrumentShortName": "eop:instrumentShortName",
                              "acquisitionParameters": "eop:acquisitionParameters",
                              "AcquisitionParameters": "eop:AcquisitionParameters",
                              "operationalMode": "eop:operationalMode",
                              "orbitDirection": "eop:orbitDirection",
                              "orbitNumber": "eop:orbitNumber",
                              "DESCENDING": "eop:DESCENDING",
                              "ASCENDING": "eop:ASCENDING",
                              "ProductInformation": "eop:ProductInformation",
                              "productInformation": "eop:productInformation",
                              "productType": "eop:productType",
                              "processingLevel": "eop:processingLevel",
                              "size": "eop:size",
                              "cloudCover": "eop:cloudCover",
                              "links": "eop:Links"
                          }
                return context
            elif(mission == "Sentinel-3"):
                context = {
                    "id": "@id",
                    "type": "@type",
                    "gj": "https://purl.org/geojson/vocab#",
                    "eop": "http://www.opengis.net/eo-geojson/1.0/",
                    "dc": "http://purl.org/dc/terms/",
                    "openAccessHub": "https://scihub.copernicus.eu/",
                    "codeDE": "https://code-de.org/",
                    "bbox": "gj:bbox",
                    "geometry": "gj:geometry",
                    "properties": "gj:properties",
                    "Properties": "gj:Properties",
                    "coordinates": "gj:coordinates",
                    "AcquisitionInformation": "eop:AcquisitionInformation",
                    "acquisitionInformation": "eop:acquisitionInformation",
                    "date": "dc:date",
                    "title": "dc:title",
                    "identifier": "dc:identifier",
                    "platform": "eop:platform",
                    "Platform": "eop:Platform",
                    "instrument": "eop:instrument",
                    "Instrument": "eop:Instrument",
                    "instrumentShortName": "eop:instrumentShortName",
                    "acquisitionParameters": "eop:acquisitionParameters",
                    "AcquisitionParameters": "eop:AcquisitionParameters",
                    "orbitDirection": "eop:orbitDirection",
                    "orbitNumber": "eop:orbitNumber",
                    "DESCENDING": "eop:DESCENDING",
                    "ASCENDING": "eop:ASCENDING",
                    "ProductInformation": "eop:ProductInformation",
                    "productInformation": "eop:productInformation",
                    "productType": "eop:productType",
                    "processingLevel": "eop:processingLevel",
                    "size": "eop:size",
                    "links": "eop:Links"
                }
                return context

        # CoreAttributes are: type, title, identifier and date
        def createCoreAttributes(self):
            type = "Properties"

            if(list(self.jsonEntry.keys())[0]=='title'):
                id = str(list(self.jsonEntry.values())[0])
                title = str(list(self.jsonEntry.values())[0])

            for date in self.jsonEntry['date']:
                if(date['name'] == 'beginposition'):
                    #print(date['content'])
                    print(len(date['content'].split('.')))
                    if(len(date['content'].split('.')) == 1):
                        print(date['content'])
                        nDate = date['content'].split('Z')
                        nDate = nDate[0] + '.000Z'
                        print(nDate)
                        date = datetime.datetime.strptime(str(nDate), "%Y-%m-%dT%H:%M:%S.%fZ")
                    else:
                        print(date['content'])
                        date = datetime.datetime.strptime(date['content'], "%Y-%m-%dT%H:%M:%S.%fZ")
                    #print(cDate)

            coreAttributes = dict({"cType": type, "cId": id, "cTitle": title, "cDate": date})



            return coreAttributes

        def createPlatformStructure(self):

            type = "Platform"
            platformSerialIdentifier = ""

            for value in self.jsonEntry['str']:
                if(value['name'] == 'platformname'):
                    platform = value['content']
                if(value['name'] == 'platformserialidentifier'):
                    platformSerialIdentifier = value['content']

            id = self.dataList[platform][str("idWiki_" + platform)]
            platSameAs = self.dataList[platform][str("id_" + platform)]

            platformAttributes = dict({"pType": type,"pId": id,"pSameAs": platSameAs, "pPlatform": platform, "pPlatformSI": platformSerialIdentifier})

            return platformAttributes

        def createInstrumentStructure(self, mission):

            type = "Instrument",

            for value in self.jsonEntry['str']:
                if(value['name'] == 'instrumentname'):
                    instrumentName = value['content']
                if(value['name'] == 'instrumentshortname'):
                    instrumentShortName = value['content']

            id= self.dataList[mission][str("instrument_" + instrumentShortName)]


            if(mission == "Sentinel-1"):
                for value in self.jsonEntry['str']:
                    if(value['name'] == 'sensoroperationalmode'):
                        operationalMode =value['content']
                    if(value['name'] == 'polarisationmode'):
                        polarisationmode = value['content']

                instrumentStructure = {
                    "type": type,
                    "id": id,
                    "instrument": instrumentName,
                    "instrumentShortName": instrumentShortName,
                    "operationalMode": operationalMode,
                    "polarisationChannels": polarisationmode
                    }

                return instrumentStructure

            elif(mission == 'Sentinel-2'):
                operationalMode = ""
                for value in self.jsonEntry['str']:
                    if(value['name'] == 'sensoroperationalmode'):
                        operationalMode =value['content']

                instrumentStructure = {
                    "type": type,
                    "id": id,
                    "instrument": instrumentName,
                    "instrumentShortName": instrumentShortName,
                    "operationalMode": operationalMode
                }

                return instrumentStructure

            elif(mission == 'Sentinel-3'):

                instrumentStructure = {
                    "type": type,
                    "id": id,
                    "instrument": instrumentName,
                    "instrumentShortName": instrumentShortName
                }

                return instrumentStructure

        def createAcquisitionParameters(self):

            type = "AcquisitionParameters"

            for value in self.jsonEntry['str']:
                if(value['name'] == 'orbitdirection'):
                    if(value['content'] == "ascending"):
                        orbitDirection = "ASCENDING"
                    elif(value['content'] == "descending"):
                        orbitDirection = "DESCENDING"
                    else:
                        orbitDirection = value['content']

            for value in self.jsonEntry['int']:
                if(value['name'] == 'orbitnumber'):
                    orbitNumber = value['content']

            acquisitionParameterStructure = {
                "type": type,
                "orbitDirection": orbitDirection,
                "orbitNumber": orbitNumber
            }

            return acquisitionParameterStructure

        def createProductInformation(self, mission):

            type = "ProductInformation"
            for value in self.jsonEntry['str']:
                if(value['name'] == 'producttype'):
                    productType = value['content']
                if(value['name'] == 'size'):
                    size = value['content']

            if(mission == 'Sentinel-1'):
                productStructure = {
                    "type": type,
                    "productType": productType,
                    "size": size
                }
                return productStructure
            elif(mission == 'Sentinel-2'):
                cloudCover = 999
                for value in self.jsonEntry['str']:
                    if(value['name'] == 'processinglevel'):
                        processingLevel = value['content']
                for value in self.jsonEntry['double']:
                    if(len(self.jsonEntry['double']) == 2):
                        if(str(self.jsonEntry['double']).split("'")[3] == "cloudcoverpercentage"):
                            cloudCover = str(self.jsonEntry['double']).split("'")[7]
                    else:
                        if(value['name'] == 'cloudcoverpercentage'):
                            cloudCover = value['content']

                productStructure = {
                    "type": type,
                    "productType": productType,
                    "processingLevel": processingLevel,
                    "size": size,
                    "cloudCover": float(cloudCover)
                }
                return productStructure
            elif(mission == 'Sentinel-3'):
                for value in self.jsonEntry['str']:
                    if(value['name'] == 'processinglevel'):
                        processingLevel = value['content']
                productStructure = {
                    "type": type,
                    "productType": productType,
                    "size": size,
                    "processingLevel": processingLevel
                }
                return productStructure

        def createESALinks(self):
            selfLink = "https://scihub.copernicus.eu/dhus/search?q=" + str(list(self.jsonEntry.values())[0])
            selfTitle = "Metadata"

            for value in self.jsonEntry['link']:
                if('rel' in value):
                    if(value['rel'] == 'icon'):
                        thumbnailLink = value['href']
                        thumbnailTitle = "Thumbnail"
                else:
                    downloadLink = value['href']
                    downloadTitle = "Download"


            esaLinkAttributes = dict({"oacSelfLink": selfLink, "oacSelfTitle": selfTitle,
                                      "oacThumbnailLink": thumbnailLink, "oacThumbnailTitle": thumbnailTitle,
                                      "oacDownloadLink": downloadLink, "oacDownloadTitle": downloadTitle})

            return esaLinkAttributes

        self.coreAttributes = createCoreAttributes(self)
        self.platformAttributes = createPlatformStructure(self)
        self.contextAttributes = createContext(self, self.platformAttributes['pPlatform'])
        self.instrumentAttributes = createInstrumentStructure(self, self.platformAttributes['pPlatform'])
        self.acquisitionAttributes = createAcquisitionParameters(self)
        self.productAttributes = createProductInformation(self, self.platformAttributes['pPlatform'])
        self.esaLinkAttributes = createESALinks(self)

        self.structure = {
                             "@context": self.contextAttributes,
                             "type": type,
                             "id": id,
                             "bbox":
                                 bbox,
                             "geometry": {
                               "type": gType,
                               "coordinates": geomCoordinates
                             },
                             "properties": {
                                 "type": self.coreAttributes['cType'],
                                 "date": self.coreAttributes['cDate'],
                                 "title": self.coreAttributes['cTitle'],
                                 "identifier": self.coreAttributes['cId'],
                                 "AcquisitionInformation": {
                                     "type": "AcquisitionInformation",
                                     "platform": {
                                         "type": self.platformAttributes['pType'],
                                         "id": self.platformAttributes['pId'],
                                         "sameAs": self.platformAttributes['pSameAs'],
                                         "platform": self.platformAttributes['pPlatform'],
                                         # nur Sentinel-2
                                         "platformSerialIdentifier": self.platformAttributes['pPlatformSI']
                                     },
                                     "instrument": self.instrumentAttributes,
                                     "acquisitionParameters": self.acquisitionAttributes

                                 },
                                 "productInformation": self.productAttributes,
                                 "links": {
                                     "openAccessHub": [
                                         {
                                             "href": self.esaLinkAttributes['oacSelfLink'],
                                             "title": self.esaLinkAttributes['oacSelfTitle']
                                         },
                                         {
                                             "href": self.esaLinkAttributes['oacDownloadLink'],
                                             "title": self.esaLinkAttributes['oacDownloadTitle']
                                         },
                                         {
                                             "href": self.esaLinkAttributes['oacThumbnailLink'],
                                             "title": self.esaLinkAttributes['oacThumbnailTitle']
                                         }
                                     ]
                                 }
                             }
                         }
        self.structure = json.dumps(self.structure)

        return self.structure
        #print(self.structure)
        #dict = collections.OrderedDict(self.structure)
        #print(dict)




