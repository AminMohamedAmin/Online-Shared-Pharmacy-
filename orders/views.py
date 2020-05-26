from django.shortcuts import render
from .forms import OrderCreateForm
from .models import OrderItem
from cart.cart import Cart
from login.models import Actions


def order_create(request):
	cart = Cart(request)
	if request.method == 'POST':
		form = OrderCreateForm(request.POST)
		if form.is_valid():
			order = form.save()
			for item in cart:
				OrderItem.objects.create(
					order=order,
					product=item['medicine'],
					price=item['medicine_price'],
					quantity=item['quantity'])

			cart.clear()
			neww = Actions()
			neww.action = 'New Order added'
			neww.type = 'Order'
			neww.save()
			context = {
				'order':order,
			}
			return render(request,'order/orderdone.html',context)

	else:
		form = OrderCreateForm()
	context = {
		'cart':cart,
		'form':form
	}
	return render(request, 'order/order.html', context)