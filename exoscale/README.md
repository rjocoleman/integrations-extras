# Agent Check: Exoscale

## Overview

This check monitors [Exoscale][1] DBaaS metrics through Datadog Agent.

## Setup

### Installation

To install the Exoscale check on your host:

1. Install the [developer toolkit]
   (https://docs.datadoghq.com/developers/integrations/new_check_howto/#developer-toolkit)
   on any machine.

2. Run `ddev release build exoscale` to build the package.

3. [Download the Datadog Agent][2].

4. Upload the build artifact to any host with an Agent and
   run `datadog-agent integration install -w
path/to/exoscale/dist/<ARTIFACT_NAME>.whl`.

You may also need to install dependencies since those aren't packaged into the wheel

`sudo -u dd-agent -H /opt/datadog-agent/embedded/bin/pip3 install requests-exoscale-auth`

### Configuration

1. <List of steps to setup this Integration>

### Validation

<Steps to validate integration is functioning as expected>

## Data Collected

### Metrics

See [metadata.csv][8] for a list of metrics provided by this check.

### Service Checks

See [service_checks.json][9] for a list of service checks provided by this integration.

### Events

The Exoscale integration does not include any events.

## Troubleshooting

Need help? Contact [Datadog support][3].

[1]: https://exoscale.com
[2]: https://app.datadoghq.com/account/settings#agent
[3]: https://docs.datadoghq.com/agent/kubernetes/integrations/
[4]: https://github.com/DataDog/integrations-extras/blob/master/exoscale/datadog_checks/exoscale/data/conf.yaml.example
[5]: https://docs.datadoghq.com/agent/guide/agent-commands/#start-stop-and-restart-the-agent
[6]: https://docs.datadoghq.com/agent/guide/agent-commands/#agent-status-and-information
[7]: https://github.com/DataDog/integrations-extras/blob/master/exoscale/metadata.csv
[8]: https://github.com/DataDog/integrations-extras/blob/master/exoscale/assets/service_checks.json
[9]: https://docs.datadoghq.com/help/
