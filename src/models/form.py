import datetime

from mongoengine import Document, StringField, EmbeddedDocument, ListField, EmbeddedDocumentField, BooleanField, \
    DateTimeField, EmbeddedDocumentListField

from src.utils import str_object_id


class SlackFormField(EmbeddedDocument):
    id = StringField(required=True, default=str_object_id)
    type = StringField()
    title = StringField()
    options = ListField(StringField())
    meta = dict(strict=False)


class SlackForm(Document):
    team_id = StringField()
    user_id = StringField()
    user_name = StringField()
    name = StringField()
    fields = EmbeddedDocumentListField(SlackFormField)
    meta = dict(strict=False)

    def number_of_submissions(self):
        return Submission.objects.filter(form_id=str(self.pk)).count()


class SubmissionField(EmbeddedDocument):
    title = StringField()
    value = StringField()

    @property
    def display_title(self):
        if not self.title.endswith('?') and not self.title.endswith(':'):
            return self.title + ':'
        return self.title


class Submission(Document):
    form_id = StringField()
    user_id = StringField()
    user_name = StringField()
    fields = ListField(EmbeddedDocumentField(SubmissionField))
    created_at = DateTimeField(default=datetime.datetime.now)

    @property
    def formatted_date(self):
        return self.created_at.strftime('%b. %-d, %Y')

    @property
    def formatted_time(self):
        return self.created_at.strftime('%H:%M')
