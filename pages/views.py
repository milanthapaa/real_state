from django.shortcuts import render
from realtors.models import Realtor
from listings.models import Listing
from listings.choices import bedroom_choices, price_choices, state_choices


# Create your views here.
def index(request):
    # Get all realtors
    listings = Listing.objects.order_by('-list_date').filter(is_published=True)[0:3]

    context = {
        'listings': listings,
        'bedroom_choices': bedroom_choices,
        'price_choices': price_choices,
        'state_choices': state_choices,
    }

    # Reature app template with context
    return render(request, 'pages/index.html', context)


def about(request):
    # Get all realtors
    realtors = Realtor.objects.order_by('-hired_date')

    # Get MVP
    mvp_realtors = Realtor.objects.all().filter(is_mvp=True)

    context = {
        'realtors': realtors,
        'mvp_realtors': mvp_realtors,
    }

    # Reature app template with context
    return render(request, 'pages/about.html', context)
