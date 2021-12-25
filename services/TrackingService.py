from models.LoginLog import LoginLog
from models.HardwareTracking import HardwareTracking
from models.ActivityTracking import ActivityTracking
from datetime import datetime


class TrackingService:
    @staticmethod
    def get_login_logs(username: str = "", start_time: datetime = None, end_time: datetime = None):
        return list(LoginLog.select().where(
            (LoginLog.user.contains(username))
            & ((start_time is None) | (LoginLog.time >= start_time))
            & ((end_time is None) | (LoginLog.time <= end_time))
        ))

    @staticmethod
    def get_resource_tracking(start_time: datetime = None, end_time: datetime = None):
        return list(HardwareTracking.select().where(
            ((start_time is None) | (HardwareTracking.time >= start_time))
            & ((end_time is None) | (HardwareTracking.time <= end_time))
        ))

    @staticmethod
    def get_action_tracking(start_time: datetime = None, end_time: datetime = None):
        return list(ActivityTracking.select().where(
            ((start_time is None) | (ActivityTracking.time >= start_time))
            & ((end_time is None) | (ActivityTracking.time <= end_time))
        ))

    @staticmethod
    def add_action(username: str, action: str):
        try:
            ActivityTracking.create(user=username, action=action, time=datetime.now())
        except Exception as e:
            print("Error when add action", username, action)
