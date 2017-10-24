import requests
from requests.adapters import HTTPAdapter
from urllib3 import Retry

from micro_utilities.config import ConfigManager

request_session = None
retry_attempts = ConfigManager.get_value_default('retry-attempts',3)

def session():
    global request_session
    if request_session is None:
        request_session = requests.Session()

        # This will allow 5 tries at a url, with an increasing backoff.  Only applies to a specific set of codes
        request_session.mount('https://', HTTPAdapter(
            max_retries=Retry(
                total=retry_attempts,
                status_forcelist=[429, 500, 502, 503],
                backoff_factor=5,
            )
        ))
        request_session.mount('http://', HTTPAdapter(
            max_retries=Retry(
                total=retry_attempts,
                status_forcelist=[429, 500, 502, 503],
                backoff_factor=5,
            )
        ))

    return request_session
