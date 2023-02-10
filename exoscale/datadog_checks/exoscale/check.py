import json
from urllib.error import HTTPError

from requests.exceptions import InvalidURL, Timeout

from exoscale_auth import ExoscaleV2Auth

from datadog_checks.base import AgentCheck, ConfigurationError
from datadog_checks.base.errors import CheckException

BASE_URL = "https://api-{region}.exoscale.com/v2{path}"
METRICS = "/dbaas-service-metrics/{service_name}"
WARNING_QUOTA = 75
CRITICAL_QUOTA = 85


class ExoscaleCheck(AgentCheck):
    __NAMESPACE__ = 'exoscale'

    def __init__(self, name, init_config, instances):
        super(ExoscaleCheck, self).__init__(name, init_config, instances)

        self.region = self.instance.get('region')
        self.api_key = self.instance.get('api_key')
        self.api_secret = self.instance.get('api_secret')
        self.service_name = self.instance.get('service_name')
        self.period = self.instance.get('period', 'hour')

        self.validate_config()

        self.log.debug('Exoscale DBaaS monitoring starting for %s', self.service_name)

        self.tags = self.instance.get('tags', [])
        self.tags.append('region:{}'.format(self.region))
        self.tags.append('service_name:{}'.format(self.service_name))

    def validate_config(self):
        if not self.region:
            raise ConfigurationError('Configuration error, please specify region in conf.yaml.')

        if not self.api_key:
            raise ConfigurationError('Configuration error, please specify an api_key in conf.yaml.')

        if not self.api_secret:
            raise ConfigurationError('Configuration error, please specify an api_secret in conf.yaml')

        if not self.service_name:
            raise ConfigurationError('Configuration error, please specify the service_name in conf.yaml')

    def get_full_path(self, path):
        path1 = path.format(service_name=self.service_name)
        url = BASE_URL.format(region=self.region, path=path1)
        return url

    # Get stats from REST API as json
    def get_api_json(self, url):
        try:
            auth = ExoscaleV2Auth(self.api_key, self.api_secret)
            payload = json.dumps({'period': self.period}).encode()
            response = self.http.post(
                url,
                auth=auth,
                data=payload,
            )
        except Timeout as e:
            error_message = "Request timeout: {}, {}".format(url, e)
            self.log.warning(error_message)
            self.service_check(
                "can_connect",
                AgentCheck.CRITICAL,
                message=error_message,
                hostname=self.service_name,
                tags=self.tags,
            )
            raise

        except (HTTPError, InvalidURL, ConnectionError) as e:
            error_message = "Request failed: {}, {}".format(url, e)
            self.log.warning(error_message)
            self.service_check(
                "can_connect",
                AgentCheck.CRITICAL,
                message=error_message,
                hostname=self.service_name,
                tags=self.tags,
            )
            raise

        except json.JSONDecodeError as e:
            error_message = "JSON Parse failed: {}, {}".format(url, e)
            self.log.warning(error_message)
            self.service_check(
                "can_connect",
                AgentCheck.CRITICAL,
                message=error_message,
                hostname=self.service_name,
                tags=self.tags,
            )
            raise

        except ValueError as e:
            error_message = str(e)
            self.log.warning(error_message)
            self.service_check(
                "can_connect",
                AgentCheck.CRITICAL,
                message=error_message,
                hostname=self.service_name,
                tags=self.tags,
            )
            raise

        if response.status_code != 200:
            error_message = "Expected status code 200 for url {}, but got status code: {}.".format(
                url, response.status_code
            )
            response_json = response.json()
            if 'errors' in response_json:
                for error in response_json["errors"]:
                    if 'description' in error and 'message' in error:
                        error_message += " {} {}.".format(error['description'], error['message'])

            self.log.warning(error_message)
            self.service_check(
                "can_connect",
                AgentCheck.CRITICAL,
                message=error_message,
                hostname=self.service_name,
                tags=self.tags,
            )
            raise CheckException(error_message)
        else:
            self.service_check(
                "can_connect",
                AgentCheck.OK,
                hostname=self.service_name,
                tags=self.tags,
            )

        return response.json()

    def get_database_metrics(self):
        url = self.get_full_path(METRICS)
        response_json = self.get_api_json(url)
        return response_json

    def get_parsed_metrics_info(self):
        response_json = self.get_database_metrics()

        disk_used = -1
        disk_mark = self.UNKNOWN
        disk_used = -1
        load_average = -1
        mem_usage = -1
        diskio_writes = -1
        cpu_usage = -1
        diskio_read = -1
        net_send = -1
        net_receive = -1

        if 'metrics' in response_json and 'disk_usage' in response_json['metrics']:
            if (
                'data' in response_json['metrics']['disk_usage']
                and 'rows' in response_json['metrics']['disk_usage']['data']
            ):
                disk_used = response_json['metrics']['disk_usage']['data']['rows'][0][1]
                disk_mark = self.OK
            else:
                self.log.warning("Error when parsing JSON for disk usage")
        else:
            self.log.warning("Error while parsing JSON for metrics information")

        if disk_mark == self.OK:
            if disk_used >= CRITICAL_QUOTA:
                disk_mark = self.CRITICAL
            elif disk_used >= WARNING_QUOTA:
                disk_mark = self.WARNING

        if 'metrics' in response_json and 'load_average' in response_json['metrics']:
            if (
                'data' in response_json['metrics']['load_average']
                and 'rows' in response_json['metrics']['load_average']['data']
            ):
                load_average = response_json['metrics']['load_average']['data']['rows'][0][1]
            else:
                self.log.warning("Error when parsing JSON for load average")
        else:
            self.log.warning("Error while parsing JSON for metrics information")

        if 'metrics' in response_json and 'mem_usage' in response_json['metrics']:
            if (
                'data' in response_json['metrics']['mem_usage']
                and 'rows' in response_json['metrics']['mem_usage']['data']
            ):
                mem_usage = response_json['metrics']['mem_usage']['data']['rows'][0][1]
            else:
                self.log.warning("Error when parsing JSON for memory usage")
        else:
            self.log.warning("Error while parsing JSON for metrics information")

        if 'metrics' in response_json and 'diskio_writes' in response_json['metrics']:
            if (
                'data' in response_json['metrics']['diskio_writes']
                and 'rows' in response_json['metrics']['diskio_writes']['data']
            ):
                diskio_writes = response_json['metrics']['diskio_writes']['data']['rows'][0][1]
            else:
                self.log.warning("Error when parsing JSON for disk io writes")
        else:
            self.log.warning("Error while parsing JSON for metrics information")

        if 'metrics' in response_json and 'cpu_usage' in response_json['metrics']:
            if (
                'data' in response_json['metrics']['cpu_usage']
                and 'rows' in response_json['metrics']['cpu_usage']['data']
            ):
                cpu_usage = response_json['metrics']['cpu_usage']['data']['rows'][0][1]
            else:
                self.log.warning("Error when parsing JSON for cpu usage")
        else:
            self.log.warning("Error while parsing JSON for metrics information")

        if 'metrics' in response_json and 'diskio_read' in response_json['metrics']:
            if (
                'data' in response_json['metrics']['diskio_read']
                and 'rows' in response_json['metrics']['diskio_read']['data']
            ):
                diskio_read = response_json['metrics']['diskio_read']['data']['rows'][0][1]
            else:
                self.log.warning("Error when parsing JSON for disk io read")
        else:
            self.log.warning("Error while parsing JSON for metrics information")

        if 'metrics' in response_json and 'net_send' in response_json['metrics']:
            if (
                'data' in response_json['metrics']['net_send']
                and 'rows' in response_json['metrics']['net_send']['data']
            ):
                net_send = response_json['metrics']['net_send']['data']['rows'][0][1]
            else:
                self.log.warning("Error when parsing JSON for net send")
        else:
            self.log.warning("Error while parsing JSON for metrics information")

        if 'metrics' in response_json and 'net_receive' in response_json['metrics']:
            if (
                'data' in response_json['metrics']['net_receive']
                and 'rows' in response_json['metrics']['net_receive']['data']
            ):
                net_receive = response_json['metrics']['net_receive']['data']['rows'][0][1]
            else:
                self.log.warning("Error when parsing JSON for net receive")
        else:
            self.log.warning("Error while parsing JSON for metrics information")

        metrics_info = {
            'disk_mark': disk_mark,
            'disk_used': disk_used,
            'load_average': load_average,
            'mem_usage': mem_usage,
            'diskio_writes': diskio_writes,
            'cpu_usage': cpu_usage,
            'diskio_read': diskio_read,
            'net_send': net_send,
            'net_receive': net_receive,
        }
        return metrics_info

    def check(self, _):
        metrics_info = self.get_parsed_metrics_info()

        self.gauge("dbaas.disk.usedPercent", metrics_info['disk_used'], tags=self.tags, hostname=self.service_name)
        self.gauge("dbaas.load.average", metrics_info['load_average'], tags=self.tags, hostname=self.service_name)
        self.gauge("dbaas.memory.usedPercent", metrics_info['mem_usage'], tags=self.tags, hostname=self.service_name)
        self.gauge("dbaas.disk.writeIOsPS", metrics_info['diskio_writes'], tags=self.tags, hostname=self.service_name)
        self.gauge("dbaas.cpuutilization", metrics_info['cpu_usage'], tags=self.tags, hostname=self.service_name)
        self.gauge("dbaas.disk.readIOsPS", metrics_info['diskio_read'], tags=self.tags, hostname=self.service_name)
        self.gauge("dbaas.network.wrBytesPS", metrics_info['net_send'], tags=self.tags, hostname=self.service_name)
        self.gauge("dbaas.network.rdBytesPS", metrics_info['net_receive'], tags=self.tags, hostname=self.service_name)

        disk_msg = "Percentage disk used: {}%".format(metrics_info['disk_used'])
        self.service_check(
            'dbaas.disk_usage',
            metrics_info['disk_mark'],
            message=disk_msg if metrics_info['disk_mark'] != AgentCheck.OK else "",
            hostname=self.service_name,
            tags=self.tags,
        )
