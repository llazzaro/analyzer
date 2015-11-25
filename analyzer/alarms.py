import logging
import smtplib
from email.mime.text import MIMEText

from analyzer.constant import (
    CONF_ANALYZER_SECTION,
)

logger = logging.getLogger(__name__)


class Alarm(object):

    def __init__(self, pubsub, config):
        self.config = config
        self.pubsub = pubsub

    def listen(self, channel):
        self.channel = channel
        self.pubsub.subscribe(channel)

    def execute(self, message):
        raise NotImplementedError('Abstract method')

    def consume(self):
        for message in self.pubsub.listen():
            self.execute(message)


class EmailAlarm(Alarm):

    def execute(self, message):
        subject = 'Analyzer Alarm {0}'.format(self.channel)
        logger.info('Sending email with subject {0}'.format(subject))
        msg = MIMEText(str(message))
        msg['Subject'] = subject
        msg['From'] = self.config.get(CONF_ANALYZER_SECTION, 'alarm_from')
        msg['To'] = self.config.get(CONF_ANALYZER_SECTION, 'alarm_to')
        server = smtplib.SMTP(self.config.get(CONF_ANALYZER_SECTION, 'smtp_host'), self.config.get(CONF_ANALYZER_SECTION, 'smtp_port'))
        server.ehlo()
        server.starttls()
        server.login(self.config.get(CONF_ANALYZER_SECTION, 'smtp_login'), self.config.get(CONF_ANALYZER_SECTION, 'smtp_password'))
        try:
            server.send_message(msg)
        except AttributeError:
            server.sendmail(msg['From'], [msg['To']], msg.as_string())

        server.quit()
