from setuptools import setup, find_packages

version = '1.0.0'

setup(
    name="alerta-falcon",
    version=version,
    description='Alerta Webhook for Open-Falcon',
    url='https://github.com/cxjchocolate/alerta-contrib',
    license='MIT',
    author='Kevin Cai',
    author_email='kevin.cai@nio.com',
    packages=find_packages(),
    py_modules=['alerta_falcon'],
    install_requires=[],
    include_package_data=True,
    zip_safe=True,
    entry_points={
        'alerta.webhooks': [
            'falcon = alerta_falcon:FalconWebhook'
        ]
    }
)
