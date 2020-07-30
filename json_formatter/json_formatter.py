import json
import datetime
import traceback
import logging


DROP = set(['msg', 'args', 'levelname', 'levelno', 'created', 'msecs',
            'relativeCreated', 'message', 'asctime'])


class JSONFormatter:
    def format(self, record):
        ts = datetime.datetime.utcfromtimestamp(record.created)
        obj = {
            'level': record.levelname.lower(),
            'ibm_datetime': ts.strftime('%Y-%m-%dT%H:%M:%S') + '.%03dZ' % record.msecs,
            'label': record.name,
        }

        if isinstance(record.args, tuple) and len(record.args):
            obj['message'] = record.msg % record.args
        else:
            obj['message'] = record.msg

        for attr, value in record.__dict__.items():
            if attr not in DROP and value is not None:
                obj[attr] = value

        einfo = record.exc_info
        if einfo is not None:
            obj['type'] = 'exception'
            obj['exc_info'] = traceback.format_exception(*einfo)

        return json.dumps(obj)


class JSONFilter(logging.Filter):
    def __init__(self, **kwargs):
        self.info = kwargs

    def filter(self, record):
        record.structured_info = self.info
        return True
