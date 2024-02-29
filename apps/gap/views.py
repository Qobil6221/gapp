from django.contrib import messages
from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.views import View
from django.views.generic import CreateView

from apps.gap.forms import UserLoginForm, UserRegisterForm
from apps.gap.models import Room, Opinion, Comment, OpinionLike


class RoomListView(View):
    def get(self, request):
        rooms = Room.objects.all()
        return render(request, 'gap/rooms.html', {"rooms": rooms})


class RoomDetailView(View):
    def get(self, request, pk):
        room = Room.objects.get(pk=pk)
        opinions = sorted(Opinion.objects.filter(room=room), key=lambda o: o.like_count, reverse=True)
        context = {
            "room": room,
            "opinions": opinions
        }
        return render(request, "gap/opinoins.html", context=context)


class LikeOpinionView(LoginRequiredMixin, View):
    def get(self, request, pk):
        opinion = Opinion.objects.get(pk=pk)
        like, created = OpinionLike.objects.get_or_create(user=request.user, opinion=opinion)
        if not created:
            like.delete()
        return redirect(reverse("gap:room", kwargs={"pk": opinion.room.pk}))


class OpinionDetailView(LoginRequiredMixin, View):
    def get(self, request, pk):
        opinion = Opinion.objects.get(pk=pk)
        comments = opinion.comments.all().order_by("-created_at")
        comments = sorted(comments, key=lambda c: c.like_count, reverse=True)
        context = {
            "opinion": opinion,
            "comments": comments
        }
        return render(request, "gap/comments.html", context=context)


class CommentLikeView(View):
    def get(self, request, pk):
        comment = Comment.objects.get(pk=pk)


class SearchOpinionView(View):
    def get(self, request):
        q = request.GET.get('q', None)
        if q:
            opinions = Opinion.objects.filter(Q(title__icontains=q) | Q(body__icontains=q))
        else:
            opinions = None

        context = {
            'param': q,
            'opinions': opinions
        }
        return render(request, 'gap/search-opinion.html', context=context)


class Loginview(View):
    def get(self, request):
        form = UserLoginForm()
        return render(request, "gap/login.html", {'form': form})

    def post(self, request):
        form = UserLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f"you have login as {username}")
                return redirect('landing_page')
            else:
                messages.error(request, "Wrong username or password")
                return render(request, "gap/login.html", {"form": form})
        else:
            return render(request, "gap/login.html", {"form": form})


class UserRegisterView(View):
    def get(self, request):
        form = UserRegisterForm()
        return render(request, "gap/register.html", {'form': form})

    def post(self, request):
        form = UserRegisterForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Sucessfully registered")
            return redirect("gap:login-page")
        else:
            return render(request, "gap/register.html", {'form': form})


class UserLogoutView(View):
    def get(self, request):
        logout(request)
        messages.success(request, "User successfully loged out")
        return redirect("landing_page")


class AddOpinionView(CreateView):
    model = Opinion
    fields = ['room', 'title', 'body']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        messages.success(self.request, "Opinion added successfully")
        return reverse('gap:opinion', kwargs={'pk': self.object.pk})


@login_required()
def delete_opinion(request, id):
    opinion = get_object_or_404(Opinion, pk=id)
    context = {'opinion': opinion}
    if request.user == opinion.author:
        if request.method == "POST":
            return render(request, "gap/opinion_delete.html", context)
        else:
            opinion.delete()
            messages.success(request, "The opinion has been deleted successfully.")
            return redirect('gap:opinion', pk=id)
    else:
        messages.warning(request, "sorry not your opinion")
        return redirect('gap:opinion')
