
import pytest


@pytest.fixture(scope='session')
def dd_environment():
    yield


@pytest.fixture()
def instance_good():
    instance = {'region': 'ch-gva-2', 'api_key': 'aaa', 'api_secret': 'bbb', 'service_name': 'test-database-name'}
    return instance


@pytest.fixture()
def instance_empty():
    instance = {}
    return instance


@pytest.fixture()
def instance_region_none():
    instance = {'region': None, 'api_key': 'aaa', 'api_secret': 'bbb', 'service_name': 'test-database-name'}
    return instance


@pytest.fixture()
def instance_api_key_none():
    instance = {'region': 'ch-gva-2', 'api_key': None, 'api_secret': 'bbb', 'service_name': 'test-database-name'}
    return instance


@pytest.fixture()
def instance_api_secret_none():
    instance = {'region': 'ch-gva-2', 'api_key': 'aaa', 'api_secret': None, 'service_name': 'test-database-name'}
    return instance


@pytest.fixture()
def instance_service_name_none():
    instance = {'region': 'ch-gva-2', 'api_key': 'aaa', 'api_secret': 'bbb', 'service_name': None}
    return instance


@pytest.fixture()
def metrics_test_json():
    metrics_json = {
        "metrics": {
            "disk_usage": {
                "hints": {"title": "Disk space usage %"},
                "data": {
                    "rows": [
                        ["2023-02-09T05:14:00", 54.65627660475069],
                        ["2023-02-09T05:14:30", 54.65627660475069],
                        ["2023-02-09T05:15:00", 54.65627660475069],
                    ],
                    "cols": [
                        {"type": "date", "label": "time"},
                        {"type": "number", "label": "test-database-name-1 (master)"},
                    ],
                },
            },
            "load_average": {
                "hints": {"title": "Load average (5 min)"},
                "data": {
                    "rows": [
                        ["2023-02-09T05:14:00", 1.67],
                        ["2023-02-09T05:14:30", 1.72],
                        ["2023-02-09T05:15:00", 1.84],
                    ],
                    "cols": [
                        {"type": "date", "label": "time"},
                        {"type": "number", "label": "test-database-name-1 (master)"},
                    ],
                },
            },
            "mem_usage": {
                "hints": {"title": "Memory usage %"},
                "data": {
                    "rows": [
                        ["2023-02-09T05:14:00", 5.139664477029322],
                        ["2023-02-09T05:14:30", 5.311909761347601],
                        ["2023-02-09T05:15:00", 5.204357197596332],
                    ],
                    "cols": [
                        {"type": "date", "label": "time"},
                        {"type": "number", "label": "test-database-name-1 (master)"},
                    ],
                },
            },
            "diskio_writes": {
                "hints": {"title": "Disk iops (writes)"},
                "data": {
                    "rows": [
                        ["2023-02-09T05:14:00", 12.4],
                        ["2023-02-09T05:14:30", 8.666666666666666],
                        ["2023-02-09T05:15:00", 10.733333333333333],
                    ],
                    "cols": [
                        {"type": "date", "label": "time"},
                        {"type": "number", "label": "test-database-name-1 (master)"},
                    ],
                },
            },
            "cpu_usage": {
                "hints": {"title": "CPU usage %"},
                "data": {
                    "rows": [
                        ["2023-02-09T05:14:00", 43.627345896460405],
                        ["2023-02-09T05:14:30", 43.53623626208132],
                        ["2023-02-09T05:15:00", 45.443364527115236],
                    ],
                    "cols": [
                        {"type": "date", "label": "time"},
                        {"type": "number", "label": "test-database-name-1 (master)"},
                    ],
                },
            },
            "diskio_read": {
                "hints": {"title": "Disk iops (reads)"},
                "data": {
                    "rows": [
                        ["2023-02-09T05:14:00", 0],
                        ["2023-02-09T05:14:30", 0.03333333333333333],
                        ["2023-02-09T05:15:00", 0.8],
                    ],
                    "cols": [
                        {"type": "date", "label": "time"},
                        {"type": "number", "label": "test-database-name-1 (master)"},
                    ],
                },
            },
            "net_send": {
                "hints": {"title": "Network transmit (bytes/s)"},
                "data": {
                    "rows": [["2023-02-09T05:14:00", 135684.8], ["2023-02-09T05:14:30", 139807]],
                    "cols": [
                        {"type": "date", "label": "time"},
                        {"type": "number", "label": "test-database-name-1 (master)"},
                    ],
                },
            },
            "net_receive": {
                "hints": {"title": "Network receive (bytes/s)"},
                "data": {
                    "rows": [
                        ["2023-02-09T05:14:00", 76198.53333333334],
                        ["2023-02-09T05:14:30", 81039.33333333333],
                        ["2023-02-09T05:15:00", 84442.46666666666],
                    ],
                    "cols": [
                        {"type": "date", "label": "time"},
                        {"type": "number", "label": "test-database-name-1 (master)"},
                    ],
                },
            },
        }
    }
    return metrics_json


@pytest.fixture()
def disk_resp_warning():
    disk_resp_warning = {
        "metrics": {
            "disk_usage": {
                "hints": {"title": "Disk space usage %"},
                "data": {
                    "rows": [
                        ["2023-02-09T05:14:00", 80],
                    ],
                    "cols": [
                        {"type": "date", "label": "time"},
                        {"type": "number", "label": "test-database-name-1 (master)"},
                    ],
                },
            }
        }
    }
    return disk_resp_warning


@pytest.fixture()
def disk_resp_critical():
    disk_resp_critical = {
        "metrics": {
            "disk_usage": {
                "hints": {"title": "Disk space usage %"},
                "data": {
                    "rows": [
                        ["2023-02-09T05:14:00", 100],
                    ],
                    "cols": [
                        {"type": "date", "label": "time"},
                        {"type": "number", "label": "test-database-name-1 (master)"},
                    ],
                },
            }
        }
    }
    return disk_resp_critical
