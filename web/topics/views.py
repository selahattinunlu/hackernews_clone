from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.views.generic import CreateView, DetailView, View
from django.urls import reverse_lazy
from . import forms
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from .models import Topic, Point


# Create your views here.

def index(request):
    topics = Topic.objects.all()
    paginator = Paginator(topics, 25)
    page = request.GET.get('page', 1)
    last_topics = paginator.page(page)

    ctx = {'last_topics': last_topics}
    return render(request, 'topics/index.html', ctx)


def upvote(request, id):
    topic = Topic.objects.get(pk=id)

    if not topic:
        return JsonResponse({
            'key': 'not_found',
            'message': 'Topic is not found.'
        })

    point = Point.objects.filter(topic=topic, user=request.user).first()

    if point:
        point.delete()
        return JsonResponse({
            'key': 'vote_removed',
            'message': 'Vote was removed.'
        })

    point = Point(user=request.user, topic=topic)
    point.save()

    return JsonResponse({
        'key': 'vote_added',
        'message': 'Vote was added.'
    })


class TopicCreateView(LoginRequiredMixin, CreateView):
    template_name = 'topics/create.html'
    form_class = forms.TopicCreateForm
    success_url = reverse_lazy('home')

    def get(self, request):
        form = forms.TopicCreateForm()
        return render(request, self.template_name, {'form': form})

    def form_valid(self, form):
        topic = form.save(commit=False)
        topic.publisher = self.request.user

        if topic.body:
            topic.url = None

        topic.save()
        return super(TopicCreateView, self).form_valid(form)


class TopicDetailView(DetailView):
    template_name = 'topics/detail.html'

    def get(self, request, slug):
        comment_form = forms.CommentCreateForm()
        topic = Topic.objects.filter(slug=slug).first()
        comments = topic.comments.order_by('-id').all()

        if not topic:
            return redirect('home')

        ctx = {'topic': topic, 'comments': comments, 'comment_form': comment_form}
        return render(request, self.template_name, ctx)


class CommentView(View):
    def delete(self, request, comment_id):
        pass


class CommentCreateView(CreateView):
    form_class = forms.CommentCreateForm

    def get(self, request, id):
        topic = Topic.objects.get(pk=id)
        return redirect('topics_detail', slug=topic.slug)

    def form_valid(self, form):
        if not self.request.user:
            return redirect('home')

        topic = Topic.objects.get(pk=form.data['topic_id'])
        comment = form.save(commit=False)
        comment.topic = topic
        comment.user = self.request.user
        comment.save()
        return redirect('topics_detail', slug=topic.slug)
