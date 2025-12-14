from database import db


class SimulationState(db.Model):
    __tablename__ = "simulation_state"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))            
    state = db.Column(db.Integer, default = 0)    