from django.contrib.auth.models import User
from django.shortcuts import render, redirect, Http404
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views import generic
from django.urls import reverse_lazy
from django.core.mail import send_mail
from .models import Category
from .models import Board, Comment
from .forms import BoardForm, CommentForm
from .filters import CommentFilter
from .tasks import send_email


class BoardList(generic.ListView):
    model = Board
    template_name = 'Board/boards.html'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['board'] = Board.objects.order_by('-date_of_creation')
        context['category'] = Category.objects.all()
        return context


class BoardCategoryList(generic.ListView):
    model = Board
    template_name = 'Board/boards.html'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['board'] = Board.objects.all().filter(category_id=self.kwargs.get('pk')).order_by('-date_of_creation')
        context['category'] = Category.objects.all()
        return context


class BoardDetail(generic.DetailView):
    model = Board

    def get(self, request, *args, **kwargs):
        commentform = CommentForm()
        board = Board.objects.get(id=kwargs.get('pk'))
        comment = Comment.objects.filter(board_id=kwargs.get('pk'))
        return render(request,
                      'Board/board_detail.html',
                      {'commentform': commentform,
                       'board': board,
                       'comment': comment})

    def post(self, request, *args, **kwargs):
        commentform = CommentForm(request.POST)
        if commentform.is_valid():
            data = commentform.cleaned_data
            user = User.objects.get(id=request.user.id)
            Comment.objects.create(author=user,
                                   board=Board.objects.get(id=kwargs.get('pk')),
                                   text=data['text'])
            return redirect(f"/{kwargs.get('pk')}/")
        raise Http404('Неверные данные')


class BoardCreate(LoginRequiredMixin, generic.CreateView):
    model = Board
    fields = ('category', 'title', 'content')
    template_name = 'Board/create.html'
    from_class = BoardForm
    success_url = reverse_lazy('boardlist')

    def form_valid(self, form):
        form.instance.author = User.objects.get(id=self.request.user.id)
        return super(BoardCreate, self).form_valid(form)


class BoardUpdate(LoginRequiredMixin, generic.UpdateView):
    model = Board
    template_name = 'Board/edit.html'
    form_class = BoardForm
    success_url = reverse_lazy('boardlist')


class BoardAuthorList(UserPassesTestMixin, generic.ListView):
    queryset = Comment.objects.all()
    template_name = 'Board/comment.html'
    context_object_name = 'comment'

    def test_func(self):
        return self.request.user.id == self.kwargs.get('pk')

    def get_queryset(self):
        self.queryset = self.queryset.filter(board_id__author=self.request.user.id).exclude(deleted=True)
        return self.queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = CommentFilter(self.request.GET, queryset=self.get_queryset())
        context['board'] = Board.objects.all().filter(author_id=7)
        return context


def accept(request, *args, **kwargs):
    comment = Comment.objects.get(id=kwargs.get('pk'))
    id = comment.board_id
    board = Board.objects.get(id=id)
    if request.user.id == board.author.id:
        comment.status = 'response accepted'
        comment.save()
        user = User.objects.get(id=comment.author_id)

        board_author = board.author.username
        comment_text = comment.text
        user_email = user.email

        send_mail(
            subject='Ваш комментарий принят',
            message=f'Автор публикации {board_author} принял ваш комментарий "{comment_text}"',
            from_email='Samurraich@yandex.kz',
            recipient_list=[user_email],
        )

        return redirect('myboard', pk=request.user.id)
    raise Http404('У вас нет доступа на эту страницу')


def delete(request, *args, **kwargs):
    comment = Comment.objects.get(id=kwargs.get('pk'))
    id = comment.board_id
    board = Board.objects.get(id=id)
    if request.user.id == board.author.id:
        comment.deleted = True
        comment.save()
        return redirect('myboard', pk=request.user.id)
    raise Http404('У вас нет доступа на эту страницу')
