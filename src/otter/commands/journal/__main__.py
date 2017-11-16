"""Otter Pilot command journal."""
import logging
import pathlib
import shutil

import click
import pendulum

LOG = logging.getLogger(__name__)

PATH_FORMAT = '~/bag/journal/{year}/{month}/{date}.md'
TEMPLATE_PATH = pathlib.Path('~/.daily_template.md').expanduser()


def output_yesterday():
    """Fetch and display yesterday's journal."""
    output = []

    yesterday = pendulum.yesterday()
    LOG.debug('Yesterday: %s', yesterday)

    if yesterday.day_of_week in yesterday.get_weekend_days():
        yesterday = yesterday.previous(day_of_week=pendulum.FRIDAY)
        LOG.debug('Yesterday was a weekend, using last Friday: %s', yesterday)

    path = PATH_FORMAT.format(year=yesterday.year, month=yesterday.month, date=yesterday.to_date_string())
    path = pathlib.Path(path).expanduser()
    LOG.debug('Path of yesterday: %s', path)

    with path.open('rt') as path_handle:
        output = path_handle.readlines()
    LOG.debug('Yesterday output: %s', output)

    return output


def journal_today():
    """Write in today's journal."""
    today = pendulum.create()
    LOG.debug('Today: %s', today)

    path = PATH_FORMAT.format(year=today.year, month=today.month, date=today.to_date_string())
    path = pathlib.Path(path).expanduser()
    LOG.debug('Path of today: %s', path)

    parent = path.parent
    if not parent.exists():
        parent.mkdir(exist_ok=True)
        LOG.debug('Created new path: %s', parent)

    if not path.exists():
        shutil.copyfile(TEMPLATE_PATH, path)

    text = click.edit(filename=path)

    return text


@click.command()
@click.option('-y', '--yesterday', 'yesterday_option', is_flag=True, help='Grab journal from yesterday.')
def main(yesterday_option):
    """Otter Pilot journal.

    Good for taking care of business.
    """
    if yesterday_option:
        output = output_yesterday()
        print(''.join(output))
    else:
        journal_today()
    print('Otter Pilot journal reporting for duty!')


if __name__ == '__main__':
    main()
