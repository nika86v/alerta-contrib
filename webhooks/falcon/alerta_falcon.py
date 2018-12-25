
from alerta.models.alert import Alert
from alerta.webhooks import WebhookBase
import json

class FalconWebhook(WebhookBase):

    def incoming(self, query_string, payload):

        # Default parameters
        environment = 'Production'
        severity = query_string["priority"]
        status = query_string["status"]
        group = 'Falcon'
        resource = query_string["endpoint"]
        event = query_string["metric"]
        service = 'Falcon'
        text = 'nothing'
        tags = query_string["endpoint"].split(',')
        attributes = {}
        origin = ''

        if status == 'OK':
            severity = 'ok'

        return Alert(
            resource=resource,
            event=event,
            environment=environment,
            severity=severity,
            service=service,
            group=group,
            value=query_string["left_value"],
            text=text,
            tags=tags,
            attributes=attributes,
            origin=origin,
            raw_data=json.dumps(query_string, indent=4)
        )
