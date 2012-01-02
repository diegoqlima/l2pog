# -*- coding: UTF-8 -*-
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.core.mail import send_mail

from datetime import datetime
import time
import random
import base64
import hashlib
import urllib2

from forms import *
from L2POG.l2pog.models import *

def authentic(f):
    def wrap(request, *args, **kwargs):
        #this check the session if userid key exist, if not it will redirect to login page
        if 'user' not in request.session.keys():
            return HttpResponseRedirect(reverse('login'))
        return f(request, *args, **kwargs)
    wrap.__doc__=f.__doc__
    wrap.__name__=f.__name__
    return wrap

def idle(f):
    def idle2(request, *args, **kwargs):
        print request.session['time_expire']
        diff = time.time() - request.session['time_expire']
        if diff > 120:
            logout(request)
            return HttpResponseRedirect(reverse('login'))
        request.session['time_expire'] = time.time()
        return f(request, *args, **kwargs)
    idle2.__doc__=f.__doc__
    idle2.__name__=f.__name__
    return idle2

@authentic
@idle
def index(request):
    bg_image = "/media/imgs/themes/interior_banner"
    bg_image = bg_image + str(random.randint(0,9)) + ".jpg"
    notices = Notice.objects.order_by('-date')[:5]
    return render_to_response('l2pog/index.html', locals(), context_instance=RequestContext(request))

@authentic
@idle
def vote(request):
    bg_image = "/media/imgs/themes/interior_banner"
    bg_image = bg_image + str(random.randint(0,9)) + ".jpg"

    acc = Accounts.objects.get(login=request.session["user"])
    userID = User.objects.get(iduser=acc.iduser.iduser)
    ipUser = request.META['REMOTE_ADDR']
    if votedToday(userID, ipUser):
        msg_erro = "Você já votou hoje, favor aguardar 24hrs"
        return render_to_response('l2pog/vote.html', locals(), context_instance=RequestContext(request))
    links = Link.objects.all()
    if request.method == 'POST':
        form = FormChars(request.POST)
        if form.is_valid():
            if 'countVote' not in request.session.keys():
                msg_erro = "Favor efetivar seu voto !!"
                return render_to_response('l2pog/vote.html', locals(), context_instance=RequestContext(request))
            if request.session['countVote'] != links.count():
                msg_erro = "Favor efetivar seu voto !!"
                return render_to_response('l2pog/vote.html', locals(), context_instance=RequestContext(request))
            if validVote(ipUser):
                msg_erro = "Favor efetivar seu voto !!"
                return render_to_response('l2pog/vote.html', locals(), context_instance=RequestContext(request))
            vote = Vote()
            vote.datevote = datetime.today()
            vote.iduser = acc.iduser
            vote.ipvote = ipUser
            vote.save()
            itens = {6577: 1, 6578: 1, 6622: 4, 9627: 1}
            char = Characters.objects.get(accountname=acc.login)
            for itemID, qtdItem in itens.iteritems():
                lastObject = Items.objects.order_by('-objectid').values_list('objectid', flat=True)[:1]
                lastObject = lastObject[0] + 1
                item = Items()
                item.ownerid = char.charid
                item.objectid = lastObject
                item.itemid = itemID
                item.count = qtdItem
                item.enchantlevel = 0
                item.loc = 'WAREHOUSE'
                item.customtype1 = 0
                item.customtype2 = 0
                item.manaleft = -1
                item.time = -1
                item.save()
            links = ""
            form = ""
            msg_success = "Você já pode logar e receber o seu item!"
            return render_to_response('l2pog/vote.html', locals(), context_instance=RequestContext(request))
    form = FormChars()
    form.fields['character'].queryset = Characters.objects.filter(accountname=acc.login)
    return render_to_response('l2pog/vote.html', locals(), context_instance=RequestContext(request))

def votedToday(user, ipUser):
    hoje = datetime.today()
    try:
        Vote.objects.filter(datevote__year=hoje.year, datevote__month=hoje.month, datevote__day=hoje.day, iduser=user.iduser).get(datevote__year=hoje.year, datevote__month=hoje.month, datevote__day=hoje.day, ipvote=ipUser)
    except Vote.DoesNotExist:
        return False
    return True

def validVote(ipUser):
    arrIP = ipUser.split('.')
    arrIP = str(arrIP[0])+"-"+str(arrIP[1])+"-"+str(arrIP[2])
    url = "http://www.gamesites200.com/lineage2/details-28457.html"
    try:
        response = urllib2.urlopen(url)
        html = response.read()
        html = html[html.find('Last 40 Referrers'):len(html)]
        html = html[0:html.find('div class="SR">')]
        arrHtml = html.split('<a href=\"javascript:popUp')
        response.close()
    except Exception:
        return True
    count = 1
    for piece in arrHtml:
        if count > 5:
            break
        if piece.find('analyzeIP-28457-'+arrIP+'.html') >= 0:
            return False
        count += 1
    return True

def countVote(request):
    if 'countVote' not in request.session.keys():
        request.session['countVote'] = 1
    else:
        request.session['countVote'] += 1
    return render_to_response('l2pog/nothing.html', locals(), context_instance=RequestContext(request))

def cleanVote(request):
    try:
        del request.session['countVote']
    except KeyError:
        pass
    return render_to_response('l2pog/nothing.html', locals(), context_instance=RequestContext(request))

@authentic
@idle
def socio(request):
    bg_image = "/media/imgs/themes/interior_banner"
    bg_image = bg_image + str(random.randint(0,9)) + ".jpg"
    return render_to_response('l2pog/socio.html', locals(), context_instance=RequestContext(request))

def download(request):
    bg_image = "/media/imgs/themes/interior_banner"
    bg_image = bg_image + str(random.randint(0,9)) + ".jpg"
    return render_to_response('l2pog/download.html', locals(), context_instance=RequestContext(request))

def rates(request):
    bg_image = "/media/imgs/themes/interior_banner"
    bg_image = bg_image + str(random.randint(0,9)) + ".jpg"
    return render_to_response('l2pog/rates.html', locals(), context_instance=RequestContext(request))

def anuncios(request):
    bg_image = "/media/imgs/themes/interior_banner"
    bg_image = bg_image + str(random.randint(0,9)) + ".jpg"
    anuncios = range(10)
    return render_to_response('l2pog/anuncios.html', locals(), context_instance=RequestContext(request))

def contato(request):
    bg_image = "/media/imgs/themes/interior_banner"
    bg_image = bg_image + str(random.randint(0,9)) + ".jpg"
    if request.method == 'POST':
        form = FormContato(request.POST)
        if form.is_valid():
            contact = form.save(commit=False)
            contact.date = datetime.today()
            contact.save()
            msg_success = "Mensagem enviada, aguarde retorno do Administrador !!"
            form = FormContato()
    else:
        form = FormContato()
    return render_to_response('l2pog/contato.html', locals(), context_instance=RequestContext(request))

def login(request):
    bg_image = "/media/imgs/themes/interior_banner"
    bg_image = bg_image + str(random.randint(0,9)) + ".jpg"
    notices = Notice.objects.order_by('-date')[:5]
    if request.method == 'POST':
        user = request.POST['login']
        password = request.POST['password']
        try:
            #Criptografa senha digitada
            msgdigest = hashlib.sha1()
            msgdigest.update(password)
            encode = base64.b64encode(msgdigest.digest())
            
            validate = Accounts.objects.get(login=user, password=encode)
            request.session['user'] = validate
            request.session['time_expire'] = time.time()
            return HttpResponseRedirect(reverse('index'))
        except Accounts.DoesNotExist:
            msg_erro = "Login/Senha inválidos"
            return render_to_response('l2pog/index.html', locals(), context_instance=RequestContext(request))

    return render_to_response('l2pog/index.html', locals(), context_instance=RequestContext(request))

def logout(request):
    try:
        del request.session['user']
        del request.session['time_expire']
    except KeyError:
        pass
    return HttpResponseRedirect(reverse('login'))

def register(request):
    bg_image = "/media/imgs/themes/interior_banner"
    bg_image = bg_image + str(random.randint(0,9)) + ".jpg"
    form = FormRegister()
    if request.method == 'POST':
        form = FormRegister(request.POST)
        if form.is_valid():
            """ GET FIELDS ON FORM """
            username = form.cleaned_data['nome']
            email = form.cleaned_data['email']
            login = form.cleaned_data['login']
            password = form.cleaned_data['senha']

            """ CHECK IF EMAIL IS BEING USED """
            try:
                user = User.objects.get(usermail=email)
            except User.DoesNotExist:
                user = ''
            if (user):
                msg_erro = "Email já está sendo usado em outro cadastro !!"
                return render_to_response('l2pog/registro.html', locals(), context_instance=RequestContext(request))

            """ CHECK IF ACCOUNT EXISTS """
            try:
                account = Accounts.objects.get(login=login)
            except Accounts.DoesNotExist:
                account = ''
            if(account):
                msg_erro = "Login já está sendo usado em outro cadastro !!"
                return render_to_response('l2pog/registro.html', locals(), context_instance=RequestContext(request))

            """ Criptografa senha digitada """
            msgdigest = hashlib.sha1()
            msgdigest.update(password)
            pswdencode = base64.b64encode(msgdigest.digest())

            """ CREATE USER """
            user = User()
            user.username = username
            user.usermail = email
            user.userregistration = datetime.today()
            user.save()
            user = User.objects.get(usermail=email)
            """ CREATE ACCOUNT """
            account = Accounts()
            account.login = login
            account.password = pswdencode
            account.iduser = user
            account.save()
            """ SEND EMAIL """
            send_mail('Conta Criada com sucesso','Conta Criada com sucesso','lammer004@gmail.com',[email])

            form = FormRegister()
            msg_success = "Account created"
            return render_to_response('l2pog/registro.html', locals(), context_instance=RequestContext(request))

    return render_to_response('l2pog/registro.html', locals(), context_instance=RequestContext(request))
