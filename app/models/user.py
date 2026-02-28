from .payment import Payment

class User:
    def __init__(self, id, username, password, role):
        self.id=id
        self.username= username
        self.password= password
        self.role= role

class Student(User):
    def __init__(self,id, username, password, role):
        super().__init__(id, username, password, role)
        self.courses= []
        self.payments=[]
        
    def list_courses(self):
        return [course.course_name for course in self.courses]
    
    def list_payments(self, course):
        return sum(payment.amount_paid for payment in self.payments if payment.course == course)

    def check_balance(self):
        if not self.courses:
            return 0
        balance={}
        for course in self.courses:
            paid= self.list_payments(course)
            balance[course.course_name]=course.total_fees - paid
        
        return balance
        
    def add_payment(self, payment):
        self.payments.append(payment)
        payment.student= self
    

class Admin(User):
    def __init__(self, id, username, password, role):
        super().__init__(id, username, password, role)
        
    def add_student_to_course(self, student, course):
        course.add_student(student)
    