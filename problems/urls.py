from django.urls import include, path
from rest_framework import routers
from problems.views import api, problems

router = routers.DefaultRouter()
router.register(r'problem', api.ProblemViewSet)
router.register(r'testcase', api.TestCaseViewSet)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('api/', include(router.urls)),
    path('api/submission/', api.SubmissionViewSet.as_view()),

    # Home page
	path('', problems.home_view, name='home'),

    #problems
	path('problems/', problems.problems_view, name='problems_view'),
    path('problems/<int:problem_id>/' , problems.problem_view , name ='problem_view'),
    path('new_Problem/', problems.new_problem , name ='new_problem'),

    #testcases
    path('test_cases/<int:problem_id>/', problems.test_cases , name ='test_cases'),
    path('new_test_case/<int:problem_id>/', problems.new_test_case, name='new_test_case'),
    path('edit_test_case/<int:test_case_id>/', problems.edit_test_case,name='edit_test_case'),

    #contests
    path('contests/', problems.contests, name='contests'),
    path('contests/<int:contest_id>/' , problems.contest , name ='contest'),
    path('new_contest/', problems.new_contest , name ='new_contest'),

    #problemsets
    path('new_problem_set/<int:contest_id>/', problems.new_problem_set, name='new_problem_set'),
    
    #teams
    path('teams/', problems.teams, name='teams'),
    path('teams/<int:team_id>/' , problems.team, name = 'team'),
    path('new_team/', problems.new_team , name ='new_team'),
    path('new_team/<int:new_team_id>/', problems.new_team , name ='new_team_member'),

    #contestants
    path('contestants/<int:contest_id>/' , problems.contestants , name ='contestants'),
    path('new_contestant/<int:contest_id>/', problems.new_contestant, name='new_contestant'),
    path('contests/<int:contest_id>/contestants/<int:contestant_id>/' , 
        problems.contest , name ='contest_contestant'),
    path('problem_contest/<int:problem_contest_id>/contestants/<int:contestant_id>/' , problems.problem_contest , name ='problem_contest'),

    #serch users
    path('search/<int:team_id>' , problems.search , name= 'search'),

    #sumissions
    path('submissions/contest/<int:contest_id>', problems.submissions, name='submissions'),
    path('submissions/<int:submission_id>', problems.submission, name='submission'),
    path('contestants/<int:contestant_id>/<int:problem_contest_id>/new_submission/' , problems.new_submission , name ='new_submission'),


]