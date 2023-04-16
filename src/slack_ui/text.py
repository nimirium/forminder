from src.constants import SLASH_COMMAND

help_text = f""":information_desk_person: Usage:
:magic_wand: /{SLASH_COMMAND} create
:magic_wand: /{SLASH_COMMAND} list
:magic_wand: /{SLASH_COMMAND} fill"""


form_create_help_text = f""":information_desk_person: To create a form, follow these steps:

:zap: Type: /{SLASH_COMMAND} create [options] :zap:

:jigsaw: Options: :jigsaw:
Select a name
    Use --form-name followed by the form name you want.
Add fields
    - To add a single-line text field, use --text-field followed by the field name.
    - For a multi-line text field, use --multiline-field followed by the field name.
    - To add a dropdown menu, use --select-field followed by the field name and the available options separated by commas.

:airplane: Example: :airplane:
/{SLASH_COMMAND} create --form-name=“Project Update” --text-field=“Task Name” --select-field=“Progress:Not Started,In Progress,Completed” --multiline-field=“Notes or Challenges”
"""

no_forms_text = f""":information_desk_person: There are no forms yet
:information_source: use “/{SLASH_COMMAND} create” to create one"""
