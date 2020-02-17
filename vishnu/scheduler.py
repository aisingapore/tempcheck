import logging
from datetime import datetime
from os import environ

import mandrill
from apscheduler.schedulers.background import BackgroundScheduler
from django.template.loader import render_to_string

from vishnu.models import Entry

logger = logging.getLogger('vishnu.scheduler')


def generate_report():
    """Generate report
    """
    report_dict = {
        'entries': len(Entry.objects.all()),
        'date': datetime.now().strftime("%d %B %Y, %A")
    }
    logger.info(f'Report Variables:\n{report_dict}')
    send_report(report_dict)


def send_report(report_dict: dict):
    """Send reports to emails defined in env file
    """
    try:
        if not environ.get('REPORT_FROM_EMAIL'):
            logger.info(
                'Sender email address not provided. Report will not be sent via email.')
            return

        mandrill_client = mandrill.Mandrill(environ.get('MANDRILL_API_KEY'))

        message = {'subject': environ.get('REPORT_EMAIL_SUBJECT', ''),
                   'from_email': environ.get('REPORT_FROM_EMAIL'),
                   'from_name': environ.get('REPORT_FROM_NAME', ''),
                   'html': render_to_string('report.html', report_dict),
                   'preserve_recipients': False}

        to_emails = environ.get('REPORT_TO_EMAIL', '').split(',')
        to_names = environ.get('REPORT_TO_NAME', '').split(',')
        message['to'] = [{'email': email.strip(), 'name': name.strip()}
                         for email, name in zip(to_emails, to_names)]

        result = mandrill_client.messages.send(message)
        logger.info(f'Mandrill Results:\n{result}')
        logger.info('report sent')
    except mandrill.Error as error:
        logger.error(error)


def start_scheduler():
    config = {
        'second': environ.get('REPORT_SECONDS', '') or None,
        'minute': environ.get('REPORT_MINUTES', '') or None,
        'hour': environ.get('REPORT_HOURS', '') or None,
        'day': environ.get('REPORT_DAYS', '') or None
    }

    logger.info(f'Scheduler Config:\n{config}')

    if any(config.values()):
        scheduler = BackgroundScheduler()
        scheduler.add_job(generate_report, 'cron', **config)
        scheduler.start()
    else:
        logger.info('Configuration not created for report scheduler')
