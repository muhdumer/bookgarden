from django.db import models
import uuid
import os

def get_image_file_name(instance,filename):

    ext=filename.split('.')[-1]
    filename="{}.{}".format(uuid.uuid4(),ext)

    return os.path.join('book_images/',filename)


class BookCategory(models.Model):
    category_title=models.CharField(max_length=264,verbose_name="Category")    

    class Meta:
        verbose_name="Category"
        verbose_name_plural="Categories"

    def __str__(self):
        return self.category_title

class Author(models.Model):
    author_name=models.CharField(max_length=100)

    def __str__(self):
        return self.author_name

class Book(models.Model):
    book_name=models.CharField(max_length=264,verbose_name="Book Name",blank=False)
    book_category=models.ManyToManyField(BookCategory,verbose_name=("Categories"))
    book_author=models.ForeignKey(Author,verbose_name=("Author Name"),on_delete=models.CASCADE,blank=False)
    book_price=models.PositiveIntegerField(verbose_name="Display Price")
    description=models.TextField()
    in_stock=models.BooleanField(default=False,verbose_name="Is Book in Stock?")

    def __str__(self):
        return self.book_name

    def get_book_list_image(self):
        obj=self.bookimage_set.filter(is_default=True).values('image').first()
        if obj is None:
        	return obj
        return '/media/'+obj['image']

    def get_book_name_for_url(self):
        temp_book_name=self.book_name
        return temp_book_name.replace(' ','-')

    def shrink_book_description(self):
        desc=self.description
        if(len(desc)>150):
            desc=desc[:150]
            return (desc.rsplit(' ',1)[0])+'....'
        return desc     
        


class BookImage(models.Model):
    image_of_book=models.ForeignKey(Book,verbose_name=("Image Belongs to?"),on_delete=models.CASCADE)
    image=models.ImageField(upload_to=get_image_file_name,blank=False)
    is_default=models.BooleanField(default=True,help_text="By checking this the photo will appear on product template else not")

    def __str__(self):
        return self.image_of_book.book_name

    


    
