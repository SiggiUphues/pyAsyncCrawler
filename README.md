# pyCrawler
A simple Python3.7 page crawler to extract mail addresses.

Written as pythonic solution using the asyncio and
<a href="https://github.com/psf/requests-html">requests-html</a> framework

To write this program many ideas of <a href="https://github.com/gandie/pyCrawler">pyCrawler</a>
were used.

# Installation
This python package can be installed (optionally, but strongly recommended into a <a href="http://docs.python-guide.org/en/latest/dev/virtualenvs/#lower-level-virtualenv">virtualenv</a>)
after requirements have been installed.

Installation in a virtualenv:
1. Create a virtual enviroment and activate it.
```bash
virtualenv -p python3.7 venv37
source venv37/bin/activate
```
2. Install all requirements and run setup.py
```bash
pip install -r requirements.txt
python setup.py install
```

# Usage
There are two executables.
1. slow_crawler:
This crawler does the work without any workers and is very slow
```
usage: slow_crawler [-h] [-d DEPTH] [-l {Info,Warn,Debug}] url

positional arguments:
  url                   This is the url to start crawling from

optional arguments:
  -h, --help            show this help message and exit
  -d DEPTH, --depth DEPTH
                        How many generation of links to follow. Default 10
  -l {Info,Warn,Debug}, --loglevel {Info,Warn,Debug}
                        Changes verbosity of the log messages (Default: Info)

```
2. asyncio_crawler:
This crawler uses the asycio and <a href="https://github.com/psf/requests-html">requests-html</a>
framework to improve the runtime of the crawler.
```
usage: asyncio_crawler [-h] [-d DEPTH] [-n NUMWORKERS] [-l {Info,Warn,Debug}]
                       url

positional arguments:
  url                   This is the url to start crawling from

optional arguments:
  -h, --help            show this help message and exit
  -d DEPTH, --depth DEPTH
                        How many generation of links to follow. Default 10
  -n NUMWORKERS, --numworkers NUMWORKERS
                        Number of crawlers spawned. If not pass it will
                        default to the number of processors on the machine,
                        multiplied by 5
  -l {Info,Warn,Debug}, --loglevel {Info,Warn,Debug}
                        Changes verbosity of the log messages (Default: Info)


```
