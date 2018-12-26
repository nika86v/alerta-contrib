
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
            severity = payload["priority"]
            status = payload["status"]
            group = 'Falcon'
            tags = payload["tags"].split(',')
            resource = payload["endpoint"]
            event = payload["metric"]
            service = ['Falcon']
            text = payload["text"]
            attributes = {"region": region}
            origin = 'Falcon'
            create_time = self.formatTime(payload["time"])

            if status == 'OK':
                severity = 'ok'

            return Alert(
                resource=resource,
                event=event,
                environment=environment,
                severity=severity,
                service=service,
                create_time=create_time,
                group=group,
                value=payload["left_value"],
                text=text,
                tags=tags,
                attributes=attributes,
                origin=origin,
                raw_data=json.dumps(payload, indent=4)
            )
        except:
            traceback.print_exc()

    @classmethod
    def formatTime(cls, s):
        return int(time.mktime(datetime.datetime.strptime(s, "%Y-%m-%d %H:%M:%S").timetuple()))
