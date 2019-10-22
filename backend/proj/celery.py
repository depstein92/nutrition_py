from __future__ import absolute_import, unicode_literals
from celery import Celery

app = Celery('proj',
             broker='amqp://dan:dan@localhost:5672/dan_host',
             backend='db+sqlite:///data.db',
             ignore_result=False,
             include=['proj.tasks'])

# Optional configuration, see the application user guide.
app.conf.update(
    result_expires=3600,
)
