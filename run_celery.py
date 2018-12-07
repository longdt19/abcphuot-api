from celery import Celery

from config import Config

celery_app = Celery(__name__,
                    broker=Config.CELERY_BROKER,
                    backend=Config.CELERY_BROKER,
                    include=['api.celery_tasks'])

if __name__ == '__main__':
    celery_app.start()
