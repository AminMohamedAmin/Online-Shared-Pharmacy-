from django.shortcuts import render,redirect,get_object_or_404
from django.views.decorators.http import require_POST
from doctor.models import Medicine
from .cart import Cart
from .forms import CartAddProductForm
from login.models import Actions


@require_POST
def cart_add(request,medicine_id):
	cart = Cart(request)
	medicine = get_object_or_404(Medicine,id=medicine_id)
	form = CartAddProductForm(request.POST)
	if form.is_valid():
		cd = form.cleaned_data
		cart.add(
			medicine=medicine,
			quantity=cd['quantity'],
			update_quantity=cd['update']
			)
	neww = Actions()
	neww.action = medicine.medicine_name + ' ' + 'new buy'
	neww.type = 'Medicine_Buy'
	neww.save()
	return redirect('cart:cart_detail')


def cart_remove(request,medicine_id):
	cart = Cart(request)
	medicine = get_object_or_404(Medicine,id=medicine_id)
	cart.remove(medicine)
	return redirect('cart:cart_detail')


def cart_detail(request):
	cart = Cart(request)
	for item in cart:
		item['update_quantity_form'] = CartAddProductForm(initial={'quantity':item['quantity'],'update':True})
	text = 'Medicine successfully added to cart, check it '
	context = {
		'cart': cart,
		'text':text,
	}
	return render(request,'userhome.html',context)