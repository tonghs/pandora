import datetime

from peewee import Model, DateTimeField, SQL
from playhouse.shortcuts import model_to_dict, update_model_from_dict

from pandora.extensions import db


class BaseDAO(Model):
    _create_time = DateTimeField(default=datetime.datetime.now, null=False, constraints=[SQL('DEFAULT CURRENT_TIMESTAMP')])
    _update_time = DateTimeField(default=datetime.datetime.now, null=False, constraints=[SQL('DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP')])

    class Meta:
        database = db

    def save(self, *args, **kwargs):
        now = datetime.datetime.now()
        if hasattr(self, 'update_time'):
            self.update_time = now
        if hasattr(self, '_update_time'):
            self._update_time = now
        return super().save(*args, **kwargs)

    def update_from_dict(self, data) -> Model:
        update_model_from_dict(self, data)
        self.save()
        return self

    def to_dict(self, **kwargs) -> dict:
        return model_to_dict(self, **kwargs)
