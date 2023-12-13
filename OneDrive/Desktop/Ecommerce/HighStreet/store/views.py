from django.shortcuts import render,redirect
from django.http import HttpResponse
from cart.views import _cart_id
from.models import Product,Category,ReviewRating
from orders.models import OrderProduct
from cart.models import Cart,CartItem
from django.core.paginator import EmptyPage,Paginator
from django.contrib.auth.decorators import login_required
from .forms import ReviewForm
from django.contrib import messages

# Create your views here.

# @login_required(login_url='signin')
def home(request):
    search = request.GET.get('search')
    products = Product.objects.all()
    if search:
        products = products.filter(description__icontains=search)
    
    return render(request,'store/home.html',{'products':products}) 

def stores(request,category_slug):
    search = request.GET.get('search')
    
    if category_slug == 'mens-clothing':
        products = Product.objects.filter(category__parent_id__in=[5, 6], is_active=True).order_by('created_at')
    elif category_slug == 'womens-clothing':
        products = Product.objects.filter(category__parent_id__in=[1, 2], is_active=True).order_by('created_at')
    else:
        category = Category.objects.get(slug=category_slug)
        products = Product.objects.filter(category=category, is_active=True).order_by('created_at')
    product_count = products.count()
    if search:
        products = products.filter(description__icontains=search)
        
    paginator = Paginator(products,2)
    page = request.GET.get('page')
    paged_products = paginator.get_page(page)
    
    context = {
        'products':paged_products,
        'product_count':product_count
    }
    return render(request,'store/store.html',context)


def product_details(request,category_slug,product_slug):
    try:
        product_detail = Product.objects.get(category__slug = category_slug,slug = product_slug)
        in_cart = CartItem.objects.filter(cart__cart_id = _cart_id(request),product=product_detail).exists()
        
    except Exception as e:
        raise e
    
    if request.user.is_authenticated:
        try:
            order_products = OrderProduct.objects.filter(user=request.user, product_id=product_detail.id).exists()
        except OrderProduct.DoesNotExist:
            order_products = None
    else:
        order_products = None    
    
    #reviews
    reviews = ReviewRating.objects.filter(product_id = product_detail.id,status = True)
    context={
        'product_detail':product_detail,
        'in_cart':in_cart,
        'order_products':order_products,
        'reviews':reviews
    }
    return render(request,'store/product_detail.html',context)

def submit_review(request,product_id):
    url = request.META.get('HTTP_REFERER')
    if request.method == 'POST':
        try:
            review = ReviewRating.objects.get(user__id=request.user.id, product__id = product_id)
            form = ReviewForm(request.POST, instance = review)
            form.save()
            messages.success(request,"Thank you! Your review has been updated")
            return redirect(url)
        except ReviewRating.DoesNotExist:
            form = ReviewForm(request.POST)
            if form.is_valid():
                data = ReviewRating()
                data.subject = form.cleaned_data["subject"]
                data.rating = form.cleaned_data["rating"]
                data.review = form.cleaned_data["review"]
                data.ip = request.META.get('REMOTE_ADDR')
                data.product_id = product_id
                data.user_id = request.user.id
                data.save()
                messages.success(request, "Thank you ! your review is submitted.")
                return redirect(url)