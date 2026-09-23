from django.conf import settings
from django.core.mail import send_mail
from django.shortcuts import render

from .forms import ContactForm


def contact(request):
    if request.method == "POST":
        form = ContactForm(request.POST)

        if form.is_valid():
            name = form.cleaned_data["name"]
            email = form.cleaned_data["email"]
            phone = form.cleaned_data["phone"]
            subject = form.cleaned_data["subject"]
            message = form.cleaned_data["message"]

            full_message = f"""
Νέο μήνυμα από τη φόρμα επικοινωνίας του StudyCode

Ονοματεπώνυμο: {name}
Email: {email}
Τηλέφωνο: {phone or "Δεν δόθηκε"}

Θέμα:
{subject}

Μήνυμα:
{message}
"""

            send_mail(
                subject=f"[StudyCode] {subject}",
                message=full_message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[settings.DEFAULT_FROM_EMAIL],
                fail_silently=False,
            )

            return render(
                request,
                "contact/contact.html",
                {
                    "form": ContactForm(),
                    "success": True,
                },
            )

    else:
        form = ContactForm()

    return render(
        request,
        "contact/contact.html",
        {"form": form},
    )

