from django.shortcuts import render
from django.http import JsonResponse
from django.apps import apps
from django.shortcuts import render, redirect
from django.contrib import messages,messages

from django.views.decorators.csrf import csrf_exempt
import csv
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth import authenticate, logout
from django.contrib.auth.models import User,auth
from django.contrib.auth.forms import AuthenticationForm
from .feature import extract_features, calculate_importance
def home(request):
    return render(request, 'predictor/index.html')
def page(request):
    return render(request, 'predictor/page.html')

def predict(request):
    if request.method == 'POST':
        text = request.POST.get('text')
        features = extract_features(text)
        percentage, feature_importances  = calculate_importance(features)
        if text:
            X_predict = [str(text)]
            # Access the model from the app config
            phish_model = apps.get_app_config('app').model
            y_predict = phish_model.predict(X_predict)
            prediction = 0 
            if  y_predict == 'phishing' :
                prediction = 0
            elif y_predict == 'benign':
                prediction=1
            elif y_predict == 'defacement':
                prediction=2
            elif y_predict == 'malware':
                prediction=3
            
            return JsonResponse({'prediction': int(prediction), 'percentage': percentage, 'feature_importances':feature_importances })
        else:
            return JsonResponse({'error': 'Input text not provided.'})
    else:
        return JsonResponse({'error': 'Invalid request method.'})


@csrf_exempt
def save_feedback(request):
    if request.method == 'POST':
        url = request.POST.get('url')
        feedback = request.POST.get('feedback')

        if url and feedback:
            # Assuming 'feedback.csv' exists in your media directory
            with open('media/feedback.csv', mode='a', newline='') as feedback_file:
                feedback_writer = csv.writer(feedback_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                feedback_writer.writerow([url, feedback])
            
            return JsonResponse({'message': 'Feedback saved successfully.'})
        else:
            return JsonResponse({'error': 'URL or feedback not provided.'})
    else:
        return JsonResponse({'error': 'Invalid request method.'})


def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate( username=username, password=password )

        if user is not None:
            auth.login(request, user)
            return redirect('page')  # Redirect to desired page after login
        else:
            messages.error(request, 'Invalid credentials.')
            return redirect('/')

    return render(request, 'user_auth/login.html')
  
def signup(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']
        if password == password2:
            if User.objects.filter(username=username).exists():
                messages.error(request, 'Username already exists.')
                return redirect('signup')
            if User.objects.filter(email=email).exists():
                messages.error(request, 'email already exists.')
                return redirect('signup')

            elif len(password) < 6:
                messages.error(request, 'Password must be at least 6 characters long.')
                return redirect('signup')
            else:
                user = User.objects.create_user(username=username, email=email, password=password)
                user.save()
                messages.success(request, 'Registration successful.')
                return redirect('login')
        else:
            messages.info(request, 'password not matching..')
            return redirect('signup') 
 
    else:
        return render(request, 'user_auth/signup.html')
    
def logout(request):
    auth.logout(request)
    return redirect('page/')
