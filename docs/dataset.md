# Dataset
Датасет взят из [IBM Transactions for Anti Money Laundering (AML)](https://www.kaggle.com/datasets/ealtman2019/ibm-transactions-for-anti-money-laundering-aml/data) 

## Структура
| Поле           | Тип      | Описание               |
| -------------- | -------- | ---------------------- |
| Timestamp | datetime   | Время совершения операции |
| From Bank      | int64 | Банк отправителя         |
| Account      | string   | Отправитель            |
| To Bank    | int64   | Банк получателя             |
| Account.1         | string    | Получатель                  |
| Amount Received  | float64      | Полученная сумма     |
| Receiving Currency  | object      | Валюта получателя     |
| Amount Paid  | float64      | Сумма перевода     |
| Payment Currency  | object      | Валюта перевода     |
| Payment Format  | object      | Способ проведения транзакции     |
| Is Laundering  | bool      | Целевая переменная     |
