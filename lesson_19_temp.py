import argparse, datetime,json
class UserDoesNotExist (Exception):
    ...

def decorate(func: any)->bool:
    """
    Decorator function. Checks for data transfer between functions the check_password and authenticate
    :param func:
    :return: Takes the value of a function parameter
    """
    def wrapper(username: any, password: any) -> bool:
        try:
            check_password(username, password)
        except UserDoesNotExist:
            return False
        if not authenticate(username, password):
            return False
        return func(username, password)

    return wrapper

def check_password(username:str, password:str)->bool:
    """
    The function checks for the presence of a login in the global dictionary
    :param username:
    :param password:
    :return: true or false
    """
    try:
        return temp[username]
    except KeyError:
        raise UserDoesNotExist

def authenticate(username:any, password:any)->bool:
    """
    The function authenticates the user
    :param username:
    :param password:
    :return: brings out the truth
    """
    return temp.get(username) == password

@decorate
def login(username:any, password:any)->bool:
    """
    The function enters into something
    :param username:
    :param password:
    :return: brings out the truth
    """
    return True

def func_time(date)->bool:
    """
    The function checks the period of time for which the user entered the wrong login or password
    :param date: Date and time of the last incorrect login or password entry
    :return: outputs a boolean value
    """
    return date > datetime.datetime.now() - datetime.timedelta(minutes=5)

def save_last_wrong_time_login():
    """
    A function that saves the date and time of the last unsuccessful login and password entry
    :return: data and time
    """
    return datetime.datetime.now().strftime('%d-%m-%Y %H:%M:%S')


if __name__ == '__main__':


 with open('file.json', 'r') as f:
     temp = json.load(f)
     saving_login_error = datetime.datetime.strptime(temp["save_last_wrong_time_login"],'%d-%m-%Y %H:%M:%S')
     minut = (saving_login_error + datetime.timedelta(minutes=5)) - datetime.datetime.now()

 while func_time(saving_login_error) == True:
     print(f'Вы заблокированы! Следующая попытка через {minut} мин.')
     break
 else:

     prov_parser = argparse.ArgumentParser()
     prov_parser.add_argument("-u", "--username", action="store")
     prov_parser.add_argument("-p", "--password", action="store")
     args = prov_parser.parse_args()
     print(args)
     if args.username is None and args.password is None:
         print("Введите значение username и password")
     elif args.username is None:
         print("Введите значение username")
     elif args.password is None:
         print("Введите значение password")
     count = 3
     while count != 0:
             per = login(args.username or input(), args.password or input())
             if per == True:
                 print(f'Вы в системе!')
                 break
             else:
                 count -= 1
                 print('Неверный пароль. У вас осталось ', count, 'попыток')
                 args.username=input()
                 args.password=input()
                 print(args)
     else:
         print(f'Попытки истекли')
         saving_login_error = save_last_wrong_time_login()
         temp.update({'save_last_wrong_time_login': saving_login_error})
         with open('file.json', 'w') as f:
             json.dump(temp, f, indent=4)



