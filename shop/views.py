from django.shortcuts import render
from .models import Product
from django.core.paginator import Paginator

# Create your views here.
def itemList(request):
    product_list = Product.objects.all()

    item_name = request.GET.get('item_name')
    if item_name!="" and item_name is not None:
        product_list = product_list.filter(title__icontains=item_name)

    paginator = Paginator(product_list,12)
    page_num = request.GET.get('page')
    product_list = paginator.get_page(page_num)

    context={
        'product_list':product_list,
    }
    return render(request,'shop/home.html',context)


def detail(request,id):
    product_object = Product.objects.get(id=id)
    return render(request,'shop/detail.html',{'product_object':product_object})
