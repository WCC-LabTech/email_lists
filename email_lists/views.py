from django.http import HttpResponse
from django.utils import simplejson
from django.core import serializers
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User, Group
from django.forms.models import model_to_dict

# Email imports
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


@csrf_exempt
def list_groups(request):
    try:
        data = simplejson.dumps({'groups':
                                    [model_to_dict(x) 
                                    for x in Group.objects.all()]
        })
        return HttpResponse(data)
    except:
        return HttpResponse(status=400)

@csrf_exempt
def display_users(request, pk):
    try:
        users = Group.objects.get(pk=pk).user_set.all()
        data = [{
                'username': user.username,
                'pk': user.pk,
                'email': user.email,
            }
            for user in users]
        data = simplejson.dumps({'users': data})
        return HttpResponse(data)
    except:
        return HttpResponse(status=400)
    
@csrf_exempt
def send_email(request):
    sender_email = request.user.email
    to_emails = [x.email for x in 
                    Group.objects.get(pk=request.POST['group']).user_set.all()]

    # Set up message
    msg = MIMEMultipart('alternative')
    msg['Subject'] = request.POST['subject']
    msg['From'] = sender_email
    msg['To'] = to_emails
    body = request.POST['body']

    # Set MIME types
    part = MIMEText(body, 'plain')
    msg.attach(part)
    try:
        for email in to_emails:
            server = smtplib.SMTP('smtp.wccnet.edu', 25)
            server.sendmail(sender_email, email, msg.as_string())
        server.quit()
    except:
        data = simplejson.dumps({'message': 'Could not send email'})
        return HttpResponse(data, status=400)
    data = simplejson.dumps({'message': ''})
    return HttpResponse(data, status=200, mimetype='application/json') 
