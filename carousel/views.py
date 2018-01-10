from django.shortcuts import render
from .forms import DocumentForm
from .models import Presentation
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required

from .scripts import unzip, generate_json

import os
import shutil
import json


# Create your views here.
@login_required
def upload_documents(request):
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)

        #get file extension
        extension = os.path.splitext(request.FILES['docfile'].name)[1][0:].lower() # extention
        original_name = os.path.splitext(request.FILES['docfile'].name)[0][0:] # name without extention

        # Check extension. Must be .zip
        if extension == '.zip':

            if form.is_valid():

                newdoc = Presentation(docfile=request.FILES['docfile'],
                                    title =request.POST['title'] ,
                                    json='NA')
                newdoc.save()
                try:
                    path = newdoc.docfile.name
                    #path = path.docfile.name
                    input_path = 'media/' + path
                    output_path = 'media/' + os.path.dirname(path)
                    
                    unzip(input_path, output_path)
                    # update path field

                    newdoc.docfile = os.path.dirname(newdoc.docfile.name)+ '/' + original_name # set path to unziped folder
                    newdoc.save()

                    # update JSON
                
                    json = generate_json(newdoc.docfile.name, request.POST['title'])
                    newdoc.json = json
                    newdoc.save()
                    # No errors
                    error = ''
                except Exception:
                    # Display error + Delete files
                    error = 'Import error.'
                    path = 'media/' + os.path.dirname(newdoc.docfile.name)
                    shutil.rmtree(path)
                    newdoc.delete()


            else:
                error = "Form is not valid."

        else:
            error = "Wrong file format. You must use .zip only."

    else:
        form = DocumentForm() # Empty
        error="" # Empty

    # Render list page with the documents and the form and error if needed

    documents = Presentation.objects.all()

    return render(
                    request, 'upload.html',
                    {'documents': documents,
                    'form': form,
                    'error': error}
                    )

@login_required
def DeleteList(request):

    # values from the check box
    values = request.POST.getlist('delete_list')

    # Delete files. If file path does not exist pass. It prevents failes in dispalyng presentations with deleted or ranamed paths
    try:
        for value in values:
            doc = Presentation.objects.get(pk = value)
            path = 'media/' + os.path.dirname(doc.docfile.name)
            shutil.rmtree(path)
    except FileNotFoundError:
        pass
    
    # Delete from the database

    Presentation.objects.filter(pk__in=values).delete()
    # Render page elements
    documents = Presentation.objects.all()
    form = DocumentForm()
    error = ''
    
    return HttpResponseRedirect(reverse('carousel:upload'))

# LISTING FUNCTIONS

def list_classes(request):
    documents = Presentation.objects.all()
    return render(
        request, 'classes.html',
        {'documents':documents}
    )

def list_lectures(request, class_id, key = None):
    # generate list of lectures
    document = Presentation.objects.get(pk=class_id)
    dic = document.json
    # check if JSON was correctly saved and stored
    if type(dic) == dict:
        lectures = list(dic['lectures'].keys())
        titles = []
        for lecture in lectures:
            # list tuples (key, value)
            titles.append(
                (lecture , dic['lectures'][lecture]['lecture_title']))
        lectures = titles
        # generate list of subchapters
        if key == None:
            key = lectures[0][0]
        
        if 'subchapters' in dic['lectures'][key]:
            subchapters = list(dic['lectures'][key]['subchapters'].keys())
            titles = []
            for sub in subchapters:
                # list tuples (title , slide)
                titles.append(
                    (
                    dic['lectures'][key]['subchapters'][sub]['title'],
                    int(dic['lectures'][key]['subchapters'][sub]['slide'])-1 # -1 to get position of the slide with Title
                    )
                )
            subchapters = titles
        else:
            subchapters = ''

        # generate slides
        
        slides = list(dic['lectures'][key]['slides'].values())
        length = range(0, len(slides))
        error = ''
    # return empty variables if there was no dictionary
    else:
        subchapters =''
        slides =''
        key = ''
        length = ''
        error = 'JSON does not exist or damaged'


    return render(
        request, 'lectures.html', 
        {'lectures':lectures,
        'document': document,
        'subchapters':subchapters,
        'slides':slides,
        'key': key,
        'length': length,
        'error': error}
    )

