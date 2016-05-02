from . import app
from flask import render_template, jsonify, request, url_for
from . import token
from . import call
from . import twiml_generator
from .models import ActiveCall
AGENT_WAIT_URL = 'http://twimlets.com/holdmusic?Bucket=com.twilio.music.classical'


@app.route('/')
def root():
    return render_template('index.html')


@app.route('/conference/connect/client', methods=['POST'])
def connect_client():
    conference_id = request.form['CallSid']
    connect_agent_url = url_for('connect_agent', agent_id='agent1',
                                conference_id=conference_id)
    call.call_agent('agent1', connect_agent_url)
    ActiveCall.create('agent1', conference_id)
    return str(twiml_generator.generate_connect_conference(conference_id,
                                                           url_for('wait'),
                                                           False,
                                                           True))


@app.route('/<agent_id>/token', methods=['POST'])
def generate_token(agent_id):
    return jsonify(token=token.generate(agent_id),
                   agentId=agent_id)


@app.route('/conference/<agent_id>/call', methods=['POST'])
def call_agent(agent_id):
    conference_id = ActiveCall.conference_id_for('agent1')
    connect_agent_url = url_for('connect_agent', agent_id=agent_id,
                                conference_id=conference_id)
    return call.call_agent(agent_id, connect_agent_url)


@app.route('/conference/wait', methods=['POST'])
def wait():
    return str(twiml_generator.generate_wait())


@app.route('/conference/<conference_id>/connect/<agent_id>', methods=['POST'])
def connect_agent(conference_id, agent_id):
    exit_on_end = 'agent2' in agent_id
    return str(twiml_generator.generate_connect_conference(conference_id,
                                                           AGENT_WAIT_URL,
                                                           True,
                                                           exit_on_end))
