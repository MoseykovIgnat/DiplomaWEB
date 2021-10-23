from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.hashers import *
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
import SQLParser.xxxdbrc
import pymysql as MySQLdb
import crypt
from hmac import compare_digest as compare_hash


def create_connect_to_db(config):
    connection = MySQLdb.connect(host=config["hostname"],
                                 user=config["username"],
                                 passwd=config["password"],
                                 db=config["dbname"],
                                 port=config["port"],
                                 charset='utf8')

    return connection


def get_crypted_pass_by_username(username):
    config = SQLParser.xxxdbrc.config('adm')
    connection = create_connect_to_db(config)
    cursor = connection.cursor(MySQLdb.cursors.DictCursor)
    query_for_crypted_password = "select c_passwd from t_shadow where c_account=%s"
    cursor.execute(query_for_crypted_password, username)
    try:
        crypted_password = cursor.fetchone()['c_passwd']
    except:
        crypted_password = False
    finally:
        cursor.close()
        connection.close()
        return crypted_password


UserModel = get_user_model()


class PersonalizedLoginBackend(ModelBackend):
    def authenticate(self, request=None, username=None, password=None, **kwars):
        crypted_password = get_crypted_pass_by_username(username)
        print(crypted_password)
        try:
            # If user already in Django DB let's check pass in SND t_shadow
            user = UserModel._default_manager.get_by_natural_key(username)
            return None
                # if compare_hash(crypt.crypt(password, crypted_password), crypted_password)
                # user = UserModel._default_manager.get_by_natural_key(username)
                # user.check_password(password)


        except:
            print("Let's create a user")
            print(crypted_password)
            if compare_hash(crypt.crypt(password, crypted_password), crypted_password):
                user = User.objects.create_user(username=username, password=password)
                user.save()
                print('User was created')
            return None
