import pandas as pd
import csv
from datetime import datetime 
from data_entry import get_date, get_amount, get_category, get_description

class CSV:
    CSV_FILE = 'finance_data.csv'
    COLUMNS = ['date', 'amount', 'category', 'description']
    DATE_FORMAT = '%d-%m-%Y'

    @classmethod
    def initialize_csv(self):
        try:
            pd.read_csv(self.CSV_FILE)
        except FileNotFoundError:
            df = pd.DataFrame(columns=self.COLUMNS)
            df.to_csv(self.CSV_FILE, index=False)

    @classmethod
    def add_entry(self, date, amount, category, description):
        new_entry = {
            'date': date,
            'amount': amount,
            'category': category,
            'description': description
        }

        with open(self.CSV_FILE, 'a', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=self.COLUMNS)
            writer.writerow(new_entry)
        print('Entry added successfully!')

    @classmethod
    def get_transaction(self, start_date, end_date):
        df = pd.read_csv(self.CSV_FILE)
        df['date'] = pd.to_datetime(df['date'], format=self.DATE_FORMAT)
        start_date = datetime.strptime(start_date, self.DATE_FORMAT)
        end_date = datetime.strptime(end_date, self.DATE_FORMAT)

        mask = (df['date'] >= start_date) & (df['date'] <= end_date)
        filtered_df = df.loc[mask]

        if filtered_df.empty:
            print('No transaction found in the given date range')
        else:
            print(f'Transactions from {start_date.strftime(self.DATE_FORMAT)} to {end_date.strftime(self.DATE_FORMAT)}')
            print(filtered_df.to_string(index=False, formatters={'date': lambda x: x.strftime(self.DATE_FORMAT)}))

            total_income = filtered_df[filtered_df['category'] == 'Income']['amount'].sum()
            total_expense = filtered_df[filtered_df['category'] == 'Expense']['amount'].sum()
            print('\n')
            print('Summary')
            print(f'Total income: €{total_income:.2f}')
            print(f'Total expense: €{total_expense:.2f}')
            print(f'Remaining balance: €{(total_income - total_expense):.2f}')
        return filtered_df 

def add():
    CSV.initialize_csv()
    date = get_date('Enter the transaction date (dd-mm-yyyy) or press enter for today\'s date: ', allow_default=True)
    amount = get_amount()
    category = get_category()
    description = get_description()

    CSV.add_entry(date, amount, category, description)

def main():
    while True:
        print('1. Add transaction')
        print('2. View transaction summary within a date range')
        print('3. Exit')
        print('\n')
        choice = input('Choose number 1, 2, or 3: ')

        if choice == '1':
            add()
        elif choice == '2':
            start_date = get_date('Enter the start date (dd-mm-yyyy): ')
            end_date = get_date('Enter the end date (dd-mm-yyyy): ')
            CSV.get_transaction(start_date, end_date)
        elif choice == '3':
            print('Exiting!')
            break

if __name__ == '__main__':
    main()