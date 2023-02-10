import pytest
from mock import MagicMock

from datadog_checks.base import ConfigurationError
from datadog_checks.dev.utils import get_metadata_metrics
from datadog_checks.exoscale import ExoscaleCheck


@pytest.mark.unit
def test_empty_instance(aggregator, instance_empty):
    with pytest.raises(ConfigurationError):
        ExoscaleCheck('exocale', {}, [instance_empty])


@pytest.mark.unit
def test_region_none(aggregator, instance_region_none):
    with pytest.raises(ConfigurationError):
        ExoscaleCheck('exocale', {}, [instance_region_none])


@pytest.mark.unit
def test_api_key_none(aggregator, instance_api_key_none):
    with pytest.raises(ConfigurationError):
        ExoscaleCheck('exocale', {}, [instance_api_key_none])


@pytest.mark.unit
def test_api_secret_none(aggregator, instance_api_secret_none):
    with pytest.raises(ConfigurationError):
        ExoscaleCheck('exocale', {}, [instance_api_secret_none])


@pytest.mark.unit
def test_service_name_none(aggregator, instance_service_name_none):
    with pytest.raises(ConfigurationError):
        ExoscaleCheck('exocale', {}, [instance_service_name_none])


def test_check(aggregator, instance_good, metrics_test_json):
    check = ExoscaleCheck('exoscale', {}, [instance_good])
    check.get_database_metrics = MagicMock(return_value=metrics_test_json)
    check.check(None)

    aggregator.assert_service_check('exoscale.dbaas.disk_usage', ExoscaleCheck.OK)
    aggregator.assert_metric("exoscale.dbaas.disk.usedPercent", 54.65627660475069, count=1)
    aggregator.assert_metric("exoscale.dbaas.load.average", 1.67, count=1)
    aggregator.assert_metric("exoscale.dbaas.memory.usedPercent", 5.139664477029322, count=1)
    aggregator.assert_metric("exoscale.dbaas.disk.writeIOsPS", 12.4, count=1)
    aggregator.assert_metric("exoscale.dbaas.cpuutilization", 43.627345896460405, count=1)
    aggregator.assert_metric("exoscale.dbaas.disk.readIOsPS", 0, count=1)
    aggregator.assert_metric("exoscale.dbaas.network.wrBytesPS", 135684.8, count=1)
    aggregator.assert_metric("exoscale.dbaas.network.rdBytesPS", 76198.53333333334, count=1)

    aggregator.assert_all_metrics_covered()
    aggregator.assert_metrics_using_metadata(get_metadata_metrics())


def test_check_bad_usage(aggregator, instance_good, disk_resp_warning, disk_resp_critical):
    check = ExoscaleCheck("exoscale", {}, [instance_good])

    # Check for usage warning
    check.get_database_metrics = MagicMock(return_value=disk_resp_warning)
    check.check(None)

    aggregator.assert_service_check("exoscale.dbaas.disk_usage", ExoscaleCheck.WARNING)
    aggregator.assert_metric("exoscale.dbaas.disk.usedPercent", 80.0, count=1)

    # Check for usage critical
    check.get_database_metrics = MagicMock(return_value=disk_resp_critical)
    check.check(None)

    aggregator.assert_service_check("exoscale.dbaas.disk_usage", ExoscaleCheck.CRITICAL)
    aggregator.assert_metric("exoscale.dbaas.disk.usedPercent", 100.0, count=1)
