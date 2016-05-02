from warm_transfer_flask import db


class ActiveCall(db.Model):
    __tablename__ = 'active_calls'

    id = db.Column(db.Integer, primary_key=True)
    agent_id = db.Column(db.String, nullable=False)
    conference_id = db.Column(db.String, nullable=False)

    def __init__(self, agent_id, conference_id):
        self.agent_id = agent_id
        self.conference_id = conference_id
