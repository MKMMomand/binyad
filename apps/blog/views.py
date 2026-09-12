from django.db.models import Q
from django.views.generic import ListView, DetailView
from .models import Post, Category


class PostListView(ListView):
    model = Post
    template_name = "blog/list.html"
    context_object_name = "posts"
    paginate_by = 9

    def get_queryset(self):
        qs = Post.objects.filter(status=Post.Status.PUBLISHED)
        q = self.request.GET.get("q")
        if q:
            qs = qs.filter(Q(title__icontains=q) | Q(content__icontains=q))
        return qs

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["categories"] = Category.objects.all()
        ctx["query"] = self.request.GET.get("q", "")
        return ctx


class CategoryView(ListView):
    template_name = "blog/list.html"
    context_object_name = "posts"
    paginate_by = 9

    def get_queryset(self):
        return Post.objects.filter(status=Post.Status.PUBLISHED, category__slug=self.kwargs["slug"])

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["categories"] = Category.objects.all()
        ctx["current_category"] = Category.objects.filter(slug=self.kwargs["slug"]).first()
        return ctx


class PostDetailView(DetailView):
    model = Post
    template_name = "blog/detail.html"
    context_object_name = "post"
    queryset = Post.objects.filter(status=Post.Status.PUBLISHED)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["related"] = Post.objects.filter(
            status=Post.Status.PUBLISHED,
            category=self.object.category,
        ).exclude(pk=self.object.pk)[:3]
        return ctx