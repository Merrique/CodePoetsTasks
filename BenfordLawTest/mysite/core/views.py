from django.shortcuts import render
from mysite.core.utils import BenfordAnalysis
      

def home(request):
    if request.method == 'POST':
        uploaded_file = request.FILES['document']

        columntitle = request.POST['columntitle']

        chisquare = BenfordAnalysis(uploaded_file,columntitle)
    

        if chisquare is None:
            return render(request,'error.html')
        else:
            return render(request,'results.html',{'wynik':chisquare})
        

    return render(request,'home.html')


