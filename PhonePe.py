import streamlit as st 
import pymysql
import pandas as pd
import numpy as np
import requests
import json
import plotly.express as px
import plotly.figure_factory as ff

#tConnection to SQL
myconnection1= pymysql.connect(host = '127.0.0.1',user='root',passwd='admin@123')
cur = myconnection1.cursor()
cur.execute("create database if not exists project2sql")
myconnection = pymysql.connect(host = '127.0.0.1',user='root',passwd='admin@123',database = "project2sql")
cur = myconnection.cursor()


#page set up of streamlit
st.set_page_config(layout='wide')
st.title(":rainbow[Phonepe Pulse Data Visualization and Exploration]")
st.caption("(***Data from 2018 to 2023 in INDIA***)")
select = st.radio("select one",(":green[Transaction]",":green[User]",":green[Analysis Quaries]",":green[State wise Analysis]"))
#For Transaction based analysis
if select==":green[Transaction]":
        col1, col2, col3 = st.columns(3)
        with col1:
              option1=st.selectbox("SELECT YEAR",("2018","2019","2020","2021","2022","2023"))
        with col2:
              option2=st.selectbox("SELECT QUARTER ",("1","2","3","4"))
              st.write("1(January-March) ,2(April-June) ,3( July-September) ,4(October-December)")
        with col3:
            option3=st.selectbox("SELECT PAYMENT METHOD",("Recharge & bill payments","Peer-to-peer payments","Merchant payments","Merchant payments","Financial Services","Others"),key="option3")
        sqlquery1=cur.execute("select Year,Quater,Transaction_Type, Transaction_Count, Transaction_Amount from table_aggregated_transaction")
        fetch1=cur.fetchall()
        dataframe1=pd.DataFrame(fetch1,columns=['Year','Quarter','Transaction_Type', 'Transaction_Count', 'Transaction_Amount'])
        df1=dataframe1[(dataframe1['Year']==int(option1))&(dataframe1["Quarter"]==int(option2)) &  (dataframe1["Transaction_Type"]==option3)]
        df2=df1.groupby("Transaction_Type")["Transaction_Amount"].sum()
        df3=df1.groupby("Transaction_Type")["Transaction_Count"].sum()
        col4,col5=st.columns(2)
        with col4:
             st.write(":red[Total Transaction Amount  :]",df2.values)
        with col5:
           st.write(":red[Total Number of  Transaction:]",df3.values)
        
        #Geo plot
        cur.execute("select state,sum(Transaction_Amount),avg(Transaction_Amount) from table_aggregated_transaction group by State")
        state_trans=cur.fetchall()
        df_state_trans=pd.DataFrame(state_trans,columns=["State",'Total_Transaction_Amount',"Average_transaction"])
        df_state_trans.drop(columns=['State'], inplace=True)

        url= "https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
        response = requests.get(url)
        data1= json.loads(response.content)
        states_name= [feature["properties"]["ST_NM"] for feature in data1["features"]]
        states_name.sort()
        geo_state_name_df=pd.DataFrame({"states":states_name})
        geo_state_name_df["Transaction_Amount"]=df_state_trans['Total_Transaction_Amount']
        geo_state_name_df["Average_transaction"]=df_state_trans["Average_transaction"]
        
        fig = px.choropleth(
                geo_state_name_df,
                geojson=url,
                featureidkey='properties.ST_NM',locations='states',color='Transaction_Amount',hover_name="states",hover_data="Average_transaction",color_continuous_scale='thermal',title = 'Transaction Amount Analysis')
        fig.update_geos(fitbounds="locations", visible=False)
        fig.update_layout(title_font=dict(size=33),title_font_color='#6739b7',width=800, height=800)
        fig['layout']['xaxis']['fixedrange'] = False 
        fig['layout']['yaxis']['fixedrange'] = False
        st.plotly_chart(fig,use_container_width=True)

        fig_trans= px.bar(dataframe1 , x = 'Year', y ='Transaction_Amount',color='Quarter', title = ' All indai Transaction Analysis Chart', height = 700,)
        fig_trans.update_layout(title_font=dict(size=33),title_font_color='#6739b7')
        st.plotly_chart(fig_trans)

        fig_avg= px.line(geo_state_name_df, x='states', y='Average_transaction',title = ' Average Transaction in each state of india from 2018 to 2023',markers=True)
        st.plotly_chart(fig_avg)


#For user based analysis      
if select==":green[User]":
                     col6,col7=st.columns(2)
                     with col6:
                        option1=st.selectbox("SELECT YEAR",("2018","2019","2020","2021","2022","2023"))
                     with col7:
                          option2=st.selectbox("SELECT QUARTER ",("1","2","3","4"))
                          st.write("1(January-March) ,2(April-June) ,3( July-September) ,4(October-December)***")
        
        
                     sqlquery2=cur.execute("select Year,Quater,Registered_Users,No_of_apps_Open from table_map_user")
                     fetch2=cur.fetchall()
                     dataframe2=pd.DataFrame(fetch2,columns=['Year','Quarter', 'Registered_Users', 'No_of_apps_Open'])
                     df4=dataframe2[(dataframe2['Year']==int(option1))&(dataframe2["Quarter"]==int(option2))]
                     df5=df4[["Year",'Registered_Users']].groupby("Year")['Registered_Users'].sum()
                     df6=df4[["Year",'No_of_apps_Open']].groupby("Year")['No_of_apps_Open'].sum()
                     
                     col9,col8=st.columns(2)
                     with col9:
                        st.write(":red[Total Registered_Users  :]",df5.values)
                        
                     with col8:
                        st.write(":red[Total Number of  apps opened :]",df6.values)
                    
                     #gio plot
                     cur.execute("select state,sum(Registered_Users) from table_map_user group by State")
                     state_user=cur.fetchall()
                     df_state_user=pd.DataFrame(state_user,columns=["State",'Registered_Users'])
                     df_state_user.drop(columns=['State'], inplace=True)
                     url="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
                     response = requests.get(url)
                     data1= json.loads(response.content)
                     states_name= [feature["properties"]["ST_NM"] for feature in data1["features"]]
                     states_name.sort()
                     geo_state_name_df=pd.DataFrame({"states":states_name})
                
                     geo_state_name_df["Registered_Users"]=df_state_user

                     fig1 = px.choropleth(
                       geo_state_name_df,
                geojson=url,
                featureidkey='properties.ST_NM',locations='states',color='Registered_Users',color_continuous_scale='Viridis',title = 'User Count Analysis')
                     fig1.update_geos(fitbounds="locations", visible=False)
                     fig1.update_layout(title_font=dict(size=33),title_font_color='#6739b7',width=800, height=800)
                     fig1['layout']['xaxis']['fixedrange'] = False 
                     fig1['layout']['yaxis']['fixedrange'] = False
                     st.plotly_chart(fig1,use_container_width=True)

                     fig_user= px.bar(dataframe2 , x = 'Year', y ='Registered_Users', title = ' All indai User Analysis Chart', height = 700,)
                     fig_user.update_layout(title_font=dict(size=33),title_font_color='#6739b7')
                     st.plotly_chart(fig_user)



        
if select==":green[Analysis Quaries]":
         
               selectBox1=st.selectbox("Select a Query",("1**Most used Smart phone Brands  for phonePe ",
                                                        "2**Top 10 Districts based on  Transaction Amount",
                                                        "3** Bottom level  district based on Transaction_Amount",
                                                        "4**Top districts based on Transaction_count",
                                                        "5**Average Transaction based on year",
                                                        "6**Districts in which phonePe Usage is very low",
                                                       "7**Average Transaction based on Quarter",
                                                       "8**Top 10 state,Districts with high number of Registered_Users",
                                                       "9**Top 10 state,Districts with least number of Registered_Users",
                                                       "10**Total Number of Apps opened from 2018 to 2023"))
               
               if selectBox1=="1**Most used Smart phone Brands  for phonePe ":
                        cur.execute("select Brand,sum(User_count) from table_aggregated_user group by brand order by sum(User_count) desc")
                        fetch_brand=cur.fetchall()
                        Dataframe_brand=pd.DataFrame(fetch_brand,columns=("Year","Brand"))
                        #plot

                        fig_brand= px.scatter( Dataframe_brand, x='Year', y='Brand',title = ' Most used Brands from 2018 to 2023')
                        fig_brand.update_layout(xaxis_tickangle=-45)
                        st.plotly_chart(fig_brand)

               if selectBox1=="2**Top 10 Districts based on  Transaction Amount":
                               cur.execute("select state,  District_Name,sum(Transaction_Amount) from table_map_transaction group by state,District_Name order by sum(Transaction_Amount)  desc limit 10")
                               fetch_top_dis=cur.fetchall()
                               dataframe_top_dis=pd.DataFrame(fetch_top_dis,columns=("state","District_Name","Total_Transaction_Amount"))

                               fig_dist = px.bar(dataframe_top_dis, y='Total_Transaction_Amount', x='District_Name',color="state",title = 'Top 10 districts based on Payment')
                               fig_dist.update_layout( width=800,height=800,)
                               fig_dist.update_layout(xaxis_tickangle=-45)
                               st.plotly_chart(fig_dist)
               
               if selectBox1=="3** Bottom level  district based on Transaction_Amount":
                      cur.execute("select state,  District_Name,sum(Transaction_Amount) from table_map_transaction group by state, District_Name order by sum(Transaction_Amount)  asc limit 10")
                      fetch_least_dist=cur.fetchall()
                      dataframe_least_dist=pd.DataFrame(fetch_least_dist,columns=("state","District_Name","Total_Transaction_Amount"))
                      fig_least_dis= px.histogram(dataframe_least_dist, x="District_Name", y="Total_Transaction_Amount",color="state",title="Bottom level  districts based on Transaction_Amount") 
                      st.plotly_chart(fig_least_dis)

               

               if selectBox1=="4**Top districts based on Transaction_count":
                       
                           cur.execute("SELECT State, District_Name, SUM(Transaction_count) AS Total_count FROM  table_map_transaction GROUP BY State, District_Name ORDER BY Total_count DESC LIMIT 10")
                           fetch_top_count=cur.fetchall()
                           dataframe_top_count=pd.DataFrame(fetch_top_count,columns=("state","District_Name","Total_Transaction_count"))
                           
                           fig_count_top = px.bar(dataframe_top_count, x="District_Name", y="Total_Transaction_count",color="state",title="Top districts based on Transaction_count")
                           st.plotly_chart(fig_count_top)

               if selectBox1=="5**Average Transaction based on year":
                       cur.execute("select year,avg(Transaction_Amount)as total from table_aggregated_transaction group by year")
                       fetch_Avg_year=cur.fetchall()
                       dataframe_avg_year=pd.DataFrame(fetch_Avg_year,columns=("year","Average_Transaction_Amount"))
                           
                       
                       fig_year_ = px.pie(dataframe_avg_year,names='year', values='Average_Transaction_Amount',
                                   title='Average Transaction based on year')
                       st.plotly_chart(fig_year_)

               
               if selectBox1=="6**Districts in which phonePe Usage is very low":
                       
                           cur.execute("SELECT State, District_Name, SUM(Transaction_count) AS Total_count FROM  table_map_transaction GROUP BY State, District_Name ORDER BY Total_count asc LIMIT 10")
                           fetch_least_count=cur.fetchall()
                           dataframe_least_count=pd.DataFrame(fetch_least_count,columns=("state","District_Name","Total_Transaction_count"))
                           
                           fig_count_least = px.bar(dataframe_least_count, x="District_Name", y="Total_Transaction_count",color="state",title="10 Districts in which phonePe Usage is very low")
                           st.plotly_chart(fig_count_least)

               
               if selectBox1=="7**Average Transaction based on Quarter":
                       cur.execute("select Quater,avg(Transaction_Amount)as total from table_aggregated_transaction group by Quater")
                       fetch_Avg_=cur.fetchall()
                       dataframe_avg_=pd.DataFrame(fetch_Avg_,columns=("Quarter","Average_Transaction_Amount"))
                           
                       
                       fig_avg_ = px.pie(dataframe_avg_,names='Quarter', values='Average_Transaction_Amount',
                                   title='Average Transaction based on Quarter')
                       st.plotly_chart(fig_avg_)


               if selectBox1=="8**Top 10 state,Districts with high number of Registered_Users":
                       cur.execute("select state,District_name ,sum(Registered_Users) from table_map_user group by state,District_name order by sum(Registered_Users) desc limit 10")
                       fetch_user_=cur.fetchall()
                       dataframe_user_=pd.DataFrame(fetch_user_,columns=("state","District_Name","Total_Registered_Users"))
                           
                       
                       fig_user=px.scatter(dataframe_user_, x="District_Name", y="Total_Registered_Users", color="state",title="Top 10 state,Districts with high number of Registered_Users")
                       st.plotly_chart(fig_user)

                  

                  
               if selectBox1=="9**Top 10 state,Districts with least number of Registered_Users":
                       cur.execute("select state,District_name ,sum(Registered_Users) from table_map_user group by state,District_name order by sum(Registered_Users) asc limit 10")
                       fetch_user=cur.fetchall()
                       dataframe_user=pd.DataFrame(fetch_user,columns=("state","District_Name","Total_Registered_Users"))
                           
                       
                       fig_user_=px.bar(dataframe_user, x="District_Name", y="Total_Registered_Users", color="state",title="Top 10 state,Districts with least number of Registered_Users")
                       st.plotly_chart(fig_user_)



               if selectBox1=="10**Total Number of Apps opened from 2018 to 2023":
                       cur.execute("select year,sum(no_of_apps_open) from table_map_user group by year order by sum(no_of_apps_open)")
                       fetch_apps_=cur.fetchall()
                       dataframe_apps_=pd.DataFrame(fetch_apps_,columns=("Year","Total_Number_of_apps_opened"))
                           
                       fig_apps=px.pie(dataframe_apps_, values='Total_Number_of_apps_opened', names='Year', 
                                      title='Total Number of Apps opened from 2018 to 2023', 
                                            color_discrete_sequence=px.colors.sequential.RdBu)
                       st.plotly_chart(fig_apps)
                       
                       

if select==":green[State wise Analysis]":
              col1_,col2_=st.columns(2)
              with col1_:
                        select_state=st.selectbox("Select one state",(' Andaman & Nicobar', 'Andhra Pradesh', ' Arunachal Pradesh','Assam', 'Bihar', 
                        'Chandigarh', 'Chhattisgarh','Dadra and Nagar Haveli and Daman and Diu', 'Delhi', 'Goa', 'Gujarat', 'Haryana', ' Himachal Pradesh', 
                        'Jammu & Kashmir', 'Jharkhand', 'Karnataka', 'Kerala', 'Ladakh', 'Lakshadweep', 'Madhya Pradesh','Maharashtra', 'Manipur', 
                        'Meghalaya', 'Mizoram', 'Nagaland','Odisha', 'Puducherry', 'Punjab', 'Rajasthan', 'Sikkim', 'Tamil nadu', 'Telangana', 
                        'Tripura', 'Uttar Pradesh', 'Uttarakhand', 'West Bengal'))

                        
              with col2_:
                                
                  select2=st.selectbox("SELECT YEAR",("2018","2019","2020","2021","2022","2023"))

              cur.execute('select TA.state,TA.year,TA.Transaction_Amount,TA.Transaction_count,TU.Registered_Users from table_aggregated_transaction TA join table_map_user TU on TA.state=TU.state')
              feth_data=cur.fetchall()
              dataframe_=pd.DataFrame(feth_data,columns=("state","year","Transaction_Amount","Transaction_count","Registered_Users"))

              
              df__new=dataframe_[(dataframe_["state"]==select_state) &(dataframe_["year"]==int(select2))]
              fig12 = px.box(df__new, x='year', y='Transaction_Amount', title='Based on Transaction_Amount')
              fig13 = px.box(df__new, x='year', y='Transaction_count', title='Based on Transaction_count')
              fig14 = px.box(df__new, x='year', y='Registered_Users', title='Basd on Registered_Users')
              st.plotly_chart(fig12)
              st.plotly_chart(fig13)
              st.plotly_chart(fig14)
             
#txt = st.text_area("From this Visualizations we can get insights like :"
                 #  'Overall ranking on a particular Year and Quarter.') 

#st.info('#### From this Visualizations we can get insights like :'
      #  '\n Overall ranking on a particular Year and Quarter.'

        #'Top 10 State, District based on Total number of transaction and Total amount spent on phonepe.')
txt = st.text_area(
    "From this Visualizations we can get insights like :",
        "*Overall ranking on a particular Year and Quarter. "
        "\n *Top 10 State, District based on Total number of transaction and Total amount spent on phonepe. "
        "\n *Top 10 State, District based on Total phonepe users and their app opening frequency. "
        "\n *Top 10 mobile brands based on the how many people use phonepe. "
        "\n *Almost 66 percent of PhoneP active users are from  Maharashtra,Telangana and Karnataka. "
        "\n *After Covid the usage of PhonePe continueasly increasing,Of course we know that in covid time poeple go to online payment than direct payment and Most poeples continues."
        "\n *Digital India  concept of honourable PM also effected the PhonePe usage in Rural areas")