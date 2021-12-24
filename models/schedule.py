from datetime import datetime, timedelta

from mongoengine import Document, StringField, ListField, ReferenceField, DateTimeField, EmbeddedDocument, EmbeddedDocumentField, IntField

from util.utils import get_datetime_as_timezone


class TimeField(EmbeddedDocument):
    hour = IntField()
    minute = IntField()
    second = IntField()


class SlackFormSchedule(Document):
    user_id = StringField()
    user_name = StringField()
    form_id = StringField()
    days_of_the_week = ListField(StringField())
    timezone = StringField()
    time_local = EmbeddedDocumentField(TimeField)
    meta = dict(strict=False)

    def schedule_next(self):
        execution_time_utc = self.get_next_time()
        ScheduledTime(schedule=self, execution_time_utc=execution_time_utc, status='Pending').save()

    def get_next_time(self):
        now_local = get_datetime_as_timezone(datetime.now())
        target_time_local = now_local.replace(hour=self.time_local.hour,
                                              minute=self.time_local.minute,
                                              second=self.time_local.second)
        if target_time_local <= now_local:
            target_time_local += timedelta(days=1)

        while target_time_local.weekday() not in self.days_of_the_week:
            target_time_local += timedelta(days=1)
        return target_time_local


class ScheduledTime(Document):
    schedule = ReferenceField(SlackFormSchedule)
    execution_time_utc = DateTimeField
    status = StringField()
    meta = dict(strict=False)


def create_schedule(schedule: SlackFormSchedule):
    schedule.save()
