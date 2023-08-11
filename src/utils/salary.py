import re

def convert_salary_to_int(salary: str) -> int:
    if not salary:
        return 0
    
    salary = salary.replace(' ', '')
    salary = salary.replace('\xa0', '')
    salary = salary.replace('\u202f', '')
    numbers = re.findall(r'\d+', salary)
    average_salary = sum(map(int, numbers)) // len(numbers)
    currency_symbol = salary[-1]
    currency_rates = {'₸': 0.0025, '₽': 0.014, '€': 1.17}
    if currency_symbol in currency_rates:
        average_salary *= currency_rates[currency_symbol]

    return average_salary