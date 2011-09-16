from django.template import Context, loader
from django.shortcuts import get_object_or_404, render_to_response
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from website.models import *
from django.contrib.auth import authenticate, login, logout
from website.forms import *
from settings import SECRET_KEY
from Http import Http
import re
import codecs


@csrf_exempt
def loginfun(req):
   if req.method == 'POST':
      form = LoginForm(req.POST)
      if form.is_valid():
         idul = req.POST['idul']
         pasw = req.POST['pasw']
         user = authenticate(username=idul, password=pasw+idul)
         if user is not None:
            login(req, user)
            return HttpResponseRedirect('/home/')
         else:
            user = User.objects.create_user(idul, '', pasw+idul)
            user.is_active = False
            user.save()
            profile = user.get_profile()

            http = Http()
            http.get('https://capsuleweb.ulaval.ca/pls/etprod7/twbkwbis.P_WWWLogin')
            http.post('https://capsuleweb.ulaval.ca/pls/etprod7/twbkwbis.P_ValLogin', { 'sid': idul, 'PIN': pasw })

            res = http.get('https://capsuleweb.ulaval.ca/pls/etprod7/bwskfshd.P_CrseSchd').decode('cp1252').encode('utf-8')
            c = re.compile('(<TABLE\s\sCLASS="datadisplaytable"(.*?)">.+?)<!--\s\s\*\* START', re.S)
            t = c.search(res).group(1)
            profile.horaire = t

            res = http.get('https://capsuleweb.ulaval.ca/pls/etprod7/bwskoacc.P_ViewAcctTotal').decode('cp1252').encode('utf-8')
            c = re.compile('<TABLE  CLASS="datadisplaytable"(.*?)">(.+?)<!--\s\s\*\* START', re.S)
            t = c.search(res).group(2)
            profile.compte = t

            res = http.post('https://capsuleweb.ulaval.ca/pls/etprod7/bwskgstu.P_StuInfo', { 'term_in': '201109' }).decode('cp1252').encode('utf-8')
            c = re.compile('<DIV class="pagetitlediv">(.+?)<!--\s\s\*\* START', re.S)
            t = c.search(res).group(1)
            profile.dossier = t

            profile.save()
            theuser = authenticate(username=idul, password=pasw+idul)
            login(req, theuser)
            return HttpResponseRedirect('/home/')
      else:
         return render_to_response('login.html', {'err':'Bad username/password'})

   res = render_to_response('login.html', {})
   res['Cache-Control'] = 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0'
   res['Pragma'] = 'no-cache'
   return res


@login_required
def home(req):
   user = get_object_or_404(User, pk=req.user.id)
   profile = user.get_profile()
   res = render_to_response('home.html', { 'user': user })
   res['Cache-Control'] = 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0'
   res['Pragma'] = 'no-cache'
   return res


@login_required
def horaire(req):
   user = get_object_or_404(User, pk=req.user.id)
   profile = user.get_profile()
   res = render_to_response('horaire.html', { 'user': user })
   res['Cache-Control'] = 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0'
   res['Pragma'] = 'no-cache'
   return res


@login_required
def dossier(req):
   user = get_object_or_404(User, pk=req.user.id)
   profile = user.get_profile()
   res = render_to_response('dossier.html', { 'user': user })
   res['Cache-Control'] = 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0'
   res['Pragma'] = 'no-cache'
   return res


@login_required
def compte(req):
   user = get_object_or_404(User, pk=req.user.id)
   profile = user.get_profile()
   res = render_to_response('compte.html', { 'user': user })
   res['Cache-Control'] = 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0'
   res['Pragma'] = 'no-cache'
   return res


@login_required
def user_logout(req):
   logout(req)
   return HttpResponseRedirect('/')
