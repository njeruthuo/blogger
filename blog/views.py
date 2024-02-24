from .models import Post, Comment
from .forms import EmailPostForm, CommentForm


from django.urls import reverse
from django.contrib import messages
from django.core.mail import send_mail
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

# Mixins CBVs
from django.views.generic import ListView


class PostListView(ListView):
    paginate_by = 3
    context_object_name = 'posts'
    queryset = Post.published.all()
    template_name = 'blog/post/list.html'


def post_list(request):
    post_list = Post.published.all()

    paginator = Paginator(post_list, 3)
    page_number = request.GET.get('page', 1)

    try:
        posts = paginator.page(page_number)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    except PageNotAnInteger:
        posts = paginator.page(1)

    return render(request, 'blog/post/list.html', {'posts': posts, 'section': 'blogs'})


@login_required
def post_detail(request, year, month, day, post):
    post = get_object_or_404(Post, status=Post.Status.PUBLISHED,
                             publish__year=year, publish__month=month, publish__day=day, slug=post)
    comments = post.comments.filter(active=True)

    if request.method == 'GET':
        form = CommentForm()

    form = CommentForm(request.POST)

    if form.is_valid():
        comment = form.save(commit=False)
        comment.post = post
        comment.commentator = request.user
        comment.save()
        form = CommentForm()

    return render(request, 'blog/post/detail.html', {'post': post, 'comments': comments, 'form': form})


@login_required
def comment_delete(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    if request.user == comment.commentator:
        comment.delete()
        messages.success(request, 'Comment deleted successfully.')

    # Construct the redirect URL using reverse and accessing the Post object fields correctly
    return redirect(reverse('blog:post_detail', kwargs={'year': comment.post.publish.year,
                                                        'month': comment.post.publish.month,
                                                        'day': comment.post.publish.day,
                                                        'post': comment.post.slug}))


@login_required
def post_share(request, post_id):
    form = EmailPostForm()
    post = get_object_or_404(Post, id=post_id, status=Post.Status.PUBLISHED)
    sent = False

    if request.method == 'POST':
        form = EmailPostForm(request.POST)

        if form.is_valid():
            cd = form.cleaned_data

            # Send email
            post_url = request.build_absolute_uri(post.get_absolute_url())
            subject = f"{request.user.first_name or request.user.username} recommends you read {post.title}"
            message = f"Read: {post.title} at {post_url}\n\n"\
                f"{request.user.username}'s comments: {cd['comments']}"
            send_mail(subject, message,
                      'juliusn411@gmail.com', [cd['send_to']])
            sent = True

    return render(request, 'blog/post/share.html', {'form': form, 'post': post, 'sent': sent})
