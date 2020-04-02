# pylint: disable=no-member

import logging
from datetime import datetime, timedelta
from os import environ

import mandrill
import pytz
from apscheduler.schedulers.background import BackgroundScheduler
from django.contrib.auth.models import User
from django.db.models import Count, Q
from django.template.loader import render_to_string

from vishnu.models import Entry

logger = logging.getLogger('vishnu.scheduler')


def generate_report(daily_submission: int, interval: dict):
    """Generate report
    """
    pst = pytz.timezone('Singapore')
    report_dict = {'date': datetime.now(
        tz=pst).strftime("%d %B %Y %I:%M %p, %A")}

    # total submissions for reporting period
    filter_datetime = datetime.utcnow() - timedelta(**interval)
    filter_set = Entry.objects.filter(date_created__gt=filter_datetime)

    # total submissions
    report_dict['total_submissions'] = {}
    if interval['days'] == 1:
        # convert to Singapore Timezone first
        for i in filter_set:
            i.sgt_date_created = i.date_created.astimezone(pst)

        report_dict['total_submissions']['AM'] = len(
            [i for i in filter_set if i.sgt_date_created.hour < 12])
        report_dict['total_submissions']['PM'] = filter_set.count(
        ) - report_dict['total_submissions']['AM']
    else:
        report_dict['total_submissions']['Total'] = filter_set.count()

    # submissions above 38 degrees
    high_temp = filter_set.filter(temperature__gt=38).order_by('temperature')
    report_dict['high_temp'] = [{'temperature': i.temperature,
                                 'username': i.owner.get_username()} for i in high_temp]

    # incomplete submissions
    user_set = User.objects.annotate(
        number_of_entries=Count('records', filter=Q(records__date_created__gt=filter_datetime)))
    report_dict['incomplete_users'] = user_set.filter(
        number_of_entries__lt=daily_submission
    ).values_list('username', flat=True).order_by('username')

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

        message = {'subject': environ.get('REPORT_EMAIL_SUBJECT', 'Tempcheck report'),
                   'from_email': environ.get('REPORT_FROM_EMAIL'),
                   'from_name': environ.get('REPORT_FROM_NAME', 'Tempcheck'),
                   'html': render_to_string('report.html', report_dict, using='jinja2'),
                   'preserve_recipients': False}

        to_emails = environ.get('REPORT_TO_EMAIL', '').split(',')
        to_names = environ.get('REPORT_TO_NAME', '').split(',')
        message['to'] = [{'email': email.strip(), 'name': name.strip()}
                         for email, name in zip(to_emails, to_names)]

        result = mandrill_client.messages.send(message)
        logger.info(f'Mandrill Results:\n{result}')
        logger.info('Report sent')
    except mandrill.Error as error:
        logger.error(error)


def start_scheduler():
    config = {
        'seconds': int(environ.get('REPORT_INTERVAL_SECONDS', 0) or 0),
        'minutes': int(environ.get('REPORT_INTERVAL_MINUTES', 0) or 0),
        'hours': int(environ.get('REPORT_INTERVAL_HOURS', 0) or 0),
        'days': int(environ.get('REPORT_INTERVAL_DAYS', 0) or 0)
    }

    args = {
        'daily_submission': int(environ.get('REPORT_EXPECTED_DAILY', '1')),
        'interval': config
    }

    logger.info(f'Scheduler Config: {config}')

    if any(config.values()):
        scheduler = BackgroundScheduler()
        # interval timing starts at 12am SGT
        scheduler.add_job(generate_report, 'interval', kwargs=args,
                          start_date='2020-01-01 16:00:00', **config)
        scheduler.start()
    else:
        logger.info('Configuration not created for report scheduler')
