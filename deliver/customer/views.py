from django.shortcuts import render
from django.views import View

from deliver.customer.models import OrderModel
from deliver.customer.models import MenuItem

class Index(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'customer/index.html')
    
class About(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'customer/about.html')
    
class Order(View):
    def get(self, request, *args, **kwargs):
        #get every item from each category
        lanches = MenuItem.objects.filter(category__name__contains='Lanches')
        salgados = MenuItem.objects.filter(category__name__contains='Salgados')
        bebidas = MenuItem.objects.filter(category__name__contains='Bebidas')
        sobremesas = MenuItem.objects.filter(category__name__contains='Sobremesas')
        
        #pass into context
        context ={
            'lanches': lanches,
            'salgados': salgados,
            'bebidas': bebidas,
            'sobremesas': sobremesas,
        }

        #render the template
        return render(request,'customer/order.html', context)
    
    def post(self, request, *args, **kwargs):
        order_items = {
            'items':[]
        }

        items = request.POST.getlist('items[]')

        for item in items:
            menu_item = MenuItem.objects.get(pk__contains=int(item))
            
            item_data = {
                'id': menu_item.pk,
                'name': menu_item.name,
                'price': menu_item.price,
            }

            order_items['items'].append(item_data)

            price = 0 
            item_ids = []

            for item in order_items['items']:
                price += item['price']
                item_ids.append(item['id'])

            order = OrderModel.objects.create(price=price)
            order.items.add(*item_ids)

            context = {
                'items': order_items['items'],
                'price': price,
            }

            return render(request, 'customer/order_confirmation.html', context)

