
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from .models import Expense, MonthlyBudget


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
@login_required(login_url="/login/")
def delete_expense(request, expense_id):
    expense = get_object_or_404(Expense, id=expense_id)
    expense.delete()
    return redirect("home")


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


@login_required(login_url="/login/")
def home(request):

    today = timezone.now().date()

    # -----------------------------
    # SET MONTHLY BUDGET
    # -----------------------------
    if request.method == "POST" and request.POST.get("budget_form") == "1":

        budget_amount = request.POST.get("budget_amount")

        if budget_amount:
            monthly_budget, created = MonthlyBudget.objects.update_or_create(
                month=today.replace(day=1),
                defaults={
                    "amount": budget_amount
                }
            )

        return redirect("home")


    # -----------------------------
    # ADD EXPENSE
    # -----------------------------
    if request.method == "POST":

        title = request.POST.get("title")
        amount = request.POST.get("amount")
        category = request.POST.get("category")
        date = request.POST.get("date")
        description = request.POST.get("description")

        Expense.objects.create(
            title=title,
            amount=amount,
            category=category,
            date=date,
            description=description
        )

        return redirect("home")


    # -----------------------------
    # GET EXPENSES
    # -----------------------------
    expenses = Expense.objects.all().order_by("-date")


    # -----------------------------
    # CURRENT MONTH BUDGET
    # -----------------------------
    monthly_budget = MonthlyBudget.objects.filter(
        month__year=today.year,
        month__month=today.month
    ).first()


    # -----------------------------
    # CURRENT MONTH EXPENSES
    # -----------------------------
    monthly_expenses = expenses.filter(
        date__year=today.year,
        date__month=today.month
    )


    # -----------------------------
    # TOTAL EXPENSE
    # -----------------------------
    total_expense = sum(
        expense.amount for expense in expenses
    )


    # -----------------------------
    # MONTHLY SPENT
    # -----------------------------
    monthly_spent = sum(
        expense.amount for expense in monthly_expenses
    )


    # -----------------------------
    # MONTHLY BALANCE
    # -----------------------------
    if monthly_budget:
        monthly_balance = monthly_budget.amount - monthly_spent
    else:
        monthly_balance = 0


    return render(request, "home.html", {
        "expenses": expenses,
        "total_expense": total_expense,
        "expense_count": expenses.count(),
        "latest_expense": expenses.first(),

        "monthly_budget": monthly_budget,
        "monthly_spent": monthly_spent,
        "monthly_balance": monthly_balance,

        "today": today,
    })
