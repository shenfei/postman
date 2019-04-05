# Postman: *A newsletter deliver tool*

This small tool helps you to send newsletter through [mailgun's API](https://www.mailgun.com/).

The main benefits of using a python script is the ability to create some automatic workflows.

## Usage

#### 0. Install dependencies

- python >= 3.6
    - requests
    - PyYAML
- pandoc (only if you want to write newsletter in markdown format)
- R (only if you want to write newsletter in RMarkdown format)
    - rmarkdown

#### 1. Set up config

Copy `config_template.yml` to `config.yml` (or whatever name you like), and modify it with your own configuration,
like api key, address, and subject line (optional).
Though only mailgun's API were tested, you can hack it to adapt other mail services.

#### 2. Draft a newsletter

Use your favorite editor/client to draft a newsletter, and convert it to a support file format.
Currently, `postman` supports *html*, *markdown (.md)*, and *RMarkdown (.Rmd)* files.

#### 3. Send with a commond

For example,

```shell
python3 post_letter.py \
    -i INPUT_FILE_PATH \
    -c config.yml \
    -s "An interesting letter"
```
