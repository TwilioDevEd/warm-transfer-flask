from . import app
from flask import render_template, jsonify
from . import token
from . import call
from twilio import twiml


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
    twiml_response = twiml.Response()
    wait_message = 'Thank you for calling. Please wait in line for a few seconds. An agent will be with you shortly.'
    wait_music = 'http://com.twilio.music.classical.s3.amazonaws.com/BusyStrings.mp3'
    twiml_response.say(wait_message)
    twiml_response.play(wait_music)
    return str(twiml_response)
