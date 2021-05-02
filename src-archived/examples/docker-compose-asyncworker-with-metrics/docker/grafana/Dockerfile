FROM grafana/grafana

# More on: https://grafana.com/docs/grafana/latest/administration/provisioning/
COPY ./provisioning/dashboards /etc/grafana/provisioning/dashboards
COPY ./provisioning/datasources /etc/grafana/provisioning/datasources

COPY ./dashboards /var/lib/grafana/dashboards
