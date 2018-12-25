Open-Falcon Webhook
================

Receive [Open-Falcon](https://www.open-falcon.org) ban notifications via webhook callbacks.

Installation
------------

Clone the GitHub repo and run:

```plain
python setup.py install
```

Or, to install remotely from GitHub run:

```plain
pip install git+https://github.com/cxjchocolate/alerta-contrib.git#subdirectory=webhooks/falcon
```

**Note:** If Alerta is installed in a python virtual environment then plugins
need to be installed into the same environment for Alerta to dynamically
discover them.

Configuration
-------------

### Alerta

The custom webhook will be auto-detected and added to the list of available API endpoints.

### Open-Falcon

See [Open-Falcon](../../integrations/falcon/README.md)

Example Request
--------------

```plain
curl -sSL -X POST -H 'Content-Type: application/json' -d \
  '
    {
      "hostname": "foo",
      "severity": "critical",
      "attributes": {
        "bannedIp": "1.2.3.4"
      },
      "environment": "Development",
      "resource": "SSHD",
      "event": "The IP 1.2.3.4 has just been banned by Fail2Ban after 6 attempts!",
      "message": "test"
    }
  ' \
  'http://localhost:8080/api/webhooks/fail2ban?api-key=<API_KEY>'
```

License
-------
