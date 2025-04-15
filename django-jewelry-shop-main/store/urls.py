from store.forms import LoginForm, PasswordChangeForm, PasswordResetForm, SetPasswordForm
from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from .views import admin_dashboard

app_name = 'store'


urlpatterns = [
    path('', views.home, name="home"),
    # URL for Cart and Checkout
    path('add-to-cart/', views.add_to_cart, name="add-to-cart"),
    path('remove-cart/<int:cart_id>/', views.remove_cart, name="remove-cart"),
    path('plus-cart/<int:cart_id>/', views.plus_cart, name="plus-cart"),
    path('minus-cart/<int:cart_id>/', views.minus_cart, name="minus-cart"),
    path('cart/', views.cart, name="cart"),
    path('checkout/', views.checkout, name="checkout"),
    path('orders/', views.orders, name="orders"),
    path('cancel-order/<int:order_id>/', views.cancel_order, name='cancel_order'),
    path('success/',views.payment_success,name='success'),
    path('generate-payment/', views.generate_payment, name='generate-payment'),
    path('wishlist/', views.wishlist_view, name='wishlist'), 
    path('add-to-wishlist/<int:product_id>/', views.add_to_wishlist, name='add-to-wishlist'),
    path('orders/track/', views.track_order, name='track_order'),
    path('order/track/<str:tracking_uid>/', views.track_order_direct, name='track_order_direct'),
    path('search/', views.search_products, name='search'),

    
    
    path('contact/',views.contact,name='contact'),
    path('blog/', views.blog_list, name='blog_list'),
    path('return_refund/',views.services, name='return_refund'),
    path('online_store/',views.stores, name='online_store'),
    path('terms_conditions/',views.terms_conditions,name='terms_conditons'),
    path('what_we_do/',views.what_we_do, name='what_we_do'),
    path('services/',views.service, name='services'),
    path('faqs/',views.faqs,name='faqs'),
    
    path('blog/<slug:slug>/', views.blog_detail, name='blog_detail'),
     

    #URL for Products
    path('product/<slug:slug>/', views.detail, name="product-detail"),
    path('categories/', views.all_categories, name="all-categories"),
    path('<slug:slug>/', views.category_products, name="category-products"),

    path('shop/', views.shop, name="shop"),
   

    # URL for Authentication
    path('accounts/register/', views.RegistrationView.as_view(), name="register"),
    path('accounts/login/', auth_views.LoginView.as_view(template_name='account/login.html', authentication_form=LoginForm), name="login"),
    path('accounts/profile/', views.profile, name="profile"),
    path('accounts/add-address/', views.AddressView.as_view(), name="add-address"),
    path('accounts/remove-address/<int:id>/', views.remove_address, name="remove-address"),
    path('accounts/logout/', auth_views.LogoutView.as_view(next_page='store:login'), name="logout"),
    path('accounts/otpverification', views.otp_verification, name='otpverification'),
    path('accounts/resend-otp',views.resend_otp, name="resend_otp"),


    
    path('accounts/password-change/', auth_views.PasswordChangeView.as_view(template_name='account/password_change.html', form_class=PasswordChangeForm, success_url='/accounts/password-change-done/'), name="password-change"),
    path('accounts/password-change-done/', auth_views.PasswordChangeDoneView.as_view(template_name='account/password_change_done.html'), name="password-change-done"),

    path('accounts/password-reset/', auth_views.PasswordResetView.as_view(template_name='account/password_reset.html', form_class=PasswordResetForm, success_url='/accounts/password-reset/done/'), name="password-reset"), # Passing Success URL to Override default URL, also created password_reset_email.html due to error from our app_name in URL
    path('accounts/password-reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='account/password_reset_done.html'), name="password_reset_done"),
    path('accounts/password-reset-confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='account/password_reset_confirm.html', form_class=SetPasswordForm, success_url='/accounts/password-reset-complete/'), name="password_reset_confirm"), # Passing Success URL to Override default URL
    path('accounts/password-reset-complete/', auth_views.PasswordResetCompleteView.as_view(template_name='account/password_reset_complete.html'), name="password_reset_complete"),

    path('product/test/', views.test, name="test"),
    path('dashboard/admin/', admin_dashboard, name='admin-dashboard'),
    
]
