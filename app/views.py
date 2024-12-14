from django.shortcuts import render,redirect
from django.http import HttpResponse,JsonResponse
from .models import *
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.http import JsonResponse
import json
from django.db.models import Sum, F, CharField, Func
from django.db.models.functions import TruncDate,TruncWeek,TruncMonth,TruncYear,ExtractWeek, ExtractYear,Concat
from django.db.models import Value
from django.db.models.expressions import Window
from django.db.models.functions import DenseRank
from datetime import datetime, timedelta
from django.db.models import DateField
from django.db import transaction

# Create your views here.

def detail_page(request):
  quantity=0
  id=request.GET.get('id','')
  product = Product.objects.get(id=id)
  products = Product.objects.filter(category__in = product.category.all()).exclude(id=product.id).distinct()[:5]
  product_category = product.category.all()
  categories = Categorie.objects.filter(is_sub = False)
  if request.user.is_authenticated:
    customer = request.user
    order, created = Order.objects.get_or_create(customer = customer,complete=False)
    items = order.orderitem_set.all()
    cartItems = order.get_cart_items
  else:
    items = []
    order = {'get_cart_total':0,'get_cart_items':0}
    cartItems = order['get_cart_items']
  for i in items:
    if i.product.id == product.id:
      quantity = i.quantity
  context= {'products':products,'product':product,'quantity': quantity,'order':order,'cartItems':cartItems,'categories': categories,'product_category': product_category}
  return render(request,'app/detail.html',context)

def category(request):
  categories = Categorie.objects.filter(is_sub = False)
  active_category = request.GET.get('category','')
  if active_category:
    products = Product.objects.filter(category__slug = active_category)
  if request.user.is_authenticated:
    customer = request.user
    order, created = Order.objects.get_or_create(customer = customer,complete=False)
    items = order.orderitem_set.all()
    cartItems = order.get_cart_items
  else:
    items = []
    order = {'get_cart_total':0,'get_cart_items':0}
    cartItems = order['get_cart_items']
  context ={'categories':categories,'active_category':active_category,'products':products,'cartItems':cartItems}
  return render(request,'app/category.html',context)

def search(request):
    searched = ""
    keys = Product.objects.none()
    group_price = 0  # Default value

    if request.method == "POST":
        searched = request.POST.get("searched", "")
        filter_price = request.POST.get("filter_price", "default")

        # Filter products based on the statistic type
        if filter_price == "less_50":
            group_price = 50
            keys = Product.objects.filter(name__icontains=searched, price__lt=50)
        elif filter_price == "less_100":
            group_price = 100
            keys = Product.objects.filter(name__icontains=searched, price__lt=100)
        elif filter_price == "less_150":
            group_price = 150
            keys = Product.objects.filter(name__icontains=searched, price__lt=150)
        elif filter_price == "less_200":
            group_price = 200
            keys = Product.objects.filter(name__icontains=searched, price__lt=200)
        else:
            keys = Product.objects.filter(name__icontains=searched)

    # Handle cart data
    if request.user.is_authenticated:
        customer = request.user
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        items = []
        order = {'get_cart_total': 0, 'get_cart_items': 0}
        cartItems = order['get_cart_items']

    # Fetch all products and categories
    products = Product.objects.all()
    categories = Categorie.objects.filter(is_sub=False)

    context = {
        'searched': searched,
        'keys': keys,
        'products': products,
        'cartItems': cartItems,
        'categories': categories,
        'group_price': group_price,
    }

    return render(request, 'app/search.html', context)

def register(request):
  form = CreateUserForm()
  if request.method == "POST":
    form = CreateUserForm(request.POST)
    if form.is_valid():
      form.save()
      return redirect('login')
  context = {'form': form}
  return render(request,'app/register.html',context)

def loginPage(request):
  if request.user.is_authenticated:
    return redirect('home')
  if request.method == "POST":
    username = request.POST.get('username')
    password = request.POST.get('password')
    user = authenticate(request,username=username,password=password)
    if user is not None:
      login(request,user) 
      return redirect('home')
    else: messages.info(request,'User or password not correct')
  context = {}
  return render(request,'app/login.html',context)
def logoutPage(request):
  logout(request)
  return redirect('login')

def home(request):
  if request.user.is_authenticated:
    customer = request.user
    order, created = Order.objects.get_or_create(customer = customer,complete=False)
    items = order.orderitem_set.all()
    cartItems = order.get_cart_items
  else:
    items = []
    order = {'get_cart_total':0,'get_cart_items':0}
    cartItems = order['get_cart_items']
  products = Product.objects.all()
  categories = Categorie.objects.filter(is_sub = False)
  context= {'products': products,'cartItems': cartItems,'categories': categories}
  return render(request,'app/home.html', context)

def cart(request):
  if request.user.is_authenticated:
    customer = request.user
    order, created = Order.objects.get_or_create(customer = customer,complete=False)
    items = order.orderitem_set.all()
    cartItems = order.get_cart_items
  else:
    items = []
    order = {'get_cart_total':0,'get_cart_items':0}
    cartItems = order['get_cart_items']
  categories = Categorie.objects.filter(is_sub = False)
  context= {'items':items,'order':order,'cartItems':cartItems,'categories': categories}
  return render(request,'app/cart.html', context)

def checkout(request):
  if request.user.is_authenticated:
    customer = request.user
    order, created = Order.objects.get_or_create(customer = customer,complete=False)
    items = order.orderitem_set.all()
    cartItems = order.get_cart_items
  else:
    items = []
    order = {'get_cart_total':0,'get_cart_items':0}
    cartItems = order['get_cart_items']
  categories = Categorie.objects.filter(is_sub = False)
  context= {'items':items,'order':order,'cartItems':cartItems,'categories': categories}
  # thanhtoan
  if request.method == "POST":
    name = request.POST.get("name", "").strip()
    address = request.POST.get("address", "").strip()
    mobile = int(request.POST.get("mobile", "").strip())
    identify = request.POST.get("identify", "").strip()

    # Kiểm tra nếu bất kỳ trường nào bị bỏ trống
    if not name or not address or not mobile or not identify:
      context['error'] = "Vui lòng điền đầy đủ thông tin trước khi thanh toán!"
      return render(request, 'app/checkout.html', context)
    if mobile<0 or mobile>=1000000000000:
      context['error'] = "Sai số điện thoại"
      return render(request, 'app/checkout.html', context)
    # Thực hiện lưu vào cơ sở dữ liệu hoặc xử lý thêm
    # ...
    order.name = name
    order.address = address
    order.numberphone = mobile
    order.transaction_id = identify
    order.complete =True
    order.save()
    response =  '''<script type="text/javascript">alert("Thông tin thanh toán đã được xử lý thành công!");window.location.href = '/checkout/';</script>'''
    return HttpResponse(response)
  return render(request,'app/checkout.html', context)
def updateItem(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']
    customer = request.user
    product = Product.objects.get(id=productId)

    # Cập nhật purchased_quantity trước khi kiểm tra
    product.purchased_quantity = sum(item.quantity for item in OrderItem.objects.filter(product=product))
    product.save()

    # Lấy hoặc tạo đơn hàng
    order, created = Order.objects.get_or_create(customer=customer, complete=False)
    orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

    if action == 'add':
        if product.remaining_quantity > 0:
            orderItem.quantity += 1
            product.purchased_quantity += 1
            product.save()
        else:
            return JsonResponse({'error': 'Hết hàng rồi'}, status=400)
    elif action == 'remove':
        orderItem.quantity -= 1
        product.purchased_quantity -= 1
        product.save()
    orderItem.save()
    if orderItem.quantity <= 0:
        orderItem.delete()
    return JsonResponse({'message': 'Cập nhật thành công'}, safe=False)

def contact(request):
  return render(request, 'app/contact.html')

def introduce(request):
  return render(request, 'app/introduce.html')
# Chỉ cho phép nhân viên hoặc admin truy cập
def manage(request):
  return render(request, 'admin/base_site.html')

# format date
class DateFormat(Func):
  function = 'DATE_FORMAT'
  template = "%(function)s(%(expressions)s, '%(format)s')"
  output_field = CharField()

  def __init__(self, expression, format, **extra):
    super().__init__(expression, format=format, **extra)

def statistic(request):
  #----------------------------------------statistic sales------------------------------------------
  
  # Default to showing last 30 days of data
  end_date = datetime.now().date()
  start_date = end_date - timedelta(days=30)
  
  # Default to daily statistics
  group_by = 'day'

  if request.method == "POST":
    # Get date range from form
    start_date_str = request.POST.get('date-start')
    end_date_str = request.POST.get('date-end')
    group_by = request.POST.get('statistic-type', 'day')

    # Convert string dates to datetime objects
    if start_date_str:
      start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
    if end_date_str:
      end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()

  # Perform statistics based on grouping
  if group_by == 'day':
    statistics = (
      OrderItem.objects
      .filter(date_added__range=[start_date, end_date])
      .annotate(date=TruncDate('date_added', output_field=DateField()))
      .annotate(date_str=DateFormat('date_added', '%%d/%%m'))
      .values('date_str')
      .annotate(
        total_quantity=Sum('quantity'),
        total_revenue=Sum(F('quantity') * F('product__price'))
      )
      .order_by('date')
    )
  elif group_by == 'week':
    # Group by week
    statistics = (
      OrderItem.objects
      .filter(date_added__range=[start_date, end_date])
      .annotate(
        week=ExtractWeek('date_added'),  # Lấy số tuần
        year=ExtractYear('date_added')  # Lấy năm
      )
      .annotate(
        week_str=Concat(
          Value('Tuần '), F('week'), Value(' - Năm '), F('year'),
          output_field=CharField()
        )
      )
      .values('week_str')  # Nhóm theo chuỗi định dạng tuần
      .annotate(
        total_quantity=Sum('quantity'),
        total_revenue=Sum(F('quantity') * F('product__price'))
      )
      .order_by('year', 'week')  # Sắp xếp theo năm và tuần
    )
  elif group_by == 'month':
    # Group by month
    statistics = (
      OrderItem.objects
      .filter(date_added__range=[start_date, end_date])
      .annotate(month=TruncMonth('date_added', output_field=DateField()))
      .annotate(month_str=DateFormat('date_added', '%%m/%%Y'))
      .values('month_str')
      .annotate(
        total_quantity=Sum('quantity'),
        total_revenue=Sum(F('quantity') * F('product__price'))
      )
      .order_by('month')
    )
  else:  # year
    # Group by year
    statistics = (
      OrderItem.objects
      .filter(date_added__range=[start_date, end_date])
      .annotate(year=TruncYear('date_added', output_field=DateField()))
      .annotate(year_str=DateFormat('date_added', '%%Y'))
      .values('year_str')
      .annotate(
        total_quantity=Sum('quantity'),
        total_revenue=Sum(F('quantity') * F('product__price'))
      )
      .order_by('year')
    )

  #--------------------------------------statistic bestselling--------------------------------------
  
  # Tổng số lượng sản phẩm đã bán
  orders = Order.objects.filter(complete=True)
  orderItems = OrderItem.objects.filter(order__in=orders)
  sum_quantity = orderItems.aggregate(total_quantity=Sum('quantity'))['total_quantity'] or 0

  # Lọc danh sách sản phẩm bán chạy với số lượng >= 5
  bestSellings = (
    orderItems
    .values('product__name')  # Nhóm theo tên sản phẩm
    .annotate(
      total_quantity=Sum('quantity'),  # Tổng số lượng bán
      percent_quantity=(Sum('quantity') * 100) / sum_quantity if sum_quantity > 0 else 0  # Tính tỷ lệ phần trăm
    )
    .filter(total_quantity__gte=5)  # Chỉ lấy sản phẩm có số lượng >= 5
    .order_by('-total_quantity')  # Sắp xếp giảm dần theo số lượng
  )
  
  context = {
    'bestSellings': list(bestSellings),
    'statistics': list(statistics),
    'start_date': start_date,
    'end_date': end_date,
    'group_by': group_by
  }
  return render(request, 'app/statistic.html', context)
