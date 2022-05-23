from django.db.models.base import Model
from django.shortcuts import render,redirect
from django.http import HttpResponse

from seller.models import Category, Product, Seller, SubCategory
from .myforms import SelSignup, Sellerlogin
from django.contrib.auth.hashers import make_password

from django.views.generic import ListView,CreateView,UpdateView,DeleteView
from django.urls import reverse_lazy




# Create your views here.

# def home(request):
#     # return HttpResponse("<h1> Still in progress. comming Soon.</h1>")  Mvc Sentence
#     return render(request,'ecom/home.html')

def SignupSel(request):
    f=SelSignup(request.POST or None)
    if f.is_valid():
        sel=f.save(commit=False)    
        p=f.cleaned_data.get('password')
        # print(p)
        encp = make_password(p)
        sel.password=encp
        # print(sel)
        sel.save()
        # return HttpResponse("<h1>Form Submitted successfully</h1>")
        return redirect("ecom:signin")
    return render(request,'ecom/sellerreg.html',{'form':f})


def signinseller(request):
    f=Sellerlogin(request.POST or None)
    if f.is_valid():
        c = f.cleaned_data.get("company")
        obj=Seller.objects.get(company=c)
        # session create
        # request.session['user']=obj
        # return redirect(request,'ecom/sellerreg.html',{'form':f})
        request.session['user_log']={'username':obj.name,'company':obj.company}
        # request.session['user_log']=obj
        return redirect("ecom:home")
    return render(request,'ecom/sellerreg.html',{'form':f})


#function base
# def home(request):
#     u=request.session.get("user_log",None)
#     return render(request,"ecom/sellermaster.html",{'usr':u})

class Home(ListView):
    template_name="ecom/home.html"
    context_object_name='cat'
    # def get_queryset(self):
    #     return Category.objects.all()
    # model=Category
    def get_queryset(self):
        selid=self.request.session.get("user_log")
        if selid:
            sell=Seller.objects.get(company=selid.get("company"))
            return {'cate':Category.objects.all(),'prod':Product.objects.filter(slid=sell)}
        else:
            return None


def logouts(request):
    request.session.pop("user_log")
    return redirect("ecom:home")
        



# class Products(ListView):
#     template_name='ecom/products.html'
#     context_object_name='data'
#     model=SubCategory
#     def get_queryset(self):
#         selid=self.request.session.get("user_log")
#         subid=self.kwargs.get("pk")
#         sub=SubCategory.objects.get(id=subid)
#         if selid:
#             sell=Seller.objects.get(company=selid.get("company"))
#             return {'sub':sub,'prod':Product.objects.filter(slid=sell,subid=sub)}
#         else:
#             return None


class Products(ListView):
    template_name="ecom/products.html"
    context_object_name='data'
    model=SubCategory
    def get_queryset(self):
        selid=self.request.session.get("user_log")
        subid=self.kwargs.get("pk")
        sub=SubCategory.objects.get(id=subid)
        if selid:
            sell=Seller.objects.get(company=selid.get("company"))
            return {'sub':sub,'prod':Product.objects.filter(slid=sell,subid=sub)}
        else:
            return None
    

        
class Addproduct(CreateView):
    template_name='ecom/addproduct.html'
    model=Product
    fields=['name','brand','desc','price','discount','image']
    context_object_name='form'
    def form_valid(self,form):
        subid=self.kwargs.get("pk")
        sub=SubCategory.objects.get(id=subid)
        selid=self.request.session.get("user_log")
        sell=Seller.objects.get(company=selid.get("company"))
        # form.instance['slid']=sell
        # form.instance['subid']=sub
        form.instance.slid=sell
        form.instance.subid=sub
        return super().form_valid(form)


class Upproduct(UpdateView):
    template_name='ecom/addproduct.html'
    model=Product
    fields=['name','brand','desc','price','discount','image']
    context_object_name='form'

class Delproduct(DeleteView):
    template_name='ecom/delproduct.html'
    model=Product
    context_object_name='prod'
    success_url=reverse_lazy('ecom:home')
    success_message='product deleted'