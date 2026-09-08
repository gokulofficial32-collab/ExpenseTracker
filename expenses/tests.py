{% load static %}

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Edit Expense</title>

    <link rel="stylesheet"
          href="{% static 'css/style.css' %}">
</head>

<body>

<div class="container">

    <div class="form-box">

        <div class="section-title">
            <div>
                <p class="small-title">EDIT TRANSACTION</p>
                <h2>Edit Expense</h2>
            </div>
        </div>

        <form method="POST">

            {% csrf_token %}

            <div class="form-group">
                <label>Expense Name</label>
                <input
                    type="text"
                    name="title"
                    value="{{ expense.title }}"
                    required>
            </div>

            <div class="form-group">
                <label>Amount</label>
                <input
                    type="number"
                    name="amount"
                    value="{{ expense.amount }}"
                    step="0.01"
                    required>
            </div>

            <div class="form-group">
                <label>Category</label>
                <input
                    type="text"
                    name="category"
                    value="{{ expense.category }}"
                    required>
            </div>

            <div class="form-group">
                <label>Date</label>
                <input
                    type="date"
                    name="date"
                    value="{{ expense.date|date:'Y-m-d' }}"
                    required>
            </div>

            <div class="form-group">
                <label>Description</label>
                <textarea name="description">{{ expense.description }}</textarea>
            </div>

            <button type="submit">
                Update Expense
            </button>

        </form>

        <br>

        <a href="{% url 'home' %}">
            ← Back to Home
        </a>

    </div>

</div>

</body>
</html>