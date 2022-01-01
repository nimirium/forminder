from mongoengine import Q

from models.form import SlackForm
from models.schedule import SlackFormSchedule
from util import slack_blocks
from util.slack_blocks import random_skin_tone


def _no_forms_text():
    return f""":information_desk_person:{random_skin_tone()} There are no forms yet
:information_source: use “/ask-remind create form” to create one"""


def list_form_blocks(user_id):
    forms = SlackForm.objects(Q(user_id=user_id) or Q(public=True))
    if forms.count() == 0:
        return [slack_blocks.text_block_item(_no_forms_text())]
    blocks = [slack_blocks.text_block_item("*List of forms:*"), slack_blocks.divider]
    for i, form in enumerate(forms):
        schedules = SlackFormSchedule.objects(form_id=str(form.id))
        for block in slack_blocks.form_list_item(form, schedules):
            blocks.append(block)
        blocks.append(slack_blocks.form_list_item_action_buttons(str(form.id)))
        if i < forms.count():
            blocks.append(slack_blocks.divider)
    return blocks
