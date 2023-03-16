from fingerpaint.models import User


def create_user(username, userpwd):
    if exists(username):
        return False #already existing username
    User.objects.create ( username = username, password = userpwd, email = username)
    return True #successfully created user

def get_user(username):
    return User.objects.get(username=username)


def get_all_users():
    return User.objects.all()


def exists(username):
    try:
        User.objects.get(username=username)
        return True
    except:
        return False


def password_check(password, check):
    if password == check:
        return True
    else:
        return False


def get_username(user):
    return user.username


def set_username(user, new_username):
    if new_username is None:
        raise Exception("Username is null")
    elif len(new_username) > 25:
        raise Exception("Username is > 25")
    elif exists(new_username):
        raise Exception("Username already exists")
    else:
        user.username = new_username
        user.save()


def get_password(user):
    return user.password


def set_password(user, new_password):
    if new_password is None:
        raise Exception("Password is null")
    elif len(new_password) > 25:
        raise Exception("Password is too long")
    else:
        user.password = new_password
        user.save()


def get_email(user):
    return user.email


def set_email(user, new_email):
    if new_email is None:
        raise Exception("Email is null")
    elif len(new_email) > 40:
        raise Exception("Email is too long")
    else:
        user.email = new_email
        user.save()


def add_user(username, password, email):
    new_user = User(username=" ", password=" ", email=" ")
    try:
        set_username(new_user, username)
        set_password(new_user, password)
        set_email(new_user, email)
        new_user.save()
    except Exception as e:
        raise Exception(str(e))


def delete_user(user):
    try:
        user.delete()
    except:
        raise Exception("User doesn't exist")
