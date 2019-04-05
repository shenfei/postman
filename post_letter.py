import argparse
from subprocess import getoutput, run
from pathlib import Path

from yaml import safe_load as load_yaml
import requests


def render_mail(inpath: str):
    '''Generate a html body from `inpath` file

    Input file type can be html, markdown (.md), or RMarkdown (.Rmd)
    '''
    inpath = Path(inpath)

    if inpath.suffix == '.html':
        with open(inpath) as fin:
            mail = fin.read()

    elif inpath.suffix == '.Rmd':
        cmd = f"R -e \"rmarkdown::render('{inpath}', 'blogdown::html_page', output_dir = '.')\""
        run(cmd, shell=True)
        out_file = Path(f'{inpath.stem}.html')
        with open(out_file) as fin:
            mail = fin.read()
        out_file.unlink()

    elif inpath.suffix == '.md':
        mail = getoutput(f'pandoc {inpath} -f markdown -t html')

    return mail


def send_email(inpath: str, subject: str, config: dict):
    mail_text = render_mail(inpath)
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

    config = load_yaml(open(args.config))

    if args.subject is None:
        if args.serial is None:
            raise ValueError('Please input newsletter subject or serial number')
        subject = config.get('subject', '#{}').format(args.serial)
    else:
        subject = args.subject

    send_email(args.input, subject, config)
