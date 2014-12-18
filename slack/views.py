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

    # TOO Submit the tip

    return HttpResponse("hi, @%s" % tippee)


def home(request):
    return HttpResponse("OK")
