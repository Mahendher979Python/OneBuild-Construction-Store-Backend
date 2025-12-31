from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.utils.crypto import get_random_string

from django.conf import settings
from .models import (
    Order,
    PasswordOTP,
    Seller,
    LabourContract,
)

User = settings.AUTH_USER_MODEL


# ======================================================
# ORDER : AUTO ORDER ID GENERATION
# ======================================================
@receiver(pre_save, sender=Order)
def generate_order_id(sender, instance, **kwargs):
    """
    Auto-generate order_id if not present
    Example: OBX8F3K9Q2
    """
    if not instance.order_id:
        instance.order_id = "OB" + get_random_string(8).upper()


# ======================================================
# ORDER : DEFAULT STATUS SAFETY
# ======================================================
@receiver(post_save, sender=Order)
def set_default_order_status(sender, instance, created, **kwargs):
    if created and not instance.status:
        instance.status = "Pending"
        instance.save(update_fields=["status"])


# ======================================================
# PASSWORD OTP : AUTO EXPIRE (LOGICAL FLAG)
# ======================================================
@receiver(post_save, sender=PasswordOTP)
def mark_old_otps_used(sender, instance, created, **kwargs):
    """
    When new OTP is created, mark previous OTPs as used
    """
    if created:
        PasswordOTP.objects.filter(
            user=instance.user,
            is_used=False
        ).exclude(id=instance.id).update(is_used=True)


# ======================================================
# SELLER : BASIC VALIDATION SIGNAL
# ======================================================
@receiver(post_save, sender=Seller)
def seller_post_create(sender, instance, created, **kwargs):
    """
    Placeholder for future:
    - email notification
    - admin approval workflow
    """
    if created:
        # future logic (email / notification)
        pass


# ======================================================
# LABOUR CONTRACT : LOCK ON CREATE
# ======================================================
@receiver(post_save, sender=LabourContract)
def lock_labour_contract(sender, instance, created, **kwargs):
    if created and instance.is_locked is False:
        instance.is_locked = True
        instance.save(update_fields=["is_locked"])

