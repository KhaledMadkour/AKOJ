from django.db import models
from django.contrib.auth.models import User
from django.contrib.admin import widgets


Languages = (
    ('py', 'Python'),
    ('cpp', 'C++'),
    ('c', 'C Language'),
    ('java', 'Java'),
)

Verdicts = (
    ('ACC', 'Accepted'),
    ('TLE', 'Time Limit Exceeded'),
    ('WA', 'Wrong Answer'),
    ('MLE', 'Memory Limit Exceeded'),
)

Difficulity = (
    ('Easy' , 'Easy'),
    ('Medium' , 'Medium'),
    ('Hard' , 'Hard'),
    ('Insane' , 'Insane'),
)

class Problem(models.Model):
    Problem_Name = models.CharField(max_length = 10)
    statement = models.TextField()
    solution = models.TextField()
    solution_language = models.CharField(max_length=4, choices=Languages)
    Time_limit = models.DecimalField(max_digits=5, decimal_places=3)
    Memory_limit = models.DecimalField(max_digits=1000, decimal_places=8)
    date_added = models.DateTimeField (auto_now_add = True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE , null = True )   
    def __str__(self):
        return self.Problem_Name

    class Meta:
        ordering = ('date_added' , )

class TestCase(models.Model):
    problem = models.ForeignKey(Problem, related_name='testcases', on_delete=models.CASCADE)
    Input  = models.TextField()
    Output = models.TextField()

    def __str__(self):
        return "test case {} for problem {}".format(self.pk, self.problem.Problem_Name)


class Contest(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=255)
    difficulity = models.CharField(max_length=6, choices=Difficulity)
    duration = models.TimeField()
    date = models.DateField()
    time = models.TimeField()


    def __str__(self):
        return self.name

class Problemset(models.Model):
    problem = models.ForeignKey(Problem, on_delete=models.CASCADE)
    contest = models.ForeignKey(Contest, on_delete=models.CASCADE)
    score = models.IntegerField()
    index = models.CharField(max_length=2)

    class Meta:
        ordering = ('contest' , 'index',)

    def __str__(self):
        return "Problemset {}. {} in contest {} ".format(self.index, self.problem,self.contest)
 
class Team(models.Model):
    members = models.ManyToManyField(User)
    name = models.CharField(max_length=20 , unique=True)
    slogan = models.CharField(max_length=20, default=None, blank=True, null=True)
    def __str__(self):
        return self.name


class Contestant(models.Model):
    contest = models.ForeignKey(Contest, on_delete=models.CASCADE) 
    team = models.ForeignKey(Team, on_delete=models.CASCADE) 

    def __str__(self):
        return " {} , {}  ".format(self.team.name , self.contest.name)

class Submission(models.Model):
    problem = models.ForeignKey(Problem, on_delete=models.CASCADE)
    contestant = models.ForeignKey(Contestant , on_delete=models.CASCADE , null = True) 
    Code = models.TextField()
    Code_language = models.CharField(max_length=4, choices=Languages)
    Verdict = models.CharField(max_length=4, choices=Verdicts)
    Time = models.DecimalField(max_digits=5, decimal_places=3 ,default=None, blank=True, null=True)
    Memory = models.DecimalField(max_digits=5, decimal_places=3 ,default=None, blank=True, null=True)
    Score = models.DecimalField(max_digits=5, decimal_places=3 ,default=None, blank=True, null=True)
    date_added = models.DateTimeField (auto_now_add = True)

    def __str__(self):
         return " {} , {} , {} ".format(self.id , self.problem , self.contestant )



