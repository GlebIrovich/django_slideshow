#comments/views

from django.http import JsonResponse
from user_management.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.template import loader
from carousel.models import Presentation
from .models import PostComment

# Helper functions
class Comments:
    def __init__(self, request):
        self.first_lecture = "lecture1"
        self.level = 1
        self.request = request
        print("USER USER USER {}".format(User))
        self.author = User.objects.get(pk=self.request.user.id)
    def gather(self, item):
        return self.request.POST.get(item, '')
    def sort_comments(self, class_id, lecture, slide):
        return PostComment.objects.filter(class_id_id=class_id, lecture=lecture, slide = slide).order_by('main', 'created','level')
    # get all input data from the request
    def post(self, inputs): # inputs is a list of required variable
        vars = []
        for i in inputs:
            # apply special rule for key (it can be none)
            if i == "key":
                if self.gather('key'):
                    vars.append(self.gather('key'))
                else:
                    vars.append(self.first_lecture)
            # else gather input value
            else:
                vars.append(self.gather(i))
        # return list
        return vars

# main views for Axaj
def create_post(request):
    if request.method == 'POST':
        com = Comments(request)
        required_inputs = ['the_post_text', 'class_id', 'slide', 'user_tag', 'key']
        post_text, class_id, slide, user_tag, lecture = com.post(required_inputs)
           
        response_data = {}
        post = PostComment(author_id = com.author, 
                            slide = slide,
                            text = post_text,
                            user_tag = user_tag,
                            class_id_id = Presentation.objects.get(pk = class_id).id,
                            lecture = lecture
                            )
        post.save()
        # set main to self id
        main = post.id
        post.main_id = main
        post.save()
        # get commets list
        comments = com.sort_comments(class_id, lecture, slide)
        result = "Comment successfuly added!"
        # build a html posts list with the paginated posts
        comments_html = loader.render_to_string(
                                    'lectures/comments.html',
                                    {'comments': comments,
                                    # send user to know if he is auth
                                    'user':request.user}
                                    )
        # package output data and return it as a JSON object
        output_data = {'comments_html':comments_html,'result':result}
        return JsonResponse(output_data)

@staff_member_required
def delete_post(request):

    if request.method == 'POST':
        com = Comments(request)
        comment_id = com.gather('comment_id')
        response_data = {}

        post = PostComment.objects.get(pk = comment_id )
        # get data to render comments
        lecture = post.lecture
        class_id = post.class_id_id
        slide = post.slide
        # delete
        post.delete()
        result = 'Comment successfuly deleted!'
        comments = com.sort_comments(class_id, lecture, slide)
        comments_html = loader.render_to_string(
                                    'lectures/comments.html',
                                    {'comments': comments,
                                    # send user to know if he is auth
                                    'user':request.user}
                                   )
        # package output data and return it as a JSON object
        output_data = {'comments_html': comments_html,'result':result}
        return JsonResponse(output_data)
    else:
        result = 'Something went wrong. Please reload the page.'
        output_data = {'result':result}
        return JsonResponse(output_data)

def reply(request):
    if request.method == 'POST':
        com = Comments(request)
        required_inputs = ['the_post_text', 'class_id', 'slide', 'user_tag', 'key', 'main', 'parent']
        post_text, class_id, slide, user_tag, lecture, main, parent = com.post(required_inputs)
        level = com.level
        response_data = {}
        post = PostComment(author_id = com.author, 
                                slide = slide,
                                text = post_text,
                                class_id_id = Presentation.objects.get(pk = class_id).id,
                                lecture = lecture,
                                main_id = PostComment.objects.get(pk=main).id,
                                parent_id = PostComment.objects.get(pk=parent).id,
                                level = level,
                                replied_to = PostComment.objects.get(pk=parent).author,
                                user_tag = user_tag
                                )
        post.save()
        # get refreshed list of commetns for this page
        comments = com.sort_comments(post.class_id_id, lecture, slide)
        result = "Reply successfuly added"
        # build a html posts list with the paginated posts
        comments_html = loader.render_to_string(
                                    'lectures/comments.html',
                                    {'comments': comments,
                                    # send user to know if he is auth
                                    'user':request.user}
                                   )
        # package output data and return it as a JSON object
        output_data = {'comments_html': comments_html,'result':result}
        return JsonResponse(output_data)

def show_reply_form(request):
    if request.method == 'POST':
        html = loader.render_to_string(
                                    'lectures/comments_form_reply.html'
                                    )
        # package output data and return it as a JSON object
        output_data = {
                        'html': html
        }
        return JsonResponse(output_data)

@staff_member_required
def admin_tag(request):
    if request.method == 'POST':
        com = Comments(request)
        required_inputs = ['class_id', 'slide', 'tag', 'key', 'id']
        class_id, slide, admin_tag, lecture, comment_id = com.post(required_inputs)        
        response_data = {}
        post = PostComment.objects.get(pk=comment_id)
        post.admin_tag = admin_tag
        post.save()
        # get refreshed list of commetns for this page
        comments = com.sort_comments(class_id,lecture,slide)
        result = "Reply successfuly added"
        # build a html posts list with the paginated posts
        comments_html = loader.render_to_string(
                                    'lectures/comments.html',
                                    {'comments': comments,
                                    # send user to know if he is auth
                                    'user':request.user}
                                   )
        # package output data and return it as a JSON object
        output_data = {
                        'comments_html': comments_html
        }
        return JsonResponse(output_data)
