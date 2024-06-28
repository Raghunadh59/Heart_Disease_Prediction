from django.shortcuts import render
import numpy as np
import pickle
import pandas as pd
import google.generativeai as genai

genai.configure(api_key="AIzaSyAIktHsJFgpEYm_pokNzyjZcLksRIk6p28")


model = pickle.load(open(r'C:\Users\91901\OneDrive\Desktop\Heart\HeartDiseasePrediction\model.pkl', 'rb'))
scale = pickle.load(open(r'C:\Users\91901\OneDrive\Desktop\Heart\HeartDiseasePrediction\sc.pkl', 'rb'))

def home(request):
    return render(request, 'home.html')

def predict(request):
    return render(request, 'input.html')

def submit(request):
    details = {
        'name': request.POST['name1'],
        'gender': int(request.POST['gender']),
        'age': int(request.POST['age']),
        'sm_status': int(request.POST['sm']),
        'bp_status': int(request.POST['bp']),
        'hs_status': int(request.POST['hs']),
        'diabetic': int(request.POST['dia']),
        'dia_lev': int(request.POST['dia_lev']),
        'cholestrol': int(request.POST['chol']),
        'sys_bp': int(request.POST['sys_bp']),
        'dia_bp': int(request.POST['dia_bp']),
        'bmi': int(request.POST['bmi']),
        'hrt': int(request.POST['hrt'])
    }

    details['sm_status1'] = 1 if details['sm_status'] == 0 else 0
    details['bp_status1'] = 1 if details['bp_status'] == 0 else 0
    details['hs_status1'] = 1 if details['hs_status'] == 0 else 0
    details['diabetic1'] = 1 if details['diabetic'] == 0 else 0

    input_data = [
        details['gender'], details['age'], details['cholestrol'], details['sys_bp'], details['dia_bp'],
        details['bmi'], details['hrt'], details['dia_lev'], details['sm_status'], details['sm_status1'], details['bp_status'],
        details['bp_status1'], details['hs_status'], details['hs_status1'], details['diabetic'], details['diabetic1']
    ]
    
    input_data = np.array(input_data).reshape(1, -1)
    names = [
        'male', 'age', 'totChol', 'sysBP', 'diaBP', 'BMI', 'heartRate', 'glucose',
        'currentSmoker_0', 'currentSmoker_1', 'BPMeds_0.0', 'BPMeds_1.0',
        'prevalentStroke_0', 'prevalentStroke_1', 'diabetes_0', 'diabetes_1'
    ]
    data = pd.DataFrame(input_data, columns=names)
    
    scaled_data = scale.transform(data)
    
    prediction = model.predict(scaled_data)

    genres = genai.GenerativeModel(model_name="gemini-1.5-flash")
    response = genres.generate_content(["Tips for good heart"])
    entities=response.text
    

    if prediction == 1:
        return render(request, 'chat.html', {'response': 1, 'name': details['name'],'reply':entities})
    else:
        return render(request, 'chat.html', {'response': 0, 'name': details['name'],'reply':entities})
