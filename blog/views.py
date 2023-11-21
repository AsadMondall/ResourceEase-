# -*- coding: utf-8 -*-
from django.contrib import messages
from django.db.models import Q
from django.shortcuts import redirect, render, reverse
from django.urls import reverse_lazy
from django.views.generic import TemplateView

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, HttpResponseBadRequest
import shutil
from django.views import View
from .run import convert_uploaded_pdf_to_docx
from .forms import PDFUploadForm  
import os
import openai
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView,
    View,
)

from accounts.models import Author
from blog.forms import CommentForm, PostForm
from blog.models import Category, Newsletter, Post


class IndexView(View):
    def get(self, request, *args, **kwargs):
        featured_posts = Post.objects.filter(featured=True)[0:3]
        latest_posts = Post.objects.order_by("-timestamp")[0:3]
        context = {"featured_posts": featured_posts, "latest_posts": latest_posts}
        return render(request, "blog/index.html", context=context)

    def post(self, request, *args, **kwargs):
        email = request.POST.get("email")
        newsletter = Newsletter()
        newsletter.email = email
        newsletter.save()
        messages.info(request, "Successfully subscribed!")
        return redirect("index")


class PostDetailView(DetailView):

    model = Post
    template_name = "blog/resource_detail.html"
    _comment_form = CommentForm()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["latest_posts"] = Post.objects.all().order_by("-timestamp")[0:3]
        context["categories"] = Category.objects.all()
        context["comment_form"] = self._comment_form
        return context

    def post(self, request, *args, **kwargs):
        _post = self.get_object()
        _comment_form = CommentForm(request.POST)
        if _comment_form.is_valid():
            _comment_form.instance.user = request.user.author
            _comment_form.instance.post = _post
            _comment_form.save()
            return redirect(_post)


class PostListView(ListView):

    model = Post
    template_name = "blog/resource_list.html"
    paginate_by = 4

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["latest_posts"] = Post.objects.all().order_by("-timestamp")[0:3]
        context["categories"] = Category.objects.all()
        return context


class SearchView(View):
    def get(self, request, *args, **kwargs):
        q = request.GET.get("q", "")
        search_result = Post.objects.filter(
            Q(title__icontains=q) | Q(overview__icontains=q)
        ).all()
        context = {"search_result": search_result}
        return render(request, "blog/search.html", context=context)


class ContributeView(TemplateView):
    template_name = 'blog/contribute.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, context={})

    def post(self, request, *args, **kwargs):
        # Handle the POST request here if needed
        return HttpResponse("POST request handled.")


class PostCreateView(CreateView):
    model = Post
    template_name = "blog/resource_create.html"
    form_class = PostForm

    def form_valid(self, form):
        form.instance.author = Author.objects.filter(user=self.request.user).first()

        # Handle the uploaded thumbnail
        thumbnail = self.request.FILES.get("thumbnail")
        if thumbnail:
            form.instance.thumbnail = thumbnail

        form.save()
        return redirect(reverse("resource_detail", kwargs={"slug": form.instance.slug}))

class PostUpdateView(UpdateView):
    model = Post
    template_name = "blog/resource_update.html"
    form_class = PostForm

    def form_valid(self, form):
        if form.instance.author == self.request.user.author:
            form.save()
            return redirect(reverse("resource_detail", kwargs={"slug": form.instance.slug}))


class PostDeleteView(DeleteView):
    model = Post
    template_name = "blog/resource_delete.html"
    success_url = reverse_lazy("index")



class ResourceUploadPDFView(View):
    def get(self, request):
        form = PDFUploadForm()
        return render(request, 'upload_pdf.html', {'form': form})

    def post(self, request):
        form = PDFUploadForm(request.POST, request.FILES)
        if form.is_valid():
            pdf_file = request.FILES['pdf_file']
            output_folder = r'C:\Users\USER\Desktop\ResourceEase\re\blog\static\blog\output'

            # Save the uploaded PDF file to a temporary location
            uploaded_file_path = r'C:\Users\USER\Desktop\ResourceEase\re\blog\static\blog\input\uploaded_file.pdf'
            with open(uploaded_file_path, 'wb') as destination:
                for chunk in pdf_file.chunks():
                    destination.write(chunk)

            # Call the function to process the uploaded PDF
            output_docx = convert_uploaded_pdf_to_docx(uploaded_file_path, output_folder)

            # Generate a response to download the DOCX file
            with open(output_docx, 'rb') as docx_file:
                response = HttpResponse(docx_file.read(), content_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document')
                response['Content-Disposition'] = 'attachment; filename="result.docx"'

            # Close the file
            docx_file.close()

            # Empty the output folder after sending the response
            shutil.rmtree(output_folder)
            os.makedirs(output_folder, exist_ok=True)

            return response
        return render(request, 'upload_pdf.html', {'form': form})



from django.shortcuts import render
def chatbot_ui(request):
    return render(request, 'blog/chatbot_ui.html')

openai.api_key = 'your_API_Key'

@csrf_exempt
def get_bot_response(request):
    if request.method == 'POST':
        message = request.POST.get("message")

        # Send the message to OpenAI's API and receive the response
        completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "user", "content": message}
            ]
        )

        chatbot_response = completion['choices'][0]['message']['content']

        return JsonResponse({'response': chatbot_response})

    return JsonResponse({'response': 'Failed to Generate response!'})
    