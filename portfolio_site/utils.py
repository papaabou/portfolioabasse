import io
import os
import tempfile

from django.core.files.base import ContentFile
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


def extract_video_frame(video_file_field, seek_fraction=0.15, max_width=1600, quality=85):
    """
    Extract a representative JPEG frame from an already-saved video FileField
    (local disk or remote storage like R2), seeking a bit into the clip to
    avoid black/blank intro frames. Returns a ContentFile ready to assign to
    an ImageField, or None if extraction fails.
    """
    import cv2
    from PIL import Image

    tmp_path = None
    try:
        with video_file_field.open("rb") as src:
            with tempfile.NamedTemporaryFile(suffix=".mp4", delete=False) as tmp:
                tmp_path = tmp.name
                for chunk in src.chunks():
                    tmp.write(chunk)

        cap = cv2.VideoCapture(tmp_path)
        frame_count = cap.get(cv2.CAP_PROP_FRAME_COUNT) or 0
        target_frame = int(frame_count * seek_fraction)
        cap.set(cv2.CAP_PROP_POS_FRAMES, target_frame)
        ok, frame = cap.read()
        cap.release()

        if not ok:
            return None

        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(rgb_frame)
        if img.width > max_width:
            ratio = max_width / img.width
            img = img.resize((max_width, int(img.height * ratio)), Image.LANCZOS)

        buf = io.BytesIO()
        img.save(buf, format="JPEG", quality=quality, optimize=True)
        buf.seek(0)
        return ContentFile(buf.read())
    except Exception:
        logger.exception("Video frame extraction failed")
        return None
    finally:
        if tmp_path and os.path.exists(tmp_path):
            os.remove(tmp_path)
