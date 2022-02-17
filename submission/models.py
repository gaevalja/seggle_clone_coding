from django.db import models
from account.models import User
from competition.models import Competition
from problem.models import Problem
from classes.models import Class
from contest.models import Contest, Contest_problem
from utils.common import upload_to_submission

# Create your models here.

class Path(models.Model):
    username = models.ForeignKey(User, on_delete=models.CASCADE, db_column="username", to_field="username")
    path = models.TextField()
    problem_id = models.ForeignKey(Problem, on_delete=models.CASCADE, db_column="problem_id")
    score = models.FloatField(null=True)
    created_time = models.DateTimeField(auto_now_add=True)
    ip_address = models.TextField(null=True)
    on_leaderboard = models.BooleanField(default=False) # 1이면 leaderboard에 보이고 0이면 보이지 않음
    status = models.IntegerField(default=0) # 0이면 문제 없음 , 1이면 에러 발생

    class Meta:
        db_table = "path"

class SubmissionClass(models.Model):
    username = models.ForeignKey(User, on_delete=models.CASCADE, db_column="username", to_field="username")
    path = models.ForeignKey(Path, on_delete=models.CASCADE, db_column="path")
    class_id = models.ForeignKey(Class, on_delete=models.CASCADE, db_column="class_id")
    contest_id = models.ForeignKey(Contest, on_delete=models.CASCADE, db_column="contest_id")
    c_p_id = models.ForeignKey(Contest_problem, on_delete=models.CASCADE, db_column="c_p_id")
    csv = models.FileField(blank=True,null=True,upload_to=upload_to_submission)
    ipynb = models.FileField(blank=True,null=True,upload_to=upload_to_submission)
    
    class Meta:
        db_table = "submission_class"

class SubmissionCompetition(models.Model):
    username = models.ForeignKey(User, on_delete=models.CASCADE, db_column="username", to_field="username")
    path = models.ForeignKey(Path, on_delete=models.CASCADE, db_column="path")
    competition_id = models.ForeignKey(Competition, on_delete=models.CASCADE, db_column="competition_id")
    csv = models.FileField(blank=True,null=True,upload_to=upload_to_submission)
    ipynb = models.FileField(blank=True,null=True,upload_to=upload_to_submission)
    
    class Meta:
        db_table = "submission_competition"