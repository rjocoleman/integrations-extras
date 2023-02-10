FROM datadog/agent:7

ENV DD_EXO_VERSION 0.0.1

COPY dist/datadog_exoscale-${DD_EXO_VERSION}-py3-none-any.whl /tmp/datadog_exoscale-${DD_EXO_VERSION}-py3-none-any.whl

RUN agent integration install -w -r /tmp/datadog_exoscale-${DD_EXO_VERSION}-py3-none-any.whl \
  && /opt/datadog-agent/embedded/bin/pip3 install requests-exoscale-auth \
  && rm /tmp/datadog_exoscale-${DD_EXO_VERSION}-py3-none-any.whl
