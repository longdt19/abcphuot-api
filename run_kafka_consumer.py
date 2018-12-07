from kafka import KafkaConsumer

from api.celery_tasks import sync_customer_task


def run():
    consumer = KafkaConsumer('crm-staging', bootstrap_servers=['103.69.195.228:9092'])
    for message in consumer:
        raw_data = message.value.decode('utf-8')
        sync_customer_task.delay(raw_data)


if __name__ == '__main__':
    run()
