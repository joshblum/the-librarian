"""
    Simple server to provide API to interact with Librarian.
"""
from metastore import MetaCon
from constants import HOST, PORT, DEBUG
from flask import Flask, request, jsonify

import uuid


app = Flask(__name__)
metacon = MetaCon()


@app.route("/entity_drop")
def entity_drop():
    """
        Endpoint for giving a srcpath to an entity and the 
        entity type
    """
    srcpath = request.args.get('srcpath', '')
    entity_type = request.args.get('entity_type', '')

    res = {
        'success': False,
        'job_id': None,
    }

    if srcpath and entity_type:
        job_id = str(uuid.uuid4())
        job_doc = metacon.get_job_doc(job_id, entity_type, srcpath)
        metacon.add_job(job_doc)

        res['job_id'] = job_id
        res['success'] = True

    return jsonify(**res)


@app.route("/progess/<job_id>")
def progress(job_id):
    """
        Returns the progress report for a given job_id
    """
    job_doc = self.metacon.find_job(job_id)

    return jsonify({
        'job_doc': job_doc,
    })


@app.route("/modify")
def modify(self):
    """
        Update a given entity's attributes in the metastore
    """
    # TODO
    raise NotImplementedError

if __name__ == "__main__":
    app.debug = DEBUG
    app.run(host=HOST, port=PORT)
