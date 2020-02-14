import logging
from os import environ

import mandrill
from apscheduler.schedulers.background import BackgroundScheduler

from vishnu.models import Entry


def generate_report():
    """
    Temporary placeholder function to test scheduler
    """
    # print(f'Number of entries: {len(Entry.objects.all())}')
    pass


def send_report():
    try:
        if not environ.get('REPORT_FROM_EMAIL'):
            logging.info(
                'Sender email address not provided. Report will not be sent via email.')
            return

        mandrill_client = mandrill.Mandrill(environ.get('MANDRILL_API_KEY'))

        message = {'subject': environ.get('REPORT_EMAIL_SUBJECT', ''),
                   'from_email': environ.get('REPORT_FROM_EMAIL'),
                   'from_name': environ.get('REPORT_FROM_NAME', ''),
                   'html': '<p>Example HTML content</p>',
                   'preserve_recipients': False}

        to_emails = environ.get('REPORT_TO_EMAIL', '').split(',')
        to_names = environ.get('REPORT_TO_NAME', '').split(',')
        message['to'] = [{'email': email.strip(), 'name': name.strip()}
                         for email, name in zip(to_emails, to_names)]

        result = mandrill_client.messages.send(message)
        logging.info(f'Mandrill Results:\n{result}')
    except mandrill.Error as error:
        logging.error(error)


def start_scheduler():
    config = {
        'second': environ.get('REPORT_SECONDS', '') or None,
        'minute': environ.get('REPORT_DAY', '') or None,
        'hour': environ.get('REPORT_HOURS', '') or None,
        'day': environ.get('REPORT_MINUTES', '') or None
    }

    logging.info(f'Scheduler Config:\n{config}')

    scheduler = BackgroundScheduler()
    scheduler.add_job(generate_report, 'cron', **config)
    scheduler.start()
