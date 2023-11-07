from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Comment, Post, Subscribe
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import PostForm, CommentForm, NewsLetterSignupForm
from django.urls import reverse_lazy
from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages

class AboutView(TemplateView):
    template_name = 'about.html'


class PostListView(ListView):
    model = Post

    def get_queryset(self):
        # Zwraca posty, które mają ustawioną datę publikacji i są uporządkowane od najnowszych do najstarszych
        return Post.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')


class PostDetailView(DetailView):
    model = Post


class CreatePostView(LoginRequiredMixin, CreateView):
    login_url = '/login/'
    redirect_field_name = 'blog/post_detail.html'
    form_class = PostForm
    model = Post


class PostUpdateView(LoginRequiredMixin, UpdateView):
    login_url = '/login/'
    redirect_field_name = 'blog/post_detail.html'
    form_class = PostForm
    model = Post


class PostDeleteView(LoginRequiredMixin, DeleteView):
    model = Post
    success_url = reverse_lazy ('post_list')


class DraftListView(LoginRequiredMixin, ListView):
    login_url = '/login/'
    redirect_field_name = 'blog/post_detail.html'
    model = Post

    def get_queryset(self):
        return Post.objects.filter(published_date__isnull=True).order_by('create_date')

@login_required()
def post_publish(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.publish()
    return redirect('post_detail', pk=post.pk)


@login_required
def add_comment_to_post(request, pk):
    post = get_object_or_404(Post, pk=pk)

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = CommentForm
    return render(request, 'blog/comment_form.html', {'form':form})

def comment_approve(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    #Taking from Models and changing it from False to True beacause we taking this def
    comment.approve()
    return redirect('post_detail', pk=comment.post.pk)

@login_required
def comment_edit(request, pk):
    comment = get_object_or_404(Comment, pk=pk)

    if request.method == 'POST':
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            form.save()
            return redirect('post_detail', pk=comment.post.pk)
    else:
        form = CommentForm(instance=comment)

    return render(request, 'blog/comment_form.html', {'form': form})


def comment_remove(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    post_pk = comment.post.pk
    comment.delete()
    return redirect('post_detail', pk=post_pk)


def search_post(request):
    if request.method == "POST":
        searched = request.POST['searched']
        posts = Post.objects.filter(title__contains=searched)
        return render(request, 'blog/search_post.html', {'searched': searched, 'posts': posts})
    else:
        return render(request, 'blog/search_post.html')


def newsletter(request):
    if request.method == 'POST':
        form = NewsLetterSignupForm(request.POST)
        if form.is_valid():
            subscriber, created = Subscribe.objects.get_or_create(
                email=form.cleaned_data['email'], defaults={'name': form.cleaned_data['name']}
            )
            if created:
                try:
                    # Wysyłanie maila powitalnego
                    send_mail(
                        'Subskrypcja Newslettera',
                        'Dziękujemy za zapisanie się do naszego newslettera!',
                        settings.EMAIL_HOST_USER,
                        [subscriber.email],
                        fail_silently=False,
                    )
                    messages.success(request, "Dziękujemy za zapisanie się do newslettera!")  # Wiadomość potwierdzająca
                    return redirect('success_page')  # Przekieruj do strony z potwierdzeniem
                except Exception as e:
                    # Logowanie wyjątku może być tutaj pomocne
                    messages.error(request, "Wystąpił błąd podczas wysyłania wiadomości e-mail.")
            else:
                # Informacja dla użytkownika, że już istnieje subskrypcja
                messages.info(request, "Ten email jest już zapisany na naszą listę mailingową.")
        else:
            # Dodaj komunikaty o błędach formularza, jeśli walidacja nie powiedzie się
            for error in form.errors:
                messages.error(request, form.errors[error])
    else:
        form = NewsLetterSignupForm()

    return render(request, 'newsletter_signup.html', {'form': form})


def success_view(request):
    return render(request, 'success.html')