from django.shortcuts import render, redirect
from store_app.models import Product, Categories, Filter_Price, Color, Brand, Tag, Contact_us, Order, OrderItem
from django.conf import settings
from django.core.mail import send_mail
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from cart.cart import Cart
from django.views.decorators.csrf import csrf_exempt

import razorpay

client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))


def BASE(request):
    return render(request, 'Main/base.html')


def HOME(request):
    product = Product.objects.filter(status='Publish')

    context = {'product': product}

    return render(request, 'Main/index.html', context)


def PRODUCT(request):
    categories = Categories.objects.all()
    filter_price = Filter_Price.objects.all()
    color = Color.objects.all()
    brand = Brand.objects.all()
    COLORID = request.GET.get('color')
    BRANDID = request.GET.get('brand')

    ATOZID = request.GET.get('ATOZ')
    ZTOAID = request.GET.get('ZTOA')

    CATID = request.GET.get('categories')
    PRICE_FILTER_ID = request.GET.get('filter_price')

    PRICE_LOWTOHIGHID = request.GET.get('PRICE_LOWTOHIGH')
    PRICE_HIGHTOLOWID = request.GET.get('PRICE_HIGHTOLOW')

    NEW_PRODUCT_ID = request.GET.get('NEW_PRODUCT')
    OLD_PRODUCT_ID = request.GET.get('OLD_PRODUCT')

    if CATID:
        product = Product.objects.filter(categories=CATID, status='Publish')
    elif PRICE_FILTER_ID:
        product = Product.objects.filter(filter_price=PRICE_FILTER_ID, status='Publish')
    elif COLORID:
        product = Product.objects.filter(color=COLORID, status='Publish')
    elif BRANDID:
        product = Product.objects.filter(brand=BRANDID, status='Publish')
    elif ATOZID:
        product = Product.objects.filter(status='Publish').order_by('name')
    elif ZTOAID:
        product = Product.objects.filter(status='Publish').order_by('-name')
    elif PRICE_LOWTOHIGHID:
        product = Product.objects.filter(status='Publish').order_by('price')
    elif PRICE_HIGHTOLOWID:
        product = Product.objects.filter(status='Publish').order_by('-price')
    elif NEW_PRODUCT_ID:
        product = Product.objects.filter(condition='New', status='Publish').order_by('-id')
    elif OLD_PRODUCT_ID:
        product = Product.objects.filter(condition='Old', status='Publish')
    else:
        product = Product.objects.filter(status='Publish').order_by('-id')

    context = {'product': product,
               'categories': categories,
               'filter_price': filter_price,
               'color': color,
               'brand': brand}

    return render(request, 'Main/product.html', context)


def SEARCH(request):
    query = request.GET.get('query')
    product = Product.objects.filter(name__icontains=query)

    context = {
        'product': product
    }

    return render(request, 'Main/search.html', context)


def PRODUCT_DETAIL_PAGE(request, id):
    prod = Product.objects.filter(id=id).first()

    context = {
        'prod': prod
    }
    return render(request, 'Main/product_single.html', context)


def Contact_Page(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')

        contact = Contact_us(
            name=name,
            email=email,
            subject=subject,
            message=message
        )
        subject = subject
        message = message
        email_from = settings.EMAIL_HOST_USER
        try:
            send_mail(subject, message, email_from, ['noobda4967@gmail.com'])
            contact.save()
            return redirect('home')
        except:
            return redirect('contact')

    return render(request, 'Main/contact.html')


def HandleRegister(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        pass1 = request.POST.get('pass1')
        pass2 = request.POST.get('pass2')

        customer = User.objects.create_user(username, email, pass1)
        customer.first_name = first_name
        customer.last_name = last_name
        customer.save()
        return redirect('register')

    return render(request, 'Registration/auth.html')


def HandleLogin(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            return redirect('login')

    return render(request, 'Registration/auth.html')


def HandleLogout(request):
    logout(request)
    return redirect('home')



@login_required(login_url="/login/")
def cart_add(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.add(product=product)
    return redirect("home")


@login_required(login_url="/login/")
def item_clear(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.remove(product)
    return redirect("cart_detail")


@login_required(login_url="/login/")
def item_increment(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.add(product=product)
    return redirect("cart_detail")


@login_required(login_url="/login/")
def item_decrement(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.decrement(product=product)
    return redirect("cart_detail")


@login_required(login_url="/login/")
def cart_clear(request):
    cart = Cart(request)
    cart.clear()
    return redirect("cart_detail")


@login_required(login_url="/login/")
def cart_detail(request):
    return render(request, 'Cart/cart_details.html')


def Check_out(request):
    amount_str = request.POST.get('amount')
    if amount_str:
        try:
            amount_float = float(amount_str)
            amount_in_rupees = int(amount_float)
            amount_in_paise = amount_in_rupees * 100
        except ValueError:
            amount_in_paise = 0
    else:
        amount_in_paise = 0
    if amount_in_paise > 0:
        payment = client.order.create({
            "amount": amount_in_paise,  # Send amount in paise
            "currency": "INR",
            "payment_capture": "1"
        })
        order_id = payment['id']
        context = {'order_id': order_id, 'payment': payment, 'amount': amount_in_rupees}
    else:
        context = {'error': 'Invalid payment amount'}
    return render(request, 'Cart/checkout.html', context)



def PLACE_ORDER(request):
    if request.method == 'POST':
        uid = request.session.get('_auth_user_id')
        user = User.objects.get(id=uid)
        cart = request.session.get('cart')
        firstname = request.POST.get('firstname')
        lastname = request.POST.get('lastname')
        country = request.POST.get('country')
        address = request.POST.get('address')
        city = request.POST.get('city')
        state = request.POST.get('state')
        postcode = request.POST.get('postcode')
        phone = request.POST.get('phone')
        email = request.POST.get('email')
        notes = request.POST.get('notes')
        order_id = request.POST.get('order_id')
        payment = request.POST.get('payment')
        amount = request.POST.get('amount')

        context = {
            'order_id':order_id,
        }
        order = Order(
            user=user,
            firstname=firstname,
            lastname=lastname,
            country=country,
            address=address,
            city=city,
            state=state,
            postcode=postcode,
            phone=phone,
            email=email,
            payment_id=order_id,
            amount=amount
        )
        order.save()
        for i in cart:
            a = cart[i]['price']  # Price as a string
            b = cart[i]['quantity']  # Quantity as an integer

            print(type(a))  # Should show <class 'str'>
            print(type(b))  # Should show <class 'int'>

            # Convert price from string to float or int
            price_as_int = int(float(a))  # Convert to float first if there are decimal points

            # Now you can multiply
            total = price_as_int * b
            print(f"Total for item {i}: {total}")

            item = OrderItem(
                user=user,
                order=order,
                product=cart[i]['name'],
                image=cart[i]['image'],
                quantity=cart[i]['quantity'],
                price=cart[i]['price'],
                total=total
            )
            item.save()

        return render(request, 'Cart/placeorder.html', context)

@csrf_exempt
def success(request):
    if request.method == 'POST':
        a = request.POST
        order_id = ""
        for key, val in a.items():
            if key == 'razorpay_order_id':
                order_id = val
                break

        user = Order.objects.filter(payment_id=order_id).first()
        user.paid = True
        user.save()
    return render(request,'Cart/thank-you.html')


def Your_Order(request):
    uid = request.session.get('_auth_user_id')
    user = User.objects.get(id=uid)
    order = OrderItem.objects.filter(user=user).order_by('-id')
    context = {
        'order': order
    }
    return render(request, 'Main/your_order.html', context)