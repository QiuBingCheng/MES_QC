from django.shortcuts import render
from MES.models import Customer,Product,Category
from django.views.decorators.clickjacking import xframe_options_exempt
from django.shortcuts import redirect,render_to_response
from django import forms
from django.http import HttpResponse
from MES.form import PostForm
#coding=utf8
def index(request):  
	Customers = Customer.objects.all().order_by('id')  #讀取資料表, 依 id 遞增排序
	return render(request, "index.html", locals())
def post1(request):  #新增資料，資料不作驗證
	if request.method == "POST":	  #如果是以POST方式才處理
		last_name = request.POST['last_name'] #取得表單輸入資料
		first_name =  request.POST['first_name']
		email =  request.POST['email']
		address = request.POST['address']
		#新增一筆記錄
		unit = customer.objects.create(last_name=last_name, first_name=first_name, email=email, address=address)
		unit.save()  #寫入資料庫
		return redirect('/index/')	
	else:
		message = 'Please complete the form(data is not verified)'
	return render(request, "post1.html", locals())	

def delete(request):  #刪除資料
	if request.method == "POST":  #如果是以POST方式才處理
		id=request.POST['cId'] #取得表單輸入的編號
		try:
			unit = customer.objects.get(id=id)  
			unit.delete()
			return redirect('/index/')
		except:
			message = "error!"			
	return render(request, "delete.html", locals())	

 # index.html EDIT
def edit(request,id=None,mode=None):
    if mode == None: 
    	unit = Customer.objects.get(id=id)  
    	return render(request, "edit.html", locals())

 #edit.html COMMIT
def edit2(request,id=None,mode=None): 
    unit = Customer.objects.get(id=id) 
    unit.last_name=request.POST['last_name']
    unit.first_name=request.POST['first_name']
    unit.address=request.POST['address']
    unit.email=request.POST['email']
    unit.save()  #寫入資料
    message = 'updated...'
    return redirect('/index/')

import json  
from django import forms
import decimal
class DecimalEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, decimal.Decimal):
             return float(obj)
        return super(DecimalEncoder, self).default(obj)


import controlchart
import random
import statistics
from random import choice
from datetime import datetime, timedelta
def QC(request):
    if  request.method == "POST":
        postform=PostForm(request.POST) #初始值為表單傳送資料
        #從表單讀取各種參數
        ProductID= request.POST.get('ProductID',False)
        start_date=request.POST.get('start_date',False)
        end_date=request.POST.get('end_date',False)
        size=request.POST.get('sample_size',False)
        chart_type=request.POST.get('chart_type',False)
        
        #從str type 轉成date type 
        start_date = datetime.strptime(start_date, '%Y-%m-%d')
        end_date = datetime.strptime(end_date, '%Y-%m-%d')

        #連續抽樣幾天
        duration=(end_date-start_date).days+1
        
        #將抽樣日期裝進列表，以當作折線圖的x座標
        sample_date=[]
        for i in range(duration):
            delta=timedelta(days=i)
            n_days=start_date+delta
            for i in range(3):  #一天抽取三組 所以日期要重複三次
                sample_date.append(n_days.strftime('%Y-%m-%d'))
         
         
        x_bar=[]
        data=[]
        R=[]
        for i in range(duration):
            delta=timedelta(days=i)
            n_days=start_date+delta
            n_days=n_days.strftime('%Y-%m-%d')
            objs=Product.objects.raw(
            "SELECT* FROM MES_Product where date(created_at)=%s and ProductID=%s",[n_days,ProductID])
            
            #每天抽取三組
            for j in range(3):
                temp=[]
                sample = random.sample(list(objs), int(size)) #隨機抽取N個樣本
                for i in sample:
                    temp.append(i.width)

                #計算管制界線的二維data ex[[1,2,3,4,5],[6,7,8,9,10],...] 
                data.append(temp) 

                #繪圖的data(sample mean)
                x_bar.append(round(statistics.mean(temp),2))  
                #繪圖的data(sample range)
                R.append(round(max(temp)-min(temp),2))
            
        #判別何種管制圖
        if chart_type=='x_bar_chart':
            CL,LCL,UCL=controlchart.get_stats_x_bar_r_x(data,int(size))
            spc=controlchart.Spc(data,"x_bar R - X",sizes=int(size))
            drawn_data= x_bar

        else:
            CL,LCL,UCL=controlchart.get_stats_x_bar_r_r(data,int(size))
            drawn_data= R

        #標記違規管制線紅點
        violating_point=[]
        for i in range(len(drawn_data)):
            if (drawn_data[i]>UCL) or (drawn_data[i]<LCL):violating_point.append(i)

        return render(request, "QC.html", {
            'drawn_data': json.dumps(drawn_data),
            'postform':postform,
            'ProductID':ProductID,
            'UCL':UCL,
            'LCL':LCL,
            'CL':CL,
            'chart_type':chart_type,
            'R':R,
            'violating_point':json.dumps(violating_point),
            'sample_date': json.dumps(sample_date),
    
        })
    postform=PostForm()
    return render(request, "QC.html", locals())


import numpy as np
from django.utils import timezone
import pytz
import random
#從今天開始逆推，10天一循環
def data(request):  
    ProductID="A001"
    today=timezone.now()
    width = 14+random.random()*2
    unit = Product.objects.create(ProductID= ProductID, width = width,created_at=today)
    unit.save()  
    Products = Product.objects.raw("select *from MES_Product order by id desc limit 1")
    '''mu,sigma=17,0.4   
    widths = np.random.normal(mu, sigma,20)
    ProductID="A002"
    today=timezone.now()
    for width in widths:
        unit = Product.objects.create(ProductID=ProductID, width=round(width,2),created_at=today)
        unit.save()  #寫入資料庫
    Products = Product.objects.raw("select *from MES_Product order by id desc limit 20")'''
    return render(request,'data.html',locals())  
 
def test(request):
    if request.method == "POST":
        postform = PostForm(request.POST)
        message = 'something wrong!'
        ProductID = request.POST['ProductID']
        sample_size = request.POST['sample_size']
        a=[1,2,3,4,5]
        return  JsonResponse({'ProductID':ProductID,'a':a})

    postform = PostForm()
    return render(request,'test.html',locals())  
           
 


from django.http import JsonResponse
from django.views.decorators.csrf import ensure_csrf_cookie


@ensure_csrf_cookie

def QC_test(request):
    if  request.method == "POST":
        postform=PostForm(request.POST) #初始值為表單傳送資料
        #從表單讀取各種參數
        ProductID = request.POST.get('ProductID',False)
        start_date = request.POST.get('start_date',False)
        end_date = request.POST.get('end_date',False)
        size = request.POST.get('sample_size',False)
        chart_type = request.POST.get('chart_type',False)
        
        #從str type 轉成date type 
        start_date = datetime.strptime(start_date, '%Y-%m-%d')
        end_date = datetime.strptime(end_date, '%Y-%m-%d')

        #連續抽樣幾天
        duration=(end_date-start_date).days+1
        
        #將抽樣日期裝進列表，以當作折線圖的x座標
        sample_date=[]
        for i in range(duration):
            delta=timedelta(days=i)
            n_days=start_date+delta
            for i in range(3):  #一天抽取三組 所以日期要重複三次
                sample_date.append(n_days.strftime('%Y-%m-%d'))
         
         
        x_bar=[]
        data=[]
        R=[]
        for i in range(duration):
            delta=timedelta(days=i)
            n_days=start_date+delta
            n_days=n_days.strftime('%Y-%m-%d')
            objs=Product.objects.raw(
            "SELECT* FROM MES_Product where date(created_at)=%s and ProductID=%s",[n_days,ProductID])
            
            #每天抽取三組
            for j in range(3):
                temp=[]
                sample = random.sample(list(objs), int(size)) #隨機抽取N個樣本
                for i in sample:
                    temp.append(i.width)

                #計算管制界線的二維data ex[[1,2,3,4,5],[6,7,8,9,10],...] 
                data.append(temp) 

                #繪圖的data(sample mean)
                x_bar.append(round(statistics.mean(temp),2))  
                #繪圖的data(sample range)
                R.append(round(max(temp)-min(temp),2))
            
        #判別何種管制圖
        if chart_type=='x_bar_chart':
            CL,LCL,UCL = controlchart.get_stats_x_bar_r_x(data,int(size))
            spc = controlchart.Spc(data,"x_bar R - X",sizes=int(size))
            drawn_data = x_bar

        else:
            CL,LCL,UCL = controlchart.get_stats_x_bar_r_r(data,int(size))
            drawn_data = R

        #標記違規管制線紅點
        violating_point = []
        for i in range(len(drawn_data)):
            if (drawn_data[i]>UCL) or (drawn_data[i]<LCL):violating_point.append(i)
        
        #管制界線json
        limit = {"CL":round(CL,2),"LCL":round(LCL,2),"UCL":round(UCL,2)}
        chart = {
        'chart': {'type': 'line', 'marginRight':100, 'marginLeft':100},
        'title': {'text': chart_type},
        'xAxis': {'categories': sample_date},
        'yAxis': {'max':UCL+0.5,'min':LCL-0.5,'title':'width(cm)',
                  'plotLines':[{
                    'color':'red',               #線的颜色，定义为红色
                    'dashStyle':'shortdashdot',   #虛線
                    'value':UCL,                #定义在那个值上显示标示线，这里是在x轴上刻度为3的值处垂直化一条线
                    'width':2 ,
                    'label':{
                      'text':'UCL',                  
                      'align':'left',                #標籤位置水平居左
                      'x': 0  ,                       #标签相相對於被定位的位置水平偏移的像素
                      }             
                  },{
                    'color':'red',           
                    'dashStyle':'shortdashdot',     
                    'value':LCL,               
                    'width':2 ,
                    'label':{
                      'text':'LCL',     
                      'align':'left' ,             
                      'x': 0 ,                      
                     }       
                  }
                 ]},
        'series': [{'name':ProductID,'data':[]}],
        'legend':{'layout':'vertical',
                  'align':'right',
                  "vertical":'top',
                  "x":0,
                  'y':150,
                  'backgroundColor':"(Highcharts.theme && Highcharts.theme.legendBackgroundColor) || '#FFFFFF'}",
                  'borderWidth':1}
        }
        
        return JsonResponse([chart,drawn_data,violating_point,limit],safe=False)
    postform=PostForm()
    return render(request, "QC_test.html", locals()) 


def monitor(request):
    if request.is_ajax():
        chart_type = "A001規格監測"
        ProductID =  'A001'
        UCL = 16
        LCL = 14
        CL = 15
        drawn_data = []
        #取15個點繪製
        objs = Product.objects.raw(
                "SELECT* FROM MES_Product ORDER BY created_at DESC limit 15" )
        for obj in objs:
            drawn_data.append(obj.width)

        drawn_data.reverse()
        
        #標記違規管制線紅點
        violating_point = []
        for i in range(len(drawn_data)):
            if (drawn_data[i]>UCL) or (drawn_data[i]<LCL):
                violating_point.append(i)
        
        #管制界線json
        limit = {"CL":round(CL,2),"LCL":round(LCL,2),"UCL":round(UCL,2)}
        chart = {
        'chart': {'type': 'line', 'marginRight':100, 'marginLeft':100},
        'title': {'text': chart_type},
        #'xAxis': {'categories': sample_date},
        'yAxis': {'max':UCL,'min':LCL,'title':'width(cm)',
                  'plotLines':[{
                    'color':'red',               #線的颜色，定义为红色
                    'dashStyle':'shortdashdot',   #虛線
                    'value':UCL,                #定义在那个值上显示标示线，这里是在x轴上刻度为3的值处垂直化一条线
                    'width':2 ,
                    'label':{
                      'text':'UCL',                  
                      'align':'left',                #標籤位置水平居左
                      'x': 0  ,                       #标签相相對於被定位的位置水平偏移的像素
                      }             
                  },{
                    'color':'red',           
                    'dashStyle':'shortdashdot',     
                    'value':LCL,               
                    'width':2 ,
                    'label':{
                      'text':'LCL',     
                      'align':'left' ,             
                      'x': 0 ,                      
                     }       
                  }
                 ]},
        'series': [{'name':ProductID,'data':[]}],
        'legend':{'layout':'vertical',
                  'align':'right',
                  "vertical":'top',
                  "x":0,
                  'y':150,
                  'backgroundColor':"(Highcharts.theme && Highcharts.theme.legendBackgroundColor) || '#FFFFFF'}",
                  'borderWidth':1}
        }
        
        return JsonResponse([chart,drawn_data,violating_point,limit],safe=False)

    return render(request, "monitor.html", locals()) 
