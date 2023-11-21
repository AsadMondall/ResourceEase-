from django import forms
from tinymce.widgets import TinyMCE

from blog.models import Comment, Post, Category

class PostForm(forms.ModelForm):
    content = forms.FileField(
        widget=forms.ClearableFileInput(attrs={"class": "form-control"})
    )
    thumbnail = forms.ImageField(
        required=False, widget=forms.FileInput(attrs={"class": "form-control"})
    )

    # Use ModelMultipleChoiceField for categories to allow multiple selections
    category = forms.ModelMultipleChoiceField(
        queryset=Category.objects.all(),  # All categories from the database
        widget=forms.CheckboxSelectMultiple(attrs={"class": "form-check-input"}),  # CheckboxSelectMultiple for multiple selections
    )

    class Meta:
        model = Post
        fields = ("title", "overview", "content", "featured", "category", "thumbnail")

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ("content",)

class PDFUploadForm(forms.Form):
    pdf_file = forms.FileField(label='Select a PDF file')
