#report/views
from django.http import HttpResponse
from django.shortcuts import render
import csv
from comments.models import PostComment
from user_management.models import Student, User
from django.db.models import Count

class Data():
    def __init__(self):
        self.tag_names = ['general feedback', 'improvement', 'mistake']
        self.general_feedback = 0
        self.improvement = 0
        self.mistake = 0
        self.total = 1
    def get_data_tags(self, person, comments):
        one = comments.filter(author_id=person)          
        tags = one.values_list("user_tag").annotate(Count("user_tag"))
        for tag in tags:
            self.total = one.count()
            if tag[0] == self.tag_names[0]:
                self.general_feedback = tag[1]
            elif tag[0] == self.tag_names[1]:
                self.improvement = tag[1]
            elif tag[0] == self.tag_names[2]:
                self.mistake = tag[1]

    def get_data_user(self, person):
        u = User.objects.get(username=person)
        self.first_name = u.first_name
        self.last_name = u.last_name
        s = Student.objects.get(pk = u.id)
        self.student_id = s.student_id

def report_comments(request, document_id):
    # Create the HttpResponse object with the appropriate CSV header.
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="report_activity_in_comments.csv"'
    comments = PostComment.objects.filter(class_id_id = document_id)
    people = comments.values_list("author_id", flat=True).distinct()
    
    # Start writing header
    writer = csv.writer(response)
    writer.writerow(['first_name', 'last_name', 'student_id', 'total_number','general_feedback','improvement','mistake'])
    
    data = Data()
    for person in people:
        u = User.objects.get(username=person)
        if u.is_student == True:
            data.get_data_tags(person, comments)
            data.get_data_user(person)

            # write row for person
            writer.writerow([data.first_name, data.last_name, data.student_id, data.total,data.general_feedback, data.improvement , data.mistake ])

    
    return response