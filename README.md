# gitlabenv2csv

![Docker Pulls](https://img.shields.io/docker/pulls/zales/gitlabenv2csv?style=flat-square) ![Docker Cloud Build Status](https://img.shields.io/docker/cloud/build/zales/gitlabenv2csv?style=flat-square) ![Docker Cloud Automated build](https://img.shields.io/docker/cloud/automated/zales/gitlabenv2csv?style=flat-square) ![Docker Image Size (latest by date)](https://img.shields.io/docker/image-size/zales/gitlabenv2csv?style=flat-square) ![GitHub](https://img.shields.io/github/license/zales/gitlabenv2csv?style=flat-square)

## About

gitlabenv2csv allows you to download GitLab ENV variables to a csv file. Manually edit and upload back to the project / group.

## Install

### pip

Install dependecies:

```bash
pip3 install gitlabenv2csv
```
And execute script:

```bash
gitlabenv2csv.py -d -i <project/gitlab id> -g -c config.ini
```

### Docker

Or you can use prebuild docker container and execute script like this:

```bash
docker run -v ${PWD}/backups:/app/backups -v ${PWD}:/app/file -it zales/gitlabenv2csv:latest -l https://gitlab.example.com -t <api_token> -i <project/gitlab id> -p -u -f /app/file/gitlab_env.csv
```

## Usage

```
./gitlabenv2csv.py -h
usage: gitlabenv2csv.py [-h] [-c MY_CONFIG] -l GITLAB_URL -t GITLAB_TOKEN (-g | -p) -i ELEMENT_ID [-f FILE_PATH] (-d | -u)

Args that start with '--' (eg. -l) can also be set in a config file (config.ini or specified via -c). Config file syntax allows: key=value, flag=true, stuff=[a,b,c] (for details, see syntax at
https://goo.gl/R74nmi). If an arg is specified in more than one place, then commandline values override config file values which override defaults.

optional arguments:
  -h, --help            show this help message and exit
  -c MY_CONFIG, --my-config MY_CONFIG
                        config file path
  -l GITLAB_URL, --gitlab_url GITLAB_URL
                        Gitlab url
  -t GITLAB_TOKEN, --gitlab_token GITLAB_TOKEN
                        Gitlab token
  -g, --group           Edit group ENV
  -p, --project         Edit project ENV
  -i ELEMENT_ID, --element_id ELEMENT_ID
                        Gitab project/group id
  -f FILE_PATH, --file_path FILE_PATH
  -d, --download        Download gitlab ENV to csv
  -u, --upload          Upload csv to gitlab ENV
```

### Example

```bash
gitlabenv2csv.py -d -i 243 -g -c config.ini
```

---

<a href="https://www.buymeacoffee.com/zales" target="_blank"><img src="https://www.buymeacoffee.com/assets/img/custom_images/yellow_img.png" alt="Buy Me A Coffee"></a>
