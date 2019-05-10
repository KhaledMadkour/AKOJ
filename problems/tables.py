import django_tables2 as tables
from django_tables2.utils import A
from .models import Submission , Contest , Contestant
class SubmissionTable(tables.Table):
    id = tables.LinkColumn('problems:submission', args=[ A('pk')], orderable=False)
    class Meta:
        model = Submission
        fields = [
        'id',
        'date_added',
        'problem',
        'contestant.team',
        'Code_language',
        'Verdict',
        'Time',
        'Memory',
        'Score',
        ]
