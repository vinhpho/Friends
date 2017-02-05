from django.shortcuts import render, redirect,HttpResponse
from . models import User,Friend
from collections import Counter
# Create your views here.
def index(request):
    return render(request, 'friendapp/index.html')
def createuser(request):
    did_create = User.objects.createuser(request)
    if did_create:
        return redirect('/main')
    else:
        return redirect('/main')
def login(request):
    did_login = User.objects.login(request)
    print "*"*50
    print did_login
    if did_login:
        return redirect('/main/friends')
    else:
        return redirect('/main')
def friends(request):
    if 'logged_in'in request.session:
        loginuser=User.objects.get(id=request.session['logged_in'])
        friends=User.objects.all().exclude(id=request.session['logged_in'])
        notfriends=User.objects.exclude(id__in=Friend.objects.filter(id=request.session['logged_in']).values_list('id',flat=True))

        context = {
                "loginuser":loginuser,
                "friends":friends,
                "notfriends":notfriends,

        }
        return render(request, 'friendapp/login.html',context)
    else:
        return HttpResponse("Please check username and password")
        return redirect('/main')

def show_profile(request, id):
    friend=User.objects.get(id=id)

    context = {
            "friend":friend
    }
    return render(request, 'friendapp/show_profile.html',context)




def logout(request):
    try:
        del request.session['logged_in']
    except KeyError:
        pass
    return HttpResponse("You're successfully logged out.")
    return redirect('/main')
