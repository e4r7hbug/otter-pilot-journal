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
    """Fetch path to yesterday's journal.

    Args:
        max_past_days (int): Max allowed days to go back in time.

    Returns:
        list: Lines from yesterday's journal.

    """
    path = None

    for yesterday_path in yesterdays(max_past_days=max_past_days):
        if yesterday_path.is_file():
            path = yesterday_path
            LOG.debug('Found last known journal.')
            break
    else:
        raise ValueError('Could not find previous journal in past {0:d} days.'.format(max_past_days))

    return path


def journal_today():
    """Create today's journal if needed and return path."""
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

    return path


def edit_or_output(output=True, path=None):
    """Open the journal file for editing or outputting.
    
    Args:
        output (bool): Print journal when :obj:`True` or open editor.
        path (pathlib.Path): Path of Journal file.

    """
    text = None

    if output:
        with path.open('rt') as path_handle:
            text = path_handle.read()
        click.echo(''.join(text))
    else:
        text = click.edit(filename=path)

    return text


@click.command()
@click.option('-o', '--output', is_flag=True, help='Only output journal contents.')
@click.option('-y', '--yesterday', 'yesterday_option', is_flag=True, help='Grab journal from yesterday.')
def main(output, yesterday_option):
    """Otter Pilot journal.

    Good for taking care of business.
    """
    if yesterday_option:
        path = output_yesterday()
    else:
        path = journal_today()

    edit_or_output(output=output, path=path)

    LOG.info('Otter Pilot journal reporting for duty!')


if __name__ == '__main__':
    main()
