from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse , Http404
from django.urls import reverse
from django.core.exceptions import *

from django.contrib.auth.models import User
from ..models import Problem,  TestCase , Problemset , Contest , Team , Contestant , Submission
from ..forms import ProblemForm , TestCaseForm , ContestForm , ProblemsetForm , TeamForm , ContestantForm , SubmissionForm
from ..tables import SubmissionTable
from ..compilar import Compilar

def home_view(request):
    """The home page for Online judge"""
    return render(request , 'problems/home.html')

def problems_view(request):
    """show all problems"""
    problems_view_obj = Problem.objects.all().order_by('date_added')
    context = {'problems_obj' :problems_view_obj}
    return render(request, 'problems/problems.html', context)


def problem_view(request ,  problem_id ):
    problem_view_obj = Problem.objects.get(id=problem_id)
    test_cases = TestCase.objects.all().filter( problem = problem_id )
    context = {'problem_obj': problem_view_obj , 'test_cases' : test_cases}
    return render(request, 'problems/problem.html', context)    

@login_required
def new_problem(request):
    """ Add new new_problem"""
    if request.method != 'POST':
        # No data submitted; create a blank form.
        form = ProblemForm()
    else:
        # POST data submitted; process data.
        form = ProblemForm(request.POST)
        if form.is_valid():
            new_problem = form.save(commit=False)
            new_problem.owner = request.user
            new_problem.save()
            return HttpResponseRedirect(reverse('problems:problem_view',
                                            args=[new_problem.id]))
    
    context = {'form':form}
    return render (request , 'problems/new_problem.html',context)

@login_required
def new_test_case(request, problem_id):
    problem = Problem.objects.get(id=problem_id)
    test_cases = TestCase.objects.all().filter( problem = problem_id )
    if request.method != 'POST':
        # No data submitted; create a blank form.
        form = TestCaseForm()
    else:
        # POST data submitted; process data.
        form = TestCaseForm(data=request.POST)
        if form.is_valid():
            new_test_case = form.save(commit=False)
            new_test_case.problem = problem
            Compile_TestCase(new_test_case)
            new_test_case.save()
            return HttpResponseRedirect(reverse('problems:new_test_case',
                                            args=[problem_id]))
    context = {'problem_obj': problem, 'form': form , 'test_cases' : test_cases}
    return render(request, 'problems/new_test_case.html', context)

def Compile_TestCase(created_testcase):

    code_language = created_testcase.problem.solution_language
    source_code = created_testcase.problem.solution

    compilar = Compilar(source_code, code_language)

    if compilar.language != 'python':
        result = compilar.compile(compilar.file_name)
        print("compilation result : {}".format(compilar.codes[result]))

    result = compilar.run(created_testcase.Input, created_testcase.problem.Time_limit)
    if compilar.codes[result] == 'success':
        created_testcase.Output = open(compilar.program_output, "r").read()


def test_cases(request , problem_id):
    """show all TestCases"""
    test_cases = TestCase.objects.all().filter( problem = problem_id )
    context = {'test_cases' :test_cases , 'problem_id' : problem_id}
    return render(request, 'problems/test_cases.html', context)


@login_required
def edit_test_case(request, test_case_id):
    test_case = TestCase.objects.get(id=test_case_id)
    problem = test_case.problem

    if problem.owner != request.user:
        raise Http404

    if request.method != 'POST':
        # No data submitted; create a blank form.
        form = TestCaseForm(instance=test_case)
    else:
        # POST data submitted; process data.
        form = TestCaseForm(instance=test_case, data=request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('problems:test_cases',
                                            args=[test_case.problem.id]))
    context = {'test_case_obj':test_case, 'problem_obj': problem, 'form': form}
    return render(request, 'problems/edit_test_case.html', context)

def contests(request):
    """show all Contests"""
    contests = Contest.objects.all()
    context = {'contests' :contests}
    return render(request, 'problems/contests.html', context)

def contest(request , contest_id , contestant_id = 0):
    contest = Contest.objects.get(id=contest_id)
    problem_set = Problemset.objects.all().filter( contest = contest_id )
    if (contestant_id):
        contestant = Contestant.objects.get(id = contestant_id )
        context = {'contest': contest  , 'problem_set' :problem_set , 'contestant' : contestant}
    else:
        context = {'contest': contest  , 'problem_set' :problem_set}
    return render(request, 'problems/contest.html', context)    

@login_required
def new_contest(request):
    """ Add new new_contest"""
    if request.method != 'POST':
        # No data submitted; create a blank form.
        form = ContestForm()
    else:
        # POST data submitted; process data.
        form = ContestForm(request.POST)
        if form.is_valid():
            new_contest = form.save(commit=False)
            new_contest.owner = request.user
            new_contest.save()
            return HttpResponseRedirect(reverse('problems:contests'))
    
    context = {'form':form}
    return render (request , 'problems/new_contest.html',context)

@login_required
def new_problem_set(request, contest_id):
    contest = Contest.objects.get(id=contest_id)
    problem_sets = Problemset.objects.all().filter( contest = contest_id )
    if request.method != 'POST':
        # No data submitted; create a blank form.
        form = ProblemsetForm()
    else:
        # POST data submitted; process data.
        form = ProblemsetForm(data=request.POST)
        if form.is_valid():
            new_problem_set = form.save(commit=False)
            new_problem_set.contest = contest
            form.save()
            return HttpResponseRedirect(reverse('problems:contest',
                                            args=[contest_id]))
    context = {'problem_sets': problem_sets, 'form': form , 'contest' : contest}
    return render(request, 'problems/new_problem_set.html', context)

def problem_contest(request , problem_contest_id , contestant_id ):
    problem_contest = Problemset.objects.get( id = problem_contest_id )
    contestant =  Contestant.objects.get(id= contestant_id)
    context = {'problem_contest' :problem_contest , 'contestant' : contestant }
    return render(request, 'problems/problem_contest.html', context)


def teams(request):
    """show all problems"""
    teams = Team.objects.all()
    context = {'teams' :teams}
    return render(request, 'problems/teams.html', context)

def team (request, team_id):
    team = Team.objects.get(id = team_id)
    members = team.members.all()
    context = {'team' : team , 'members' : members }
    return render(request, 'problems/team.html', context)

def search(request , team_id):
    if request.method == 'POST':
        search_id = request.POST.get('textfield', None)
        try:
            usr = User.objects.get(username = search_id)
            team = Team.objects.get(id = team_id)
            team.members.add(usr)
            return HttpResponseRedirect(reverse('problems:new_team_member',
                                            args=[team_id]))
        except User.DoesNotExist:
            return HttpResponse("no such user")  
    else:
        return render(request, 'problems/new_team.html')

@login_required
def new_team(request , new_team_id = 0):
    """ Add new new_problem"""
    users = User.objects.all()
    if (new_team_id):
        team = Team.objects.get(id = new_team_id)
        members = team.members.all()
    else:
        team = Team.objects.all()
        members = []


    if request.method != 'POST':
        # No data submitted; create a blank form.
        form = TeamForm()
    else:
        # POST data submitted; process data.
        form = TeamForm(request.POST)
        if form.is_valid():
            new_team = form.save()
            new_team.members.add(request.user)
            new_team.save()
            return HttpResponseRedirect(reverse('problems:new_team_member',
                                            args=[new_team.id]))
    
    context = {'form':form , 'members' : members , 'new_team_id' : new_team_id , 'users' : users}
    return render (request , 'problems/new_team.html',context)
@login_required



def contestants(request , contest_id):
    contestants = Contestant.objects.all().filter(contest = contest_id)
    conext = { 'contestants' : contestants , 'contest_id' : contest_id }
    return render(request, 'problems/contestants.html' , conext )


@login_required
def new_contestant(request , contest_id):
    contest = Contest.objects.get(id=contest_id)
    if request.method != 'POST':
        # No data submitted; create a blank form.
        form = ContestantForm()
    else:
        # POST data submitted; process data.
        form = ContestantForm(data=request.POST)
        if form.is_valid():
            new_contestant = form.save(commit=False)
            new_contestant.contest = contest
            form.save()
            return HttpResponseRedirect(reverse('problems:contest_contestant',
                                            args=[contest_id , new_contestant.id ]))
    context = {'form': form , 'contest' : contest}
    return render(request, 'problems/new_contestant.html', context)

def submissions(request , contest_id):
    """show all submissions"""
    contestants = Contestant.objects.filter(contest = contest_id)
    q = Submission.objects.filter(contestant__in = contestants).order_by('date_added')

    submission_table = SubmissionTable(q)
    context = {'submission_table' : submission_table , 'q' : q}
    return render(request, 'problems/submissions.html', context)

def submission (request , submission_id):
    submission = Submission.objects.get(id = submission_id)
    context = {'submission' : submission }
    return render (request , 'problems/submission.html' , context)

@login_required
def new_submission(request , contestant_id ,problem_contest_id  ):
    problem_contest = Problemset.objects.get( id = problem_contest_id )
    problem = problem_contest.problem
    contestant =  Contestant.objects.get(id = contestant_id)
    if request.method != 'POST':
        # No data submitted; create a blank form.
        form = SubmissionForm()
    else:
        # POST data submitted; process data.
        form = SubmissionForm(data=request.POST)
        if form.is_valid():
            new_submission = form.save(commit=False)
            new_submission.problem = problem
            new_submission.contestant = contestant
            Compile_Submissions( new_submission )
            form.save()
            return HttpResponseRedirect(reverse('problems:submissions',
                                            args=[contestant.contest.id]))
    context = {'form': form  , 'contestant' : contestant , 'problem_contest' : problem_contest }
    return render(request, 'problems/new_submission.html', context)


def Compile_Submissions(created_submission ):
    code_language = created_submission.Code_language
    source_code = created_submission.Code

    compilar = Compilar(source_code, code_language)

    if compilar.language != 'python':
        result = compilar.compile(compilar.file_name)
        print("compilation result : {}".format(compilar.codes[result]))

    Accepted = True
    i=0
    tescases = TestCase.objects.filter(problem = created_submission.problem )
    for testcase in tescases:
        i+=1
        result = compilar.run(testcase.Input, created_submission.problem.Time_limit)
        print("{} on test case :{}".format(compilar.codes[result],i))
        Accepted = Accepted and compilar.match(testcase.Output)
        if Accepted == False:
            print("faild on test case".format(i))
            break

    Verdict = "ACC" if Accepted == True else "WA"
    created_submission.Verdict = Verdict
    created_submission.save()

"""I don't remember why I made them , they serve zero purpose ,  still afraid to delete them """

