from IPython.display import display
import pandas as pd

db_data = [
  {
    "amount": 100,
    "customer_id": 1,
    "employee_id": 2,
    "order_create_date": "2024-01-23T14:54:25.425569",
    "order_id": 1
  }
]

df = pd.DataFrame(db_data)

# displaying the DataFrame
display(df)