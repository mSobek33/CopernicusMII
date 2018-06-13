
function search(client, es_id) {
    return client.getSource({
        index: 'copernicus',
        type: 'metadata',
        id: es_id
    })
}

function closeConnection(client) {
    client.close();
}


function getFromIndex(client) {
    return client.get({
        id: 1,
        index: 'test',
        type: 'house'
    }).then(log);

}