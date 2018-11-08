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
export FLASK_APP=company.py
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

## Todo
