from django.shortcuts import render

# Create your views here.
## mainpage 함수
def mainpage(request):
    return render(request, 'moochu/mainpage.html')