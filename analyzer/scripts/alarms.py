from analyzer.alarms import EmailAlarm

from . import (
    initialize_config,
    initialize_redis,
)


def execute(config, pubsub, channel):
    alarm = EmailAlarm(pubsub, config)
    alarm.listen(channel)

    while True:
        alarm.consume()


def main():
    config = initialize_config()
    redis_conn = initialize_redis(config)
    channel = 'actions'
    execute(config, redis_conn.pubsub(), channel)
