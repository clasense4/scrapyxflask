# Scrapy x Flask

## Introduction

Example projects that involving scraping and displaying a rest endpoint


## Requirements

- Python 3.6
- Python pip
- Python Virtualenv
- PostgreSQL 10
- Ubuntu 18.04
- [Linux Server](https://www.digitalocean.com/?refcode=6b1c3b315e1e)

## Installation

```
# Package
echo "deb http://apt.postgresql.org/pub/repos/apt/ bionic-pgdg main" > /etc/apt/sources.list.d/pgdg.list
wget --quiet -O - https://www.postgresql.org/media/keys/ACCC4CF8.asc | sudo apt-key add -
apt update
apt install postgresql-10 python3-pip -y
pip3 install virtualenv

# Setup postgresql
sudo -u postgres psql postgres
\password postgres
# Enter your strong password
\q

sudo service postgresql restart
psql -U postgres -h 127.0.0.1
CREATE DATABASE scrapy_x_flask;
\q

# Python
cd /home/
git clone https://github.com/clasense4/scrapyxflask.git
cd /home/scrapyxflask
virtualenv -p `which python3` env
source env/bin/activate
pip3 install -r requirements.txt

# Crawl
cd /home/scrapyxflask/scrapy_vietnammarkets
scrapy crawl vietnammarkets

# Import crawled result
cd /home/scrapyxflask/webserver
vim orator.yml
# Change your postgresql password
orator migrate --force
python importer.py

# Start flask app
cd /home/scrapyxflask/webserver
export FLASK_APP=main.py
flask run -h 0.0.0.0

# Get your public ip
ifconfig | grep inet | awk '{print $2}' | head -n 1
```

## Test

```
source env/bin/activate && cd webserver && sh test.sh

.....
Name      Stmts   Miss  Cover
-----------------------------
main.py      33      1    97%
----------------------------------------------------------------------
Ran 5 tests in 0.185s

OK
```

## FAQ

### 1. Which database engine you choose and why?

> I choose postgresql. Postgresql has rich feature, especially the powerfull json column.
> I can use that to store json and doing good query, in SQL language.
> Also postgre has extenstion that is really powerful, such as timescaledb, pipelinedb, postgis, citus, etc.
> Not only that, postgresql has good search support, that is trigram index. Unfortunately I'm not using that in this projects.

### 2. Which web framework you choose and why?

> Flask. It is easy and simple, but yes need to create our own skeleton app.
> I think to use great python 3 async supported framework, but I'm not really familiar with that. For example : Sanic, aiohttp, etc.

### 3. Briefly describe the architecture of your application?

> I use scrapy to crawl the content, and it has good support, for example, item pipeline.
> With single crawl, I can create multiple outputs. I have been using scrapy since 2010, and it is proven.
> I use orator orm, it is similar with laravel's eloquent
> I use nosetest with code coverage too.

