import base64
import json
import pickle

# Flask imports, to handle HTTP requests
from flask import Flask, jsonify, request
# Server startup
from gevent.pywsgi import WSGIServer
# Graph Embeddings in a separate module
from factory.GraphFactory import *

# Global vars = Models (used in multiple methods)
net = []
word2model = []
graph_factory = Node2VecGraphFactory()


# Flask App Creation
def create_app():
    app = Flask(__name__)

    @app.route('/detect', methods=['POST'])
    def detect():
        # global model
        global net, word2model

        # Receive the data object from the request
        data = json.loads(request.json)
        edges = data['edges']
        number_of_walks = data['number_of_walks']

        # Lets try to classify it
        try:
            # Get detection label (0 - Good ware,1 - Malware)
            detection = graph_factory.predict_CG(edges, net, word2model, number_of_walks)
            # Convert from numpy to native var type
            detection = int(detection)
            # At the moment, we do not have confidence results
            confidence = 100
            # Valid prediction
            result = 1
        except:
            # Error cases
            # Invalid result
            result = 0
            # Not detected
            detection = 0
            # No confidence in what we are saying (bc error)
            confidence = 0

        # Return of the HTTP Request
        # Results encoded as JSON
        resp = jsonify({'result': result, 'detection': detection, 'confidence': confidence})
        resp.status_code = 200
        return resp

    @app.route('/train', methods=['POST'])
    def train_model():
        global net, word2model

        # Receive the data object from the request
        data = json.loads(request.json)
        x_train = data['x_train']
        y_train = data['y_train']
        number_of_walks = data['number_of_walks']
        print("request to train the model")
        # Get embedding from factory and train the model
        net, word2model = graph_factory.train_CG_classifier(x_train, y_train, number_of_walks)
        # Just return
        resp = jsonify({'message': 'Model trained successfully'})
        resp.status_code = 200
        return resp

    # Method to test if the docker is operating
    @app.route('/test', methods=['GET'])
    def test_model():
        # Only return that it is working
        # Useful to test the network connectivity
        resp = jsonify({"result": "Working"})
        resp.status_code = 200
        return resp

    return app


# Create the App
app = create_app()

http_server = WSGIServer(('', 8080), app)
http_server.serve_forever()



# Get the output of the `python` command
            output = subprocess.check_output(["cd", "/Users/snehithbikumandla/PycharmProjects/Pa1Test/temp",
                                              " && ", "git clone  ", github_repository_url,
                                              " && ", "cd ", dir_name, " && ", "bash pa1-tests.sh"])

            # Print the output
            print(output)
