import datetime
import logging
from enum import Enum

import pytz as pytz
from mongoengine import Document, StringField, ListField, ReferenceField, DateTimeField, EmbeddedDocument, \
    EmbeddedDocumentField, IntField

from util.utils import DAYS_OF_THE_WEEK


class ScheduledTimeStatus(Enum):
    Pending = 'Pending'
    Success = 'Success'
    Failed = 'Failed'


class TimeField(EmbeddedDocument):
    hour = IntField()
    minute = IntField()
    meta = dict(strict=False)

    def __str__(self):
        return f"{str(self.hour).zfill(2)}:{str(self.minute).zfill(2)}"


class SlackFormSchedule(Document):
    user_id = StringField()
    user_name = StringField()
    form_id = StringField()
    days_of_the_week = ListField(IntField())
    timezone = StringField()
    time_local = EmbeddedDocumentField(TimeField)
    meta = dict(strict=False)

    def save_and_schedule_next(self):
        self.save()
        try:
            next_event = self.schedule_next()
        except Exception as e:
            logging.exception("Failed to schedule next. Deleting schedule")
            self.delete()
            raise e
        return next_event

    def schedule_next(self):
        execution_time_utc = self.get_next_time()
        next_event = ScheduledEvent(
            schedule=self,
            execution_time_utc=execution_time_utc,
            status=ScheduledTimeStatus.Pending.value
        )
        next_event.save()
        return next_event

    def get_next_time(self):
        tz = pytz.timezone(self.timezone)
        now_local = datetime.datetime.now(datetime.timezone.utc).astimezone(tz)
        target_time_local = now_local.replace(hour=self.time_local.hour,
                                              minute=self.time_local.minute,
                                              second=0)
        if target_time_local <= now_local:
            target_time_local += datetime.timedelta(days=1)

        while target_time_local.weekday() not in self.days_of_the_week:
            target_time_local += datetime.timedelta(days=1)
        return target_time_local.astimezone(datetime.timezone.utc)

    def schedule_description(self):
        weekdays = ', '.join([DAYS_OF_THE_WEEK[weekday] for weekday in self.days_of_the_week])
        return f"{weekdays} at {str(self.time_local.hour).zfill(2)}:{str(self.time_local.minute).zfill(2)} ({self.timezone})"


class ScheduledEvent(Document):
    schedule = ReferenceField(SlackFormSchedule)
    execution_time_utc = DateTimeField()
    status = StringField()
    meta = dict(strict=False)
