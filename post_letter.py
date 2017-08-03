import argparse
from subprocess import getoutput
from yaml import load as yaml_load
try:
    from yaml import CLoader as Loader
except ImportError:
    from yaml import Loader
import requests


def send_email(inpath, subject, config):
    mail_text = getoutput('pandoc %s -f markdown -t html' % inpath)
    api_url = config['mailgun'].get('api_url')
    api_key = config['mailgun'].get('api_key')
    res = requests.post(api_url, auth=('api', api_key), data={
        'from': config['from_addr'],
        'to': config['to_addr'],
        'subject': subject,
        'html': mail_text
    })
    print(res.status_code)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--input', '-i', required=True)
    parser.add_argument('--config', '-c', required=True)
    parser.add_argument('--subject', '-s')
    parser.add_argument('--serial', '-n', type=int)
    args = parser.parse_args()

    with open(args.config) as conf:
        config = yaml_load(conf, Loader=Loader)

    if args.subject is None:
        if args.serial is None:
            raise ValueError('Please input newsletter subject or serial number')
        subject = 'Selfhack Newsletter #%d' % args.serial
    else:
        subject = args.subject

    send_email(args.input, subject, config)
