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
    public = BooleanField()
    meta = dict(strict=False)

    def number_of_submissions(self):
        return Submission.objects.filter(form_id=self.pk).count()


class SubmissionField(EmbeddedDocument):
    title = StringField()
    value = StringField()


class Submission(Document):
    form_id = StringField()
    user_id = StringField()
    fields = ListField(EmbeddedDocumentField(SubmissionField))
    created_at = DateTimeField(default=datetime.datetime.now)
