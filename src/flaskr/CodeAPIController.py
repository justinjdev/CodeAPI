#!/usr/bin/python3.6
"""
    Author: Justin Jones
    Date: 5/13/2018

    File: CodeAPIController.py
    Version: 0.1

    This is a RESTful API wrapper written for the processing module from CodeChat (https://bit.ly/2rAFLga) using Flask
    for the controller. The processor is built to run on Linux, so will not execute on Windows machines without
    modification.
"""

from flask import Flask, request, json

from src.executor.Processing import Processor

app = Flask(__name__)

code_executor = Processor()
supported_langs = code_executor.get_languages()
lang_methods = code_executor.get_funcs()
lang_handler = {}
for num, lang in enumerate(supported_langs, 0):
    lang_handler[lang] = getattr(Processor, lang_methods[num])


@app.route("/executeCode", methods=['POST'])
def execute_code():
    # POST should contain token, language & code values
    content = request.get_json(silent=True)

    if (content is not None) and (content['token'] == 'wowwhatabadtoken'):
        if (content['code'] is not None) and (content['language'] in lang_handler.keys()):
            handler = lang_handler[content['language']]
            output = handler(code_executor, content['code'])
            return json.dumps({'success': True, 'output': output}), 200, {'ContentType': 'application/json'}

        else:
            return json.dumps({'success': False, 'output': 'The code or language was not found.'}), \
                   404, \
                   {'ContentType': 'application/json'}

    return json.dumps({'success': False}), 403, {'ContentType': 'application/json'}


@app.route("/retrieveLanguages", methods=['GET'])
def return_languages():
    return json.dumps({'languages': supported_langs}), 200, {'ContentType': 'application/json'}


if __name__ == '__main__':
    app.run()
