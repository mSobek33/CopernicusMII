import xml.etree.ElementTree as ET

class InspireFileHandler:
    def __init__(self, path):
        self.path=path

    def getIDFromFile(self):
        tf = open(self.path,'r')
        xmlString = str(tf.read())
        #print(type(xmlString))
        root = ET.fromstring(xmlString)
        #print(root)

        fileIDRoot = root.findall('{http://www.isotc211.org/2005/gmd}identificationInfo')


        for moc in fileIDRoot:
            for node in moc.getiterator():
                if node.tag=='{http://www.isotc211.org/2005/gco}CharacterString':
                    #print(node.text.split('.'))
                    if(len(node.text.split('.')) > 1):
                        if(node.text.split('.')[1] == 'SAFE'):
                            #print(node.text.split('.')[0])
                            id = node.text.split('.')[0]

        return id
