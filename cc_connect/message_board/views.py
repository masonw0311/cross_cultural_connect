from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Message
#----------------------------------------------------------------
@login_required
def message_board(request):
    if request.method == "POST":
        content = request.POST.get('content')
        if content:
            Message.objects.create(user=request.user, content=content)
        return redirect('message_board')

    messages = Message.objects.all().order_by('-timestamp')
    return render(request, 'message_board/message_board.html', {'messages': messages})
