import os

SLASH_COMMAND = os.environ.get('SLASH_COMMAND', 'forminder')

# Slack Actions:
DELETE_FORM = 'delete-form'
FILL_FORM_NOW = 'fill-form-now'
SCHEDULE_FORM = 'schedule-form'
CREATE_FORM_SCHEDULE = 'create-form-schedule'
DELETE_SCHEDULE = 'delete-schedule'
SUBMIT_FORM_SCHEDULED = 'submit-form-scheduled'
SUBMIT_FORM_NOW = 'submit-form-now'
VIEW_FORM_SUBMISSIONS = 'view-form-submissions'
FORM_WEEKDAYS = 'form-weekdays'
FORM_TIME = 'form-time'
FORM_FIELD_SUBMISSION = 'form-field-submission'
FORM_FIELD = 'form-field'
SEND_SCHEDULE_TO = 'send-schedule-to'

FIRST_PAGE = 'first_page'
PREVIOUS_PAGE = 'previous_page'
NEXT_PAGE = 'next_page'
LAST_PAGE = 'last_page'

LIST_FORMS_PREFIX = 'list_forms_'
FILL_FORMS_PREFIX = 'fill_forms_'

FORM_ITEMS_PER_PAGE = 5
DEFAULT_SCHEDULE_TIME = '09:00'
MAX_SCHEDULES_PER_FORM = 4
