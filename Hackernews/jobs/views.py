
from django.contrib.auth.decorators import login_required
from core.models import Submission
from django.utils import timezone
from datetime import timedelta
from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator


@login_required
def submit_job(request):
    if request.method == "POST":
        title = request.POST.get("title")
        url = request.POST.get("url")
        text = request.POST.get("text")

        if not title:
            return render(request, "jobs/submit_job.html", {
                "error": "Title is required"
            })

        Submission.objects.create(
            title=title,
            url=url,
            text=text,
            submission_type=Submission.JOB,
            author=request.user
        )

        return redirect("jobs:jobs")

    return render(request, "jobs/submit_job.html")


def jobs(request):

    thirty_days_ago = timezone.now() - timedelta(days=30)

    Submission.objects.filter(
        submission_type=Submission.JOB,
        created_at__lt=thirty_days_ago
    ).delete()

    job_list = Submission.objects.filter(
        submission_type=Submission.JOB
    ).order_by('-created_at')

    paginator = Paginator(job_list, 15)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)
    next_page = page_obj.next_page_number() if page_obj.has_next() else None
    
    return render(request, 'jobs/jobs.html', {
        'jobs': page_obj,
        'next_page': next_page
    })


@login_required
def edit_job(request, pk):
    job = get_object_or_404(
        Submission,
        pk=pk,
        submission_type=Submission.JOB
    )

    if job.author != request.user:
        return redirect("jobs:jobs")

    if request.method == "POST":
        job.title = request.POST.get("title")
        job.url = request.POST.get("url")
        job.text = request.POST.get("text")
        job.save()
        return redirect("jobs:jobs")

    return render(request, "jobs/edit_job.html", {
        "job": job
    })


@login_required
def delete_job(request, pk):
    job = get_object_or_404(
        Submission,
        pk=pk,
        submission_type=Submission.JOB
    )

    
    if job.author != request.user:
        return redirect("jobs:jobs")

    if request.method == "POST":
        job.delete()
        return redirect("jobs:jobs")

    return render(request, "jobs/delete_job.html", {
        "job": job
    })
