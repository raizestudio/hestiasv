import os

from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")

app = Celery("core")

# Using a string here means the worker doesn't have to serialize
app.config_from_object("django.conf:settings", namespace="CELERY")

app.autodiscover_tasks()


@app.task(bind=True, ignore_result=True)
def debug_task(self):
    # import pika

    # connection = pika.BlockingConnection(pika.ConnectionParameters("localhost"))
    # channel = connection.channel()
    # channel.queue_declare(queue="hello")
    # channel.basic_publish(exchange="", routing_key="hello", body="Hello World!")
    # connection.close()
    print(f"Request: {self.request!r}")
