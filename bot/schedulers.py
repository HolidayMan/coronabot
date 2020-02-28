from .utils import parse_statistics, send_statistics
import time


def do_all(timeout=43200):
    while True:
        parse_statistics()
        send_statistics()
        time.sleep(timeout)
