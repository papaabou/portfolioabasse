from django.shortcuts import render, redirect
import resend
from django.conf import settings
from threading import Thread
import logging
from email.utils import formataddr
from django.core.mail import EmailMultiAlternatives

logger = logging.getLogger(__name__)

resend.api_key = settings.RESEND_API_KEY

def render_thanks(request, session_key, redirect_url, template="general/thanks.html", extra_context=None):
    """
    Shared logic for thank-you pages:
    - Checks session key
    - Deletes session flag
    - Renders the template with extra context
    """
    if not request.session.get(session_key):
        return redirect(redirect_url)

    del request.session[session_key]

    context = extra_context or {}
    return render(request, template, context)

def send_django_email(
    *,
    subject: str,
    to: list[str],
    html: str,
    text: str | None = None,
    reply_to: str | None = None,
    sender_name: str = "Portfolio Website",
):
    from_email = formataddr((sender_name, settings.DEFAULT_FROM_EMAIL))

    email = EmailMultiAlternatives(
        subject=subject,
        body=text or "",
        from_email=from_email,
        to=to,
        reply_to=[reply_to] if reply_to else None,
    )

    email.attach_alternative(html, "text/html")

    return email.send(fail_silently=False)


def send_django_email_async(**kwargs):
    def _send():
        try:
            send_django_email(**kwargs)
        except Exception:
            logger.exception("Django email failed")

    Thread(target=_send, daemon=True).start()
