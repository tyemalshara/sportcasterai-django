from django.http.response import HttpResponse
from django.shortcuts import render, redirect  # new
from django.conf import settings  # new
from django.urls import reverse  # new

from products.models import UserPayment  # new
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt  # new
import stripe  # new
import time
from django import forms 

class PricePlanForm(forms.Form):
    football = forms.BooleanField(required=False)
    basketball = forms.BooleanField(required=False)
    tennis = forms.BooleanField(required=False)

def home(request):  # new
    stripe.api_key = settings.STRIPE_SECRET_KEY
    customer_id = request.user.id 
    if request.method == "POST":
        if 'get_profi_paket' in request.POST and request.POST['get_profi_paket'] == 'get_profi_paket':
            form = PricePlanForm(request.POST)
            if form.is_valid():
                features = sum([
                    form.cleaned_data['football'], 
                    form.cleaned_data['basketball'], 
                    form.cleaned_data['tennis']])
                base_price = 19.99
                additional_price = 3.99 * features
                total_price = base_price + additional_price
                checkout_session = stripe.checkout.Session.create(
                    payment_method_types=['card'],
                    line_items=[{
                        'price_data': {
                            'currency': 'usd',
                            'product_data': {
                                'name': 'Your Product Name',
                            },
                            'unit_amount': int(total_price * 100),  # Convert to cents
                        },
                        'quantity': 1,
                    }],
                    mode='payment',
                    customer_creation='always',
                    success_url= settings.REDIRECT_DOMAIN + '/success?session_id={CHECKOUT_SESSION_ID}',
                    cancel_url=request.build_absolute_uri(reverse("cancel")),
                )
                return redirect(checkout_session.url, code=303)
            else:
                    form = PricePlanForm()
        if 'get_premium_paket' in request.POST and request.POST['get_premium_paket'] == 'get_premium_paket':
            checkout_session = stripe.checkout.Session.create(
                line_items=[
                    {
                        "price": "price_1PyWjBAZ52UONzehTNuyljJy",  # enter yours here!!!
                        "quantity": 1,
                    }
                ],
                mode="payment",
                customer_creation='always',    # assign an 'always' string to create a cutomer id if not provided 
                success_url= settings.REDIRECT_DOMAIN + '/success?session_id={CHECKOUT_SESSION_ID}',
                # success_url=request.build_absolute_uri(reverse("success")),
                cancel_url=request.build_absolute_uri(reverse("cancel")),
            )
            return redirect(checkout_session.url, code=303)
    return render(request, "home.html")

def success(request):
    stripe.api_key = settings.STRIPE_SECRET_KEY
    print("This the request the success view function is getting: ",request)
    checkout_session_id = request.GET.get("session_id", None)
    print("this is the checkout session id: ", checkout_session_id)
    session = stripe.checkout.Session.retrieve(checkout_session_id)
    # customer = stripe.Customer.retrieve(session.customer)
    customer = session.customer    # the customer id who just paid 
    print("this is the customer id: ", customer)
    user_id = request.user.id    # the user_id of current logged in user
    print("this is the user id: ", user_id)
    user_payment = UserPayment.objects.get(app_user=user_id)
    print("this is the user payment: ", user_payment)
    # user_payment = UserPayment.objects.all()
    user_payment.stripe_checkout_id = checkout_session_id
    print("this is the user specific checkout id : ", user_payment.stripe_checkout_id)
    user_payment.save()
    return render(request, "success.html", {'customer':customer})


def cancel(request):
    return render(request, "cancel.html")

@csrf_exempt
def stripe_webhook(request):
    stripe.api_key = settings.STRIPE_SECRET_KEY
    time.sleep(10)
    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    event = None
    try:
        event = stripe.Webhook.construct_event(payload, sig_header, settings.STRIPE_WEBHOOK_SECRET_TEST)
    except ValueError as e:
        # Invalid payload
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        return HttpResponse(status=400)
    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']
        session_id = session.get('id', None)
        time.sleep(15)
        user_payment = UserPayment.objects.get(stripe_checkout_id=session_id)
        line_items = stripe.checkout.Session.list_line_items(session_id,limit=1)
        user_payment.payment_bool = True
        user_payment.save()
    return HttpResponse(status=200)