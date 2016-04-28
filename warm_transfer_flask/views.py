from . import app
from flask import render_template, jsonify
from . import token


@app.route('/')
def root():
    return render_template('index.html')


@app.route('/<agent_id>/token', methods=['POST'])
def generate_token(agent_id):
    return jsonify(token=token.generate(agent_id),
                   agentId=agent_id)
