from django.shortcuts import render

# Create your views here.
## mainpage 함수
def main(request):
    return render(request, 'moochu/main.html')