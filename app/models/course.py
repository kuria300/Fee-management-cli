from .user import Student

class Course:
    def __init__(self, course_id, course_name, total_fees, students=None):
        self.course_id= course_id
        self.course_name=course_name
        self._total_fees= total_fees
        self.students=students
        
    @property
    def fees(self):
        return self._total_fees
    @fees.setter
    def fees(self, value):
        if value < 0:
            raise ValueError("Total fees can't be negative")
        elif not isinstance(value, int):
            raise TypeError('Total fees should be an int')
        self._total_fees = value
        
    def list_students(self):
        stud_names= [stud.username for stud in self.students]
        if not stud_names:
            return "No students enrolled"
        return stud_names

        
    def add_student(self, value):
        
        if not isinstance(value , Student):
            raise TypeError('not an instance of student')
        self.students.append(value)
        value.courses.append(self)