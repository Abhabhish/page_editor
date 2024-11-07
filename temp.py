def create_post(request, folder_id):
    folder = get_object_or_404(Folder, id=folder_id)
    if request.method == 'POST':
        print(request.POST)
        return HttpResponse('form submitted')
    return render(request, 'create_post.html')
