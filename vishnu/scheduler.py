from os import environ

from apscheduler.schedulers.background import BackgroundScheduler

from vishnu.models import Entry


def generate_report():
    """
    Temporary placeholder function to test scheduler
    """
    print(f'Number of entries: {len(Entry.objects.all())}')


def start_scheduler():
    config = {
        'second': environ.get('REPORT_SECONDS', ''),
        'day': environ.get('REPORT_MINUTES', ''),
        'hour': environ.get('REPORT_HOURS', ''),
        'minute': environ.get('REPORT_DAY', '')
    }

    # process config
    for key, value in config.items():
        if value == '':
            config[key] = None

    print(config)

    scheduler = BackgroundScheduler()
    scheduler.add_job(generate_report, 'cron', **config)
    scheduler.start()
