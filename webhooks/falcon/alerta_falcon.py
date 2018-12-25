
from alerta.models.alert import Alert
from alerta.webhooks import WebhookBase
import json
import time
import datetime


class FalconWebhook(WebhookBase):

    def incoming(self, query_string, payload):

        # Default parameters
        environment = query_string.get('environment', 'prod')
        region = query_string.get('region', 'bjaws')
        severity = query_string["priority"]
        status = query_string["status"]
        group = 'Falcon'
        tags = query_string["tags"].split(',')
        resource = query_string["endpoint"]
        event = query_string["metric"]
        service = ['Falcon']
        text = 'nothing'
        attributes = {"region": region}
        origin = 'Falcon'
        create_time = self.formatTime(query_string["time"])

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
            value=query_string["left_value"],
            text=text,
            tags=tags,
            attributes=attributes,
            origin=origin,
            raw_data=json.dumps(query_string, indent=4)
        )

    @classmethod
    def formatTime(cls, s):
        return int(time.mktime(datetime.datetime.strptime(s, "%Y-%m-%d %H:%M:%S").timetuple()))
