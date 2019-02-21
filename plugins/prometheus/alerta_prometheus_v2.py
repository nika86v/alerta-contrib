import datetime
import logging
import os
import requests
import json

try:
    from alerta.plugins import app  # alerta >= 5.0
except ImportError:
    from alerta.app import app  # alerta < 5.0
from alerta.plugins import PluginBase

LOG = logging.getLogger('alerta.plugins.prometheus')

DEFAULT_ALERTMANAGER_API_URL = 'http://localhost:9093'



ALERTMANAGER_API_URL = os.environ.get('ALERTMANAGER_API_URL') or app.config.get('ALERTMANAGER_API_URL', None)
ALERTMANAGER_USERNAME = os.environ.get('ALERTMANAGER_USERNAME') or app.config.get('ALERTMANAGER_USERNAME', None)
ALERTMANAGER_PASSWORD = os.environ.get('ALERTMANAGER_PASSWORD') or app.config.get('ALERTMANAGER_PASSWORD', None)
ALERTMANAGER_SILENCE_DAYS = os.environ.get('ALERTMANAGER_SILENCE_DAYS') or app.config.get('ALERTMANAGER_SILENCE_DAYS', 1)


class AlertmanagerSilence(PluginBase):

    def __init__(self, name=None):

        self.auth = (ALERTMANAGER_USERNAME, ALERTMANAGER_PASSWORD) if ALERTMANAGER_USERNAME else None

        super(AlertmanagerSilence, self).__init__(name)

    def pre_receive(self, alert):
        return alert

    def post_receive(self, alert):
        return

    def status_change(self, alert, status, text):

        if alert.event_type != 'prometheusAlert':
            return

        try:
            silence_days = int(ALERTMANAGER_SILENCE_DAYS)
        except Exception as e:
            LOG.error("Alertmanager: Could not parse 'ALERTMANAGER_SILENCE_DAYS': %s", e)
            raise RuntimeError("Could not parse 'ALERTMANAGER_SILENCE_DAYS': %s" % e)

        if alert.status == status:
            return

        if status == 'ack':
            if alert.service == "Falcon":
                return
                
            res_dict = {}

            for i in alert.tags:
                t = i.split("=")
                res_dict[t[0]] = t[1]

            if alert.environment == "test" and res_dict.get("region","") == 'bjaws':
                NIO_DEFAULT_ALERTMANAGER_API_URL = "alertA"
            elif alert.environment == "prod" and res_dict.get("region","") == 'bjaws':
                NIO_DEFAULT_ALERTMANAGER_API_URL = "alertB"
            elif alert.environment == "test" and res_dict.get("region","") == 'shbs':
                NIO_DEFAULT_ALERTMANAGER_API_URL = "alertC"
            elif alert.environment == "prod" and res_dict.get("region","") == 'shtc':
                NIO_DEFAULT_ALERTMANAGER_API_URL = "alertD"
            else:
                NIO_DEFAULT_ALERTMANAGER_API_URL = ""

            LOG.debug('Alertmanager: Add silence for alertname=%s instance=%s', alert.event, alert.resource)
            data = {
                "matchers": [
                    {
                      "name": "alertname",
                      "value": alert.event
                    },
                    {
                      "name": "instance",
                      "value": alert.resource
                    }
                ],
                "startsAt": datetime.datetime.utcnow().replace(microsecond=0).isoformat() + ".000Z",
                "endsAt": (datetime.datetime.utcnow() + datetime.timedelta(days=silence_days))
                              .replace(microsecond=0).isoformat() + ".000Z",
                "createdBy": "alerta",
                "comment": text if text != '' else "silenced by alerta"
            }


            #base_url = ALERTMANAGER_API_URL or alert.attributes.get('externalUrl', DEFAULT_ALERTMANAGER_API_URL)
            if NIO_DEFAULT_ALERTMANAGER_API_URL:
                url = NIO_DEFAULT_ALERTMANAGER_API_URL + '/api/v1/silences'
            else:
                return "Not match Alertmanager url"

            LOG.debug('Alertmanager: URL=%s', url)
            LOG.debug('Alertmanager: data=%s', data)

            try:
                r = requests.post(url, json=data, auth=self.auth, timeout=2)
            except Exception as e:
                raise RuntimeError("Alertmanager: ERROR - %s" % e)
            LOG.debug('Alertmanager: %s - %s', r.status_code, r.text)

            # example r={"status":"success","data":{"silenceId":8}}
            try:
                silenceId = r.json()['data']['silenceId']
                alert.attributes['silenceId'] = silenceId
                text = text + ' (silenced in Alertmanager)'
            except Exception as e:
                raise RuntimeError("Alertmanager: ERROR - %s" % e)
            LOG.debug('Alertmanager: Added silenceId %s to attributes', silenceId)

        elif status == 'open':
            LOG.debug('Alertmanager: Remove silence for alertname=%s instance=%s', alert.event, alert.resource)

            silenceId = alert.attributes.get('silenceId', None)
            if silenceId:
                #base_url = ALERTMANAGER_API_URL or alert.attributes.get('externalUrl', DEFAULT_ALERTMANAGER_API_URL)
                res_dict = {}

                for i in alert.tags:
                    t = i.split("=")
                    res_dict[t[0]] = t[1]

                
                if alert.environment == "test" and res_dict.get("region","") == 'bjaws':
                    NIO_DEFAULT_ALERTMANAGER_API_URL = "alertA"
                elif alert.environment == "prod" and res_dict.get("region","") == 'bjaws':
                    NIO_DEFAULT_ALERTMANAGER_API_URL = "alertB"
                elif alert.environment == "test" and res_dict.get("region","") == 'shbs':
                    NIO_DEFAULT_ALERTMANAGER_API_URL = "alertC"
                elif alert.environment == "prod" and res_dict.get("region","") == 'shtc':
                    NIO_DEFAULT_ALERTMANAGER_API_URL = "alertD"
                else:
                    NIO_DEFAULT_ALERTMANAGER_API_URL = ""

                if NIO_DEFAULT_ALERTMANAGER_API_URL:
                    url = NIO_DEFAULT_ALERTMANAGER_API_URL + '/api/v1/silence/%s' % silenceId
                else:
                    return "Not match Alertmanager url"

                try:
                    r = requests.delete(url, auth=self.auth, timeout=2)
                except Exception as e:
                    raise RuntimeError("Alertmanager: ERROR - %s" % e)
                LOG.debug('Alertmanager: %s - %s', r.status_code, r.text)

                try:
                    alert.attributes['silenceId'] = None
                except Exception as e:
                    raise RuntimeError("Alertmanager: ERROR - %s" % e)
                LOG.debug('Alertmanager: Removed silenceId %s from attributes', silenceId)

        return alert, status, text
