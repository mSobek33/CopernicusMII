from flask import Flask, render_template, request, Response, make_response
from pyld import jsonld
import json
from Ingestion.classes import ElasticSearchHandler
app = Flask(__name__)

@app.route("/")
def start():
    return "<h1>Landing Page</h1>"

@app.route("/about")
def about():
    return "<h1>About Page</h1>"

@app.route("/landing/<page>")
def landing(page):
    es = ElasticSearchHandler("", 'elastic', 'elastic')
    startValue= 1000 *(int(page)-1)
    items = es.getItemsPerPage(int(startValue))
    sitemap_xml = render_template('sitemap.xml', items=items['hits']['hits'])
    response= make_response(sitemap_xml)
    response.headers["Content-Type"] = "application/xml"

    return response
    #return "<h1>Landing Page</h1>"

@app.route('/index/<id>')
def show_id(id):
    es = ElasticSearchHandler("", 'elastic', 'elastic')
    res = es.getEntry(id)
    strRes = json.dumps(res)
    context = res['@context']
    privateTableValues = dict()
    username = request.args.get('username')
    if(username != None):
        #print(username)
        indexes = es.findSharedIndexes(username)
        #print(indexes)
        if(indexes != None):
            privateTableValues = es.getValueFromPrivateIndexes(indexes, id)
        else:
            privateTableValues = None

    return render_template('dataset.html', origRes=res, ctx=context, strRes=strRes, privateTableValues=privateTableValues)


def getElasticSarchData():
    return None


if __name__ == '__main__':
    app.run(debug=True)