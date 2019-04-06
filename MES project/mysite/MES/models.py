from django.db import models

# Create your models here.
# Create your models here.
class Customer(models.Model):
	last_name=models.CharField(max_length=25,null=False)
	first_name=models.CharField(max_length=25,null=False)
	address=models.CharField(max_length=255,default="")
	email=models.EmailField(max_length=100,default="",unique=True)

	
class Product(models.Model):
	ProductID=models.CharField(max_length=255,null=False)
	width=models.FloatField(default=0,null=False)
	created_at = models.DateTimeField()

	def __str__(self):
        		 return self.ProductID


class Category(models.Model):
    ProductID=models.CharField(max_length=255,null=False,primary_key=True)
    Name=models.CharField(max_length=20,null=False)
    Description=models.CharField(max_length=255)
    Quantity=models.IntegerField(null=False)

    #確保admin裏面顯示的是名字而不是object
    def __str__(self):
        return self.ProductID


class Control_limit(models.Model):
	size=models.IntegerField(primary_key=True)
