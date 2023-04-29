import redis
from celery import Celery
# from web import celery_config

# Redis client to hold the cache from slow callbacks
redis_client = redis.Redis(host="localhost", port=6379, db=1)

# celery app to manage tasks
celery_app = Celery("tasks")
celery_app.config_from_object("web.celery_config")

