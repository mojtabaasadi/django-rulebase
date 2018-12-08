from django.conf import settings
import django,os,sys
from django.db import models

filename = os.path.splitext(os.path.basename(__file__))[0]
dierectory = os.path.abspath(__file__).replace(filename+".py", "")
settings.configure(
DEBUG=True,
DATABASES={
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(dierectory, 'db.sqlite3'),
    }
    },
    INSTALLED_APPS = ['test_app']
)
django.setup()


class TestModel(models.Model):
    id = models.IntegerField(primary_key=True)
    title= models.CharField()
    desc = models.CharField()
    class Meta:
        db_table = "test"