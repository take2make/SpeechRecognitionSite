from django.shortcuts import render, redirect
from django.core.files.storage import FileSystemStorage as File
from .forms import SelectForm
from .forms import language_model_choices
import scripts
import os
import threading
import time
import shutil
import os
from django.conf import settings
from django.http import FileResponse
from django.http import HttpResponse


api_url = "http://192.168.1.218:8000/api/speech_api/"

def save_result_file(session_id, result_txt):
    path = os.path.join('static', f'txt_{session_id}.txt')
    with open(path, 'w') as file:
        file.write(result_txt)
    pass

def get_data_from_session(url_session):
    session_id = url_session.split('/')[-2]
    print(session_id)
    while True:
        time.sleep(1)
        response = scripts.get_json(url_session)
        print(response)
        if response['detail'] == 200:
            result_txt = response['result']
            save_result_file(session_id, result_txt)
            break


def index(request):
    form = SelectForm()

    context = {'form': form,'text':'he will be your text ...', 'loaded': False}

    if (request.method == 'POST'):

        form = SelectForm(request.POST)
        uploaded_file = request.FILES["upload_file"]

        fs = File()
        fs.save(uploaded_file.name, uploaded_file)

        model_id = request.POST["language_model"].split('_')[-1]
        model = language_model_choices[int(model_id)][-1]

        print('uploaded_file is \n',uploaded_file.name, '\n and model is', model)

        file = os.path.join('media', uploaded_file.name)
        encoded_data = scripts.encode_file(file)
        extension = uploaded_file.name.split('.')[-1]
        os.remove(file)

        if 'choose_vocab' in request.FILES:
            print('CHOSED VOCAB')

            vocab = request.FILES["choose_vocab"]
            fs = File()
            fs.save(vocab.name, vocab)

            file_vocab = os.path.join('media', vocab.name)
            with open(file_vocab, 'r') as f:
                file_txt = f.read()
            os.remove(file_vocab)

            response = scripts.send_json(api_url, encoded_data, extension, model, file_txt)
        else:
            print('VOCAB WAS NOT CHOSEN')

            response = scripts.send_json(api_url, encoded_data, extension, model, '')

        if response['detail'] == 200:
            session_id = response['session_id']
            url_session = f'{api_url}{session_id}/'
            main_thread = threading.Thread(target=get_data_from_session, args=(url_session,))
            main_thread.start()
            main_thread.join()

            result_txt = scripts.get_json(url_session)['result']
            file = f'txt_{session_id}.txt'
            context = {'form': form, 'text': result_txt, 'file': str(file), 'loaded': True}

    return render(request, 'index.html', context=context)
