from bot import SlackBot
from django.core.cache import cache
from django.http import HttpResponse, JsonResponse, HttpResponseBadRequest
from django.views.decorators.http import require_POST
from slack.models import SlackUser
from image_response import ImageResponse
import cleverbot
import json
import re
import requests
import os

INFO_URL = "https://www.changetip.com/tip-online/slack"
MESSAGES = {
    "help": u"""Hi {user_name}. Here's some help.
To send a tip, mention *a person* and *an amount* like this:
`/changetip give @buddy $1`.
You can also use a moniker for the amount, like `a beer` or `2 coffees`.
Any questions? E-mail support@changetip.com
""",
    "help_webhooks": u"""Hi {user_name}. Here's some help.
To send a tip, mention *changetip*, *a person* and *an amount* like this:
`changetip: give @buddy $1`.
You can also use a moniker for the amount, like `a beer` or `2 coffees`.
Any questions? E-mail support@changetip.com
""",
    "duplicate": "That looks like a duplicate tip.",
    "greeting": u"Hi, {user_name}! {get_started}",
    "get_started": u"To send your first tip, login with your slack account on ChangeTip: {info_url}".format(info_url=INFO_URL),
    "unknown_receiver": u"@{user_name}, before they can receive your tip, ask them to type: *changetip: accept*",
    "out_for_delivery": u"The tip for {amount_display} is out for delivery. {receiver} needs to collect by connecting their ChangeTip account to slack at %s" % INFO_URL,
    "finished": u"The tip has been delivered, {amount_display} has been added to {receiver}'s ChangeTip wallet. {img_url}"
}


def slack_oauth(request):
    client_id = os.getenv("CLIENT_ID", None)
    client_secret = os.getenv("CLIENT_SECRET", None)
    code = request.GET.get('code', None)

    if not client_id or not client_secret or not code:
        return HttpResponseBadRequest()

    requests.get("https://slack.com/api/oauth.access?client_id={}&client_secret={}&code={}".format(client_id, client_secret, code))
    return HttpResponse("Success!")


@require_POST
def command_webhook(request):
    """
    Handle data from a webhook
    """
    print(json.dumps(request.POST.copy(), indent=2))

    if request.POST.get("noop"):
        return JsonResponse({"text": "Hi!"})

    # Separated so we can still support the legacy webhook integration
    if 'command' in request.POST.keys():
        return _slash_command(request)
    else:
        return _outgoing_webhook(request)


def _slash_command(request):
    user_name = request.POST.get("user_name")

    # TODO tagging for usernames
    # Create SlackUser. This is used for tagging
    SlackUser.objects.get_or_create(
        name=user_name,
        team_id=request.POST.get("team_id"),
        user_id=request.POST.get("user_id"),
    )

    text = request.POST.get("text", "")

    # Check for mention in the format of @userId123 (only grab first)
    mention_match = re.search('@([A-Za-z0-9]+)', text)
    if not mention_match:
        # Do they want help?
        if "help" in text:
            return JsonResponse({"text": MESSAGES["help"].format(user_name=user_name), "response_type": "in_channel"})
        else:
            # Temporarily commenting out the following because Cleverbot now has ads
            # # Say something clever
            # response = get_clever_response(user_id, text)
            # response = append_image_response(text, response)
            # return JsonResponse({"text": response, "username": "changetip-cleverbot"})
            return JsonResponse({"text": MESSAGES["help"].format(user_name=user_name), "response_type": "in_channel"})
    receiver = mention_match.group(1)

    # Submit the tip
    team_domain = request.POST.get("team_domain")
    tip_data = {
        "sender": "%s@%s" % (user_name, team_domain),
        "receiver": "%s@%s" % (receiver, team_domain),
        "message": text,
        "context_uid": SlackBot().unique_id(request.POST.copy()),
        "meta": {}
    }
    for meta_field in ["token", "team_id", "channel_id", "channel_name", "user_id", "user_name", "command"]:
        tip_data["meta"][meta_field] = request.POST.get(meta_field)

    out = submit_tip(tip_data)

    return JsonResponse({"text": out, "response_type": "in_channel"})


def _outgoing_webhook(request):
    # Do we have this user?
    user_name = request.POST.get("user_name")
    user_id = request.POST.get("user_id")
    slack_sender, created = SlackUser.objects.get_or_create(
        name=user_name,
        team_id=request.POST.get("team_id"),
        user_id=request.POST.get("user_id"),
    )

    if created:
        return JsonResponse({"text": MESSAGES["greeting"].format(user_name=user_name, get_started=MESSAGES["get_started"]), "response_type": "in_channel"})

    text = request.POST.get("text", "")

    # Check for mention in the format of <@$userid> (only grab first)
    mention_match = re.search('<@(U[A-Z0-9]+)>', text)
    if not mention_match:
        # Do they want help?
        if "help" in text:
            return JsonResponse({"text": MESSAGES["help_webhooks"].format(user_name=user_name), "response_type": "in_channel"})
        else:
            return JsonResponse({"text": MESSAGES["help_webhooks"].format(user_name=user_name), "response_type": "in_channel"})
            # Temporarily commenting out the following because Cleverbot now has ads
            # # Say something clever
            # response = get_clever_response(user_id, text)
            # response = append_image_response(text, response)
            # return JsonResponse({"text": response, "username": "changetip-cleverbot"})

    slack_receiver = SlackUser.objects.filter(team_id = slack_sender.team_id, user_id=mention_match.group(1)).first()
    if not slack_receiver:
        return JsonResponse({"text": MESSAGES["unknown_receiver"].format(user_name=user_name), "response_type": "in_channel"})

    # Substitute the @username back in (for each mention)
    for at_user_id in re.findall('(<@U[A-Z0-9]+>)', text):
        user_id_match = re.search('<@(U[A-Z0-9]+)>', at_user_id)
        if not user_id_match:
            continue
        user_id = user_id_match.group(1)
        if not user_id:
            continue
        slack_user = SlackUser.objects.filter(team_id = slack_sender.team_id, user_id=user_id).first()
        if not slack_user:
            continue
        text = text.replace(at_user_id, '@%s' % slack_user.name)

    # Submit the tip
    team_domain = request.POST.get("team_domain")
    tip_data = {
        "sender": "%s@%s" % (slack_sender.name, team_domain),
        "receiver": "%s@%s" % (slack_receiver.name, team_domain),
        "message": text,
        "context_uid": SlackBot().unique_id(request.POST.copy()),
        "meta": {}
    }
    for meta_field in ["token", "team_id", "channel_id", "channel_name", "user_id", "user_name", "command"]:
        tip_data["meta"][meta_field] = request.POST.get(meta_field)

    out = submit_tip(tip_data)

    return JsonResponse({"text": out})


def submit_tip(tip_data):
    """
    Sends the tip to the Changecoin API and returns an output message
    """

    text = tip_data['message']
    out = ""

    bot = SlackBot()
    response = bot.send_tip(**tip_data)

    try:
        if response.get("error_code") == "invalid_sender":
            out = MESSAGES["get_started"]
        elif response.get("error_code") == "duplicate_context_uid":
            out = MESSAGES["duplicate"]
        elif response.get("error_message"):
            if response.get("error_code") in ["tip_limit", "wallet_error", "pocket_error"]:
                out = "This tip cannot be completed"
            else:
                out = response.get("error_message")
        elif response.get("state") in ["ok", "accepted"]:
            tip = response["tip"]

            if tip["status"] == "out for delivery":
                out += MESSAGES["out_for_delivery"].format(amount_display=tip["amount_display"], receiver=tip["receiver"])
            elif tip["status"] == "finished":
                out += MESSAGES["finished"].format(amount_display=tip["amount_display"], receiver=tip["receiver"], img_url=tip['meta'].get('tip_img_url', ''))

        out = append_image_response(text, out)

        if "+debug" in text:
            out += "\n```\n%s\n```" % json.dumps(response, indent=2)

    except Exception as e:
        if "+debug" in text:
            return "output formatting error with: {}".format(e)

    return out


def get_clever_response(user_id, text):
    # Remember conversations per user
    cache_key = "clever_response:%s" % user_id
    cb = cache.get(cache_key)
    if not cb:
        cb = cleverbot.Cleverbot()
    text = re.sub('changetip', '', text, 1, re.I).strip('@: ')
    response = cb.ask(text)
    cache.set(cache_key, cb, 3600)
    return response


def append_image_response(text, response):
    image_response = ImageResponse().get_image_response(text, 1500000)

    if image_response[0]:
        response += " Plus %s #%s image: %s" % (image_response[1], image_response[0], image_response[2])
    return response


def home(request):
    return HttpResponse("OK")
