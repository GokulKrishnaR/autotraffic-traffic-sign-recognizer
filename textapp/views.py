import json

import cv2
from django.contrib import messages
from django.core.files.storage import FileSystemStorage
from django.http import JsonResponse
from django.shortcuts import HttpResponseRedirect, render
from django.views.decorators.http import require_POST

from .models import *
from .sign_predictor import predict_from_base64, predict_from_rgb_array


def udp(request):
    return render(request, "user/live_camera.html")


@require_POST
def predict_frame(request):
    try:
        data = json.loads(request.body)
        image_b64 = data.get("image", "")
    except (json.JSONDecodeError, TypeError):
        return JsonResponse({"error": "Invalid request"}, status=400)
    if not image_b64:
        return JsonResponse({"error": "No image provided"}, status=400)
    try:
        result = predict_from_base64(image_b64)
    except FileNotFoundError:
        return JsonResponse({"error": "Model file not found"}, status=500)
    except Exception as exc:
        return JsonResponse({"error": str(exc)}, status=500)
    if "error" in result:
        return JsonResponse(result, status=400)
    return JsonResponse(result)


def imagebyenter(request):
    if request.POST:
        image = request.FILES['image']
        fs = FileSystemStorage()
        filename = fs.save(image.name, image)
        image_path = fs.path(filename)
        img = cv2.imread(image_path)
        rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        result = predict_from_rgb_array(rgb)
        prediction = result['prediction'] or 'No sign detected (low confidence)'
        return render(request, "user/prediction.html", {"prediction": prediction})
    return render(request, "user/enterimage.html")
    
def predict(request):
    return render(request,"user/prediction.html")

def index(request):
    return render(request,"common/index.html")

def adminhome(request):
    return render(request,"admin/index.html")

def userhome(request):
    return render(request,"user/index.html")

def userreg(request):
    if request.POST:
        name = request.POST.get("name")
        address = request.POST.get("address")
        contact = request.POST.get("contact")
        email = request.POST.get("email")
        password = request.POST.get("password")

        # Check if the email already exists in the Login model
        if Login.objects.filter(username=email).exists():
            messages.info(request, "This email is already registered.")
        else:
            # If email is not taken, create user and login records
            user = User.objects.create(uname=name, uaddress=address, ucontact=contact, uemail=email, upassword=password)
            user.save()

            login = Login.objects.create(username=email, password=password, usertype='user')
            login.save()

            messages.success(request, "Registration successful!")
            
    return render(request, "common/userreg.html")

def logins(request):
    if request.POST:
        name=request.POST.get("username")
        password=request.POST.get("password")
        s=Login.objects.get(username=name,password=password)
        if s.usertype=='admin':
            return HttpResponseRedirect("/adminhome")
        elif s.usertype=='user':
            s=User.objects.get(uemail=name)
            id=s.id
            request.session['uid']=id
            return HttpResponseRedirect("/userhome")
        else: 
            msg="invalid Username Or password"
    return render(request,"common/login.html")

def adminviewuser(request):  
    s=User.objects.all()
    print(s)
    if "id" in request.GET:
        id=request.GET.get("id")
        print(id)
        User.objects.filter(id=id).delete()
    return render(request,"admin/viewuser.html",{"data":s})