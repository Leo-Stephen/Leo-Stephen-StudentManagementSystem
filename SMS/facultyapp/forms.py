from django import forms
from .models import AddCourse
from .models import Marks

class AddCourseForm(forms.ModelForm):
    class Meta:
        model = AddCourse
        fields = ['student', 'course', 'section']

    def __init__(self, *args, **kwargs):
        super(AddCourseForm, self).__init__(*args, **kwargs)
        self.fields['student'].widget.attrs.update({'class': 'form-select'})
        self.fields['course'].widget.attrs.update({'class': 'form-select'})
        self.fields['section'].widget.attrs.update({'class': 'form-select'})

class MarksForm(forms.ModelForm):
    class Meta:
        model = Marks
        fields = ['student', 'course', 'marks']
