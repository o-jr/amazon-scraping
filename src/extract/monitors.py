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

# @monitors.name('Item count')
# class ItemCountMonitor(Monitor):
#     def test_minimum_items_scraped(self):
#         items = getattr(self.data.stats, 'item_scraped_count', 0)
#         minimum_threshold = 50
#         #msg = f'Extracted less than {minimum_threshold} items: {items}'
#         msg = "EEExtracted less thanNN {} items".format(minimum_threshold)
#         self.assertTrue(items >= minimum_threshold, msg=msg)

class PeriodicExecutionTimeMonitor(Monitor, StatsMonitorMixin):
    @monitors.name('Maximum execution time reached')
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


@monitors.name('Item count')
class ItemCountMonitor(BaseStatMonitor):
    stat_name = "item_scraped_count"
    threshold_setting = "CUSTOM_MIN_ITEMS_SCRAPED"
    assert_type = ">="


@monitors.name('200 Status Code')
class StatusCodeMonitor(BaseStatMonitor):
    stat_name = "downloader/response_status_count/200"
    threshold_setting = "CUSTOM_MIN_STATUS_200"
    assert_type = ">="
    # def test_status_code(self):
    #     status = getattr(self.data.stats, 'response_status_count', {})
    #     expected_status = 200
    #     msg = f'Expected status code {expected_status}, but got {status}'
    #     self.assertTrue(status.get(expected_status, 0) > 0, msg=msg)


@monitors.name('503 Error Monitor')
class StatusErrorMonitor(BaseStatMonitor):
    stat_name = "downloader/response_status_count/503"
    threshold_setting = "CUSTOM_MAX_STATUS_503"
    assert_type = "<="  # You may want to define a threshold for acceptable errors



class SpiderCloseMonitorSuite(MonitorSuite):
    monitors = [
        ItemCountMonitor,
        ErrorCountMonitor,
        ItemValidationMonitor,
        StatusCodeMonitor,
        StatusErrorMonitor,
        PeriodicExecutionTimeMonitor,
        ] 

    monitors_finished_actions = [
        CreateFileReport,
    ]


# class PeriodicMonitorSuite(MonitorSuite):
#     monitors = [
#         PeriodicExecutionTimeMonitor,
#     ]  