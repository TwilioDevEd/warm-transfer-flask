from warm_transfer_flask import db


class ActiveCall(db.Model):
    __tablename__ = 'active_calls'

    id = db.Column(db.Integer, primary_key=True)
    agent_id = db.Column(db.String, nullable=False)
    conference_id = db.Column(db.String, nullable=False)

    @classmethod
    def create(cls, agent_id, conference_id):
        existing_call = cls.query.filter_by(agent_id=agent_id).first()
        current_call = existing_call or cls(agent_id, conference_id)
        current_call.conference_id = conference_id
        db.session.add(current_call)
        db.session.commit()

    @classmethod
    def conference_id_for(cls, agent_id):
        return cls.query.filter_by(agent_id=agent_id).first().conference_id

    def __init__(self, agent_id, conference_id):
        self.agent_id = agent_id
        self.conference_id = conference_id
