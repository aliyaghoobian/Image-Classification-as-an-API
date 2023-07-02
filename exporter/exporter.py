import os
import time
from prometheus_client import start_http_server, Gauge, Histogram, Counter
import requests
import logging

logger=logging.getLogger() 

_INF = float("inf")


class AppMetrics:
    def __init__(self, app_port=8000, polling_interval_seconds=5):
        self.app_port = app_port
        self.polling_interval_seconds = polling_interval_seconds

        # Prometheus metrics to collect
        self.total_requests = Counter("total_request","Total request")
        self.total_succ_requests = Counter("total_succ_request", "Total successful request")
        self.total_fail_requests = Counter("app_total_fail_request","Total failed request")
        self.time_dur = Histogram('python_request_duration_seconds', 'Histogram for the duration in seconds.', buckets=(1, 2, 5, 6, 10, _INF))

        self.total_number_per_label =  {
            'airplane': Counter("total_airplane_requests", "Total airplane requests"),
            'automobile': Counter("total_automobile_request", "Total automobile requests"),
            'bird': Counter("total_bird_requests", "Total bird requests"),
            'cat':Counter("total_cat_requests", "Total cat requests"),
            'deer':Counter("total_deer_requests", "Total deer requests"),
            'dog':Counter("total_dog_requests", "Total dog requests"),
            'frog':Counter("total_frog_requests", "Total frog requests"),
            'horse':Counter("total_horse_requests", "Total horse requests"),
            'ship':Counter("total_ship_requests", "Total ship requests"),
            'truck':Counter("total_truck_requests", "Total truck requests")
            }


        self.total_acc_per_label =  {
            'airplane': Gauge("total_airplane_acc", "total airplane accuracy"),
            'automobile': Gauge("total_automobile_acc", "total automobile accuracy"),
            'bird': Gauge("total_bird_acc", "total bird accuracy"),
            'cat':Gauge("total_cat_acc", "total cat accuracy"),
            'deer':Gauge("total_deer_acc", "total deer accuracy"),
            'dog':Gauge("total_dog_acc", "total dog accuracy"),
            'frog':Gauge("total_frog_acc", "total frog accuracy"),
            'horse':Gauge("total_horse_acc", "total horse accuracy"),
            'ship':Gauge("total_ship_acc", "total ship accuracy"),
            'truck':Gauge("total_truck_acc", "total truck accuracy")
            }

        self.average_acc = Gauge("average_acc", "Average accuracy for all labels")

    def run_metrics_loop(self):
        while True:
            self.fetch()
            time.sleep(self.polling_interval_seconds)

    def fetch(self):
        # Fetch raw status data from the application
        try:
            headers = {'Accept': 'application/json'}
            resp = requests.get(url=f"http://localhost:{self.app_port}/metric", headers=headers)
            status_data = resp.json()
        except Exception as e:
            print(e)

        # Update Prometheus metrics with application metrics
        self.total_requests.inc(status_data['suc_requests'] + status_data['failed_requests'] - self.total_requests._value.get())
        self.total_requests.inc(status_data['suc_requests'] - self.total_requests._value.get())
        self.total_fail_requests.inc(status_data['failed_requests'] - self.total_fail_requests._value.get())

        for item, accuracy in status_data['acc_per_label'].items():
            for acc in accuracy:
                self.total_acc_per_label[item].set(accuracy)

        for item, num in status_data['num_labels'].items():
            self.total_number_per_label[item].inc(num - self.total_number_per_label[item]._value.get())
        
        for dur in status_data['time_dur']:
            self.time_dur.observe(dur)

def main():

    polling_interval_seconds = int(os.getenv("POLLING_INTERVAL_SECONDS", "5"))
    app_port = int(os.getenv("APP_PORT", "8000"))
    exporter_port = int(os.getenv("EXPORTER_PORT", "9877"))
    logger.info(f"exporter started on port 9877")
    
    app_metrics = AppMetrics(
        app_port=app_port,
        polling_interval_seconds=polling_interval_seconds
    )
    start_http_server(exporter_port)
    app_metrics.run_metrics_loop()

if __name__ == "__main__":
    main()