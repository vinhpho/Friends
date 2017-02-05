from __future__ import unicode_literals
from django.db import models
from django.contrib import messages
import bcrypt
# Create your models here.

class UserManager(models.Manager):
    def createuser(self,request):
        is_valid = True
        if len(request.POST['name']) == 0:
            is_valid = False
            messages.error(request,'First Name is required.')
        if len(request.POST['alias'])== 0:
            is_valid = False
            messages.error(request,'Alias is required.')
        if len(request.POST['bday'])== 0:
            is_valid = False
            messages.error(request,'Birthday is required.')
        if len(request.POST['email']) == 0:
            is_valid = False
            messages.error(request,'Email is required.')
        email_check = User.objects.filter(email=request.POST['email'])
        if len(email_check) > 0:
            is_valid= False
            messages.error(request, 'Email is already exist')
        if len(request.POST['password'])< 8:
            is_valid = False
            messages.error(request, 'Password requires at least 8 characters')
        if request.POST['password'] != request.POST['confirm_password']:
            messages.error(request, 'Password and confirm password do not match')
            is_valid = False
        if not is_valid:
            return is_valid
        hashed = bcrypt.hashpw(request.POST['password'].encode('utf-8'), bcrypt.gensalt())
        new_user = User(
            name=request.POST['name'],
            alias = request.POST['alias'],
            bday = request.POST['bday'],
            email=request.POST['email'],
            password=hashed,
        )
        new_user.save()
        request.session['logged_in'] = new_user.id;
        is_valid = True
        return is_valid
    def login(self,request):
        is_valid = True
        user= User.objects.get(email=request.POST['email'])
        if len(user.email) == 0:
            messages.error(request, "The user does not exist")
            is_valid = False
            return is_valid
        dbpw=bcrypt.hashpw(request.POST['password'].encode('utf-8'), user.password.encode('utf-8'))
        if dbpw != user.password:
            messages.error(request, "Either email or password is incorrect")
            is_valid = False
            return is_valid
        #when password is correct
        request.session['logged_in'] = user.id
        return is_valid

    def logout(self,request):
        is_valid=True
        del request.session['logged_in']
        return True



class User(models.Model):
    name = models.CharField(max_length=255)
    alias = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    bday = models.DateField(auto_now=False, auto_now_add=False)
    password = models.CharField(max_length=45)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    objects = UserManager()

class Friend(models.Model):
    name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    user = models.ForeignKey(User)
