from src.slack_api.slack_client import get_users_info


class SlackUser:
    def __init__(self, user_id, user_name, team_id, team_domain):
        self.id = user_id
        self.username = user_name
        self.team_id = team_id
        self.team_domain = team_domain
        user_info = get_users_info(self.id)
        self.is_admin = user_info['is_admin']
        self.tz = user_info['tz']
