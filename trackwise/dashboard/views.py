from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from accounts.models import UserProfile, Company
from inventory.models import Product
from django.utils import timezone
from datetime import timedelta

@login_required
def dashboard_view(request):
    # Ensure user has a profile
    try:
        profile = request.user.userprofile
    except UserProfile.DoesNotExist:
        # Create a default profile if it doesn't exist
        company = Company.objects.first()
        if not company:
            company = Company.objects.create(name="Default Company")
        profile = UserProfile.objects.create(user=request.user, role='staff', company=company)
    
    # Calculate dashboard statistics
    if profile.role == 'business_owner':
        # Get products for this company
        products = Product.objects.filter(company=profile.company)
        
        # Calculate statistics
        total_products = products.count()
        low_stock = products.filter(quantity__gt=0, quantity__lte=10).count()  # 10 or less is low stock
        out_of_stock = products.filter(quantity=0).count()
        
        # Get total staff count (users in the same company with staff role)
        total_staff = UserProfile.objects.filter(company=profile.company, role='staff').count()
        
        # Get recent products (last 5 added)
        recent_products = products.order_by('-created_at')[:5]
        
        # Calculate total inventory value
        total_inventory_value = sum(product.total_value for product in products)
        
        # Get recently updated products for activity feed
        recent_activity = products.order_by('-updated_at')[:10]
        
        context = {
            'profile': profile,
            'total_products': total_products,
            'low_stock': low_stock,
            'out_of_stock': out_of_stock,
            'total_staff': total_staff,
            'recent_products': recent_products,
            'recent_activity': recent_activity,
            'total_inventory_value': total_inventory_value,
        }
        template = 'dashboard/business_owner_dashboard.html'
    else:
        # Staff dashboard - calculate similar statistics but for staff view
        products = Product.objects.filter(company=profile.company)
        
        # Calculate statistics for staff
        total_products = products.count()
        low_stock = products.filter(quantity__gt=0, quantity__lte=10).count()
        out_of_stock = products.filter(quantity=0).count()
        
        # Get recent products (last 5 added)
        recent_products = products.order_by('-created_at')[:5]
        
        # Get recently updated products for activity feed
        recent_activity = products.order_by('-updated_at')[:10]
        
        # Count today's updates (products updated today)
        today = timezone.now().date()
        recent_updates = products.filter(updated_at__date=today).count()
        
        context = {
            'profile': profile,
            'total_products': total_products,
            'low_stock': low_stock,
            'out_of_stock': out_of_stock,
            'recent_updates': recent_updates,
            'recent_products': recent_products,
            'recent_activity': recent_activity,
        }
        template = 'dashboard/staff_dashboard.html'
    
    return render(request, template, context)