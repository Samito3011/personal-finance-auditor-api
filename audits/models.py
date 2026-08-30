from django.db import models
from django.contrib.auth.models import User


class Transaction(models.Model):
    CATEGORY_CHOICES = [
        ("income", "Income"),
        ("food", "Food"),
        ("transport", "Transport"),
        ("housing", "Housing"),
        ("utilities", "Utilities"),
        ("shopping", "Shopping"),
        ("health", "Health"),
        ("education", "Education"),
        ("entertainment", "Entertainment"),
        ("other", "Other"),
    ]

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="transactions"
    )

    transaction_type = models.CharField(
        max_length=10,
        choices=[("income", "Income"), ("expense", "Expense")]
    )

    amount = models.DecimalField(
        max_digits=12,
        decimal_places=2
    )

    category = models.CharField(
        max_length=20,
        choices=CATEGORY_CHOICES
    )

    description = models.CharField(
        max_length=255,
        blank=True
    )

    transaction_date = models.DateField()

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):
        return f"{self.transaction_type} - {self.amount} - {self.category}"