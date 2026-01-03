# core/views.py
from django.shortcuts import render, redirect, get_object_or_404
from datetime import timedelta
from django.utils.timezone import now
from django.contrib.auth import login, logout, get_user_model, authenticate
from .models import CustomUser, Submission, Vote
from comments.models import Comment
from django.db.models import Q
from django.db import IntegrityError
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required



from .models import Submission


def home(request):
    sort = request.GET.get('sort', 'top')  
    page_number = request.GET.get('page', 1)

    if sort == 'new':
        submissions_qs = Submission.objects.order_by('-created_at')
    else:
        # TOP = points first, then time
        submissions_qs = Submission.objects.order_by('-points', '-created_at')

    paginator = Paginator(submissions_qs, 20)
    page_obj = paginator.get_page(page_number)

    return render(request, 'home.html', {
        'submissions': page_obj,
        'sort': sort,
        'next_page': page_obj.next_page_number() if page_obj.has_next() else None,
    })


def welcome(request):
    return render(request, "welcome.html")
# Signup view


def signup(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password1 = request.POST.get("password1")
        password2 = request.POST.get("password2")

        # Required fields check
        if not username or not password1 or not password2:
            return render(request, "registration/signup.html", {
                "error": "All fields are required."
            })

        # Password match check
        if password1 != password2:
            return render(request, "registration/signup.html", {
                "error": "Passwords do not match."
            })

        if CustomUser.objects.filter(username=username).exists():
            return render(request, "registration/signup.html", {
                "error": "Username already taken."
            })

        user = CustomUser.objects.create_user(
            username=username,
            email=email,
            password=password1
        )

        login(request, user)
        return redirect("home")

    return render(request, "registration/signup.html")

# Login view


def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect("home")
        else:
            return render(request, "registration/login.html", {
                "error": "Invalid username or password."
            })

    return render(request, "registration/login.html")


def logout_view(request):
    logout(request)
    return redirect("home")


@login_required
def submit(request):
    if request.method == "POST":
        title = request.POST["title"]
        url = request.POST.get("url")
        text = request.POST.get("text")

        Submission.objects.create(
            title=title,
            url=url,
            text=text,
            author=request.user,
        )

        return redirect("home")

    return render(request, "submit.html")


def bookmark(request):
    return render(request, "bookmarklet.html")


@login_required
def item(request, id):
    submission = get_object_or_404(Submission, id=id)

    # Handle new top-level comment
    if request.method == "POST":
        content = request.POST.get("content")
        if content:
            Comment.objects.create(
                submission=submission,
                author=request.user,
                text=content   
            )
            return redirect("item", id=submission.id)

    
    comments = Comment.objects.filter(
        submission=submission,
        parent__isnull=True
    ).order_by("created_at")

    return render(request, "item.html", {
        "submission": submission,
        "comments": comments
    })


@login_required
def upvote(request, submission_id):
    submission = get_object_or_404(Submission, id=submission_id)

    vote = Vote.objects.filter(
        user=request.user,
        submission=submission
    ).first()

    if vote:
        vote.delete()
        submission.points -= 1
        submission.author.karma -= 1
    else:
        Vote.objects.create(
            user=request.user,
            submission=submission
        )
        submission.points += 1
        submission.author.karma += 1

    submission.save()
    submission.author.save()

    return redirect(request.META.get("HTTP_REFERER", "new"))


@login_required
def edit_submission(request, id):
    submission = get_object_or_404(Submission, id=id)

    
    if request.user != submission.author:
        return redirect("item", id=submission.id)

    if request.method == "POST":
        submission.title = request.POST.get("title")
        submission.url = request.POST.get("url")
        submission.text = request.POST.get("text")
        submission.save()
        return redirect("item", id=submission.id)

    return render(request, "edit_submission.html", {
        "submission": submission
    })


@login_required
def delete_submission(request, id):
    submission = get_object_or_404(Submission, id=id)

    
    if request.user != submission.author:
        return redirect("item", id=submission.id)

    submission.delete()
    return redirect("home")


def new_stories(request):
    page_number = request.GET.get('page', 1)
    qs = Submission.objects.order_by('-created_at')

    paginator = Paginator(qs, 30)
    page_obj = paginator.get_page(page_number)

    return render(request, 'home.html', {
        'submissions': page_obj,
        'sort': 'new',
        'next_page': page_obj.next_page_number() if page_obj.has_next() else None,
    })


def past_stories(request):
    days = int(request.GET.get('days', 1))

    target_datetime = now() - timedelta(days=days)

    submissions = Submission.objects.filter(
        created_at__lt=target_datetime
    ).order_by('-created_at')

    return render(request, 'home.html', {
        'submissions': submissions,
        'sort': 'past',
        'days': days
    })


User = get_user_model()


def user_profile(request, username):
    user = get_object_or_404(User, username=username)

    return render(request, "profile.html", {
        "profile_user": user,
    })


def article_count(self):
    return self.submissions.count()


@login_required
def edit_profile(request):
    user = request.user

    if request.method == "POST":
        user.bio = request.POST.get("bio", "")
        user.save()
        return redirect("user_profile", username=user.username)

    return render(request, "edit_profile.html")


User = get_user_model()


def search(request):
    query = request.GET.get("q", "").strip()

    users = []
    submissions = []

    if query:
        
        users = User.objects.filter(username__icontains=query)

        submissions = Submission.objects.filter(
            Q(title__icontains=query) |
            Q(text__icontains=query)
        )

        if users.exists():
            submissions = submissions | Submission.objects.filter(
                author__in=users
            )

        submissions = submissions.distinct()

    return render(request, "search.html", {
        "query": query,
        "users": users,
        "submissions": submissions,
    })
