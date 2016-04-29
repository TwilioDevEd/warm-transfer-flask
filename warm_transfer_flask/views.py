from . import app
from flask import render_template, jsonify
from . import token
from . import call
from . import twiml_generator


@app.route('/')
def root():
    return render_template('index.html')


@app.route('/<agent_id>/token', methods=['POST'])
def generate_token(agent_id):
    return jsonify(token=token.generate(agent_id),
                   agentId=agent_id)


@app.route('/conference/<agent_id>/call', methods=['POST'])
def call_agent(agent_id):
    return call.call_agent(agent_id)


@app.route('/conference/wait', methods=['POST'])
def wait():
    return str(twiml_generator.generate_wait())
