import pyttsx3
import time
from http.client import HTTPResponse
from django.shortcuts import render,HttpResponse,HttpResponseRedirect
from threading import Thread
from django.core.files.storage import FileSystemStorage
from .models import *
from django.contrib import messages
from django.db.models import Max, Min,Count,Sum,Avg
import numpy as np
from PIL import Image
import cv2
import tensorflow as tf
from tensorflow.keras.preprocessing.image import img_to_array
import os
from utils.utils import decodeImage
from predict import traffic

import cv2
import tensorflow as tf
def preprocess_image(img):
    # Resize image to match model input size
    img = cv2.resize(img, (32, 32))
    # Normalize pixel values
    img = img / 255.0
    # Expand dimensions to match model input shape
    img = np.expand_dims(img, axis=0)
    return img
def preprocess_image1(frame):
    """Preprocess frame for model input"""
    img = cv2.resize(frame, (30, 30))  # Resize to (30, 30)
    img = img_to_array(img) / 255.0  # Normalize pixel values
    img = np.expand_dims(img, axis=0)  # Add batch dimension (1, 30, 30, 3)
    return img

def udp(request):
    prediction=""
    model_path = "Traffic.h5"
    loaded_model = tf.keras.models.load_model(model_path)

    # Initialize text-to-speech engine
    engine = pyttsx3.init()
    engine.setProperty("rate", 150)  # Speech speed
    engine.setProperty("volume", 1.0)  # Volume level

    # Define traffic sign labels
    sign_labels = [
        "Speed limit (20km/h)", "Speed limit (30km/h)", "Speed limit (50km/h)", "Speed limit (60km/h)",
        "Speed limit (70km/h)", "Speed limit (80km/h)", "End of speed limit (80km/h)", "Speed limit (100km/h)",
        "Speed limit (120km/h)", "No passing", "No passing vehicle over 3.5 tons", "Right-of-way at intersection",
        "Priority road", "Yield", "Stop", "No vehicles", "Vehicle over 3.5 tons prohibited", "No entry",
        "General caution", "Dangerous curve left", "Dangerous curve right", "Double curve", "Bumpy road",
        "Slippery road", "Road narrows on the right", "Road work", "Traffic signals", "Pedestrians",
        "Children crossing", "Bicycles crossing", "Beware of ice/snow", "Wild animals crossing",
        "End speed and passing limits", "Turn right ahead", "Turn left ahead", "Ahead only",
        "Go straight or right", "Go straight or left", "Keep right", "Keep left",
        "Roundabout mandatory", "End of no passing", "End of no passing vehicle over 3.5 tons"
    ]

    # Start webcam
    videoCaptureObject = cv2.VideoCapture(0)
    current_prediction = None  # Store last detected sign
    last_detection_time = 0  # Track when the last sign was detected
    DISPLAY_TIME = 1  # Keep the detected sign displayed for 3 seconds
    CONFIDENCE_THRESHOLD = 0.99  # Minimum confidence (85%) to accept detection

    # Function to speak predictions in a separate thread
    def speak_prediction(pred_text):
        engine.say(pred_text)
        engine.runAndWait()

    print("Press 'ESC' to exit...")

    while True:
        ret, frame = videoCaptureObject.read()
        if not ret:
            print("Failed to capture frame")
            break

        # Preprocess frame
        image_resized = cv2.resize(frame, (30, 30))  # Resize for model input
        input_data = np.expand_dims(image_resized, axis=0) / 255.0  # Normalize

        # Predict traffic sign
        pred = loaded_model.predict(input_data)
        confidence = pred.max()  # Get the highest probability score
        result = pred.argmax()  # Get highest probability class
        print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@",confidence)
        # Only proceed if confidence is above the threshold
        if confidence >= CONFIDENCE_THRESHOLD:
            prediction = sign_labels[result]
            
            # Only update if it's a new sign
            if prediction != current_prediction:
                current_prediction = prediction  # Update last prediction
                last_detection_time = time.time()  # Update detection time
                print(f"Detected Sign: {prediction} (Confidence: {confidence:.2f})")

                # Speak detected sign in a new thread (non-blocking)
                Thread(target=speak_prediction, args=(prediction,)).start()
        else:
            # If no new detection for DISPLAY_TIME seconds, clear the text
            if time.time() - last_detection_time > DISPLAY_TIME:
                current_prediction = None

        # Display last detected sign on the screen
        if current_prediction:
            cv2.putText(frame, current_prediction, (20, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)

        cv2.imshow("Live Traffic Sign Detection", frame)

        # Exit on 'ESC' key press
        key = cv2.waitKey(1) & 0xFF
        if key == 27:
            print("Exiting...")
            break

    # Release resources
    videoCaptureObject.release()
    cv2.destroyAllWindows()
    return render(request,"user/prediction.html",{"prediction":prediction})



def imagebyenter(request):
    if request.POST:
        image=request.FILES['image']
        fs=FileSystemStorage()
        filename=fs.save(image.name,image)
        fileurl=fs.url(filename)

        model_path = "Traffic.h5"
        loaded_model = tf.keras.models.load_model(model_path)

        imagename = image
        print(fileurl)
        image_path = fs.path(filename)
        image = cv2.imread(image_path)
        image_fromarray = Image.fromarray(image, 'RGB')
        resize_image = image_fromarray.resize((30, 30))
        expand_input = np.expand_dims(resize_image,axis=0)
        input_data = np.array(expand_input)
        input_data = input_data/255
        pred = loaded_model.predict(input_data)
        result = pred.argmax()

        
        if result == 0:
            prediction = 'Speed limit (20km/h)'
            print("image",prediction)
        elif result == 1:
            prediction = 'Speed limit (30km/h)'
            print("image",prediction)
        elif result == 2:
            prediction = 'Speed limit (50km/h)'
            print("image",prediction)
        elif result == 3:
            prediction = 'Speed limit (60km/h)'
            print("image",prediction)
        elif result == 4:
            prediction = 'Speed limit (70km/h)'
            print("image",prediction)
        elif result == 5:
            prediction = 'Speed limit (80km/h)'
            print("image",prediction)
        elif result == 6:
            prediction = 'End of speed limit (80km/h)'
            print("image",prediction)
        elif result == 7:
            prediction = 'Speed limit (100km/h)'
            print("image",prediction)
        elif result == 8:
            prediction = 'Speed limit (120km/h)'
            print("image",prediction)
        elif result == 9:
            prediction = 'No passing'
            print("image",prediction)
        elif result == 10:
            prediction = 'No passing vehicle over 3.5 tons'
            print("image",prediction)
        elif result == 11:
            prediction = 'Right-of-way at intersection'
            print("image",prediction)
        elif result == 12:
            prediction = 'Priority road'
            print("image",prediction)
        elif result == 13:
            prediction = 'Yield'
            print("image",prediction)
        elif result == 14:
            prediction = 'Stop'
            print("image",prediction)
        elif result == 15:
            prediction = 'No vehicles'
            print("image",prediction)
        elif result == 16:
            prediction = 'Vehicle over 3.5 tons prohibited'
            print("image",prediction)
        elif result == 17:
            prediction = 'No entry'
            print("image",prediction)
        elif result == 18:
            prediction = 'General caution'
            print("image",prediction)
        elif result == 19:
            prediction = 'Dangerous curve left'
            print("image",prediction)
        elif result == 20:
            prediction = 'Dangerous curve right'
            print("image",prediction)
        elif result == 21:
            prediction = 'Double curve'
            print("image",prediction)
        elif result == 22:
            prediction = 'Bumpy road'
            print("image",prediction)
        elif result == 23:
            prediction = 'Slippery road'
            print("image",prediction)
        elif result == 24:
            prediction = 'Road narrows on the right'
            print("image",prediction)
        elif result == 25:
            prediction = 'Road work'
            print("image",prediction)
        elif result == 26:
            prediction = 'Traffic signals'
            print("image",prediction)
        elif result == 27:
            prediction = 'Pedestrians'
            print("image",prediction)
        elif result == 28:
            prediction = 'Children crossing'
            print("image",prediction)
        elif result == 29:
            prediction = 'Bicycles crossing'
            print("image",prediction)
        elif result == 30:
            prediction = 'Beware of ice/snow'
            print("image",prediction)
        elif result == 31:
            prediction = 'Wild animals crossing'
            print("image",prediction)
        elif result == 32:
            prediction = 'End speed and passing limits'
            print("image",prediction)
        elif result == 33:
            prediction = 'Turn right ahead'
            print("image",prediction)
        elif result == 34:
            prediction = 'Turn left ahead'
            print("image",prediction)
        elif result == 35:
            prediction = 'Ahead only'
            print("image",prediction)
        elif result == 36:
            prediction = 'Go straight or right'
            print("image",prediction)
        elif result == 37:
            prediction = 'Go straight or left'
            print("image",prediction)
        elif result == 38:
            prediction = 'Keep right'
            print("image",prediction)
        elif result == 39:
            prediction = 'Keep left'
            print("image",prediction)
        elif result == 40:
            prediction = 'Roundabout mandatory'
            print("image",prediction)
        elif result == 41:
            prediction = 'End of no passing'
            print("image",prediction)
        elif result == 42:
            prediction = 'End of no passing vehicle over 3.5 tons'
            print("image",prediction)
        return render(request,"user/prediction.html",{"prediction":prediction})
    return render(request,"user/enterimage.html")
    
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