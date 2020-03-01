import time
import schedule
from .utils import parse_statistics, send_statistics


schedule.every(15).minutes.do(parse_statistics)
schedule.every(12).hours.do(send_statistics)


def do_all():
    parse_statistics()
    send_statistics()
    while True:
        schedule.run_pending()
        time.sleep(1)
