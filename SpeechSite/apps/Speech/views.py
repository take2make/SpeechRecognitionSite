from django.shortcuts import render, redirect
from django.core.files.storage import FileSystemStorage as File
from .forms import SelectForm
from .forms import language_model_choices
from Speech2Text import combine
import os
from pathlib import Path
import threading
import time


def speech_to_txt(audio_file, model_choice):
    model_choice = model_choice.split(' ')

    model = os.path.join('Speech2Text', 'model_'+model_choice[0]+'_'+model_choice[1])
    audio = os.path.join('media', audio_file)

    #-------------start recognition and combining-----------------#
    print(f'\n your model {model}\n and audio_file {audio} \n')
    combine.main(audio, model)
    #-------------------------------------------------------------#
    pass



def index(request):
    form = SelectForm()

    context = {'form': form,'text':'result', 'loading': False}

    if (request.method == 'POST'):

        form = SelectForm(request.POST)
        uploaded_file = request.FILES["document"]
        model_id = request.POST["language_model"].split('_')[-1]
        model = language_model_choices[int(model_id)][-1]

        fs = File()
        fs.save(uploaded_file.name, uploaded_file)

        print('uploaded_file is \n',uploaded_file.name, '\n and model is', model)
        main_thread = threading.Thread(target = speech_to_txt, args=(uploaded_file.name, model,))
        main_thread.start()
        main_thread.join()

        result = os.path.join('txt', 'out.txt')
        with open(result, 'r') as file:
            result_txt = file.read()

        context = {'form': form, 'text': result_txt, 'loading': False}

    return render(request, 'index.html', context=context)
