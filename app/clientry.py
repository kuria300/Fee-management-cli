import argparse
from app.utils.auth import Register, Login
from app.models.course import Course
from app.models.payment import Payment
from app.models.user import Admin
from app.models.user import Student
from app.utils.file_reader import read_json, save_json, payment_path, user_path, session_path, course_path
from datetime import date

current_user=None

def main():
    global current_user

    current_user= read_json(session_path)

    # print(current_user)
    parser= argparse.ArgumentParser(prog='Fee management CLI', description="Fees management using the argparse CLI", epilog="python -m app <argument> <options>")
    subparsers= parser.add_subparsers(dest='command', required=True)

    reg_parser= subparsers.add_parser("register" ,help="Register a new user")
    reg_parser.add_argument('username')
    reg_parser.add_argument('password')
    reg_parser.add_argument('role', choices=['student', 'admin'])

    log_parser=subparsers.add_parser('login', help="Login an existing user")
    log_parser.add_argument('username')
    log_parser.add_argument('password')

    lu_parser= subparsers.add_parser('logout', help='clear session in session.json')

    csa_parser= subparsers.add_parser("add-course", help="add a course")
    csa_parser.add_argument('course_name')
    csa_parser.add_argument('fees', type=int)

    ls_parser= subparsers.add_parser('list_students_in_a_course', help='list all studnets enrolled in a course')

    pay_parser= subparsers.add_parser('add-payment', help="add payment regarding course")
    pay_parser.add_argument('course_name')
    pay_parser.add_argument('amount_paid',type=int)

    

    cse_parser= subparsers.add_parser('add_student_to_course', help='Add a student to a course')
    cse_parser.add_argument('student_id', type=int)
    cse_parser.add_argument('course')

    args=parser.parse_args()

    if args.command == "register":
        Register(args.username, args.password, args.role)

    elif args.command == 'login':
        current_user=Login(args.username, args.password)

        if current_user:
            save_json(session_path, {
                "id": current_user.id,
                "password": None,
                "username": current_user.username,
                "role": current_user.role })

            print(f'welcome {args.username}')
        else:
            print('Invalid Credentials!')
    # admin
    elif args.command == 'logout':
        if not current_user:
            print('Login first!')
            return

        save_json(session_path, [])
        current_user= None
        
        print('Logged out successfully!')
        # print(current_user)

    elif args.command == "add-course":
        if not current_user or current_user['role'] != "admin":
            print('Only admin can add a course')
            return
        
        courses= read_json(course_path)
        course_id = len(courses) + 1

        course1= Course(course_id, args.course_name, args.fees)

        courses.append({
            'course_id': course_id,
            'course_name': course1.course_name,
            'fees': course1.fees
        })

        save_json(course_path, courses)

    
        print(f'course added:{course1.course_name}')
    # admin
    elif args.command == 'list_students_in_a_course':
        if not current_user or current_user['role'] != "admin":
            print('Only admin can see students enrolled in a course')
            return
        
        courses = read_json(course_path)
        
        for c in courses:
            student_data=[Student(s['id'], s['username'], None, s['role'])for s in c.get('students', [])]

            course_obj= Course(c['course_id'], c['course_name'], c['fees'], students=student_data)
            print(f"course: {course_obj.course_name} : {course_obj.list_students()}")
     
    # admin
    elif args.command == 'add_student_to_course':
        if not current_user or current_user['role'] != "admin":
            print('Only admin can enroll a student to a course')
            return

        users= read_json(user_path)
        user= (u for u in users if u['id'] ==  args.student_id)

        user=next(user, None)
        # create student obj
        stud_obj=Student( user['id'],user['username'],user['password'],user['role'])

        courses= read_json(course_path)
        course= next((c for c in courses if args.course == c['course_name']), None)
        # create course obj
        course_obj = Course(course['course_id'], course['course_name'], course['fees'])
        # create admin obj
        admin_obj=Admin( current_user['id'], current_user['username'], current_user['password'], current_user['role'])

        
        admin_obj.add_student_to_course(stud_obj, course_obj)

        for c in courses:
             if c['course_id'] == course_obj.course_id:
                c['students'] = [{"id": s.id, "username": s.username, "role": s.role} for s in course_obj.students]
            
        save_json(course_path, courses)
        
        print(f"{stud_obj.username} has been added successfully to {course_obj.course_name}")

    


    elif args.command=='add-payment':
        if not current_user or current_user['role'] != "student":
            print('Only student can make payment')
            return
        
        courses= read_json(course_path)
        course= next((c for c in courses if args.course_name == c['course_name']), None)

        Balance= int(course['fees'])- args.amount_paid

        if not course:
            print('no course found')
            return

        pays=read_json(payment_path)

        pay_id= len(pays) +1

        payemnt1= Payment(pay_id, args.amount_paid, str(date.today()), course)
        stud_obj=Student( current_user['id'], current_user['username'], current_user['password'], current_user['role'])
        stud_obj.add_payment(payemnt1)

        pays.append({
        "payment_id": pay_id,
        "student_id": current_user['id'],
        "student_username": current_user['username'],
        "course_name": course['course_name'],
        "amount_paid": args.amount_paid,
        "date_paid": str(date.today())
        })
 
        save_json(payment_path, pays)



        print(f'payment added, balance remaining {Balance}')