import yfinance as yf
import streamlit as st
from datetime import date
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
import pandas as pd
from scipy.signal import argrelextrema



today = date.today()

st.write("""
#  Project 5 


Ticker name should be from **Yahoo finance website** like AAPL, MSFT, GOGL.
For Indian stock, please enter like this BRITANNIA.NS, HEROMOTOCO.NS as mentioned in Yahoo Financial website

""")
 # valid periods: 1d,5d,1mo,3mo,6mo,1y,2y,5y,10y,ytd,max
  # valid intervals: 1m,2m,5m,15m,30m,60m,90m,1h,1d,5d,1wk,1mo,3mo
 
tickerSymbol = st.text_input("Enter any ticker symbol", value='AAPL')
tickerSymbol.upper()

options = st.selectbox('Select the time-frame of candle',("1m",'5m','15m','30m','1h','1d','1wk'))
st.write('You selected:', options,' time-frame')

if options=='1m':
    peri='5d'
elif options=='5m' or'15m':
    peri='50d'
elif options=='30m' or'1h':
    peri='5mo'
elif options=='1d' or'1wk':
    peri='5y'

data = yf.download(tickerSymbol, period=peri, interval=options)

pc=data['Close'].shift(1)
ph=data['High'].shift(1)
pl=data['Low'].shift(1)

data.reset_index(inplace = True)
size=200

width=[]
def width_fun(data):
    for i in range(0,len(data)):
        if pl.values[i] > data.High.values[i]: #### GAP DOWN OPENING
            ddd= 0.38*abs(data.Low.values[i]-pc.values[i])
            width.append(ddd)
        
        elif ph.values[i] < data.Low.values[i] :
            ddd= 0.38*abs(data.High.values[i]-pc.values[i])
            width.append(ddd)
        
        else: 
            ddd= 0.38*(data.High.values[i]-data.Low.values[i])
            width.append(ddd)
            
width_fun(data)  

wx = (pd.Series(width)).cumsum()
data['width']=wx
pp=wx.shift(1)

size = st.number_input('Insert an integer number of candle you want to see',min_value=1, max_value=None, value=100)
st.write('Currently you are seeing last ', size,' candles')

rect=['a']*size
for i in range(size):
    
    if pl.values[i-size] > data.High.values[i-size]: #### GAP DOWN OPENING
        if data.Close.values[i-size] > data.Open.values[i-size]:
            rect[i]=matplotlib.patches.Rectangle((pp.values[i-size], data.Low.values[i-size]),0.38*abs(data.Low.values[i-size]-pc.values[i-size]), (data.High.values[i-size]-data.Low.values[i-size]), facecolor ='green',edgecolor = 'black')
        elif data.Close.values[i-size] <= data.Open.values[i-size]:
            rect[i]=matplotlib.patches.Rectangle((pp.values[i-size], data.Low.values[i-size]),0.38*abs(data.Low.values[i-size]-pc.values[i-size]), (data.High.values[i-size]-data.Low.values[i-size]), facecolor ='red',edgecolor = 'black')
            
    elif ph.values[i-size] < data.Low.values[i-size] : 
         if data.Close.values[i-size] > data.Open.values[i-size]:
            rect[i]=matplotlib.patches.Rectangle((pp.values[i-size], data.Low.values[i-size]),0.38*abs(data.High.values[i-size]-pc.values[i-size]), (data.High.values[i-size]-data.Low.values[i-size]), facecolor ='green',edgecolor = 'black')
         elif data.Close.values[i-size] <= data.Open.values[i-size]:
            rect[i]=matplotlib.patches.Rectangle((pp.values[i-size], data.Low.values[i-size]),0.38*abs(data.High.values[i-size]-pc.values[i-size]), (data.High.values[i-size]-data.Low.values[i-size]), facecolor ='red',edgecolor = 'black')
    
    else:
         if data.Close.values[i-size] > data.Open.values[i-size]:
            rect[i]=matplotlib.patches.Rectangle((pp.values[i-size], data.Low.values[i-size]),0.38*(data.High.values[i-size]-data.Low.values[i-size]), (data.High.values[i-size]-data.Low.values[i-size]), facecolor ='green',edgecolor = 'black')
         elif data.Close.values[i-size] <= data.Open.values[i-size]:
            rect[i]=matplotlib.patches.Rectangle((pp.values[i-size], data.Low.values[i-size]),0.38*(data.High.values[i-size]-data.Low.values[i-size]), (data.High.values[i-size]-data.Low.values[i-size]), facecolor ='red',edgecolor = 'black')
    
        
fig = plt.figure()
ax = fig.add_subplot(111)    
data1=data[-1*size:]
dataw=data1['width'].min()
print(dataw)
max_y= data1.High.max()
min_y=data1.Low.min()
min_x=data1.width.min()
max_x=data1.width.max()

idx_max=[]
price_max=[]
idx_min=[]
price_min=[]

def slop45max(data,yy):
    #data=data.set_index('width')
    data=data.reset_index()
    max_idx = list(argrelextrema(data.High.values, np.greater, order=yy)[0])
    
    
    print(max_idx)
    indi=data['width'].values[max_idx]
    print(indi)
  
    
    pricez=data.High.values[max_idx]
    
    for jj in max_idx:
        print(jj)
        kk=data['width'].values[jj]
        print(kk)
        if kk > dataw:
            idx_max.append(kk)
            x1=kk
            price_max.append(data.High.values[jj])
            y1=data.High.values[jj]
            ax.axline((x1, y1), slope=-1., color='red',linestyle='--', label='-45 degree')
    
         
def slop45min(data,yy):
    #data=data.set_index('width')
    data=data.reset_index()
    min_idx = list(argrelextrema(data.Low.values, np.less, order=yy)[0])
    
    
   
    
    for jj in min_idx:
        print(jj)
        kk=data['width'].values[jj]
        print(kk)
        if kk > dataw:
            idx_min.append(kk)
            x1=kk
            price_min.append(data.Low.values[jj])
            y1=data.Low.values[jj]
            ax.axline((x1, y1), slope=+1., color='green', linestyle='--', label='+45 degree')
            
     
            
plt.xlim([min_x, max_x])
plt.ylim([min_y-1, max_y+1])
# ax.add_patch(rect[8])
# plt.show()
yy = st.number_input('Insert an interger number for changing the  number of slope',min_value=1, max_value=50, value=20)
st.write('Currently the maxima/minima (slope) based on ', yy,' points')
slop45max(data,yy)
slop45min(data,yy)




for j in range(size):
    ax.add_patch(rect[j])

st.pyplot(fig)    
plt.show()    

st.write('Y-axis is representing   **prices** & X-axis is representing nothing' )



pc=data['Close'].shift(1)
ph=data['High'].shift(1)
pl=data['Low'].shift(1)

width=[]

signal=[1]
stop_loss=[]
pnl=[]
cum_pnl=[]
pat=0
corr_pat=0
selling=[0]
buying=[0]

data.reset_index(inplace = True)
def width_fun(data):
    for i in range(0,len(data)):
        if pl.values[i] > data.High.values[i]: #### GAP DOWN OPENING
            ddd= 0.38*abs(data.Low.values[i]-pc.values[i])
            width.append(ddd)
        
        elif ph.values[i] < data.Low.values[i] :
            ddd= 0.38*abs(data.High.values[i]-pc.values[i])
            width.append(ddd)
        
        else: 
            ddd= 0.38*(data.High.values[i]-data.Low.values[i])
            width.append(ddd)
            
width_fun(data)  

wx = (pd.Series(width)).cumsum()
data['width']=wx
pp=wx.shift(1)

local=[0]
          
min_df=pd.DataFrame()
max_df=pd.DataFrame()
def three_red(df):
    if df['Open'].values[-1] >df['Close'].values[-1] and  df['Open'].values[-2] >df['Close'].values[-2] and df['Open'].values[-3] >df['Close'].values[-3]:
        return True
    
def three_green(df):
    if df['Open'].values[-1] < df['Close'].values[-1] and  df['Open'].values[-2] < df['Close'].values[-2] and  df['Open'].values[-3] < df['Close'].values[-3]  :
        return True      

for i in  range(100,len(data)-2):
    
    data1=data[:i]
    min_idx = list(argrelextrema(data1.Low.values, np.less, order=20)[0])[-1]
    max_idx = list(argrelextrema(data1.High.values, np.greater, order=20)[0])[-1]
    if min_idx not in local or max_idx not in local :
        if signal[-1]==1:
            
            
            if min_idx < max_idx:
                x1=data1['width'].values[min_idx]
                y1=data1.Low.values[min_idx]
    
                # min_df.loc[len(min_df.index)] = [0, 0]
                # min_df.loc[len(min_df.index)] = [0, 0]
                # min_df=min_df.shift(2)
                # min_df.loc[0] = [y1, y1]
                data1['new']= 1*(data1.width.values -x1) +y1
                if data1.High.values[-1] < data1.new.values[-1] and three_red(data1)==True :
                
                    sell=data1['Close'].values[-1]
                    signal=np.append(signal,-1)
                    selling=np.append(selling,1)
                    pat=pat+1
                    #print(buy,'= i= ',i)
                    stop_loss1= (data1.High.values[-7:]).max()
                    stop_loss=np.append(stop_loss,stop_loss1)
                    #data1['new']= 1*(data1.width.values -x1) +y1
                    data1['26.5']= 0.5*(data1.width.values -x1) +y1
                    data1['jar']= 2*(data1.width.values -x1) +y1
                    local=np.append(local,min_idx)
                    print('minimum idx==',min_idx)
                    print('seeling entry= ',sell)
                    
                
            elif  min_idx > max_idx:
                x1=data1['width'].values[max_idx]
                y1=data1.Low.values[max_idx]
    
                # max_df.loc[len(max_df.index)] = [0, 0]
                # max_df=max_df.shift(1)
                # max_df.loc[0] = [y1, y1]
                data1['new']= -1*(data1.width.values -x1) +y1
                if data1.Low.values[-1] > data1.new.values[-1] and three_green(data1)==True :
                    
                    print('maximum idx==',max_idx)
                    buy=data1['Close'].values[-1]
                    signal=np.append(signal,-1)
                    buying=np.append(buying,1)
                    pat=pat+1
                    #print(buy,'= i= ',i)
                    stop_loss1= (data1.Low.values[-7:]).min()
                    stop_loss=np.append(stop_loss,stop_loss1)
                    print('buying entry= ',buy)
                    local=np.append(local,max_idx)
                    
                    
                    data1['26.5']= -0.5*(data1.width.values -x1) +y1
                    data1['jar']= -2*(data1.width.values -x1) +y1
                   
                
                
                
                
        elif signal[-1]==-1 and selling[-1]==1:    
            if stop_loss[-1] <= data1["Close"].values[-1]:
                
                profit= sell- data["Close"].values[-1]
                
                print('selling exit point=',data["Close"].values[-1], 'sell point= ',i-1)
                pnl=np.append(pnl,profit)
                signal=np.append(signal,1)
                selling=np.append(selling,-1)
                cum_pnl=pnl.cumsum()
                if profit>0:
                    corr_pat=corr_pat+1
                    
            elif 2*(data1.width.values[-1] -x1) +y1 <= data1["Close"].values[-1]:
                
                profit= sell- data["Close"].values[-1]
                
                print('selling exit point=',data["Close"].values[-1], 'selling point= ', i-1)
                pnl=np.append(pnl,profit)
                signal=np.append(signal,1)
                selling=np.append(selling,-1)
                cum_pnl=pnl.cumsum()
                if profit>0:
                    corr_pat=corr_pat+1
                    
            elif 0.5*(data1.width.values[-1] -x1) + y1 >= data1["Close"].values[-1]:
                
                profit= sell- data["Close"].values[-1]
                
                print('selling exit point=',data["Close"].values[-1], 'sellingpoint= ', i-1)
                pnl=np.append(pnl,profit)
                signal=np.append(signal,1)
                selling=np.append(selling,-1)
                cum_pnl=pnl.cumsum()
                if profit>0:
                    corr_pat=corr_pat+1
                    
       
                    
        elif signal[-1]==-1 and buying[-1]==1:
            if stop_loss[-1] >= data1["Close"].values[-1]:
                
                profit= data1["Close"].values[-1] - buy
                print('buying exit point=',data1["Close"].values[-1],'point= ', i-1)
                pnl=np.append(pnl,profit)
                signal=np.append(signal,1)
                buying=np.append(buying,-1)
                cum_pnl=pnl.cumsum()
                if profit>0:
                    corr_pat=corr_pat+1
                    
            
            elif -2*(data1.width.values[-1] -x1) +y1 >= data1["Close"].values[-1]:
                
                profit= data["Close"].values[-1] - buy
                
                print('buying exit point=',data["Close"].values[-1], 'point= ', i-1)
                pnl=np.append(pnl,profit)
                signal=np.append(signal,1)
                buying=np.append(buying,-1)
                cum_pnl=pnl.cumsum()
                if profit>0:
                    corr_pat=corr_pat+1
                    
            elif -0.5*(data1.width.values[-1] -x1) +y1 <= data1["Close"].values[-1]:
                
                profit= data["Close"].values[-1] - buy
                
                print('buying exit point=',data["Close"].values[-1], 'point= ', i-1)
                pnl=np.append(pnl,profit)
                signal=np.append(signal,1)
                buying=np.append(buying,-1)
                cum_pnl=pnl.cumsum()
                if profit>0:
                    corr_pat=corr_pat+1

                
                             

figi = plt.figure()
axi = figi.add_subplot(111)  

try:
    lastm=np.round(cum_pnl[-1],2)
    jjjj= np.round(float(corr_pat)/float(pat),2)
    lbl= "[Accuracy = " +str(100*jjjj)+ '%]' + '[ Profit = '+ str(lastm) +'] [Total trade = '+ str(pat)+ "]  "
    #return lbl
except:
    lbl='No pattern found '

axi.plot(cum_pnl,label=lbl)
axi.legend()

st.pyplot(figi)

