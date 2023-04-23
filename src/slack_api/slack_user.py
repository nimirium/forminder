from src.slack_api.slack_client import get_users_info


class SlackUser:
    def __init__(self, user_id):
        self.id = user_id
        user_info = get_users_info(self.id)
        self.username = user_info['username']
        self.real_name = user_info['real_name']
        self.team_id = user_info['team_id']
        self.is_admin = user_info['is_admin']
        self.tz = user_info['tz']

    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'real_name': self.real_name,
            'team_id': self.team_id,
            'tz': self.tz,
        }