import requests
from django.http import HttpResponse
from django.views.generic import View
from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from settings import REDMINE_URL, API_KEY, GITLAB_URL, PRIVATE_TOKEN


def logout_view(request):
    logout(request)
    return redirect('/')


class IndexView(View):
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated():
                return redirect('/deleter/')
        return render(request, 'index.html')

    def post(self, request, *args, **kwargs):
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return redirect('/deleter/')
            else:
                return render(request, 'blockuser.html')
        else:
            return redirect('/')


@method_decorator(login_required, name='dispatch')
class DeleterView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'deleter.html')

    def post(self, request, *args, **kwargs):
        result_html = ''
        email = request.POST['email'].strip()
        redmine = int(request.POST['redmine'])
        gitlab = int(request.POST['gitlab'])
        if redmine == gitlab == 0:
            result_html = """<div>
                                You haven't chosen what is to be deleted.
                             </div>
                          """
            return HttpResponse(result_html)
        if redmine:
            result_html += redmine_del(email)
        if gitlab:
            result_html += gitlab_del(email)

        return HttpResponse(result_html)


def redmine_del(email):
    get_url = REDMINE_URL + '/users.json?name=%s' % (email, )
    req = requests.get(get_url, headers={'X-Redmine-API-Key': API_KEY})

    if req.json()[u'total_count'] > 1:
        mail_list = [user[u'mail'] for user in req.json()[u'users']]
        return '\
        <div>\
        <span style="color: red;">Redmine: </span>\
        found more than one user. Please delete user manually.\
        Found emails: %s\
        </div>' % (", ".join(mail_list), )

    if req.json()[u'total_count'] == 0:
        return '\
        <div>\
        <span style="color: red;">Redmine: </span>\
        user not found! Nothing to delete.\
        </div>'
    user_id = req.json()[u'users'][0]['id']
    del_url = REDMINE_URL + '/users/%s.json' % (user_id, )
    req = requests.delete(del_url, headers={"X-Redmine-API-Key": API_KEY})
    status_code = str(req.status_code) + " " + str(req.reason)

    return '\
        <div>\
        <span style="color: red;">Redmine: </span>\
        user deleted with status " %s ".\
        </div>' % (status_code, )


def gitlab_del(email):
    get_url = GITLAB_URL + '/api/v3/users?search=%s' % (email, )
    req = requests.get(get_url, headers={'PRIVATE-TOKEN': PRIVATE_TOKEN})
    if len(req.json()) > 1:
        mail_list = [user[u'email'] for user in req.json()]
        return '\
        <div>\
        <span style="color: red;">Gitlab: </span>\
        found more than one user. Please delete user manually.\
        Found emails: %s\
        </div>' % (", ".join(mail_list), )

    if len(req.json()) == 0:
        return '\
        <div>\
        <span style="color: red;">Gitlab: </span>\
        user not found! Nothing to delete.\
        </div>'

    user_id = req.json()[0]['id']
    del_url = GITLAB_URL + '/api/v3/users/%s' % (user_id, )
    req = requests.delete(del_url, headers={'PRIVATE-TOKEN': PRIVATE_TOKEN})
    status_code = str(req.status_code) + " " + str(req.reason)

    return '\
        <div>\
        <span style="color: red;">Gitlab: </span>\
        user deleted with status " %s ".\
        </div>' % (status_code, )
