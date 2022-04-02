from django.shortcuts import render,redirect
from django.views.generic import ListView,DetailView
from . import models
from django.http import Http404
from customer_app.models import ReviewBook
from django.contrib import messages
from django.urls import reverse
import math
# Create your views here.

class BookListView(ListView):
    template_name='shop.html'
    model=models.Book
    context_object_name='booklist'  
    paginate_by=6
 
    def get_queryset(self):
        all_authors=None
        if 'all_authors' in self.request.GET:
            all_authors=self.request.GET.getlist('all_authors')

        if 'pk' in self.kwargs:
            if all_authors!=None:
                return self.model.objects.filter(book_category__id=self.kwargs.get('pk'),book_author__in=all_authors).order_by('-pk')
            else:    
                return self.model.objects.filter(book_category__id=self.kwargs.get('pk')).order_by('-pk')
        else:
            try:
                pk_first=models.BookCategory.objects.all().first().pk
                if all_authors==None:
                    return self.model.objects.filter(book_category__id=pk_first).order_by('-pk')
                else:
                    return self.model.objects.filter(book_category__id=pk_first,book_author__in=all_authors).order_by('-pk')

            except:
                return None

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["categories"] = models.BookCategory.objects.all()
        
        if 'pk' in self.kwargs:
            try:
                context['category_pk'] = context["categories"].get(pk=self.kwargs.get('pk')).pk
            except:
                raise Http404()
        else:
            try:    
                context['category_pk'] = context["categories"].first().pk    
            except:
                context['category_pk']=0

        context['authors']=models.Author.objects.filter(book__book_category__id=context['category_pk']).distinct()  

        context['min_price']=0
        context['max_price']=0
        flag=None
        
        for item in context['booklist']:
            if flag==None:
                context['min_price']=item.book_price
                context['max_price']=item.book_price
                flag=1
                
            if context['min_price']>item.book_price:
                context['min_price']=item.book_price
            
            if context['max_price']<item.book_price:
                context['max_price']=item.book_price

        
        return context

class SingleBookView(DetailView):
    template_name='product-details.html'
    model=models.Book
    context_object_name='book'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        book_pk=self.kwargs.get('pk')
        book_images=self.model.objects.get(pk=book_pk).bookimage_set.filter(is_default=True)
        if book_images.count()>4:
            book_images=book_images[:4]
        context["book_images"] =book_images 
        review_obj=self.model.objects.get(pk=book_pk).reviewbook_set.all()
        context['count']=review_obj.count()
        if context['count']==0:
            context['is_review_empty']=True
        else:
            context['is_review_empty']=False
        avg=0.0
        for i in range(1,6):
            context[str(i)+'stars']=0

        for obj in review_obj:
            avg+=int(obj.star_rating)
            context[str(obj.star_rating)+'stars']+=1
        if context['count']!=0:    
            context['average']=round(avg/context['count'],1)
        else:
            context['average']=0.0    
        context['average_int']=round(math.floor(context['average']))    
        context['all_reviews']=review_obj
        return context
    
    def post(self,request,*args, **kwargs):
        book_pk=self.kwargs.get('pk')
        book_obj=None
        try:
            book_obj=models.Book.objects.get(pk=book_pk)
        except:
            raise Http404()
        name=None
        email=None
        if not self.request.user.is_authenticated:
            name=request.POST['name']
            email=request.POST['email']
        else:
            email=self.request.user.email
            if self.request.user.first_name=='' or self.request.user.last_name=='':
                name=self.request.user.username
            else:
                name=self.request.user.first_name+' '+self.request.user.last_name
        email=email.lower()
        review=request.POST['message']
        rating=int(request.POST['whatever1'])

        if name=='' or email =='' or review =='':
            return redirect(reverse('product_app:single_book',kwargs={'pk':book_pk,'bookname':book_obj.get_book_name_for_url()}))    
            

        if ReviewBook.objects.filter(book=book_pk,email__iexact=email).exists():
            messages.info(request,'Review already given with this email address on this product')
        else:
            review_obj=ReviewBook(book=book_obj,star_rating=rating,full_name=name,email=email,review=review)    
            review_obj.save()
            messages.success(request,'Your review was successfully recorded..')
        
        return redirect(reverse('product_app:single_book',kwargs={'pk':book_pk,'bookname':book_obj.get_book_name_for_url()}))    

class SearchListView(ListView):
    template_name='search.html'
    context_object_name='booklist'
    model=models.Book
    paginate_by=6

    def get_queryset(self):
        search=None
        if 'search' in self.request.GET:
            search=self.request.GET['search']
        else:
            raise Http404()
        search=search.lower()
        book_name_query=self.model.objects.filter(book_name__icontains=search)
        book_category_query=self.model.objects.filter(book_category__category_title__icontains=search)
        book_author_query=self.model.objects.filter(book_author__author_name__icontains=search)
        return book_name_query.union(book_category_query.union(book_author_query)).order_by('-pk')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["search"] =self.request.GET['search'] 
        return context
        
        





    


    