#coding=utf-8
from django.shortcuts import *
from django.http import HttpResponse,HttpResponseRedirect
from django.template import RequestContext
from django import forms
from models import *
from online.models import *
from django.utils.timezone import now, timedelta
from time import strftime, localtime
import datetime
import time
from datetime import timedelta


busy = {
    ('1', '被预约'),
    ('2', '出差'),
}

kindsSearch = {
    ('1', '教师ID'),
    ('2', '教师姓名'),
}

kinds = {
    ('kind1', '教师'),
    ('kind2', '学生'),
}

days ={
    ('0','今天'),
    ('1','明天'),
    ('2','后天'),
}
times ={
    ('time1','7:00:00'),
    ('time2','9:00:00'),
    ('time3','13:00:00'),}

all_time = ['07:00','09:00','13:00']
#表单
class MessageForm(forms.Form):
    date = forms.DateField()
    #ChoiceField(label="日期",choices= days)
    time = forms.CharField(label="时间")

class searchForm(forms.Form):
    kindsSearch = forms.ChoiceField(label="检索根据", choices=kindsSearch)
    teacherMessage = forms.CharField(label="检索信息", max_length=20)

class UserForm(forms.Form): 
    kind = forms.ChoiceField(label="用户类型", choices=kinds) 
    username = forms.CharField(label='用户名',max_length=100)
    password = forms.CharField(label='密码',widget=forms.PasswordInput())
    ID = forms.CharField(label='ID', max_length=10)
    major = forms.ModelChoiceField(queryset = Major.objects.all(), required=True, label=u'专业/方向', error_messages={'required': u'必选项'},)
    college = forms.ModelChoiceField(queryset = College.objects.all(), required=True, label=u'学院', error_messages={'required': u'必选项'},)
    #queue = forms.ChoiceField(label=u'队列')
    '''def __init__(self,*args,**kwargs):
        super(UserForm,self).__init__(*args,**kwargs)
        self.fields['college'].choices=((x.number,x.collegename) for x in College.objects.all())
        self.fields['major'].choices=((x.number,x.majorname) for x in Major.objects.all())'''
    #major = forms.CharField(max_length=100)

class LoginForm(forms.Form):
    kind = forms.ChoiceField(label="用户类型", choices=kinds) 
    ID = forms.CharField(label='用户ID',max_length=100)
    password = forms.CharField(label='密码',widget=forms.PasswordInput())

class MajorForm(forms.Form):
    number = forms.CharField(label="编号", max_length=20)
    name = forms.CharField(label="专业/方向简称", max_length=100)

class BusyForm(forms.Form):
    teacher = forms.ModelChoiceField(label="teacher",  required=True, queryset=Teacher.objects.all(), error_messages={'required': u'必选项'},)
    date = forms.ChoiceField(label="日期",choices= days)

class CollegeForm(forms.Form):
    number = forms.CharField(label="编号", max_length=20)
    name = forms.CharField(label="学院全称", max_length=100)

class tuijianForm(forms.Form):
    major = forms.ModelChoiceField(queryset = Major.objects.all(), required=True, label=u'专业/方向', error_messages={'required': u'必选项'},)

def jianyue(req):
    college = College.objects.all()
    userID = req.session.get('ID',default=None)
    lianjie = ''
    if userID:
        if req.method == 'POST':
            if 'tname' in req.GET:
                tname = req.GET['tname']
                t = Teacher.objects.get(teacherID__exact=tname)
                messages = Message.objects.filter(teacher=t)
            uf = MessageForm(req.POST)
            if uf.is_valid():
                date = uf.cleaned_data['date']
                tme = uf.cleaned_data['time']
                #num = int(date)
                chuchai = Busy.objects.filter(
                        teacher = t,
                        date = date,#now().date() + timedelta(days=num),
                        time = "07:00:00")
                thisday_message = Message.objects.filter(
                        teacher = t,
                        date = date,#now().date() + timedelta(days=num),
                        time = tme)
                if thisday_message or chuchai:
                    return render_to_response('jiaoshimang.html', {'lianjie':lianjie})
                else:
                    tname = req.GET['tname']
                    t = Teacher.objects.get(teacherID__exact=tname)
                    sID = req.session.get('ID',default=None)
                    s = Student.objects.get(studentID__exact=sID)
                    Message.objects.create(
                            teacher = t,
                            kind = "被预约",
                            date = date,#now().date() + timedelta(days=num),
                            time = tme,
                            student = s)
                    return render_to_response('yuyuechenggong.html', {'lianjie':lianjie})
        else:
            uf = MessageForm()
            if 'tname' in req.GET:
                tname = req.GET['tname']
                t = Teacher.objects.filter(name__exact=tname)
                messages = Message.objects.filter(teacher=t)
                busy = Busy.objects.filter(teacher=t)
                return render_to_response("yuyue2.html",{'lianjie':lianjie, 'uf':uf,'messages':messages,'tname':tname, 'busy':busy,'college':college})
        return render_to_response("yuyue2.html", {'lianjie':lianjie, 'uf':uf,'college':college})
    else:
        return render_to_response('weidneglu.html')

def superuser(req):
    return render_to_response('superuserhome.html')

def addmajor(req):
    if req.method == 'POST':
        uf = MajorForm(req.POST)
        if uf.is_valid():
            #获得表单数据
             number = uf.cleaned_data['number']
             name = uf.cleaned_data['name']
             Major.objects.create(number = number, majorname = name)
             return render_to_response('superuserok.html')
    else:
        uf = MajorForm()
    return render_to_response('addmajor.html',{'uf':uf}, context_instance=RequestContext(req))

def addmessage(req):
    if req.method == 'POST':
        uf = BusyForm(req.POST)
        if uf.is_valid():
            #获得表单数据
            t = uf.cleaned_data['teacher']
            date = uf.cleaned_data['date']
            num = int(date)
            Busy.objects.create(teacher = t, kind = '出差', date = now().date() + timedelta(days=num), time = "07:00:00")
            return render_to_response('superuserok.html')
    else:
        uf = BusyForm()
    return render_to_response('addmessage.html',{'uf':uf}, context_instance=RequestContext(req))

def addcollege(req):
    if req.method == 'POST':
        uf = CollegeForm(req.POST)
        if uf.is_valid():
            #获得表单数据
             number = uf.cleaned_data['number']
             name = uf.cleaned_data['name']
             College.objects.create(number = number, collegename = name)
             return render_to_response('superuserok.html')
    else:
        uf = CollegeForm()
    return render_to_response('addcollege.html',{'uf':uf}, context_instance=RequestContext(req))

def collegeteachers(req, num):
    colleges = College.objects.all()
    college = College.objects.get(number__exact = num)
    teachers = Teacher.objects.filter(college = college)
    kind = req.session.get('kind',default=None)
    lianjie = ''
    if kind == 'kind2':
        lianjie = ''
    if kind == 'kind1':
        lianjie = '/messages'
    return render_to_response('collegeteacher.html', {'lianjie':lianjie, 'colleges':colleges, 'college': college, 'teachers':teachers})

def home(req):
    userID = req.session.get('ID',default=None)
    kind = req.session.get('kind',default=None)
    college = College.objects.all()
    message1 = Message.objects.filter(kind = '被预约')#被预约
    message2 = Busy.objects.filter(kind = '出差')#出差
    message = []
    teacher = []
    student = []
    if userID == '0000' or (not userID):
        userID = '未登录'
        teacher = []
        student = []
        message = []
        #return HttpResponse('0')
    else:
        kind = req.session.get('kind',default=None)
        if kind == 'kind1':
            teacher = Teacher.objects.get(teacherID__exact = userID)
            message = Message.objects.filter(teacher = teacher)
            student = []
        elif kind == 'kind2':
            student = Student.objects.get(studentID__exact = userID)
            message = Message.objects.filter(student = student)
            teacher = []
        elif kind == 'kind0':
            teacher = []
            student = []
            message = []
    return render_to_response('home2.html', {'msg':message, 'std':student, 'tch':teacher, 'userID':userID, 'busy':message2, 'beiyuyue':message1, 'colleges':college})


#注册
def regist(req):
    kind1 = req.session.get('kind',default=None)
    lianjie = ''
    if kind1 == 'kind2':
        lianjie = ''
    if kind1 == 'kind1':
        lianjie = '/messages'
    if req.method == 'POST':
        uf = UserForm(req.POST)
        if uf.is_valid():
            kind = uf.cleaned_data['kind']
            username = uf.cleaned_data['username']
            password = uf.cleaned_data['password']
            ID = uf.cleaned_data['ID']
            major = uf.cleaned_data['major']
            college = uf.cleaned_data['college']
            if kind == 'kind1':
                Teacher.objects.create(kind=kind, name=username, password=password, teacherID=ID, reseachdirection = major, college =  college)
            if kind == 'kind2':
                Student.objects.create(kind=kind, name=username, password=password, studentID=ID, profession = major, college = college)

            return render_to_response('zhucechenggong.html', {'lianjie':lianjie})
    else:
        uf = UserForm()
    return render_to_response('regist.html',{'uf':uf}, context_instance=RequestContext(req))
#登陆

def showmessage(req):
    kind = req.session.get('kind',default=None)
    ID = req.session.get('ID',default=None)
    colleges = College.objects.all()
    lianjie = ''
    if kind == 'kind1':
        lianjie = '/messages'
        teacher = Teacher.objects.filter(teacherID__exact = ID)
        messages = Message.objects.filter(teacher = teacher, kind = '被预约')
        return render_to_response('message.html', {'userID':ID, 'lianjie':lianjie, 'msg':messages, 'colleges':colleges})
    if kind == 'kind2':
        student = Student.objects.filter(studentID__exact = ID)
        messages = Message.objects.filter(student = student, kind = '被预约')
        return render_to_response('message.html', {'userID':ID, 'lianjie':lianjie, 'msg':messages, 'colleges':colleges})
    return render_to_response('weidenglu.html', {'lianjie':lianjie})

def deletemessage(req):
    tid = req.GET.get('tid')
    sid = req.GET.get('sid')
    d = req.GET.get('d')
    t = req.GET.get('t')
    teacher = Teacher.objects.get(teacherID = tid)
    student = Student.objects.get(studentID = sid)
    msg = Message.objects.get(teacher = teacher, student = student, date = d, time = t)
    msg.delete()
    kind1 = req.session.get('kind',default=None)
    lianjie = ''
    if kind1 == 'kind2':
        lianjie = ''
    if kind1 == 'kind1':
        lianjie = '/messages'
    return render_to_response('shanchuchenggong.html', {'lianjie':lianjie})

def modifymessage(req):
    tid = req.GET.get('tid')
    sid = req.GET.get('sid')
    d = req.GET.get('d')
    t = req.GET.get('t')
    teacher = Teacher.objects.get(teacherID__exact = tid)
    student = Student.objects.get(studentID__exact = sid)
    msg = Message.objects.get(teacher = teacher, student = student, date = d, time = t)
    colleges = College.objects.all()
    kind = req.session.get('kind',default=None)
    lianjie = ''
    if kind == 'kind2':
        lianjie = ''
    if kind == 'kind1':
        lianjie = '/messages'
    if req.method == 'POST':
        post = req.POST
        date = post['date']
        tme = post['time']
        chuchai = Busy.objects.filter(
            teacher = teacher,
            date = date,
            time = "07:00:00")
        thisday_message = Message.objects.filter(
            teacher = teacher,
            date = date,
            time = tme)
        if (thisday_message and msg not in thisday_message) or chuchai:
             return render_to_response('jiaoshimang.html', {'lianjie':lianjie})
        else:
            msg.date = date
            msg.time = tme
            msg.save()
            return render_to_response('xiugaichenggong.html', {'lianjie':lianjie})
    return render_to_response("modify.html",{'lianjie':lianjie, 'msg':msg, 'colleges':colleges})

def login(req):
    if req.method == 'POST':
        uf = LoginForm(req.POST)
        if uf.is_valid():
            #获取表单用户密码
            ID = uf.cleaned_data['ID']
            password = uf.cleaned_data['password']
            if uf.cleaned_data['kind'] == 'kind1':
                user = Teacher.objects.filter(teacherID__exact = ID,password__exact = password)
                if user:
                    req.session['ID'] = ID
                    req.session['kind'] = 'kind1'
                    '''response = HttpResponseRedirect('/messages/')
                    response.set_cookie('ID', ID, 1800)
                    response.set_cookie('kind', 'kind1', 1800)
                    #response = HttpResponseRedirect('/messages/')
                    return response'''
                    return HttpResponseRedirect('/messages/')
                else:
                    lianjie = '/messages'
                    return render_to_response('denglushibai.html', {'lianjie':lianjie})
            if uf.cleaned_data['kind'] == 'kind2':
                user = Student.objects.filter(studentID__exact = ID,password__exact = password)
                if user:
                    #比较成功，跳转index
                    '''response = HttpResponseRedirect('/')
                    response.set_cookie('ID', ID, 1800)
                    response.set_cookie('kind', 'kind2', 1800)
                    return response'''
                    req.session['ID'] = ID
                    req.session['kind'] = 'kind2'
                    return HttpResponseRedirect('/')
                else:
                    lianjie = ''
                    return render_to_response('denglushibai.html', {'lianjie':lianjie})
    else:
        uf = LoginForm()
    return render_to_response('login.html',{'uf':uf},context_instance=RequestContext(req))

#登陆成功
def welcome(req):
    username = req.session.get('ID',default=None)
    return render_to_response('index1.html' ,{'username':username})

#退出
def logout(req):
    #清理cookie里保存username
    lianjie = ''
        #return HttpResponse("1")
    '''response = HttpResponseRedirect('/')
    response.set_cookie('ID', '0000' ,1800)
    response.set_cookie('kind', 'kind0', 1800)
        #return HttpResponse("0")
    ID = req.COOKIES['ID']
    kind = req.COOKIES['kind']'''
    del req.session['ID']
    del req.session['kind']
    return render_to_response('tuichu.html', {'lianjie':lianjie})
    
def search(req):
    college = College.objects.all()
    if req.method == 'POST':
        uf = searchForm(req.POST)
        if uf.is_valid():
            kindsSearch = uf.cleaned_data['kindsSearch']
            teacherMessage = uf.cleaned_data['teacherMessage']
            teacher=Teacher.objects.all()
            if kindsSearch == '1':
                teacher=Teacher.objects.filter(teacherID = teacherMessage)
            elif kindsSearch == '2':
                teacher=Teacher.objects.filter(name = teacherMessage)
    else:
        uf = searchForm()
        teacher=[]
    return render_to_response('search2.html',{'uf':uf,'teacher':teacher,'college':college})

def detail(req, q):
    teacher = Teacher.objects.get(teacherID__exact = q)
    message = Message.objects.filter(teacher = teacher)
    colleges = College.objects.all()
    msg = Message.objects.filter(teacher = teacher)
    busy = Busy.objects.filter(teacher = teacher)
    kind = req.session.get('kind',default=None)
    lianjie = ''
    if kind == 'kind2':
        lianjie = ''
    if kind == 'kind1':
        lianjie = '/messages'
    return render_to_response('details.html', {'lianjie':lianjie, 'teacher':teacher, 'msg':message, 'colleges':colleges, 'msg':msg, 'busy':busy})

def tuijian(req):
    college = College.objects.all()
    if req.method == 'POST':
        uf = tuijianForm(req.POST)
        if uf.is_valid():
            major = uf.cleaned_data['major']
            teacher=Teacher.objects.all()
            #return HttpResponse(kind2)
            ma = Major.objects.filter(majorname__exact = major.majorname)
            teacher=Teacher.objects.filter(reseachdirection = ma)
    else:
        uf = tuijianForm()
        teacher=[]
    return render_to_response('tuijian3.html',{'uf':uf,'teacher':teacher, 'college':college})

def deleteusers(req):
    student = Student.objects.all()
    teacher = Teacher.objects.all()
    return render_to_response('deleteuser.html', {'tch':teacher, 'std':student})

def deleteuser(req):
    ID = req.GET.get('id')
    kind = req.GET.get('kind')
    if kind == u'1' and Teacher.objects.all():#教师
        t = Teacher.objects.get(teacherID__exact = ID)
        if Message.objects.filter(teacher = t):
            msg = Message.objects.filter(teacher = t)
            for m in msg:
                m.delete()
        busy = Busy.objects.filter(teacher = t)
        for b in busy:
            b.delete()
        t.delete()
        return render_to_response('superuserok.html')
    if kind == u'0' and Student.objects.all():
        s = Student.objects.get(studentID = ID)
        msg = Message.objects.filter(student = s)
        for m in msg:
            m.delete()
        s.delete()
        return render_to_response('superuserok.html')
    return render_to_response('yichang.html')
    
    
    
    
    
    
    