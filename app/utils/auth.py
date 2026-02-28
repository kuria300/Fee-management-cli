import hashlib
from app.utils.file_reader import save_json, read_json, user_path, payment_path
from app.models.user import Student, Admin

def hashPassword(password):
    return hashlib.sha256(password.encode()).hexdigest()

def Register(username, password, role):
    users= read_json(user_path)

    user_id = len(users) + 1
    hashed = hashPassword(password)

    if role == 'admin':
        user_obj= Admin(user_id, username, hashed, role)
    else:
        user_obj= Student(user_id, username, hashed, role)

    #append user_obj to users    
    users.append({
        "id":user_id,
        "username":username,
        "password":hashed,
        "role":role
    })

    save_json(user_path, users)
    print(f"{role} registered successfully!")
    # return user_obj
    
def Login(username, password):
    users= read_json(user_path)

    hashpass=hashPassword(password)

    for user in users:
        if user['username'] == username and user['password'] == hashpass:
            
            if user['role'] == 'admin':
                return Admin(user['id'], user['username'], user['password'], user['role'])
            else:
                return Student(user['id'], user['username'], user['password'], user['role'])
        