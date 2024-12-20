from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver
from django.db import transaction

# Create your models here.
class Categorie(models.Model):
  sub_category = models.ForeignKey('self',on_delete = models.CASCADE,related_name = 'sub_categories',null=True,blank=True)
  is_sub = models.BooleanField(default=False,null=True,blank=True)
  name = models.CharField(max_length=200,null=True)
  slug = models.SlugField(max_length=200,unique=True)
  def __str__(self):
    return self.name
class CreateUserForm(UserCreationForm):
  class Meta:
    model = User
    fields = ['username','email','first_name','last_name','password1','password2']
  
class Product(models.Model):
  category = models.ManyToManyField(Categorie,related_name='product')
  name = models.CharField(max_length=200,null=True)
  price = models.FloatField(default=0)
  price_origin = models.FloatField(default=0)
  detail = models.CharField(max_length=1000,null=True)
  image = models.ImageField(null=True,blank=True)
  inventory_quantity = models.IntegerField(default = 0,null=True,blank=True)
  purchased_quantity = models.IntegerField(default = 0) 
  @property
  def remaining_quantity(self):
    return (self.inventory_quantity - self.purchased_quantity)
  def __str__(self):
    return self.name

  def ImageURL(self):
    try:
      url = self.image.url
    except:
      url = ''
    return url
  
class Order(models.Model):
  customer = models.ForeignKey(User,on_delete=models.CASCADE,blank=True,null=True)
  date_order = models.DateField(auto_now_add=True)
  complete = models.BooleanField(default=False,null=True,blank=False)
  name = models.CharField(max_length=200,null=True)
  address = models.CharField(max_length=200,null=True)
  numberphone = models.CharField(max_length=12,null=True)
  transaction_id = models.CharField(max_length=200,null=True)
  
  def __str__(self):
    return str(self.id)
  @property
  def get_cart_total(self):
    orderitems = self.orderitem_set.all()
    total = sum([item.get_total for item in orderitems])
    return total
  @property
  def get_cart_items(self):
    orderitems = self.orderitem_set.all()
    total = sum([item.quantity for item in orderitems])
    return total
  
class OrderItem(models.Model):
  product = models.ForeignKey(Product,on_delete=models.CASCADE,blank=True,null=True)
  order = models.ForeignKey(Order,on_delete=models.CASCADE,blank=True,null=True)
  quantity = models.IntegerField(default = 0,null=True,blank=True)
  date_added = models.DateField(auto_now_add=True)
  @property
  def get_total(self):
    total = self.quantity*self.product.price
    return total
        
@receiver(post_delete, sender=OrderItem)
def update_purchased_quantity_on_orderitem_delete(sender, instance, **kwargs):
    if instance.product:
      product = instance.product
      product.purchased_quantity = sum(item.quantity for item in OrderItem.objects.filter(product=product))
      product.save()
@receiver(post_save, sender=OrderItem)
def update_purchased_quantity_on_orderitem_save(sender, instance, **kwargs):
  if instance.product:
    product = instance.product
    product.purchased_quantity = sum(item.quantity for item in OrderItem.objects.filter(product=product))
    product.save()