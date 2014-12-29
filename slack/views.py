from bot import SlackBot
from django.http import HttpResponse
from django.views.decorators.http import require_POST
import json


@require_POST
def command_webhook(request):
    """
    Handle data when people issue a /tip command
    https://changecoin.slack.com/services/3245626184?added=1
    """
    usage = "Usage: /tip @tippee $amount"
    text = request.POST.get("text", "")

    bot = SlackBot()

    # Check for mention
    mentions = bot.get_mentions(text)
    if len(mentions) != 1:
        return HttpResponse(usage)

    tippee = mentions[0] # TODO

    # Submit the tip
    tip_data = {
        "sender": request.POST.get("user_id"),
        "receiver": tippee,
        "message": text,
        "context_uid": bot.unique_id(request.POST.copy()),
        "meta": {}
    }
    for meta_field in ["token", "team_id", "channel_id", "channel_name", "user_id", "user_name", "command"]:
        tip_data["meta"][meta_field] = request.POST.get(meta_field)

    if request.POST.get("noop"):
        return HttpResponse("Hi!")

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
            out += "The tip is out for delivery. %s needs to hook up their ChangeTip account to slack at %s" % (tippee, info_url)
	elif tip["status"] == "finished":
            out += "The tip has been delivered, %s has been added to %s's ChangeTip wallet." % (tip["amount_display"], tippee)

    if "+debug" in text:
    	out += "\n```\n%s\n```" % json.dumps(response, indent=2)

    return HttpResponse(out)




def home(request):
    return HttpResponse("OK")
