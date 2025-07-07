from django.db import models

class Question(models.Model):  # 또는 Project
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.question_text
    
    def average_score(self):
        scores = self.score_set.all()
        total = sum(score.score_value * score.count for score in scores)
        total_votes = sum(score.count for score in scores)
        if total_votes == 0:
            return 0
        return round(total / total_votes, 2)
    average_score.short_description = '평균 점수'

class Score(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    score_value = models.IntegerField()  # 1~5점
    count = models.IntegerField(default=0)  # 이 점수를 누른 사람 수

    class Meta:
        unique_together = ('question', 'score_value')  # 1질문당 1점~5점 각각 1개만
    
    def average_score(self):
        scores = self.score_set.all()
        total = sum(score.score_value * score.count for score in scores)
        total_votes = sum(score.count for score in scores)
        if total_votes == 0:
            return 0
        return round(total / total_votes, 2)
    
    def __str__(self):
        return f"{self.question} - {self.score_value}점 ({self.count}명)"
