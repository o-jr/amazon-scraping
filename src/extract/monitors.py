import datetime

from spidermon import Monitor, MonitorSuite, monitors
from spidermon.contrib.actions.reports.files import CreateFileReport
from spidermon.contrib.scrapy.monitors.monitors import (
    ItemValidationMonitor, 
    ErrorCountMonitor,
)


from spidermon.contrib.monitors.mixins.stats import StatsMonitorMixin
from spidermon.contrib.scrapy.extensions import Spidermon
from spidermon.contrib.scrapy.monitors.base import BaseStatMonitor

@monitors.name('Item count')
class ItemCountMonitor(Monitor):
    def test_minimum_items_scraped(self):
        items = getattr(self.data.stats, 'item_scraped_count', 0)
        minimum_threshold = 40
        msg = f'Extracted less than {minimum_threshold} items {items}'
        #msg = "EEExtracted less thanNN {} items".format(minimum_threshold)
        self.assertTrue(items >= minimum_threshold, msg=msg)

class PeriodicExecutionTimeMonitor(Monitor, StatsMonitorMixin):
    @monitors.name('Mazimum execution time reached')
    def test_maximum_execution_time(self):
        crawler = self.data.get("crawler")
        max_execution_time = crawler.settings.getint("SPIDERMON_MAX_EXECUTION_TIME")  # Default to 30 minutes
        if not max_execution_time:
            return

        tzinfo = datetime.timezone(datetime.timedelta(hours=0))  # UTC timezone
        now = datetime.datetime.now(tz=tzinfo)

        start_time = self.data.stats.get('start_time')
        if not start_time:
            return
        duration = now - start_time
        msg = "!!!The job has exceeded the maximum execution time!!!"
        self.assertLess(duration.total_seconds(), max_execution_time, msg=msg)

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
        ErrorCountMonitor,
        ItemValidationMonitor,
        #StatusCodeMonitor,
        ] 

class PeriodicMonitorSuite(MonitorSuite):
    monitors = [
        PeriodicExecutionTimeMonitor,  # Custom monitor for periodic execution time
        # ItemCountMonitor,
        # ErrorCountMonitor,
        # ItemValidationMonitor,
        # StatusCodeMonitor,
    ]

    # actions = [
    #     CreateFileReport,
    # ]

    # @monitors.name('Periodic Monitor Suite')
    # def test_periodic_monitor_suite(self):
    #     self.assertTrue(True, msg="Periodic Monitor Suite executed successfully.")        