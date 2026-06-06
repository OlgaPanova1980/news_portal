import django_filters
from django import forms
from .models import Post, Author

class PostFilter(django_filters.FilterSet):
    title = django_filters.CharFilter(
        field_name='title',
        lookup_expr='icontains',
        label='Название новости'
    )

    author = django_filters.ModelChoiceFilter(
        field_name='author',
        queryset=Author.objects.all(),
        empty_label='Все авторы',
        label='Автор'
    )

    date_after = django_filters.DateFilter(
        field_name='created_at',
        lookup_expr='gt',
        label='Позже даты',
        widget=forms.DateInput(attrs={'type': 'date'})
    )

    class Meta:
        model = Post
        fields = ['title', 'author', 'date_after']