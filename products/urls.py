from django.urls import path, include
from rest_framework import routers
from rest_framework_nested import routers as nested_routers
from products.views import ProductViewSet, ReviewViewSet, FavoriteProductViewSet, CartViewSet, TagList, ProductImageViewSet, CartItemViewSet

# Main router
router = routers.DefaultRouter()
router.register('products', ProductViewSet)
router.register('cart', CartViewSet)
router.register('favorite_products', FavoriteProductViewSet)
router.register('tags', TagList)
router.register('cart_items', CartItemViewSet, basename='cart-items')

# Nested routers
products_router = nested_routers.NestedDefaultRouter(
    router,
    'products',
    lookup='product'
)
products_router.register('images', ProductImageViewSet, basename='product-images')
products_router.register('reviews', ReviewViewSet, basename='reviews')

urlpatterns = [
    path("", include(router.urls)),
    path("", include(products_router.urls)),
]