from app import create_app
from database import db
from services.request_logs_seed_service import RequestLogSeedService

def seed_logs():
    app = create_app()
    with app.app_context():
        result = RequestLogSeedService.seed_logs(app, count=2500)
        print(result)

if __name__ == "__main__":
    seed_logs()
