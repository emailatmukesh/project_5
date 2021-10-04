import yfinance as yf
import streamlit as st
from datetime import date
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
from scipy.signal import argrelextrema



today = date.today()

st.write("""
#  Project 5 

Shown are the stock closing price and volume of ticker!

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
    peri='3mo'
elif options=='1d' or'1wk':
    peri='1y'

data = yf.download(tickerSymbol, period=peri, interval=options)

data['width']=(0.38*(data.High-data.Low.values)).cumsum()
pp=data['width'].shift(1)
data.reset_index(inplace = True)

size = st.number_input('Insert an integer number of candle you want to see',min_value=1, max_value=None, value=100)
st.write('Currently you are seeing last ', size,' candles')

rect=['a']*size
for i in range(size):
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
    max_idx = list(argrelextrema(data.High.values, np.greater, order=yy)[0])[-10:]
    
    
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
    min_idx = list(argrelextrema(data.Low.values, np.less, order=yy)[0])[-10:]
    
    
   
    
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
            
     
            
            
    
            
    # print(pricez)
    
    # len2=len(data)-a
    # ax.plot(max_idx[-5:],pricez[-5:])


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

