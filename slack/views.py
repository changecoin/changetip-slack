from bot import SlackBot
from django.http import HttpResponse, JsonResponse
from django.views.decorators.http import require_POST
from slack.models import SlackUser
import cleverbot
import json
import re


@require_POST
def command_webhook(request):
    """
    Handle data from a webhook
    """
    print json.dumps(request.POST.copy(), indent=2)
    # Do we have this user?
    slack_sender, created = SlackUser.objects.get_or_create(
        name=request.POST.get("user_name"),
        team_id=request.POST.get("team_id"),
        user_id=request.POST.get("user_id"),
    )
    if created:
        return JsonResponse({"text": "Nice to meet you!"})

    text = request.POST.get("text", "")

    # Check for mention in the format of <@$userid>
    mention_match = re.search('<@(U[A-Z0-9]+)>', text)
    if not mention_match:
        # Say something clever
        cb = cleverbot.Cleverbot()
        response = cb.ask(text.replace('changetip', ''))
        return JsonResponse({"text": response})

    slack_receiver = SlackUser.objects.filter(team_id = slack_sender.team_id, user_id=mention_match.group(1)).first()
    if not slack_receiver:
        return JsonResponse({"text": "I don't know who that person is. They should say hi."})

    # Submit the tip
    bot = SlackBot()
    team_domain = request.POST.get("team_domain")
    tip_data = {
        "sender": "%s@%s" % (slack_sender.name, team_domain),
        "receiver": "%s@%s" % (slack_receiver.name, team_domain),
        "message": text,
        "context_uid": bot.unique_id(request.POST.copy()),
        "meta": {}
    }
    for meta_field in ["token", "team_id", "channel_id", "channel_name", "user_id", "user_name", "command"]:
        tip_data["meta"][meta_field] = request.POST.get(meta_field)

    if request.POST.get("noop"):
        return JsonResponse({"text": "Hi!"})

    response = bot.send_tip(**tip_data)
    info_url = "https://www.changetip.com/tip-online/slack"
    out = ""
    if response.get("error_code") == "invalid_sender":
        out = "To send your first tip, login with your slack account on ChangeTip: %s" % info_url
    elif response.get("error_code") == "duplicate_context_uid":
        out = "Duplicate tip"
    elif response.get("error_message"):
        out = response.get("error_message")
    elif response.get("state") in ["ok", "accepted"]:
        tip = response["tip"]
    if tip["status"] == "out for delivery":
        out += "The tip is out for delivery. %s needs to collect by connecting their ChangeTip account to slack at %s" % (tip["receiver"], info_url)
    elif tip["status"] == "finished":
            out += "The tip has been delivered, %s has been added to %s's ChangeTip wallet." % (tip["amount_display"], tip["receiver"])

    if "+debug" in text:
        out += "\n```\n%s\n```" % json.dumps(response, indent=2)

    return JsonResponse({"text": out})


def home(request):
    return HttpResponse("OK")
