from django.forms import ModelForm , ModelChoiceField
from .models import Problem  , TestCase , Problemset , Contest , Team , Contestant , Submission
from django.contrib.admin import widgets

class ProblemForm(ModelForm):
    class Meta:
        model = Problem
        fields = ['Problem_Name',
        			'statement',
        			'solution',
        			'solution_language', 
        			'Time_limit',
        			'Memory_limit',
        ]

class TestCaseForm(ModelForm):
    class Meta:
        model = TestCase
        fields = ['Input',]

class ContestForm(ModelForm):
    class Meta:
        model = Contest
        fields = [  
            'name' ,
            'description' ,
            'difficulity' ,
            'duration' ,
            'date' ,
            'time',
        ]
        widgets = {
            'duration': widgets.AdminTimeWidget(),
            'date': widgets.AdminDateWidget(),
            'time': widgets.AdminTimeWidget(),

        }

class ProblemsetForm(ModelForm):
    class Meta:

        model = Problemset
        fields = [  
            'problem' ,
            'index' ,
            'score' ,

        ]
        

class TeamForm(ModelForm):
    class Meta:
        model = Team
        fields = [
            'name',
            'slogan',
        ]

class ContestantForm(ModelForm):
    class Meta:
        model = Contestant
        fields = [  
            'team' ,
        ]


class SubmissionForm(ModelForm):
    class Meta:
        model = Submission
        fields = [	'Code',
        			'Code_language',
        ]
