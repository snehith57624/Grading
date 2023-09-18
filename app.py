import base64
import json, os
import pickle

# Flask imports, to handle HTTP requests
from flask import Flask, jsonify, request
# Server startup
from gevent.pywsgi import WSGIServer
import subprocess
from gevent.pywsgi import WSGIServer
from flask_restx import Api, Resource

dir_name = ""
app = Flask(__name__)
api = Api(app, version='1.0', title='PA1 Score', description='Get Score of PA1 assignment', doc='/')

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


@api.route('/score')
class Score(Resource):
    @api.doc(params={'github_repository_url': 'GitHub Repository URL'})
    def post(self):
        global dir_name
        # print(request.args)
        args = request.args
        # print(args.get("github_repository_url"))
        
        github_repository_url = args.get("github_repository_url")
        dir_name = github_repository_url.split("/")[-1][:-4]
        os.system("rm -rf " + dir_name)
        try:
            # print(os.getcwd())
            os.system("git clone " + github_repository_url)
            curr_dir = os.getcwd()+"/"+dir_name+"/output.txt"
            os.system("cd " + dir_name + " && rm -rf pa1-tests.sh && rm -rf output.txt && mkdir received && cp ../pa1-tests.sh . && bash pa1-tests.sh >> output.txt")
            val = get_score(curr_dir)
            print(val)
            print(curr_dir)
            resp = jsonify({'Score': val})
            resp.status_code = 200

        except Exception as e:
            resp = jsonify(({"result": e}))
            resp.status_code = 400
        finally:
            os.system("rm -rf " + dir_name)

        return resp

# Method to test if the docker is operating
@api.route('/test')
class Test(Resource):
    def get(self):
        # Only return that it is working
        # Useful to test the network connectivity
        resp = jsonify({"result": "Working"})
        resp.status_code = 200
        return resp



# Create the App
# app = create_app()
if __name__ == '__main__':
    http_server = WSGIServer(('', 8080), app)
    http_server.serve_forever()
