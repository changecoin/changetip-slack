# ChangeTip Slack bot

[ChangeTip](https://www.changetip.com) is a micropayment infrastructure for the web, enabling tips to be sent over social media. This code allows users to *tip* eachother with [slack](https://slack.com/), using the [slack api](https://api.slack.com/)

This repo is managed by the ChangeCoin (ChangeTip) team, but is open source for transparency and educational purposes. Pull requests welcomed!

## Tipping


## Usage


#### Installation
Using a python [virtualenv](http://docs.python-guide.org/en/latest/dev/virtualenvs/) is recommended.

This is a django app. It pulls in the [changetip python library](https://pypi.python.org/pypi/changetip). To install the dependencies:

```
$ pip install -r requirements.txt
```

#### Running
```
uwsgi --init uswgi.ini
```

#### Running
