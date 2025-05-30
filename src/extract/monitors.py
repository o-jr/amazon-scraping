from spidermon import Monitor, MonitorSuite, monitors

from spidermon.contrib.scrapy.extensions import Spidermon
#from spidermon.contrib.monitors.mixins.stats import SpidermonStatsMixin
from spidermon.contrib.scrapy.monitors.base import BaseStatMonitor

@monitors.name('Item count')
class ItemCountMonitor(Monitor):
    def test_minimum_items_scraped(self):
        items = getattr(self.data.stats, 'item_scraped_count', 0)
        minimum_threshold = 50
        msg = f'Extracted less than {minimum_threshold} items'
        self.assertTrue(items >= minimum_threshold, msg=msg)

@monitors.name('Status code')
class StatusCodeMonitor(BaseStatMonitor):
    stat_name = 'downloader/response_status_count/200'
    threshold_setting = 'CUSTOM_MIN_STATUS_200'
    assert_type = ">="
    # def test_status_code(self):
    #     status = getattr(self.data.stats, 'response_status_count', {})
    #     expected_status = 200
    #     msg = f'Expected status code {expected_status}, but got {status}'
    #     self.assertTrue(status.get(expected_status, 0) > 0, msg=msg)

class SpiderCloseMonitorSuite(MonitorSuite):
    monitors = [
        ItemCountMonitor,
        StatusCodeMonitor,]  # Add more monitors here