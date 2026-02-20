from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError
from django.utils import timezone
from decimal import Decimal


# ────────────────────────────────────────────────
#                Abstract Base Models
# ────────────────────────────────────────────────

class TimeStampedModel(models.Model):
    """
    Abstract base model that provides self-managed 'created_at' and 'updated_at' timestamps.
    Inherit from this model to automatically include creation and modification timestamps.
    """
    created_at = models.DateTimeField(
        auto_now_add=True,
        help_text="Date and time when this record was created"
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        help_text="Date and time when this record was last updated"
    )

    class Meta:
        abstract = True


# ────────────────────────────────────────────────
#                     Choices / Enums
# ────────────────────────────────────────────────

class Status(models.TextChoices):
    """Common status choices used across multiple models"""
    ACTIVE = 'active', _('Active')
    INACTIVE = 'inactive', _('Inactive')
    DELETED = 'deleted', _('Deleted')


class OrderStatus(models.TextChoices):
    """Detailed order lifecycle status choices"""
    PENDING = 'pending', _('Pending')
    PROCESSING = 'processing', _('Processing')
    SHIPPED = 'shipped', _('Shipped')
    DELIVERED = 'delivered', _('Delivered')
    CANCELLED = 'cancelled', _('Cancelled')
    RETURNED = 'returned', _('Returned')


# ────────────────────────────────────────────────
#                   Core Business Models
# ────────────────────────────────────────────────

class Shop(TimeStampedModel):
    """
    Represents a vendor/store in the multi-vendor marketplace.
    Each shop is managed by one or more Manager instances.
    """
    name = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(max_length=255, unique=True)
    description = models.TextField(blank=True, help_text="Detailed description of the shop")
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.ACTIVE,
        help_text="Current operational status of the shop"
    )

    class Meta:
        ordering = ['-created_at']
        verbose_name = _("Shop")
        verbose_name_plural = _("Shops")

    def __str__(self):
        return self.name


class Manager(models.Model):
    """
    Associates a Django User with a Shop as its manager/admin.
    One user can only manage one shop (OneToOneField with User).
    """
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='manager_profile',
        help_text="Linked Django user account"
    )
    shop = models.ForeignKey(
        Shop,
        on_delete=models.CASCADE,
        related_name='managers'
    )
    registration_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} (Manager: {self.shop.name})"


class Category(models.Model):
    """Product categorization / department"""
    name = models.CharField(max_length=100, unique=True)

    class Meta:
        verbose_name_plural = _("Categories")
        ordering = ['name']

    def __str__(self):
        return self.name


class Brand(models.Model):
    """Product brand/manufacturer"""
    name = models.CharField(max_length=100, unique=True)
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.ACTIVE
    )

    def __str__(self):
        return self.name


class Product(TimeStampedModel):
    """
    Core product entity belonging to one Shop.
    Contains basic catalog information, pricing and inventory.
    """
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE, related_name='products')
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='products'
    )
    brand = models.ForeignKey(
        Brand,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='products'
    )
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'))],
        help_text="Regular selling price"
    )
    stock = models.PositiveIntegerField(default=0, help_text="Current available quantity")
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.ACTIVE
    )

    class Meta:
        indexes = [
            models.Index(fields=['name', 'status'], name='product_name_status_idx'),
        ]
        ordering = ['-created_at']

    def __str__(self):
        return self.name


class ProductImage(models.Model):
    """Gallery images for each product"""
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='products/%Y/%m/%d/')
    is_feature = models.BooleanField(
        default=False,
        help_text="Mark as the main/featured product image"
    )
    alt_text = models.CharField(max_length=255, blank=True, help_text="SEO-friendly alt text")

    def __str__(self):
        return f"Image for {self.product.name}"


# ────────────────────────────────────────────────
#                    Order & Delivery
# ────────────────────────────────────────────────

class DeliveryInfo(TimeStampedModel):
    """
    Shipping/delivery tracking information.
    One-to-one relationship with ShopOrder.
    """
    tracking_number = models.CharField(max_length=50, unique=True, db_index=True)
    carrier = models.CharField(max_length=100)
    shipping_date = models.DateField(null=True, blank=True)
    delivery_date = models.DateField(null=True, blank=True)
    status = models.CharField(
        max_length=20,
        choices=OrderStatus.choices,
        default=OrderStatus.PENDING
    )

    def __str__(self):
        return self.tracking_number


class Order(TimeStampedModel):
    """
    Main customer order (can contain products from multiple shops).
    The "parent" order that groups all ShopOrder instances.
    """
    user = models.ForeignKey(User, on_delete=models.PROTECT, related_name='orders')
    total_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    status = models.CharField(
        max_length=20,
        choices=OrderStatus.choices,
        default=OrderStatus.PENDING
    )

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Order #{self.id} by {self.user.username}"


class ShopOrder(TimeStampedModel):
    """
    Sub-order / vendor-order slice of a main Order.
    Groups order items belonging to the same shop.
    Contains shop-specific delivery tracking and total.
    """
    main_order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='shop_orders')
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE, related_name='vendor_orders')
    delivery_info = models.OneToOneField(
        DeliveryInfo,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='shop_order'
    )
    status = models.CharField(
        max_length=20,
        choices=OrderStatus.choices,
        default=OrderStatus.PENDING
    )
    shop_total = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    def __str__(self):
        return f"Shop Order #{self.id} – {self.shop.name}"


class OrderDetail(models.Model):
    """
    Line item in an order.
    Connects a Product to both the main Order and the ShopOrder (for multi-vendor).
    """
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    shop_order = models.ForeignKey(
        ShopOrder,
        on_delete=models.CASCADE,
        related_name='items',
        null=True,
        blank=True
    )
    product = models.ForeignKey(Product, on_delete=models.PROTECT, related_name='order_items')
    quantity = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    price = models.DecimalField(max_digits=10, decimal_places=2)   # snapshot price at time of order

    def __str__(self):
        return f"{self.quantity} × {self.product.name}"


# ────────────────────────────────────────────────
#                   Discounts & Cart
# ────────────────────────────────────────────────

class Discount(models.Model):
    """
    Time-bound percentage discount.
    Can be applied to products, categories, or whole orders (logic in views/services).
    """
    name = models.CharField(max_length=100)
    discount_percentage = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        validators=[MinValueValidator(0), MaxValueValidator(100)]
    )
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()

    def clean(self):
        if self.start_date and self.end_date and self.start_date > self.end_date:
            raise ValidationError(_("Start date cannot be after end date."))

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} ({self.discount_percentage}%)"


class Cart(TimeStampedModel):
    """User's active shopping cart (one per user)"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='cart')

    def __str__(self):
        return f"Cart: {self.user.username}"


class CartItem(models.Model):
    """Individual product line in the shopping cart"""
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1, validators=[MinValueValidator(1)])

    class Meta:
        unique_together = ('cart', 'product')
        verbose_name = _("Cart Item")
        verbose_name_plural = _("Cart Items")


class Comment(TimeStampedModel):
    """
    Customer review/comment on a product.
    Requires moderation by shop manager before public display.
    """
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.TextField()
    moderated_by = models.ForeignKey(
        Manager,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='moderated_comments'
    )
    is_approved = models.BooleanField(default=False, help_text="Approved by shop manager")

    def __str__(self):
        return f"Comment by {self.user.username} on {self.product.name}"