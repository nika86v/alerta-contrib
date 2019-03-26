from setuptools import setup, find_packages

version = '1.0.2'

setup(
    name="alerta-zabbix",
    version=version,
    description='Alerta Webhook for Zabbix',
    url='https://github.com/cxjchocolate/alerta-contrib',
    license='MIT',
    author='Zhigang.hong',
    author_email='zhigang.hong@nio.com',
    packages=find_packages(),
    py_modules=['alerta_zabbix'],
    install_requires=[],
    include_package_data=True,
    zip_safe=True,
    entry_points={
        'alerta.webhooks': [
            'zabbix = alerta_zabbix:ZabbixWebhook'
        ]
    }
)
