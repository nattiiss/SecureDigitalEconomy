from database import db


class RequestLog(db.Model):
    __tablename__ = "request_logs"

    id = db.Column(db.Integer, primary_key=True)

    method = db.Column(db.String(10))            
    path = db.Column(db.String(200))               
    ip_address = db.Column(db.String(50))

    payload = db.Column(db.Text)      

    user_id = db.Column(db.Integer, nullable=True)
    role = db.Column(db.String(50), nullable=True)

    status_code = db.Column(db.Integer)
    created_at = db.Column(db.String(30))
    defaced_flag = db.Column(db.Integer, default= 0)
