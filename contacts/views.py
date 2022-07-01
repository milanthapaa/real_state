from django.shortcuts import redirect
from contacts.models import Contact
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings


# Create your views here.
def contact(request):
    if request.method == 'POST':
        listing_id = request.POST.get('listing_id')
        listing = request.POST.get('listing')
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        message = request.POST.get('message')
        user_id = request.POST.get('user_id')
        realtor_email = request.POST.get('realtor_email')
        customer_message = f'Customer name: {name} \n' \
                           f'Customer email: {email} \n' \
                           f'Customer phone: {phone} \n' \
                           f'Customer interested property: {listing} \n' \
                           f'Customer message: {message}'

        if request.user.is_authenticated:
            user_id = request.user.id
            has_contacted = Contact.objects.filter(listing_id=listing_id, user_id=user_id)

            if has_contacted:
                messages.error(request, 'You have already made an inquery for this listing.')
                return redirect('/listings/' + listing_id)

        Contact.objects.create(listing=listing, listing_id=listing_id, name=name, email=email,
                               phone=phone, message=message, user_id=user_id, realtor_email=realtor_email)
        send_mail('Inquery for listing', customer_message, settings.EMAIL_HOST_USER,
                  [realtor_email], fail_silently=False)
        messages.success(request, 'Your request has been submitted, a realtor will get back to you asap.')

        return redirect('/listings/' + listing_id)


def reconnect(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        listing = request.POST.get('listing')
        realtor_email = request.POST.get('realtor_email')
        customer_message = f'Resubmit of the listing query:' \
                           f'Customer name: {name} \n' \
                           f'Customer email: {email} \n' \
                           f'Customer phone: {phone} \n' \
                           f'Customer interested property: {listing} \n' \
                           f'Please revert back ASAP.'
        send_mail('Inquery for listing', customer_message, settings.EMAIL_HOST_USER,
                  [realtor_email], fail_silently=False)
        messages.success(request, 'Sorry for the inconvenience, your query has been updated '
                                  'and the representative will get back to you asap.')
        return redirect('dashboard')
