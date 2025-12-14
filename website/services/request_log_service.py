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

    @staticmethod
    def get_defaced_only():
        """
        Returns only logs related to defacement / injects.
        """
        return RequestLog.query.filter_by(
            defaced_flag=1
        ).order_by(
            RequestLog.created_at.desc()
        ).all()
