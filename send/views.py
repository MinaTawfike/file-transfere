from django.shortcuts import render, redirect
from django import forms
from django.http import HttpResponse, Http404
from django.urls import reverse
from .models import File
from .forms import FileForm
import os



# Create your views here.
def file_list(request):
    files = File.objects.all()
    return render(request, 'send/file_list.html', {'files': files})


def file_upload(request):
    if request.method == "POST":
        form = FileForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('send:file_list')
        
    
    # Logic for deleting a file
    if request.GET.get('delete_pk'):  # Check if 'delete_pk' is present in GET parameters
        try:
            file_to_delete = File.objects.get(pk=request.GET.get('delete_pk'))
            file_to_delete.delete()
    # Add a success message or handle deletion success here (optional)
        except File.DoesNotExist:
    # Handle case where the file with the provided pk doesn't exist (optional)
            pass  # You can add an error message here

        return redirect('send:file_list')
    
    if request.POST.get('delete_all'):  # Check if 'delete_pk' is present in GET parameters
        confirmation = request.POST.get('confirm_delete_all', False)  # Check for confirmation checkbox
        if confirmation:
            File.objects.all().delete()  # Delete all files (caution!)
            return redirect('send:file_list')
        # Add success message or handle deletion success here (optional)
        else:
            form.add_error(None, 'Please confirm deletion by checking the box.')  # Add error message if not confirmed
            return redirect('send:file_list')


    else:
        form = FileForm()
        return render(request, 'send/file_upload.html', {
      'form': form,})

def file_download(request, pk):
    try:
        file = File.objects.get(pk=pk)
    except File.DoesNotExist:
        raise Http404("File does not EXIST")
    
    response = HttpResponse(file.file, content_type='application/octet-stream')
    response['content-Disposition'] = 'attachment; filename='+ os.path.basename(file.file.name) 
    return response