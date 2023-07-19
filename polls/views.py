from django.shortcuts import render,redirect, get_object_or_404
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic
from django.utils import timezone

from .models import Choice, Question


class IndexView(generic.ListView):
    template_name = "polls/index.html"
    context_object_name = "latest_question_list"

    def get_queryset(self):
        """Return the last five published questions."""
        return Question.objects.order_by("-pub_date")[:5]


class DetailView(generic.DetailView):
    model = Question
    template_name = "polls/detail.html"


class ResultsView(generic.DetailView):
    model = Question
    template_name = "polls/results.html"


def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST["choice"])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(
            request,
            "polls/detail.html",
            {
                "question": question,
                "error_message": "You didn't select a choice.",
            },
        )
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse("polls:results", args=(question.id,)))
    
def newChoice(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        new_choice=request.POST["new_choice"]
        if not new_choice:
            raise KeyError
    except (KeyError):
    #redisplay the question detail form.
        return render(
            request,
            "polls/addChoice.html",
            {
                "question":question,
                "error_message":"choice could not be added",
            },
        ) 
    else:
        new_choice = Choice(
            question=question,
            choice_text=new_choice
        )
        new_choice.save()
        return HttpResponseRedirect(reverse("polls:detail", args=(question.id,)))
    
    
def reset(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    for choice in question.choice_set.all():
        choice.votes = 0
        choice.save()
    return HttpResponseRedirect(reverse("polls:results", args=(question.id,)))
    
    
# def addQues(request):
#     return render(request, "polls/addQues.html")
def newQues(request):
    try:
        new_question=request.POST["new_ques"]
        if not new_question:
            raise KeyError
    except(KeyError):
        return render(
            request,
            "polls/addQues.html",
            {
                "error_message":"question could not be added",
            },
        )
    else:
        try:
            for question in Question.objects.all():
                if question.question_text==new_question:
                    raise KeyError
        except(KeyError):
            return render(
            request,
            "polls/addQues.html",
            {
                "error_message":"question already exist",
                    }
        )
        else:
            newQues=Question(
            question_text=new_question,
            pub_date = timezone.now(),
                    
        )
    newQues.save()
    return HttpResponseRedirect(reverse("polls:index"))


def editQues(request, id):
    new_question=Question.objects.get(id=id)
    if request.method == 'GET':
        return render(request, 'polls/editQues.html', { "question" : new_question})
    
    if request.method == 'POST':
        new = request.POST.get('input')
        new_question.question_text = new
        new_question.save()
        return render(request, 'polls/detail.html', { 'question':new_question })
    
def deleteQues(request, id):
    if request.method == 'GET':
        new_question=Question.objects.get(id=id)
        new_question.delete()
        return render(request, 'polls/index.html', { 'new_question':new_question })