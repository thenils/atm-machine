from apps.atm.models import ATM, ATMTransaction

import collections


class Transaction:
    def __init__(self, notes: dict, balance: float):

        self.balance = balance
        self.remain_notes = {}
        self.counted_amount = 0
        self.withdraw_amount = 0

        def get_prefix_dict(my_dict: dict):
            sorted_dict = {int(k): v for k, v in my_dict.items()}
            return collections.OrderedDict(reversed(list(sorted_dict.items())))

        self.notes = get_prefix_dict(notes)

    def withdraw(self, amount, balance):
        self.withdraw_amount = amount
        if amount > self.balance:
            return False, {}, 'Not Enough Amount in atm'
        if amount > balance:
            return False, {}, 'Not enough balance in your account'
        data = {}
        for item in self.notes.items():

            n = int(item[0])
            n_count = int(item[1])
            if amount >= n:
                notes = int(amount / n)
                if notes <= n_count:
                    self.counted_amount = notes * n
                    data.update({f'{n}': notes})
                else:
                    self.counted_amount = n_count * n
                    data.update({f'{n}': n_count})
                amount = amount - self.counted_amount

                if self.withdraw_amount == self.counted_amount:
                    break

        if amount != 0:
            return False, {}, 'this amount is note possible please re insert card and retry'

        return True, data, 'success'
