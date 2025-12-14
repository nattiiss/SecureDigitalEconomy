from database.models import SimulationState
from database import db


class InjectService:

    @staticmethod
    def is_active(name):
        state = SimulationState.query.filter_by(name=name).first()
        return state and state.state == 1

    @staticmethod
    def activate(name):
        state = SimulationState.query.filter_by(name=name).first()
        if state:
            state.state = 1
            db.session.commit()

    @staticmethod
    def deactivate(name):
        state = SimulationState.query.filter_by(name=name).first()
        if state:
            state.state = 0
            db.session.commit()

    @staticmethod
    def deactivate_all():
        SimulationState.query.update({SimulationState.state: 0})
        db.session.commit()
