from bot import SlackBot
from django.http import HttpResponse
from django.views.decorators.http import require_POST


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
        "sender": request.POST.get("user_name"),
        "receiver": tippee,
        "message": text,
        "context_uid": bot.unique_id(request.POST.copy()),
        "meta": {}
    }
    for meta_field in ["token", "team_id", "channel_id", "channel_name", "user_id", "user_name", "command"]:
        tip_data["meta"][meta_field] = request.POST.get(meta_field)

    if not request.POST.get("noop"):
        bot.handle_tip(**tip_data)

    return HttpResponse("hi, @%s" % tippee)


def home(request):
    return HttpResponse("OK")
