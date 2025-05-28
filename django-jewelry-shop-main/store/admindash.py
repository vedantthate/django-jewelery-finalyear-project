from django.db.models import Count, Sum
from django.contrib.admin.views.decorators import staff_member_required
from django.db.models.functions import TruncMonth
from django.utils.timezone import now
import calendar
from django.contrib.auth.models import User
from store.models import Category, Order, OrderItem, Product, Wishlist
from django.shortcuts import render
from .utils import *
from datetime import datetime

@staff_member_required
def admin_dash_board(request):
    today = now().date()
    start_of_month = today.replace(day=1)

    # Get filter inputs
    time_range = request.GET.get('time_range')
    month = request.GET.get('month')
    year = request.GET.get('year')
    from_date = request.GET.get('from_date')
    to_date = request.GET.get('to_date')

    orders = Order.objects.all()

    # Date range filtering
    if from_date and to_date:
        try:
            from_date_obj = datetime.strptime(from_date, "%Y-%m-%d").date()
            to_date_obj = datetime.strptime(to_date, "%Y-%m-%d").date()
            orders = orders.filter(ordered_date__range=(from_date_obj, to_date_obj))
        except ValueError:
            pass  # Ignore invalid dates

    # Month and year filtering
    elif month and year:
        orders = orders.filter(ordered_date__month=month, ordered_date__year=year)

    # Predefined time range filtering
    elif time_range:
        if time_range == "this_month":
            orders = orders.filter(ordered_date__year=today.year, ordered_date__month=today.month)
        elif time_range == "last_month":
            last_month = today.replace(day=1) - timedelta(days=1)
            orders = orders.filter(ordered_date__year=last_month.year, ordered_date__month=last_month.month)
        elif time_range == "last_3_months":
            three_months_ago = today - timedelta(days=90)
            orders = orders.filter(ordered_date__gte=three_months_ago)
        elif time_range == "last_6_months":
            six_months_ago = today - timedelta(days=180)
            orders = orders.filter(ordered_date__gte=six_months_ago)
        elif time_range == "this_year":
            orders = orders.filter(ordered_date__year=today.year)

    # Aggregations
    total_users = User.objects.count()
    total_orders = orders.count()
    product_count = Product.objects.count()
    category_count = Category.objects.count()
    wishlist_count = Wishlist.objects.count()

    total_revenue_cod = orders.filter(status='Delivered', payment_method='COD').aggregate(Sum('amount'))['amount__sum'] or 0
    total_cod_orders = orders.filter(payment_method='COD').count()
    total_online_orders = orders.filter(payment_method='Online').count()
    total_revenue_online = orders.filter(payment_method='Online').aggregate(Sum('amount'))['amount__sum'] or 0
    total_revenue = total_revenue_cod + total_revenue_online

    order_status_counts = orders.values('status').annotate(count=Count('status'))
    status_data = {status['status']: status['count'] for status in order_status_counts}

    top_product_items = OrderItem.objects.filter(order__in=orders)
    top_products = (
        top_product_items
        .values('product__title')
        .annotate(total=Count('id'))
        .order_by('-total')[:10]
    )
    top_products_data = {item['product__title']: item['total'] for item in top_products}

    year_range = list(range(2022, datetime.now().year + 1))
    month_names = list(calendar.month_name)[1:]  # January to December
    
    
    # --- Monthly Revenue Calculation ---
    current_year = today.year
    monthly_sales = [0] * 12  # Default 0 for each month

    monthly_data = (
        Order.objects
        .filter(ordered_date__year=current_year, status='Delivered')
        .annotate(month=TruncMonth('ordered_date'))
        .values('month')
        .annotate(monthly_revenue=Sum('amount'))
        .order_by('month')
    )

    for entry in monthly_data:
        month_index = entry['month'].month - 1  # Jan = 0, Dec = 11
        monthly_sales[month_index] = float(entry['monthly_revenue'])
    
    revenue_breakdown = {
        'COD': total_revenue_cod,
        'Online': total_revenue_online,
    }
    chart_data = {
        'labels': month_names,
        'monthly_sales': monthly_sales
    }
    

    context = {
        'total_users': total_users,
        'total_orders': total_orders,
        'total_revenue': total_revenue,
        'product_count': product_count,
        'category_count': category_count,
        'wishlist_count': wishlist_count,
        'total_revenue_cod': total_revenue_cod,
        'total_cod_orders': total_cod_orders,
        'total_revenue_online': total_revenue_online,
        'total_online_orders': total_online_orders,
        'status_data': status_data,
        'top_products_data': top_products_data,
        'revenue_breakdown': revenue_breakdown,
        'chart_data': chart_data,
        'year_range': year_range,
        'month_names': month_names,
    }

    return render(request, 'admin/admin_dashboard.html', context)