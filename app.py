import base64
import json, os
import pickle

# Flask imports, to handle HTTP requests
from flask import Flask, jsonify, request
# Server startup
from gevent.pywsgi import WSGIServer
import subprocess

dir_name = ""
app = Flask(__name__)

def get_score(file_path):
    # Define the file path
    # file_path = 'your_file.txt'

    # Initialize a variable to store the last score
    last_score = None

    # Open the file in read mode
    with open(file_path, 'r') as file:
        # Iterate through each line in reverse order
        for line in reversed(file.readlines()):
            # Check if the line contains 'SCORE:'
            if 'SCORE:' in line:
                # Extract the score value using string manipulation
                last_score = line.split(':')[-1].strip()
                break  # Exit the loop after finding the score
    return last_score


# Flask App Creation
def create_app():
    # app = Flask(__name__)

    @app.route('/score', methods=['POST'])
    def train_model():
        global dir_name
        data = request.json
        print(data)
        github_repository_url = data.get('github_repository_url')
        dir_name = github_repository_url.split("/")[-1][:-4]
        os.system("rm -rf " + dir_name)
        try:
            print(os.getcwd())
            # curr_dir = "/Users/snehithbikumandla/PycharmProjects/Pa1Test/"

            # os.system("cd " + curr_dir + "/temp")
            os.system("git clone " + github_repository_url)
            curr_dir = os.getcwd()+"/"+dir_name+"/output.txt"
            os.system("cd " + dir_name + " && rm -rf pa1-tests.sh && rm -rf output.txt && mkdir received && cp ../../pa1-tests.sh . && bash pa1-tests.sh >> output.txt")
            val = get_score(curr_dir)
            print(val)
            print(curr_dir)
            resp = jsonify({'message': val})
            resp.status_code = 200

        except Exception as e:
            resp = jsonify(({"result": e}))
            resp.status_code = 400
        # finally:
        #     os.system("rm -rf " + dir_name)

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
