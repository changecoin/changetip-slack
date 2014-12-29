# ChangeTip Slack bot

[ChangeTip](https://www.changetip.com) is a micropayment infrastructure for the web, enabling tips to be sent over social media. This code allows users to *tip* eachother with [slack](https://slack.com/), using the [slack api](https://api.slack.com/)

This repo is managed by the ChangeCoin (ChangeTip) team, but is open source for transparency and educational purposes. Pull requests welcomed!

## Tipping
Type `changetip:` at the beginning of a message, then mention a @username and an amount.

Examples:
`changetip: Give @victoria $5 for paying for my lunch`
`changetip: Give @jim a high five for the great work he just did`
`changetip: what is the answer to everything?`

## Slack setup
To enable tipping in slack for your team, a couple of minutes of setup is required.
1. Create a new outgoing webhook from:

https://yourdomain.slack.com/services/new/outgoing-webhook

(replace *yourdomain* with your slack domain)

2. Set the Channel to *Any*, the Trigger Word to `changetip,@changetip`, and the URL to `https://bots.changetip.com/slack/command-webhook'

![Slack Setup 1](https://cdn.changetip.com/img/screenshots/slack_setup_1.png?1 "Slack Setup 1")

3. The descriptive lable, name, and icon are up to you. If you'd like, you can use this one https://cdn.changetip.com/img/logos/changetip_round_icon.png. Note: it looks like there is a bug with slack where if you try to upload the icon while creating the webhook, you lose your data. Recommend you add the Icon after you save the webhook.

![Slack Setup 2](https://cdn.changetip.com/img/screenshots/slack_setup_2.png?1 "Slack Setup 2")

To get set up, just say hi to the slack tip bot. 


#### Installation (to run your own instance)
Using a python [virtualenv](http://docs.python-guide.org/en/latest/dev/virtualenvs/) is recommended.

This is a django app. It pulls in the [changetip python library](https://pypi.python.org/pypi/changetip). To install the dependencies:

```
$ pip install -r requirements.txt
```

#### Running
```
CHANGETIP_API_KEY=xxxx uwsgi --init uswgi.ini
```

To get an API key, contact support@changetip.com

#### Contributing

We love pull requests!

### License
BSD
