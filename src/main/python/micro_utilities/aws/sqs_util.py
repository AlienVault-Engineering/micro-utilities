import logging
from types import FunctionType

from boto import sqs, connect_s3
from boto.sqs.jsonmessage import JSONMessage

from micro_utilities.config import ConfigManager


def _init_queue(queue_name):
    conn = sqs.connect_to_region(region_name=ConfigManager.get_value_default("region", "us-west-2"))
    queue = conn.create_queue(queue_name)
    queue.set_message_class(JSONMessage)

    return conn, queue


def monitor_queue(queue_name_config_key, processing_function_pointer):
    # type: (str, FunctionType) -> None
    conn, queue = _init_queue(ConfigManager.get_value(queue_name_config_key))
    logging.info("Listening to queue %s", queue.name)
    while True:
        result_set = conn.receive_message(queue, number_messages=10, wait_time_seconds=20)
        count = 0
        if result_set:
            to_delete = []
            logging.info("Received %d messages", len(result_set))
            for message in result_set:
                try:
                    processing_function_pointer(message.get_body())
                    to_delete.append(message)
                    count += 1
                except Exception as e:
                    logging.error("Error peristing message %s", e.message)
            if len(to_delete) >0:
                conn.delete_message_batch(queue=queue, messages=to_delete)
