from django.shortcuts import render
from .forms import DocumentForm, PostForm
from .models import Presentation, PostComment
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.views import View
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.template import loader

from .scripts import unzip, generate_json

import os
import shutil


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
                    input_path = settings.MEDIA_ROOT + path
                    output_path = settings.MEDIA_ROOT + os.path.dirname(path)
                    
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
                    path = settings.MEDIA_ROOT + os.path.dirname(newdoc.docfile.name)
                    shutil.rmtree(path)
                    newdoc.delete()  # OUTCOMMENT


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
            path = settings.MEDIA_ROOT + os.path.dirname(doc.docfile.name)
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

# manual page
@login_required
def manual(request):
    return render(
        request, 'upload_manual.html'
    )
# LISTING FUNCTIONS

def list_classes(request):
    documents = Presentation.objects.all()
    return render(
        request, 'classes.html',
        {'documents':documents}
    )
  
class ListLectures(View):
    error = ''
    
    # define dict generating function
    def list_lectures(self, request, class_id, key = None):
        # generate list of lectures
        self.document = Presentation.objects.get(pk=class_id)
        dic = self.document.json
        # check if JSON was correctly saved and stored
        if dic['lectures'].keys():
            lectures = list(dic['lectures'].keys())
            titles = []
            for lecture in lectures:
                # list tuples (key, value)
                titles.append(
                    (lecture , dic['lectures'][lecture]['lecture_title']))
            self.lectures = titles
            
            # generate list of subchapters
            # if key is none (first page after redirect) display first lecture
            if key == None:
                key = self.lectures[0][0]
            
            if 'subchapters' in dic['lectures'][key]:
                subchapters = list(dic['lectures'][key]['subchapters'].keys())
                titles = []
                for sub in subchapters:
                    # Check if there is a link
                    try:
                        link = dic['lectures'][key]['subchapters'][sub]['link']
                    except KeyError:
                        link = ''

                    # list tuples (title , slide)
                    titles.append(
                        (
                        dic['lectures'][key]['subchapters'][sub]['title'],
                        int(dic['lectures'][key]['subchapters'][sub]['slide'])-1, # -1 to get position of the slide with Title
                        link
                        )
                    )
                self.subchapters = titles
            else:
                self.subchapters = ''
            # Get logo
            try:
                self.logo = dic['logo']
            except KeyError:
                self.logo = ''

            # generate slides
            self.key = key
            self.slides = list(dic['lectures'][key]['slides'].values())
            self.length = range(0, len(self.slides))
        # return empty variables if there was no dictionary
        else:
            self.lectures = ''
            self.subchapters =''
            self.slides =''
            self.key = ''
            self.length = ''
            self.error = 'JSON does not exist or damaged'

    def get(self, request, *args, **kwargs):
        
        # get required parameters to list leectures
        try:
            self.list_lectures(request, kwargs['class_id'], kwargs['key'])
            self.comments = PostComment.objects.filter(class_id_id=kwargs['class_id'], lecture=kwargs['key']).order_by('slide', '-created') 
        except KeyError:
            self.list_lectures(request, kwargs['class_id'])
            self.comments = PostComment.objects.filter(class_id_id=kwargs['class_id'], lecture = 'lecture1').order_by( 'slide', '-created')
        return render(
            request, 'lectures/lectures.html', 
            {'lectures':self.lectures,
            'document': self.document,
            'subchapters':self.subchapters,
            'slides':self.slides,
            'key': self.key,
            'length': self.length,
            'error': self.error,
            'comments': self.comments,
            'logo': self.logo}
        )

# def create_post(request, **kwargs):

#     if request.method == 'POST':
#         post_text = request.POST.get('the_post_text', '')
#         post_author = request.POST.get('the_post_author', '')
#         class_id = request.POST.get('class_id', '')
#         slide = request.POST.get('slide', '')
#         if request.POST.get('key', ''):
#             lecture = request.POST.get('key', '')
#         else:
#             lecture = 'lecture1'
#         response_data = {}

#         post = PostComment(author = post_author, 
#                                 slide = slide,
#                                 text = post_text,
#                                 class_id_id = Presentation.objects.get(pk = class_id).id,
#                                 lecture = lecture 
#                                 )
#         post.save()

#         response_data['result'] = 'Create post successful!'
#         response_data['postpk'] = post.pk
#         response_data['text'] = post.text
#         response_data['created'] = post.created.strftime('%B %d, %Y %I:%M %p')
#         response_data['author'] = post.author
#         response_data['slide'] = post.slide

        
        
#         return JsonResponse(response_data)
#     else:
#        return JsonResponse(
#            ({"nothing to see": "this isn't happening"}))


def delete_post(request, **kwargs):

    if request.method == 'POST':
        comment_id = request.POST.get('comment_id', '')
        response_data = {}

        post = PostComment.objects.get(pk = comment_id )
        post.delete()

        response_data['result'] = 'Comment successfuly deleted!'
        
        return JsonResponse(response_data)
    else:
       return JsonResponse(
           ({"nothing to see": "this isn't happening"}))

def lazy_load(request):
    page = request.POST.get("page")
    class_id = request.POST.get('class_id', '')
    #slide = request.POST.get('slide', '')
    # check if key was transmitted
    if request.POST.get('key', ''):
        lecture = request.POST.get('key', '')
    else:
        lecture = 'lecture1'
    comments = PostComment.objects.filter(class_id_id=class_id, lecture=lecture).order_by('-created') # get just 2 posts
    # use Django’s pagination

    results_per_page = 2
    paginator = Paginator(comments, results_per_page)
    try:
        comments = paginator.page(page)
    except PageNotAnInteger:
        comments = paginator.page(2)
    except EmptyPage:
        comments = paginator.page(paginator.num_pages)
    # build a html posts list with the paginated posts
    comments_html = loader.render_to_string(
                                'comments.html',
                                {'comments': comments,
                                # send user to know if he is auth
                                'user':request.user}
                                )
    # package output data and return it as a JSON object
    output_data = {
                    'lectures/comments_html': comments_html,
                    'has_next': comments.has_next()
    }
    return JsonResponse(output_data)

def create_post(request):
    if request.method == 'POST':
        post_text = request.POST.get('the_post_text', '')
        post_author = request.POST.get('the_post_author', '')
        class_id = request.POST.get('class_id', '')
        slide = request.POST.get('slide', '')
        if request.POST.get('key', ''):
            lecture = request.POST.get('key', '')
        else:
            lecture = 'lecture1'
        response_data = {}

        post = PostComment(author = post_author, 
                                slide = slide,
                                text = post_text,
                                class_id_id = Presentation.objects.get(pk = class_id).id,
                                lecture = lecture 
                                )
        post.save()
        # convert to list ot iterate over
        post = [post]
        # build a html posts list with the paginated posts
        comments_html = loader.render_to_string(
                                    'lectures/comments.html',
                                    {'comments': post,
                                    # send user to know if he is auth
                                    'user':request.user}
                                    )
        # package output data and return it as a JSON object
        output_data = {
                        'comments_html': comments_html
        }
        return JsonResponse(output_data)

def change_color(request):
    if request.method == 'POST':
        class_id = request.POST.get('class_id', '')
        color = request.POST.get('color', '')

        post = Presentation.objects.get(pk = class_id)
        post.color = color
        post.save()

        # build a html posts list with the paginated posts
        response = 'Color successfuly changed'
        # package output data and return it as a JSON object
        output_data = {
                        'response': response
        }
        return JsonResponse(output_data)

    