"""Otter Pilot command journal."""
import logging
import pathlib
import shutil

import click
import pendulum

LOG = logging.getLogger(__name__)

PATH_FORMAT = '~/bag/journal/{year}/{month}/{date}.md'
TEMPLATE_PATH = pathlib.Path('~/.daily_template.md').expanduser()


def yesterdays(max_past_days=10):
    """Generate previous days starting from yesterday.

    Args:
        max_past_days (int): Max allowed days to go back in time.

    Yields:
        PosixPath: Fully qualified path to potential journal file.

    """
    yesterday = pendulum.yesterday()
    LOG.debug('Yesterday: %s', yesterday)

    for number_of_days in range(max_past_days):
        past = yesterday.subtract(days=number_of_days)
        path = PATH_FORMAT.format(year=past.year, month=past.month, date=past.to_date_string())
        path = pathlib.Path(path).expanduser()
        LOG.debug('Path of past day: %s', path)

        yield path


def output_yesterday(max_past_days=10):
    """Fetch and display yesterday's journal.

    Args:
        max_past_days (int): Max allowed days to go back in time.

    Returns:
        list: Lines from yesterday's journal.

    """
    output = []

    path = None

    for yesterday_path in yesterdays(max_past_days=max_past_days):
        if yesterday_path.is_file():
            path = yesterday_path
            LOG.debug('Found last known journal.')
            break
    else:
        raise ValueError('Could not find previous journal in past {0:d} days.'.format(max_past_days))

    with path.open('rt') as path_handle:
        output = path_handle.readlines()
    LOG.debug('Yesterday output: %s', output)

    return output


def journal_today():
    """Write in today's journal."""
    today = pendulum.today()
    LOG.debug('Today: %s', today)

    path = PATH_FORMAT.format(year=today.year, month=today.month, date=today.to_date_string())
    path = pathlib.Path(path).expanduser()
    LOG.debug('Path of today: %s', path)

    parent = path.parent
    if not parent.exists():
        parent.mkdir(parents=True, exist_ok=True)
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
    LOG.info('Otter Pilot journal reporting for duty!')


if __name__ == '__main__':
    main()
