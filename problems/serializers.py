from .models import Problem, Submission , TestCase
from rest_framework import serializers


class ProblemSerializer(serializers.HyperlinkedModelSerializer):
    testcases = serializers.HyperlinkedIdentityField(view_name="problems:testcase-detail")

    class Meta:
        model = Problem
        fields = ('Problem_Name' , 'statement', 'solution', 'solution_language', 'Time_limit','Memory_limit', 'testcases' )


class SubmissionSerializer(serializers.HyperlinkedModelSerializer):
    problem = serializers.CharField(source='problem.id')


    class Meta:
        model = Submission
        fields = ('problem', 'Code', 'Code_language', 'Verdict','Time','Memory','Score')
        read_only_fields = ('Verdict', 'Time','Memory','Score')



class TestCaseSerializer(serializers.HyperlinkedModelSerializer):
    problem = serializers.CharField(source='problem.id')


    class Meta:
        model = TestCase
        fields = ('problem', 'Input','Output')
        read_only_fields = ('Output',)