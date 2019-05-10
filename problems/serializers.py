from .models import Problem, Submission , TestCase
from rest_framework import serializers


class ProblemSerializer(serializers.ModelSerializer):

    class Meta:
        model = Problem
        fields = ('Problem_Name' , 'statement', 'solution', 'solution_language', 'Time_limit','Memory_limit', 'testcases' )
        read_only_fields = ('testcases',)

class SubmissionSerializer(serializers.ModelSerializer):


    class Meta:
        model = Submission
        fields = ('problem', 'Code', 'Code_language', 'Verdict','Time','Memory','Score')
        read_only_fields = ('Verdict', 'Time','Memory','Score')



class TestCaseSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = TestCase
        fields = ('problem', 'Input','Output')
        read_only_fields = ('Output',)