from django.db.models import Q, Count
from django.shortcuts import get_object_or_404
from django.views.generic import ListView, DetailView

from .models import Post, Category


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------
def _published():
    """Base queryset of published posts with related data prefetched."""
    return (
        Post.objects
        .filter(status=Post.Status.PUBLISHED)
        .select_related("category")
        .prefetch_related("tags")
    )


def _categories_with_counts():
    """Categories that actually have at least one published post."""
    return (
        Category.objects
        .annotate(post_count=Count(
            "posts",
            filter=Q(posts__status=Post.Status.PUBLISHED),
        ))
        .filter(post_count__gt=0)
        .order_by("name")
    )


def _attach_reading_time(post):
    """Compute a reading-time (minutes) if the model doesn't provide one."""
    if getattr(post, "reading_time", None):
        return post.reading_time
    content = getattr(post, "content", "") or ""
    words = len(content.split())
    return max(1, round(words / 200))


# ---------------------------------------------------------------------------
# List views
# ---------------------------------------------------------------------------
class PostListView(ListView):
    model = Post
    template_name = "blog/list.html"
    context_object_name = "posts"
    paginate_by = 9

    def get_queryset(self):
        qs = _published().order_by("-published_at", "-pk")

        q = self.request.GET.get("q", "").strip()
        if q:
            qs = qs.filter(
                Q(title__icontains=q)
                | Q(content__icontains=q)
                | Q(excerpt__icontains=q)
            )

        category_slug = self.request.GET.get("category", "").strip()
        if category_slug:
            qs = qs.filter(category__slug=category_slug)

        return qs

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["categories"] = _categories_with_counts()
        ctx["query"] = self.request.GET.get("q", "")
        ctx["current_category"] = None
        return ctx


class CategoryView(ListView):
    template_name = "blog/list.html"
    context_object_name = "posts"
    paginate_by = 9

    def get_queryset(self):
        self.category = get_object_or_404(Category, slug=self.kwargs["slug"])
        return (
            _published()
            .filter(category=self.category)
            .order_by("-published_at", "-pk")
        )

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["categories"] = _categories_with_counts()
        ctx["current_category"] = self.category
        ctx["query"] = ""
        return ctx


# ---------------------------------------------------------------------------
# Detail view
# ---------------------------------------------------------------------------
class PostDetailView(DetailView):
    model = Post
    template_name = "blog/detail.html"
    context_object_name = "post"

    def get_queryset(self):
        return _published()

    def get_object(self, queryset=None):
        queryset = queryset or self.get_queryset()
        return get_object_or_404(queryset, slug=self.kwargs["slug"])

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        post = self.object

        post.reading_time = _attach_reading_time(post)

        base = _published()

        if post.published_at:
            ctx["prev_post"] = (
                base.filter(published_at__lt=post.published_at)
                    .order_by("-published_at")
                    .first()
            )
            ctx["next_post"] = (
                base.filter(published_at__gt=post.published_at)
                    .order_by("published_at")
                    .first()
            )
        else:
            ctx["prev_post"] = None
            ctx["next_post"] = None

        related_qs = base.exclude(pk=post.pk)

        if post.category_id:
            same_cat = list(
                related_qs
                .filter(category_id=post.category_id)
                .order_by("-published_at")[:3]
            )
            if len(same_cat) < 3:
                extra = (
                    related_qs
                    .exclude(pk__in=[p.pk for p in same_cat])
                    .order_by("-published_at")[: 3 - len(same_cat)]
                )
                same_cat.extend(extra)
            ctx["related"] = same_cat
        else:
            ctx["related"] = list(
                related_qs.order_by("-published_at")[:3]
            )

        return ctx