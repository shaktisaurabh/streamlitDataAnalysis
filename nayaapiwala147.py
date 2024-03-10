import pandas as pd 
import streamlit as st 
import matplotlib.pyplot as plt
st.set_page_config(layout='wide',page_title='WhatAShot')

df=pd.read_csv(r"C:\Users\LENOVO\Downloads\startup_cleaned.csv") 
df['date']=pd.to_datetime(df['date'],errors='coerce') 
df['year']=df['date'].dt.year 
df['month']=df['date'].dt.month 
st.sidebar.title('Startup Funding Analysis') 
def band1():
    st.header('Overall Analysis')
    #total invested amount
    total=round(df['amount'].sum()) 
    #max amount infused in a startup
    max=round(df.groupby('startup')['amount'].max().sort_values(ascending=False).head(1).values[0]) 
    #avg ticket size
    avg=round(df.groupby('startup')['amount'].sum().mean())
    #total funded startups 
    num_startups=df['startup'].nunique() 
    col1,col2,col3,col4=st.columns(4) 
    with col1:
        st.metric('Total',str(total)+' Cr') 
    with col2:
        st.metric('Max',str(max)+' Cr') 
    with col3:
        st.metric('Average',str(avg)+' Cr') 
    with col4:
        st.metric('Funded startups',num_startups)
    st.subheader('MOM chart') 
    option=st.selectbox('Select option',['Total','Count']) 
    if option=='Total':
        temp_df=df.groupby(['year','month'])['amount'].sum().reset_index()
    else:
        temp_df=df.groupby(['year','month'])['amount'].count().reset_index()  
    temp_df['x_axis']=temp_df['year'].astype('str')+'-'+temp_df['month'].astype('str')
    fig,ax=plt.subplots() 
    ax.bar(temp_df['x_axis'],temp_df['amount']) 
    st.pyplot(fig)
     

def band(amb):
    st.title(amb) 
    df5=df[df['investors'].str.contains(amb)].sort_values('date',ascending=False).head()
    st.subheader('Most recent investment') 
    st.dataframe(df5)
    col1,col2,col3,col4=st.columns(4) 
    with col1:
      df6=df[df['investors'].str.contains(amb)].groupby('startup')['amount'].sum().sort_values(ascending=False).head()
      st.subheader('Biggest investments')
      fig,ax=plt.subplots() 
      ax.bar(df6.index,df6.values) 
      st.pyplot(fig) 
    with col2:
        df7=df[df['investors'].str.contains(amb)].groupby('vertical')['amount'].sum().sort_values(ascending=False)
        st.subheader('Sectors invested in') 
        fig,ax=plt.subplots() 
        ax.pie(df7,labels=df7.index,autopct="%0.01f%%") 
        st.pyplot(fig) 
    with col3:
        df8=df[df['investors'].str.contains(amb)].groupby('City  Location')['amount'].sum().sort_values(ascending=False)
        st.subheader('Investments w.r.t cities') 
        fig,ax=plt.subplots() 
        ax.pie(df8,labels=df8.index,autopct="%0.01f%%") 
        st.pyplot(fig) 
    with col4:
        df9=df[df['investors'].str.contains(amb)].groupby('round')['amount'].sum().sort_values(ascending=False) 
        st.subheader('Investments w.r.t sectors') 
        fig,ax=plt.subplots() 
        ax.pie(df9,labels=df9.index,autopct="%0.01f%%") 
        st.pyplot(fig) 
    df['year']=df['date'].dt.year 
    df10=df[df['investors'].str.contains(amb)].groupby('year')['amount'].sum()
    st.subheader('YOY investment analysis') 
    fig,ax=plt.subplots() 
    ax.plot(df10.index,df10.values) 
    st.pyplot(fig)









a1=st.sidebar.selectbox('Select one',['Overall analysis','Startup','Investor']) 
if a1=='Overall analysis':
        band1()
elif a1=='Investor':
    st.title('Investor analysis') 

    amb=st.sidebar.selectbox('Enter investor name',sorted(set(df['investors'].str.split(',').sum())))
    btn1=st.sidebar.button('Find investor details') 
    if btn1:
        band(amb)
else:
    st.title('Startup names') 
    st.sidebar.selectbox('Enter startup names',sorted(df['Startup Name'].unique().tolist())) 
    btn2=st.sidebar.button('Find startup analysis') 