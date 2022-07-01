from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404
from listings.models import Listing
from listings.choices import bedroom_choices, price_choices, state_choices


# Create your views here.
def listings(request):
    # Get all realtors
    primary_listings = Listing.objects.order_by('-list_date').filter(is_published=True)

    paginator = Paginator(primary_listings, 6)
    page = request.GET.get('page')
    paged_listings = paginator.get_page(page)

    context = {
        'primary_listings': paged_listings,
        'bedroom_choices': bedroom_choices,
        'price_choices': price_choices,
        'state_choices': state_choices,
    }

    # Reature app template with context
    return render(request, 'listings/listings.html', context)


def listing(request, listing_id):
    single_listing = get_object_or_404(Listing, pk=listing_id)

    context = {
        'single_listing': single_listing
    }

    return render(request, 'listings/listing.html', context)


def search(request):
    queryset_list = Listing.objects.order_by('-list_date')
    if request.method == 'GET':
        keyword = request.GET.get('keywords')
        if keyword:
            queryset_list = queryset_list.filter(description__icontains=keyword)
        city = request.GET.get('city')
        if city:
            queryset_list = queryset_list.filter(city__iexact=city)
        state = request.GET.get('state')
        if state:
            queryset_list = queryset_list.filter(state__iexact=state)
        bedroom = request.GET.get('bedrooms')
        if bedroom:
            queryset_list = queryset_list.filter(bedroom__lte=bedroom)
        price = request.GET.get('price')
        if price:
            queryset_list = queryset_list.filter(price__lte=price)

        context = {
            'bedroom_choices': bedroom_choices,
            'price_choices': price_choices,
            'state_choices': state_choices,
            'queryset_list': queryset_list,
            'values': request.GET
        }
        return render(request, 'listings/search.html', context)

    return render(request, 'listings/search.html')
