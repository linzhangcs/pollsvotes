from django.shortcuts import render, get_object_or_404
from django.template import loader
from django.http import Http404, HttpResponseRedirect, HttpResponse
from django.urls import reverse

from .models import Question, Choice
# Create your views here.

def index(request):
    # return HttpResponse("Hello world, you are at my poll site")
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    # output = ', '.join([q.question_text for q in latest_question_list])
    # template = loader.get_template('polls/index.html')
    context = {
        'latest_question_list': latest_question_list
    }
    # return HttpResponse(template.render(context, request))
    return render(request, 'polls/index.html', context)


def detail(request, question_id):
    # try:
    #     question = Question.objects.get(pk=question_id)
    # except Question.DoesNotExist:
    #     raise Http404(" This question does not exist")
    # return render(request, 'polls/detail.html', {'question': question})
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/detail.html', {'question': question})

def results(request, question_id):
    # response = "you're looking at the results of question %s." % question_id
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/result.html', {'question': question})

def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        vote = question.choice_set.get(pk=request.POST['choice'])
    except(KeyError, Choice.DoesNotExist):
        return render(request, 'polls/detail.html', {'question': question, 'error_message': "you didn't select a choice"})
    else:
        vote.votes += 1
        vote.save()
    return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))
    # return HttpResponse("you're voting on question %s." % question_id)

