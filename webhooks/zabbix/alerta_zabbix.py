#coding: utf-8

import json
import time
import datetime
import traceback
from alerta.models.alert import Alert
from alerta.webhooks import WebhookBase


class ZabbixWebhook(WebhookBase):

    def incoming(self, query_string, payload):

        try:
            # Default parameters
            print(payload)
            severity = payload.get("priority", "P0")
            status = payload.get("status", "unknown")
            group = 'Zabbix'
            resource = payload.get("host", "")
            service = ['Zabbix']
            text = payload.get("trigger")
            origin = 'Zabbix'
            event = payload.get("host","zabbix not event")
            value = payload.get("value", 0)

            environment = ""
            attributes = ""

            res = resource.split("-")

            if len(res)> 1:
                region = res[1]
                if res[0] == 'p' or res[0] == 's':
                    environment = "prod"
                else:
                    environment = "test"

                attributes = {"region": region}
            else:
                region = "shbs"
                environment = "test"
                attributes = {"region": region}

            if severity == "Disaster":
                alert_level = "P0"
            elif severity == "High":
                alert_level = "P1"
            elif severity == "Average":
                alert_level = "P2"
            elif severity == "Warning":
                alert_level = "P3"
            elif severity == "Information":
                alert_level = "P4"
            elif severity == "Not classified":
                alert_level = "P5"
            else:
                alert_level = "P0"

            if status == 'OK':
                severity = 'ok'

            return Alert(
                resource=resource,
                event=event,
                environment=environment,
                severity=alert_level,
                service=service,
                group=group,
                value=value,
                text=text,
                attributes=attributes,
                origin=origin,
                raw_data=json.dumps(payload, indent=4)
            )
        except:
            traceback.print_exc()
