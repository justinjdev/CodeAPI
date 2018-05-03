from flask import Flask, request, json

app = Flask(__name__)


@app.route("/executeCode", methods=['POST'])
def execute_code():
    content = request.get_json(silent=True)

    if (content is not None) and (content['token'] is not 'wowwhatabadtoken'):
        return json.dumps({'success': False}), 403, {'ContentType': 'application/json'}

    return json.dumps({'success': True}), 403, {'ContentType': 'application/json'}



if __name__ == '__main__':
    app.run()