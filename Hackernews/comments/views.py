# comments/views.py
from django.shortcuts import redirect, get_object_or_404, render
from django.contrib.auth.decorators import login_required
from core.models import Submission
from .models import Comment


@login_required
def add_comment(request, submission_id):
    submission = get_object_or_404(Submission, id=submission_id)

    if request.method == "POST":
        content = request.POST.get("content")
        parent_id = request.POST.get("parent_id")
        parent = Comment.objects.get(id=parent_id) if parent_id else None
        if content:
            Comment.objects.create(
                submission=submission,
                author=request.user,
                text=content,
                parent=parent
            )
        return redirect('item', id=submission.id)


def item_detail(request, id):
    submission = get_object_or_404(Submission, id=id)
    comments = Comment.objects.filter(submission=submission, parent=None)
    return render(
        request, 'item_detail.html', {
            'submission': submission, 'comments': comments})


def show_comments(request):
    comments = (
        Comment.objects
        .select_related("author", "submission",)
        .order_by("-created_at")
    )

    return render(
        request,
        "comments/show_comment.html",
        {"comments": comments}
    )


@login_required
def edit_comment(request, pk):
    comment = get_object_or_404(Comment, pk=pk)

    if comment.author_id != request.user.id:
        return redirect("item", id=comment.submission.id)

    if request.method == "POST":
        comment.text = request.POST.get("text")
        comment.save()
        return redirect("item", id=comment.submission.id)

    return render(request, "comments/edit_comment.html", {
        "comment": comment
    })


@login_required
def delete_comment(request, pk):
    comment = get_object_or_404(Comment, pk=pk)

    if comment.author_id != request.user.id:
        return redirect("item", id=comment.submission.id)

    if request.method == "POST":
        submission_id = comment.submission.id
        comment.delete()
        return redirect("item", id=submission_id)

    return render(request, "comments/delete_comment.html", {
        "comment": comment
    })
