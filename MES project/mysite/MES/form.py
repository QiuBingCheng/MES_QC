from django import forms
from  MES import models
from django.contrib.admin.widgets import AdminDateWidget



class PostForm(forms.Form):
 		ProductID=forms.ChoiceField(#這裏使用value_list是因為傳遞給choices的格式剛好是一個列表包括的元組格式
        choices=models.Category.objects.all().values_list('ProductID', 'ProductID'),label="產品編號")
 		start_date=forms.DateField(widget=forms.widgets.DateInput(attrs={'type': 'date'}),label='抽樣起始日')
 		end_date=forms.DateField(widget=forms.widgets.DateInput(attrs={'type': 'date'}),label='抽樣結束日')
      

 		sample_size= forms.ChoiceField(
 			choices=(('2','2'),('3','3'),('4','4'),('5','5')),label="抽樣大小")

 		chart_type=forms.ChoiceField(
        	choices=(('x_bar_chart','平均值管制圖'),('R_chart','全距管制圖')),label="管制方式")

#objs=Product.objects.raw("SELECT id,created_at  FROM MES_Product where date(created_at)=='2019-01-21' limit 3" )
