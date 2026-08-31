from decimal import Decimal

from django.db.models import Sum, Count
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from drf_spectacular.utils import extend_schema, OpenApiResponse

from .models import Transaction
from .serializers import TransactionSerializer


class TransactionViewSet(viewsets.ModelViewSet):
    serializer_class = TransactionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = Transaction.objects.filter(
            user=self.request.user
        )

        transaction_type = self.request.query_params.get("transaction_type")
        category = self.request.query_params.get("category")

        if transaction_type:
            queryset = queryset.filter(
                transaction_type=transaction_type
            )

        if category:
            queryset = queryset.filter(
                category=category
            )

        return queryset

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class InsightsView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        responses={
            200: OpenApiResponse(
                description="Financial insights for the authenticated user."
            )
        }
    )
    def get(self, request):
        transactions = Transaction.objects.filter(
            user=request.user
        )

        total_income = (
            transactions
            .filter(transaction_type="income")
            .aggregate(total=Sum("amount"))["total"]
            or Decimal("0.00")
        )

        total_expenses = (
            transactions
            .filter(transaction_type="expense")
            .aggregate(total=Sum("amount"))["total"]
            or Decimal("0.00")
        )

        balance = total_income - total_expenses

        expense_categories = (
            transactions
            .filter(transaction_type="expense")
            .values("category")
            .annotate(total=Sum("amount"))
            .order_by("-total")
        )

        if expense_categories:
            highest_category = expense_categories[0]["category"]
            highest_category_amount = expense_categories[0]["total"]
        else:
            highest_category = None
            highest_category_amount = Decimal("0.00")

        return Response({
            "total_income": total_income,
            "total_expenses": total_expenses,
            "balance": balance,
            "total_transactions": transactions.count(),
            "highest_spending_category": highest_category,
            "highest_spending_amount": highest_category_amount,
            "financial_status": (
                "Positive"
                if balance > 0
                else "Negative"
                if balance < 0
                else "Balanced"
            ),
        })


class CategoryAnalysisView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        responses={
            200: OpenApiResponse(
                description="Spending analysis by category for the authenticated user."
            )
        }
    )
    def get(self, request):
        transactions = Transaction.objects.filter(
            user=request.user
        )

        expenses = (
            transactions
            .filter(transaction_type="expense")
            .values("category")
            .annotate(total=Sum("amount"))
            .order_by("-total")
        )

        total_expenses = (
            transactions
            .filter(transaction_type="expense")
            .aggregate(total=Sum("amount"))["total"]
            or Decimal("0.00")
        )

        results = {}

        for expense in expenses:
            category = expense["category"]
            amount = expense["total"]

            percentage = (
                (amount / total_expenses) * 100
                if total_expenses > 0
                else 0
            )

            if percentage >= 50:
                status = "High"
            elif percentage >= 25:
                status = "Moderate"
            else:
                status = "Low"

            results[category] = {
                "amount": amount,
                "percentage": round(percentage, 2),
                "status": status,
            }

        return Response({
            "total_expenses": total_expenses,
            "categories": results,
        })


class AuditAlertsView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        responses={
            200: OpenApiResponse(
                description="Audit alerts for the authenticated user's transactions."
            )
        }
    )
    def get(self, request):
        transactions = Transaction.objects.filter(
            user=request.user
        )

        expenses = (
            transactions
            .filter(transaction_type="expense")
            .values("category")
            .annotate(total=Sum("amount"))
            .order_by("-total")
        )

        total_expenses = (
            transactions
            .filter(transaction_type="expense")
            .aggregate(total=Sum("amount"))["total"]
            or Decimal("0.00")
        )

        alerts = []

        for expense in expenses:
            category = expense["category"]
            amount = expense["total"]

            percentage = (
                (amount / total_expenses) * 100
                if total_expenses > 0
                else 0
            )

            if percentage >= 50:
                alerts.append({
                    "category": category,
                    "amount": amount,
                    "percentage": round(percentage, 2),
                    "message": (
                        f"{category.title()} spending is significantly high."
                    ),
                })

        return Response({
            "total_expenses": total_expenses,
            "alerts": alerts,
        })


class LargeTransactionView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        responses={
            200: OpenApiResponse(
                description="Large expense transactions for the authenticated user."
            )
        }
    )
    def get(self, request):
        threshold = Decimal("100000.00")

        transactions = (
            Transaction.objects
            .filter(
                user=request.user,
                transaction_type="expense",
                amount__gte=threshold
            )
            .order_by("-amount")
        )

        results = []

        for transaction in transactions:
            results.append({
                "id": transaction.id,
                "amount": transaction.amount,
                "category": transaction.category,
                "description": transaction.description,
                "transaction_date": transaction.transaction_date,
                "severity": "High",
                "message": "Transaction exceeds the audit threshold.",
            })

        return Response({
            "threshold": threshold,
            "large_transactions": results,
        })


class UnusualTransactionView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        responses={
            200: OpenApiResponse(
                description="Unusual transactions based on the user's average expense."
            )
        }
    )
    def get(self, request):
        expenses = (
            Transaction.objects
            .filter(
                user=request.user,
                transaction_type="expense"
            )
            .order_by("-amount")
        )

        if not expenses.exists():
            return Response({
                "average_expense": Decimal("0.00"),
                "unusual_transactions": [],
                "total_unusual_transactions": 0,
            })

        total_expense_amount = (
            expenses.aggregate(total=Sum("amount"))["total"]
            or Decimal("0.00")
        )

        average_expense = (
            total_expense_amount / expenses.count()
        )

        unusual_transactions = []

        for transaction in expenses:
            if transaction.amount >= average_expense * 3:
                unusual_transactions.append({
                    "id": transaction.id,
                    "amount": transaction.amount,
                    "category": transaction.category,
                    "description": transaction.description,
                    "transaction_date": transaction.transaction_date,
                    "average_expense": round(average_expense, 2),
                    "severity": "High",
                    "message": (
                        "Transaction is significantly higher "
                        "than the average expense."
                    ),
                })

        return Response({
            "average_expense": round(average_expense, 2),
            "unusual_transactions": unusual_transactions,
            "total_unusual_transactions": len(unusual_transactions),
        })


class AuditSummaryView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        responses={
            200: OpenApiResponse(
                description="Overall audit summary and risk assessment for the authenticated user."
            )
        }
    )
    def get(self, request):
        transactions = Transaction.objects.filter(
            user=request.user
        )

        total_transactions = transactions.count()

        total_expenses = (
            transactions
            .filter(transaction_type="expense")
            .aggregate(total=Sum("amount"))["total"]
            or Decimal("0.00")
        )

        # Large transactions
        large_transaction_count = (
            transactions
            .filter(
                transaction_type="expense",
                amount__gte=Decimal("100000.00")
            )
            .count()
        )

        # Duplicate transactions
        duplicate_groups = (
            transactions
            .values(
                "transaction_type",
                "amount",
                "category",
                "description",
                "transaction_date",
            )
            .annotate(count=Count("id"))
            .filter(count__gt=1)
        )

        duplicate_group_count = duplicate_groups.count()

        # Unusual transactions
        expenses = transactions.filter(
            transaction_type="expense"
        )

        unusual_transaction_count = 0

        if expenses.exists():
            average_expense = (
                expenses.aggregate(total=Sum("amount"))["total"]
                / expenses.count()
            )

            unusual_transaction_count = expenses.filter(
                amount__gte=average_expense * 3
            ).count()

        # High spending categories
        high_category_count = 0

        if total_expenses > 0:
            categories = (
                transactions
                .filter(transaction_type="expense")
                .values("category")
                .annotate(total=Sum("amount"))
            )

            for category in categories:
                percentage = (
                    category["total"] / total_expenses
                ) * 100

                if percentage >= 50:
                    high_category_count += 1

        # Determine overall risk
        risk_indicators = (
            large_transaction_count
            + duplicate_group_count
            + unusual_transaction_count
            + high_category_count
        )

        if risk_indicators >= 3:
            overall_risk = "High"
        elif risk_indicators >= 1:
            overall_risk = "Moderate"
        else:
            overall_risk = "Low"

        return Response({
            "total_transactions": total_transactions,
            "total_expenses": total_expenses,
            "large_transactions": large_transaction_count,
            "duplicate_transaction_groups": duplicate_group_count,
            "unusual_transactions": unusual_transaction_count,
            "high_spending_categories": high_category_count,
            "overall_risk": overall_risk,
        })


class DuplicateTransactionView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        responses={
            200: OpenApiResponse(
                description="Potential duplicate transactions for the authenticated user."
            )
        }
    )
    def get(self, request):
        transactions = Transaction.objects.filter(
            user=request.user
        )

        duplicate_groups = (
            transactions
            .values(
                "transaction_type",
                "amount",
                "category",
                "description",
                "transaction_date",
            )
            .annotate(count=Count("id"))
            .filter(count__gt=1)
            .order_by("-count")
        )

        duplicates = []

        for group in duplicate_groups:
            matching_transactions = (
                transactions
                .filter(
                    transaction_type=group["transaction_type"],
                    amount=group["amount"],
                    category=group["category"],
                    description=group["description"],
                    transaction_date=group["transaction_date"],
                )
                .values(
                    "id",
                    "transaction_type",
                    "amount",
                    "category",
                    "description",
                    "transaction_date",
                )
            )

            duplicates.append({
                "transaction_type": group["transaction_type"],
                "amount": group["amount"],
                "category": group["category"],
                "description": group["description"],
                "transaction_date": group["transaction_date"],
                "count": group["count"],
                "transactions": list(matching_transactions),
                "severity": "High",
                "message": "Potential duplicate transaction detected.",
            })

        return Response({
            "duplicate_groups": duplicates,
            "total_duplicate_groups": len(duplicates),
        })