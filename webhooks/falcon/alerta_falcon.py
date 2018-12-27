
import json
import time
import datetime
import traceback
from alerta.models.alert import Alert
from alerta.webhooks import WebhookBase


class FalconWebhook(WebhookBase):

    def incoming(self, query_string, payload):

        try:
            # Default parameters
            environment = payload.get('environment', 'prod')
            region = payload.get('region', 'bjaws')
            severity = payload.get("priority", "P0")
            status = payload.get("status", "unknown")
            group = 'Falcon'
            tags = payload.get("tags", "").split(',')
            resource = payload.get("endpoint", "")
            event = payload.get("metric")
            service = ['Falcon']
            text = payload.get("text")
            attributes = {"region": region}
            origin = 'Falcon'
            # create_time = payload.get("time")

            if status == 'OK':
                severity = 'ok'

            return Alert(
                resource=resource,
                event=event,
                environment=environment,
                severity=severity,
                service=service,
                # create_time=create_time,
                group=group,
                value=payload.get("left_value", 0),
                text=text,
                tags=tags,
                attributes=attributes,
                origin=origin,
                raw_data=json.dumps(payload, indent=4)
            )
        except:
            traceback.print_exc()
