from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.db.models import Sum

from .models import Expense, MonthlyBudget


# =============================
# LOGIN
# =============================
def signin(request):

    if request.method == "POST":

        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:
            login(request, user)
            return redirect("home")

        return render(request, "signin.html", {
            "error": "Invalid username or password"
        })

    return render(request, "signin.html")


# =============================
# SIGNUP
# =============================
def signup(request):

    if request.method == "POST":

        username = request.POST.get("username")
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")

        if password != confirm_password:
            return render(request, "signup.html", {
                "error": "Passwords do not match"
            })

        if User.objects.filter(username=username).exists():
            return render(request, "signup.html", {
                "error": "Username already exists"
            })

        User.objects.create_user(
            username=username,
            password=password
        )

        return redirect("login")

    return render(request, "signup.html")


# =============================
# DELETE EXPENSE
# =============================
@login_required(login_url="/login/")
def delete_expense(request, expense_id):

    expense = get_object_or_404(
        Expense,
        id=expense_id
    )

    expense.delete()

    return redirect("home")


# =============================
# EDIT EXPENSE
# =============================
@login_required(login_url="/login/")
def edit_expense(request, expense_id):

    expense = get_object_or_404(
        Expense,
        id=expense_id
    )

    if request.method == "POST":

        expense.title = request.POST.get("title")
        expense.amount = request.POST.get("amount")
        expense.category = request.POST.get("category")
        expense.date = request.POST.get("date")
        expense.description = request.POST.get("description")

        expense.save()

        return redirect("home")

    return render(request, "edit_expense.html", {
        "expense": expense
    })


# =============================
# HOME
# =============================
@login_required(login_url="/login/")
def home(request):

    today = timezone.now().date()

    # =============================
    # SET MONTHLY BUDGET
    # =============================
    if (
        request.method == "POST"
        and request.POST.get("budget_form") == "1"
    ):

        budget_amount = request.POST.get("budget_amount")

        if budget_amount:

            MonthlyBudget.objects.update_or_create(
                month=today.replace(day=1),
                defaults={
                    "amount": budget_amount
                }
            )

        return redirect("home")

    # =============================
    # ADD EXPENSE
    # =============================
    if request.method == "POST":

        title = request.POST.get("title")
        amount = request.POST.get("amount")
        category = request.POST.get("category")
        date = request.POST.get("date")
        description = request.POST.get("description")

        if title and amount and category and date:

            Expense.objects.create(
                title=title,
                amount=amount,
                category=category,
                date=date,
                description=description
            )

        return redirect("home")

    # =============================
    # ALL EXPENSES
    # =============================
    expenses = Expense.objects.all().order_by(
        "-date",
        "-id"
    )

    # =============================
    # CURRENT MONTH BUDGET
    # =============================
    monthly_budget = MonthlyBudget.objects.filter(
        month__year=today.year,
        month__month=today.month
    ).first()

    # =============================
    # CURRENT MONTH SPENT
    # =============================
    monthly_spent = Expense.objects.filter(
        date__year=today.year,
        date__month=today.month
    ).aggregate(
        total=Sum("amount")
    )["total"] or 0

    # =============================
    # TOTAL EXPENSE
    # =============================
    total_expense = Expense.objects.aggregate(
        total=Sum("amount")
    )["total"] or 0

    # =============================
    # MONTHLY BALANCE
    # =============================
    if monthly_budget:

        monthly_balance = (
            monthly_budget.amount - monthly_spent
        )

    else:

        monthly_balance = 0

    # =============================
    # EXPENSE COUNT
    # =============================
    expense_count = expenses.count()

    # =============================
    # LATEST EXPENSE
    # =============================
    latest_expense = expenses.first()

    # =============================
    # SEND DATA TO HTML
    # =============================
    context = {

        "expenses": expenses,

        "total_expense": total_expense,

        "expense_count": expense_count,

        "latest_expense": latest_expense,

        "monthly_budget": monthly_budget,

        "monthly_spent": monthly_spent,

        "monthly_balance": monthly_balance,

        "today": today,
    }

    return render(
        request,
        "home.html",
        context
    )