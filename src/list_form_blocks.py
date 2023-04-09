import os

from src import slack_ui_blocks
from src.constants import SLASH_COMMAND
from src.models.form import SlackForm
from src.models.schedule import FormSchedule
from src.slack_api.slack_user import SlackUser


def _no_forms_text():
    return f""":information_desk_person: There are no forms yet
:information_source: use “/{SLASH_COMMAND} create” to create one"""


def list_form_blocks(user: SlackUser):
    """
    Slack UI blocks with a list of Forms
    """
    forms = SlackForm.objects(user_id=user.id)
    if forms.count() == 0:
        return [slack_ui_blocks.text_block_item(_no_forms_text())]
    blocks = [slack_ui_blocks.text_block_item(
        f"*List of forms* <{os.environ['DOMAIN']}/forms|[View in the Forminder website]>"), slack_ui_blocks.divider]
    for i, form in enumerate(forms):
        schedules = FormSchedule.objects(form_id=str(form.id))
        for block in slack_ui_blocks.form_list_item(form, schedules):
            blocks.append(block)
        can_delete = form.user_id == user.id or user.is_admin
        blocks.append(slack_ui_blocks.form_list_item_action_buttons(str(form.id), can_delete))
        if i < forms.count():
            blocks.append(slack_ui_blocks.divider)
    return blocks
