#!/usr/bin/python3
import re
import datetime
from dateutil.relativedelta import relativedelta
from datetime import timezone
from tzlocal import get_localzone

BEACON_START = 1378395540

tz = get_localzone()


def timestamp(dt):
    return (dt - datetime.datetime(1970, 1, 1, tzinfo=timezone.utc)).total_seconds()
    # return dt.timestamp()


def get_datetime_from_timestamp(timestamp):
    return datetime.datetime.fromtimestamp(int(timestamp))


def get_datetime_delta(argument):
    invalid_argument_message = '[ERROR]: Invalid argument: [{}]. All datetime values should be positive integers.'
    p = re.compile('(\W*\d+\s+\w+)')
    units = re.findall(p, argument)
    if len(units) == 0:
        print('[ERROR]: No time units found.')
    else:
        delta = {'month': 0, 'day': 0, 'hour': 0, 'minute': 0}
        for pair in units:
            try:
                count, unit = int(pair.split()[0]), pair.split()[1]
            except ValueError:
                print(invalid_argument_message.format(pair))
                return False
            if count < 0:
                print(invalid_argument_message.format(pair))
                return False
            for unit_name in delta.keys():
                if unit.startswith(unit_name):
                    delta[unit_name] = count
                    break
        return delta


def get_relative_datetime(start_date, delta):
    try:
        return start_date - relativedelta(months=delta['month'], days=delta['day'],
                                          hours=delta['hour'], minutes=delta['minute'])
    except ValueError:
        print("[ERROR]: Current date minus delta [{}] results in a date out of range.".format(delta))


def is_args_format_valid(args):
    if len(args) != 5 or (args[1] != '--from' or args[3] != '--to'):
        print('[ERROR]: Invalid input arguments format: --from and --to options not found.')
    elif not (args[2].endswith('ago') and args[4].endswith('ago')):
        print('[ERROR]: "From" and "to" values should end with "ago" word, e.g. "3 months ago". '
              'To prove that you are not a robot, and you have read and understood this message, '
              'please add it :)')
    else:
        return True


def is_date_interval_valid(from_datetime, to_datetime):
    resulting_dates_message = "[INFO ]: Resulting dates: from = {}; to = {}".format(from_datetime, to_datetime)
    if from_datetime > to_datetime:
        print("[ERROR]: 'From' points at the moment of time after 'to'.")
        print(resulting_dates_message)
    else:
        try:
            start_date_valid = timestamp(from_datetime) >= BEACON_START
            if not start_date_valid:
                print("[ERROR]: 'From' points at the moment of time before the start of the beacon, "
                      "1378395540 Unix Epoch time.")
                print(resulting_dates_message)
        except OverflowError:
            print("[ERROR]: 'From' points at the moment of time before the start of Unix Epoch time.")
            print(resulting_dates_message)
            start_date_valid = False
        return start_date_valid


def get_timestamps(args):
    if is_args_format_valid(args):
        from_delta, to_delta = get_datetime_delta(args[2]), get_datetime_delta(args[4])
        if from_delta and to_delta:
            now = datetime.datetime.now(tz)
            from_datetime = get_relative_datetime(now, from_delta)
            to_datetime = get_relative_datetime(now, to_delta)
            if from_datetime and to_datetime and is_date_interval_valid(from_datetime, to_datetime):
                return {'from': str(timestamp(from_datetime)).split(".")[0],
                        'to': str(timestamp(to_datetime)).split(".")[0]}