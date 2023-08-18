

# Створити порожній словник transactions.
# 2 Заповніть словник transactions даними про кілька транзакцій. Для кожної транзакції мають бути зазначені такі дані:
#     "id": унікальний ідентифікатор транзакції
#     "date": дата та час, коли була зроблена транзакція (використовуйте формат дати YYYY-MM-DD HH:MM:SS)
#     "amount": сума транзакції
#     "status": поточний статус транзакції (може бути "pending", "completed" або "failed")
#     "customer": словник з інформацією про платника, що містить такі ключі:
#         "name": рядок з ім'ям платника
#         "email": рядок з електронною поштою платника
#         "phone": рядок із номером телефону платника      
# Усі дані про транзакції повинні бути збережені у словнику трансакцій з відповідними ключами.
# 3 На екрані виведіть значення всіх ключів словника transactions.
# 4 Змініть значення ключа "status" для однієї з транзакцій у словнику transactions.
# 5 Видаліть інформацію про одну з транзакцій із словника transactions.
# 6 Використовуючи цикл for, виведіть на екран лише ідентифікатори всіх транзакцій із словника transactions.
# 7 Створіть словник customers, що містить інформацію про всіх платників, які здійснили транзакції у додатку. Кожен ключ у словнику customers має бути ім'ям платника, а кожне значення – списком ідентифікаторів транзакцій, які були здійснені цим платником.
# 8 Використовуючи цикл for, виведіть на екран список усіх платників та відповідні списки ідентифікаторів транзакцій, які були здійснені кожним платником, із словника customers.


transactions = {
    '1': {
        "id": "1",
        "date": "2023-08-18 15:30:00",
        "amount": 150.75,
        "status": "completed",
        "customer": {
            "name": "John Smith",
            "email": "john@example.com",
            "phone": "123-456-7890"
        }
    },
    '2': {
        "id": "2",
        "date": "2023-08-18 10:15:00",
        "amount": 50.20,
        "status": "failed",
        "customer": {
            "name": "Jane Doe",
            "email": "jane@example.com",
            "phone": "987-654-3210"
        }
    },
    '3': {
        "id": "3",
        "date": "2023-08-17 18:45:00",
        "amount": 200.00,
        "status": "pending",
        "customer": {
            "name": "John Smith",
            "email": "alice@example.com",
            "phone": "555-123-4567"
        }
    },
    '4': {
        "id": "4",
        "date": "2023-08-19 09:00:00",
        "amount": 75.50,
        "status": "completed",
        "customer": {
            "name": "Jane Doe",
            "email": "robert@example.com",
            "phone": "222-333-4444"
        }
    },
    '5': {
        "id": "5",
        "date": "2023-08-20 14:20:00",
        "amount": 300.25,
        "status": "completed",
        "customer": {
            "name": "John Smith",
            "email": "emily@example.com",
            "phone": "777-888-9999"
        }
    },
    '6': {
        "id": "6",
        "date": "2023-08-20 14:20:00",
        "amount": 300.25,
        "status": "completed",
        "customer": {
            "name": "John Smith",
            "email": "dasdasd@fasd.com",
            "phone": "777-888-9999"
        },
    }
}


# все пользователи
all_customers = {}

# all_customers = []
for transaction in transactions.values():
    if transaction['customer']['name'] not in all_customers:# если такого пользователя нет в списке
        all_customers[transaction['customer']['name']] = [] # добавляем его в список
    all_customers[transaction['customer']['name']].append(transaction['id']) # добавляем id транзакции в список пользователя
    
        
print(all_customers)