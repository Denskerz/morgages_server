import json
import logging
from pythonjsonlogger import jsonlogger


class JsonFormatter(jsonlogger.JsonFormatter):
    EXTRA_PREFIX = "extra_"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def add_fields(self, log_record, record, message_dict):
        super().add_fields(log_record, record, message_dict)
        # update the timestamp format
        log_record["timestamp"] = self.formatTime(record, self.datefmt)
        log_record["level"] = record.levelname
        # log_record["system_message"] = record.exc_info
        # log_record["logger_name"] = record.name
        # trace = self._get_trace_id()

        # if trace:
        #    log_record["trace_id"] = trace

        return self.set_extra_keys(record, log_record, self._skip_fields)

    def jsonify_log_record(self, log_record):
        """Returns a json string of the log record."""
        return self.json_serializer(log_record,
                                    default=self.json_default,
                                    cls=self.json_encoder,
                                    indent=self.json_indent,
                                    ensure_ascii=False)

    @staticmethod
    def is_private_key(key):
        return hasattr(key, "startswith") and key.startswith("_")

    @staticmethod
    def is_extra_key(key):
        return hasattr(key, "startswith") and key.startswith(JsonFormatter.EXTRA_PREFIX)

    @staticmethod
    def set_extra_keys(record, log_record, reserved):
        """
        Add the extra data to the log record.
        prefix will be added to all custom tags.
        """
        record_items = list(record.__dict__.items())
        records_filtered_reserved = [item for item in record_items if item[0] not in reserved]
        records_filtered_private_attr = [item for item in records_filtered_reserved if
                                         not JsonFormatter.is_private_key(item[0])]

        for key, value in records_filtered_private_attr:
            if not JsonFormatter.is_extra_key(key):
                if isinstance(value, (dict, list)):
                    value = json.dumps(value, ensure_ascii=False)
                new_key_name = f"{JsonFormatter.EXTRA_PREFIX}{key}"
                log_record[new_key_name] = value
                log_record.pop(key, None)

    @staticmethod
    def _get_trace_id():
        """
        The trace id can be used for tracing logs across multiple services.
        It's fetched from the headers of the request.
        Should be implemented according to the tracing mechanism of the service.
        e.g in flask or fastapi:
        trace_id = request.headers.get("X-Trace-Id")
        """

        return "example_trace_id"


logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

file_handler = logging.FileHandler('logs.json', "w", encoding='UTF-8')
file_handler.setLevel(logging.DEBUG)

file_handler.setFormatter(JsonFormatter())
logger.addHandler(file_handler)
