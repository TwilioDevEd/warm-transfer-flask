from flask import render_template, jsonify, request, url_for
from . import token
from . import call
from . import twiml_generator
from .models import ActiveCall

AGENT_WAIT_URL = 'http://twimlets.com/holdmusic?Bucket=com.twilio.music.classical'


def routes(app):
    app.route('/')(root)
    app.route('/conference/connect/client', methods=['POST'])(connect_client)
    app.route('/<agent_id>/token', methods=['POST'])(generate_token)
    app.route('/conference/<agent_id>/call', methods=['POST'])(call_agent)
    app.route('/conference/wait', methods=['POST'])(wait)
    app.route('/conference/<conference_id>/connect/<agent_id>', methods=['POST'])(
        connect_agent
    )


def root():
    return render_template('index.html')


def connect_client():
    conference_id = request.form['CallSid']
    connect_agent_url = url_for(
        'connect_agent', agent_id='agent1', conference_id=conference_id, _external=True
    )
    call.call_agent('agent1', connect_agent_url)
    ActiveCall.create('agent1', conference_id)
    return str(
        twiml_generator.generate_connect_conference(
            conference_id, url_for('wait'), False, True
        )
    )


def generate_token(agent_id):
    return jsonify(token=token.generate(agent_id), agentId=agent_id)


def call_agent(agent_id):
    conference_id = ActiveCall.conference_id_for(agent_id)
    connect_agent_url = url_for(
        'connect_agent', agent_id='agent2', conference_id=conference_id, _external=True
    )
    return call.call_agent('agent2', connect_agent_url)


def wait():
    return str(twiml_generator.generate_wait())


def connect_agent(conference_id, agent_id):
    exit_on_end = 'agent2' == agent_id
    return str(
        twiml_generator.generate_connect_conference(
            conference_id, AGENT_WAIT_URL, True, exit_on_end
        )
    )
