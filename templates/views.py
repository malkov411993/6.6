from django.contrib.auth.mixins import (
    LoginRequiredMixin, PermissionRequiredMixin)
from django.views.generic import (
    ListView, DetailView, CreateView, UpdateView, DeleteView)
from news.models import Post, Category
from news.forms import PostForm
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404, redirect
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.core.cache import cache

class PostDetail(DetailView):
    model = Post
    template_name = 'post.html'
    context_object_name = 'post'
    queryset = Post.objects.all()

    def get_object(self, *args, **kwargs):
        obj = cache.get(f'post-{self.kwargs["pk"]}', None)
        if not obj:
            obj = super().get_object(queryset=self.queryset)
            cache.set(f'post-{self.kwargs["pk"]}', obj)
        return obj


class PostCreate(PermissionRequiredMixin, LoginRequiredMixin, CreateView):
    permission_required = ('news.add_post',)
    form_class = PostForm
    model = Post
    template_name = 'edit.html'

    def form_valid(self, form):
        post = form.save(commit=False)
        if self.request.path == '/news/create/':
            post.content_type = 'новость'
        elif self.request.path == '/articles/create/':
            post.content_type = 'статья'
        return super().form_valid(form)


class PostEdit(PermissionRequiredMixin, LoginRequiredMixin, UpdateView):
    permission_required = ('news.change_post',)
    form_class = PostForm
    model = Post
    template_name = 'edit.html'
    success_url = reverse_lazy('post_detail')


class PostDelete(PermissionRequiredMixin, LoginRequiredMixin, DeleteView):
    permission_required = ('news.delete_post',)
    model = Post
    template_name = 'delete.html'
    success_url = reverse_lazy('news')


class CategoryList(ListView):
    model = Category
    template_name = 'categories.html'
    context_object_name = 'categories'


class PostOfCategoryList(ListView):
    model = Post
    ordering = '-id'
    template_name = 'news.html'
    context_object_name = 'posts'

    def get_queryset(self):
        self.queryset = Category.objects.get(
            pk=self.kwargs['pk']).PostCategory.all()
        return super().get_queryset()


def subscribe_to_category(request, pk):
    category = get_object_or_404(Category, pk=pk)
    if request.user.is_authenticated:
        category.subscribers.add(request.user)
    return redirect('posts_of_categories_list', pk=pk)


def send_news_notification(user_email, category, news):
    subject = f"Новая статья в категории {category}"
    html_message = render_to_string('email/notification.html',
                                    {'category': category, 'news': news})
    plain_message = strip_tags(html_message)
    send_mail(subject, plain_message, 'your_email@example.com',
              [user_email], html_message=html_message)
