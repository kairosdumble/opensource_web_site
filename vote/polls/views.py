from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from .models import Question, Score
from django.db.models import Sum, F, IntegerField

def index(request):
    latest_question_list = Question.objects.all().order_by('-pub_date')
    return render(request, 'polls/index.html', {'latest_question_list': latest_question_list})

def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/detail.html', {'question': question})

def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_score = int(request.POST['score_value'])
        score_obj, created = Score.objects.get_or_create(
            question=question,
            score_value=selected_score
        )
        score_obj.count += 1
        score_obj.save()
    except (KeyError, ValueError):
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "점수를 선택해주세요.",
        })
    return HttpResponseRedirect(reverse('polls:vote_result', args=(question.id,)))

def vote_result(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    score_stats = Score.objects.filter(question=question).order_by('-score_value')

    total_score = sum(score.score_value * score.count for score in score_stats)
    total_votes = sum(score.count for score in score_stats)
    avg_score = round(total_score / total_votes, 2) if total_votes > 0 else 0

    return render(request, 'polls/vote.html', {
        'question': question,
        'score_stats': score_stats,
        'total_score': total_score,
        'avg_score': avg_score,
        'total_votes': total_votes,
    })
