# ChangeTip Slack Bot

[ChangeTip](https://www.changetip.com) is a micropayment infrastructure for the web, enabling tips to be sent over social media. This code allows users to *tip* eachother with [slack](https://slack.com/), using the [slack api](https://api.slack.com/)

![Slack Tipping](https://cdn.changetip.com/img/screenshots/slack_tip.png "Slack tipping")


This repo is managed by the ChangeCoin (ChangeTip) team, but is open source for transparency and educational purposes. Pull requests welcomed!

## Tipping
Type `changetip:` at the *beginning* of a message, then mention a @username and an amount.

Examples:

```
changetip: Give @victoria $5 for paying for my lunch
```

```
changetip: Give @jim a high five for the great work he just did
```
In addition to tips, you can also have some fun. Try asking anything.

```
changetip: what is the answer to everything?
```

```
changetip: are you happy?
```

Before using ChangeTip, **you will need to send a message to it so it knows who you are**. It's as simple as saying Hi.


```
changetip: hi!
```

ChangeTip will respond with instructions on how to hook up your ChangeTip account to slack.

Note: It only works in channels, not private chats, this is because slack doesn't send data for private chats via the webhook.

## Slack setup

<a href="https://slack.com/oauth/authorize?scope=incoming-webhook,commands&client_id=2661501386.15060437890"><img alt="Add to Slack" height="40" width="139" src="https://platform.slack-edge.com/img/add_to_slack.png" srcset="https://platform.slack-edge.com/img/add_to_slack.png 1x, https://platform.slack-edge.com/img/add_to_slack@2x.png 2x"></a>

To enable tipping in slack for your team, 94 seconds of setup is required. Like this:

##### Create a new outgoing webhook from:

Go to https://yourdomain.slack.com/services/new/outgoing-webhook

(replace *yourdomain* with your slack domain)

Create a new "Outgoing Webhook".

1. Leave the Channel to `Any`
2. Set the Trigger Word to `changetip,@changetip`
3. Set the URL to `https://bots.changetip.com/slack/command-webhook`

Like this:

![Slack Setup 1](https://cdn.changetip.com/img/screenshots/slack_setup_1.png?1 "Slack Setup 1")

The descriptive label, name, and icon are up to you. If you'd like, you can use this icon https://cdn.changetip.com/img/logos/changetip_round_icon.png . 

Note: it looks like there is a bug with slack where if you try to upload the icon while creating the webhook, you lose your data. Recommend you add the Icon after you save the webhook.

![Slack Setup 2](https://cdn.changetip.com/img/screenshots/slack_setup_2.png?1 "Slack Setup 2")

That's it! Start tipping! The bot will provide instructions with what to do. Don't be scared. :)


### Support

If you have any questions, or recommendations for new features, we'd like to hear from you - support@changetip.com



## Contributing

We love pull requests!

#### Installation to run your own copy
Using a python [virtualenv](http://docs.python-guide.org/en/latest/dev/virtualenvs/) is recommended.

This is a django app. It pulls in the [changetip python library](https://pypi.python.org/pypi/changetip). To install the dependencies:

```
$ pip install -r requirements.txt
```

#### Configure the needed variables
Register your application with Slack:
https://api.slack.com/applications

Set your Redirect URI to your local environment to enable OAuth. You will likely need to ngrok it.
https://mylocaldevenv.io/slack/auth

Set your environment variables:
```
export SLACK_CLIENT_ID=xxxx
export SLACK_CLIENT_SECRET=xxxx
```

#### Running
```
CHANGETIP_API_KEY=xxxx uwsgi --init uswgi.ini
```

To get an API key, contact support@changetip.com


### License
BSD
