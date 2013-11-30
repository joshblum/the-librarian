"""
    Simple server to provide API to interact with Librarian.
"""

from constants import HOST, PORT, DEBUG
from flask import Flask, request, jsonify

import uuid


app = Flask(__name__)

@app.route("/entity_drop")
def entity_drop():
    """
        Endpoint for giving a srcpath to an entity and the 
        entity type
    """
    srcpath = request.args.get('srcpath', '')
    entity_type = request.args.get('entity_type', '')
    res = {
        'success' : False,
        'job_id' : None,
    }
    if srcpath and entity_type:
        #todo first search metastore
        res['job_id'] = str(uuid.uuid4())

    return jsonify(**res)

@app.route("/progess/<job_id>")
def progress(job_id):
    """
        Returns the progress report for a given job_id
    """
    #TODO
    raise NotImplementedError

@app.route("/modify")
def modify(self):
    """
        Update a given entity's attributes in the metastore
    """
    #TODO
    raise NotImplementedError

if __name__ == "__main__":
    app.debug = DEBUG
    app.run(host=HOST, port=PORT)