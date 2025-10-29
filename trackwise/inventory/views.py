from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.db.models import Q
from .models import Product
from .forms import ProductForm
from accounts.models import UserProfile

@login_required
def inventory_list(request):
    try:
        profile = request.user.userprofile
    except UserProfile.DoesNotExist:
        messages.error(request, 'User profile not found.')
        return redirect('dashboard')
    
    # Both business owners and staff can access inventory, but with different permissions
    products = Product.objects.filter(company=profile.company)
    
    # Search functionality
    search_query = request.GET.get('search', '')
    if search_query:
        products = products.filter(
            Q(item_name__icontains=search_query) |
            Q(category__icontains=search_query)
        )
    
    # Cost filter
    cost_filter = request.GET.get('cost_filter', '')
    if cost_filter == 'low':
        products = products.order_by('cost_price')
    elif cost_filter == 'high':
        products = products.order_by('-cost_price')
    
    # Calculate total inventory value
    total_inventory_value = sum(product.total_value for product in products)
    
    context = {
        'products': products,
        'search_query': search_query,
        'cost_filter': cost_filter,
        'profile': profile,
        'total_inventory_value': total_inventory_value
    }
    
    # Use different templates for owner vs staff
    if profile.role == 'business_owner':
        return render(request, 'inventory/inventory_list.html', context)
    else:
        return render(request, 'inventory/inventory_list_staff.html', context)

@login_required
def product_detail(request, pk):
    try:
        profile = request.user.userprofile
    except UserProfile.DoesNotExist:
        messages.error(request, 'User profile not found.')
        return redirect('dashboard')
    
    # Both owners and staff can view product details
    product = get_object_or_404(Product, pk=pk, company=profile.company)
    
    # Only business owners can edit products
    if request.method == 'POST':
        if profile.role != 'business_owner':
            messages.error(request, 'Access denied. Only business owners can edit products.')
            return redirect('inventory_list')
        
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, f'Product "{product.item_name}" updated successfully!')
            return redirect('inventory_list')
    else:
        form = ProductForm(instance=product)
    
    context = {
        'form': form,
        'product': product,
        'profile': profile
    }
    
    # Use different templates for owner vs staff
    if profile.role == 'business_owner':
        return render(request, 'inventory/product_detail.html', context)
    else:
        return render(request, 'inventory/product_detail_staff.html', context)

@login_required
def product_add(request):
    try:
        profile = request.user.userprofile
    except UserProfile.DoesNotExist:
        messages.error(request, 'User profile not found.')
        return redirect('dashboard')
    
    # Both owners and staff can add products
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            product.company = profile.company
            product.save()
            messages.success(request, f'Product "{product.item_name}" added successfully!')
            return redirect('inventory_list')
    else:
        form = ProductForm()
    
    context = {
        'form': form,
        'profile': profile
    }
    return render(request, 'inventory/product_add.html', context)

@login_required
def increase_stock(request, pk):
    if request.method == 'POST':
        try:
            profile = request.user.userprofile
            product = Product.objects.get(pk=pk, company=profile.company)
            product.quantity += 1
            product.save()
            return JsonResponse({
                'success': True,
                'new_quantity': product.quantity,
                'display_quantity': product.get_display_quantity(),
                'total_value': float(product.total_value)
            })
        except (Product.DoesNotExist, UserProfile.DoesNotExist):
            return JsonResponse({'success': False, 'error': 'Product not found'})
    return JsonResponse({'success': False, 'error': 'Invalid request'})

@login_required
def decrease_stock(request, pk):
    if request.method == 'POST':
        try:
            profile = request.user.userprofile
            product = Product.objects.get(pk=pk, company=profile.company)
            if product.quantity > 0:
                product.quantity -= 1
                product.save()
            return JsonResponse({
                'success': True,
                'new_quantity': product.quantity,
                'display_quantity': product.get_display_quantity(),
                'total_value': float(product.total_value)
            })
        except (Product.DoesNotExist, UserProfile.DoesNotExist):
            return JsonResponse({'success': False, 'error': 'Product not found'})
    return JsonResponse({'success': False, 'error': 'Invalid request'})

@login_required
def product_delete(request, pk):
    try:
        profile = request.user.userprofile
        product = Product.objects.get(pk=pk, company=profile.company)
        
        # Only business owners can delete products
        if profile.role != 'business_owner':
            messages.error(request, 'Access denied. Only business owners can delete products.')
            return redirect('inventory_list')
        
        if request.method == 'POST':
            product_name = product.item_name
            product.delete()
            messages.success(request, f'Product "{product_name}" deleted successfully!')
            return redirect('inventory_list')
    except (Product.DoesNotExist, UserProfile.DoesNotExist):
        messages.error(request, 'Product not found.')
        return redirect('inventory_list')
    
    context = {
        'product': product,
        'profile': profile
    }
    return render(request, 'inventory/product_delete.html', context)