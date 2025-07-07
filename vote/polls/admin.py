from django.contrib import admin
from django.db.models import Sum, F, FloatField, ExpressionWrapper
from .models import Question, Score

class QuestionAdmin(admin.ModelAdmin):
    list_display = ('question_text', 'average_score_display', 'pub_date')
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        qs = qs.annotate(
            total_score=Sum(F('score__score_value') * F('score__count')),
            total_count=Sum('score__count')
        ).annotate(
            average_score=ExpressionWrapper(
                F('total_score') * 1.0 / F('total_count'),
                output_field=FloatField()
            )
        )
        return qs

    def average_score_display(self, obj):
        avg = getattr(obj, 'average_score', None)
        return round(avg, 2) if avg is not None else 0

    average_score_display.short_description = '평균 점수'
    average_score_display.admin_order_field = 'average_score'
admin.site.register(Question, QuestionAdmin)
admin.site.register(Score)
