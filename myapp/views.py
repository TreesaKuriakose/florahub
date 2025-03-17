from django.shortcuts import render
from .models import CustomUser 
from .models import Plant  
from django.contrib.auth import logout

# Create your views here.
def index(request):

    return render (request,'index.html')
def cart(request):

    return render (request,'cart.html')


def home(request):
    # Assuming you have a logged-in user and you're fetching their order
    order = None
    if request.user.is_authenticated:
        order = Order.objects.filter(user=request.user).first()  # Adjust the filter based on your model

    return render(request, 'home.html', {'order': order})

def forget_password(request):
    return render (request,'forget_password.html')

def register_view(request):
    return render (request,'register.html')


def login_view(request):
    return render (request,'login.html')

def register(request):
    if request.method == "POST":
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        
        # Check if passwords match
        if password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return redirect('register')
        
        # Check if username already exists
        if CustomUser.objects.filter(username=username).exists():
            messages.error(request, "Username already taken.")
            return redirect('register')

        # Check if email already exists
        if CustomUser.objects.filter(email=email).exists():
            messages.error(request, "Email already in use.")
            return redirect('register')

        try:
            # Create a new user if all checks pass
            user = CustomUser.objects.create_user(username=username, email=email, password=password)
            user.save()
            
            # Automatically log the user in after registration
            login(request, user)
            messages.success(request, "Registration successful!")
            return redirect('home')  # Redirect to home or other page as needed
        
        except IntegrityError as e:
            messages.error(request, "An error occurred while registering. Please try again.")
            return redirect('register')

    return render(request, 'register.html')




from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages

def login1(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        
        # Try to authenticate the user
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            return redirect('home')  # Redirect to home page after successful login
        else:
            messages.error(request, 'Invalid username or password.')
            return render(request, 'login.html')
    
    return render(request, 'login.html')


def custom_logout(request):
    logout(request)  # This logs the user out
    messages.success(request, "You have been logged out successfully!")  # Optional: Show a success message
    return redirect('login_view')








def plant_list(request):
    plants = Plant.objects.all()  # Fetch all plants
    return render(request, 'plant_list.html', {'plants': plants})





from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import Http404
from .models import Cart, CartItem, Plant
from django.contrib import messages

# View for viewing the user's cart
@login_required
def cart_view(request):
    # Get the cart for the current user, or create one if it doesn't exist
    cart, created = Cart.objects.get_or_create(user=request.user)

    # Get all items in the user's cart
    cart_items = CartItem.objects.filter(cart=cart)

    # Calculate total price
    total_price = cart.total_price()

    # Return the context to the template
    return render(request, 'cart.html', {
        'cart_items': cart_items,
        'total_price': total_price
    })

# View for adding a plant to the cart
@login_required
def add_to_cart(request, plant_id):
    try:
        plant = Plant.objects.get(id=plant_id)
    except Plant.DoesNotExist:
        raise Http404("Plant not found")
    
    # Get or create a cart for the current user
    cart, created = Cart.objects.get_or_create(user=request.user)
    
    # Check if the plant is already in the cart
    cart_item, created = CartItem.objects.get_or_create(cart=cart, plant=plant)
    
    if not created:
        # If the plant is already in the cart, increase the quantity
        cart_item.quantity += 1
        cart_item.save()
    
    # Optionally add a success message
    messages.success(request, f'Added {plant.name} to your cart!')
    
    return redirect('cart_view')
# View for removing a plant from the cart
@login_required
def remove_from_cart(request, cart_item_id):
    cart_item = get_object_or_404(CartItem, id=cart_item_id, cart__user=request.user)
    cart_item.delete()
    
    messages.success(request, 'Item removed from your cart.')
    return redirect('cart_view')  # Redirect to the cart view


# View for updating the quantity of a cart item
@login_required
def update_quantity(request, cart_item_id):
    cart_item = get_object_or_404(CartItem, id=cart_item_id, cart__user=request.user)
    
    if request.method == 'POST':
        new_quantity = int(request.POST.get('quantity', 1))
        
        if new_quantity > 0:
            cart_item.quantity = new_quantity
            cart_item.save()
            messages.success(request, f'Quantity of {cart_item.plant.name} updated to {new_quantity}.')
        else:
            messages.error(request, 'Quantity must be greater than zero.')
    
    return redirect('cart_view')



def checkout_view(request):
    # Get the user's cart
    cart = Cart.objects.filter(user=request.user).first()

    if not cart:
        return redirect('plant_list')  # Redirect to plants list if cart is empty

    cart_items = cart.items.all()
    total_price = cart.total_price()

    # Render the checkout page
    return render(request, 'checkout.html', {
        'cart_items': cart_items,
        'total_price': total_price
    })



from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Cart, CartItem, Order

@login_required
def checkout(request):
    # Retrieve the user's cart
    cart = Cart.objects.filter(user=request.user, items__isnull=False).first()
    if not cart:
        return HttpResponse("Your cart is empty.", status=400)
    
    cart_items = cart.items.all()
    total_price = cart.total_price()

    # Handle form submission
    if request.method == 'POST':
        name = request.POST.get('name')
        address = request.POST.get('address')
        phone = request.POST.get('phone')
        email = request.POST.get('email')

        # Create an order from the cart
        order = Order.objects.create(
            user=request.user,
            cart=cart,
            total_price=total_price,
        )

        # Optionally, you could save user details into the order as well
        order.name = name
        order.address = address
        order.phone = phone
        order.email = email
        order.save()

        # After creating the order, redirect to a success page or confirmation page
        return redirect('order_confirmation', order_id=order.id) # Redirect to an order confirmation page

    return render(request, 'checkout.html', {
        'cart_items': cart_items,
        'total_price': total_price,
    })


from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Order
from django.contrib import messages

@login_required
def payment_view(request, order_id):
    try:
        order = Order.objects.get(id=order_id, user=request.user)
    except Order.DoesNotExist:
        messages.error(request, 'Order not found.')
        return redirect('home')

    # Simulate payment processing
    if request.method == 'POST':
        # Simulate a successful payment (you can integrate actual payment gateways here)
        messages.success(request, 'Your payment was successful!')
        return redirect('order_confirmation', order_id=order.id)

    return render(request, 'payment.html', {
        'order': order,
        'total_price': order.total_price,
    })

from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Order

@login_required
def order_confirmation(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, 'order_confirmation.html', {
        'order': order
    })





from django.shortcuts import render, redirect, get_object_or_404
from django.http import Http404
from .models import Order

# View to display the order details and allow cancellation
def order_details(request, order_id):
    # Get the order
    order = get_object_or_404(Order, id=order_id)

    # Check if the order belongs to the logged-in user
    if order.user != request.user:
        raise Http404("You do not have permission to view this order.")

    return render(request, 'order_details.html', {'order': order})

# View to handle the order cancellation
def cancel_order(request, order_id):
    # Get the order
    order = get_object_or_404(Order, id=order_id)

    # Check if the order belongs to the logged-in user
    if order.user != request.user:
        raise Http404("You do not have permission to cancel this order.")

    # If the order is cancellable (e.g., not shipped yet), cancel it
    if order.status not in ['shipped', 'delivered']:  # Adjust status check as per your logic
        order.status = 'cancelled'
        order.save()

        # Redirect to order confirmation or another page
        return redirect('order_cancellation_confirmation')  # Redirect to a confirmation page

    else:
        # If the order is already shipped or delivered, inform the user
        return redirect('order_not_cancellable') 
    

from django.shortcuts import render
from .models import Order

def orders_list(request):
    # Prefetch related OrderItems and their associated Plants
    orders = Order.objects.prefetch_related('items__plant').filter(user=request.user)
    return render(request, 'orders_list.html', {'orders': orders})



from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.contrib import messages
from .models import Order
from .models import Order, OrderItem
@login_required

def cancel_order(request, order_id):
    # Fetch the order based on the provided order ID and ensure it belongs to the logged-in user
    order = get_object_or_404(Order, id=order_id, user=request.user)
    
    # If necessary, mark each OrderItem as canceled
    order_items = OrderItem.objects.filter(order=order)
    
    for item in order_items:
        # Example: You can update a field in OrderItem like 'canceled' if you want to track each item.
        # If you want to delete them, you could use item.delete().
        item.delete()  # Delete each order item as part of the cancellation (or update if needed)
    
    # Optionally, you can also delete the order itself if required
    order.delete()
    
    messages.success(request, "Your order has been successfully canceled.")
    return redirect('orders_list') 






def product_list(request):
    plants = Plant.objects.all()  # Fetch all plants
    return render(request, 'product_list2.html', {'plants': plants})
