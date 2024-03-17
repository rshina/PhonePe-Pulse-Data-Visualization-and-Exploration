# PhonePe-Pulse-Data-Visualization-and-Exploration

About PhonePe:\n
   PhonePe is a leading digital wallet using which you can transfer money through UPI, recharge prepaid mobile, make utility bill payments, and much more. Just add your bank account details and generate a UPI ID. Without worrying about recharging your wallet, you can begin shopping safely and securely.\n
   
**Tools install

  1.python
  
  2.VSCODE
  
  3.MYSQL
  
  4.Streamlit
  
  5.github
  
**Imported Libraries
  1.git
  2.pymysql
  3.pandas
  4.plotly express
  5.streamlit
  6.requests
  7.json
  

In this Project there are 3 steps:
  1)Extract data and store the data as Dataframe
  2)Process and Transform the data
  3)Load data and Display the data using visualization tools

1)Extract data
     Initially, I Clone the data from the Phonepe GitHub repository by using Python libraries.And stored the data as Dataframe

2)Process and Transform the data
     This stage includes the cleaning of data,Here no need cleaning(data without missing data),Have to transform the data 
              structure of some columns(state).
              
  3)Load data and Display the data using visualization tools
          Finally, create a connection to the MySQL server and create a Database and stored the Transformed data in the MySQL         server,And Disply the visulization output in streamlit
      
User Guide:
   step1:
       Select any one option from transaction or User or Analysis Queries or statewise analysis.
   step2:
      If you select transaction by selecting year,quarter,payment method you will get total trasction and Geomap of          india
   step3:
      If you select User by selecting year,quarter you will get User based Visualization and Geomap of india
  step4:
     If you select Analysis Queries you have to select any query from 10 will get   Visualization basedon perticular query
  step4:
     If you select statewise analysis by selecting state,year you will get state wise transaction and user data Visualization


   Here completed the project PhonePe-Pulse-Data-Visualization-and-Exploration


     
     
