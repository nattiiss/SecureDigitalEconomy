from database.models import RequestLog


class RequestLogService:

    @staticmethod
    def get_all():
        """
        Returns all request logs (latest first).
        Used for SOC / dashboard table.
        """
        return RequestLog.query.order_by(
            RequestLog.created_at.desc()
        ).all()

