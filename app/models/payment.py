from datetime import date


class Payment:
    def __init__(self, payment_id, amount_paid, date_paid, course):
        self.student= None
        self.payment_id=payment_id
        self._amount_paid=amount_paid
        self.date_paid=date_paid
        self.course= course
        
    @property
    def amount_paid(self):
        return self._amount_paid
    
    @amount_paid.setter
    def amount_paid(self, value):
        if value < 0:
            raise ValueError("amount paid can't be negative")
        elif not isinstance(value, int):
            raise TypeError('payment should be an int')
        self._amount_paid = value