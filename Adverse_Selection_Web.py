import streamlit as st
import re
import pandas as pd
import numpy as np


csv_gh = "https://raw.githubusercontent.com/Noel-Ocean/Testing/main/CMED6902%20-%20Adverse%20Selection%20Experiment%20Dataset.csv"
df = pd.read_csv(csv_gh)
df.columns=["Character Descriptions", "Pr(minor), Cost=$8K", "Pr(major), Cost=$200K",
            "Expected Cost of Care($)", "Bronze($)", "Silver($)", "Gold($)"]

st.set_page_config(layout="wide")

# sidebar
st.sidebar.write("**CMED6902 Health Economics**")
st.sidebar.write("Adverse Selection: A Classroom Experiment")
st.sidebar.write("**Reference**: Hodgson, A. (2014). Adverse Selection in Health Insurance Markets: A Classroom Experiment. The Journal of Economic Education, 45(2), 90-100.")

st.write("**Please choose a page**")
page = st.selectbox("", ["About this Web App", "View/Download Dataset", "Run Experiment"])

if page=='About this Web App':
    st.subheader("About this Web App")
    st.write("This web app is run as a seminar activity for Health Economics.")
    st.write("The activity mimics the consumer decision making, price rises and market collapse in heatlh insurance market, illustrating the concept of Adverse Selection.")
    st.write("**Adverse Selection** occurs as a result of asymmetric information of on the characteristics of the insured between the insurer and insured in the health insurance market. Individuals may have better idea of their risk status than does the insurance company. Insurer set upprice premium based on the “average” probability of adverse event.")

elif page=="View/Download Dataset":
    st.subheader("View/Downlad Dataset")
    @st.cache
    def convert_df(dataframe):
        return dataframe.to_csv().encode('utf-8')
        
    csv = convert_df(df)
    st.download_button(
     label="Download data as CSV",
     data=csv,
     file_name='Adverse_Experiment.csv',
     mime='text/csv')

    st.table(df)
    # table = ff.create_table(df)
    # iplot.iplot(table, filename='pandas_table')

elif page=="Run Experiment":
    st.subheader("Run Experiment")

    Bronze=[]
    for i,j in zip(range(1,31), df["Bronze($)"]):
        Bronze.append(f"Character{i}, ${j}")

    Silver=[]
    for i,j in zip(range(1,31), df["Silver($)"]):
        Silver.append(f"Character{i}, ${j}")
    
    Gold=[]
    for i,j in zip(range(1,31), df["Gold($)"]):
        Gold.append(f"Character{i}, ${j}")

    Bronze_plan =  st.multiselect('Bronze', options=Bronze, default=Bronze, key=int)
    Silver_plan = st.multiselect('Silver', options=Silver, default=Silver, key=int) 
    Gold_plan = st.multiselect('Gold', options=Gold, default=Gold, key=int) 

    Bronze_cal = []
    for i in Bronze_plan:
        find = re.findall('(\w+)\s*$', i)
        Bronze_cal.append(int(find[0]))

    Silver_cal = []
    for i in Silver_plan:
        find = re.findall('(\w+)\s*$', i)
        Silver_cal.append(int(find[0]))
   
    Gold_cal = []
    for i in Gold:
        find = re.findall('(\w+)\s*$', i)
        Gold_cal.append(int(find[0]))

    Bronze_average = sum(Bronze_cal)/30
    Silver_average = sum(Silver_cal)/30
    Gold_average = sum(Gold_cal)/30

    st.write("**Please monitor the change**")
    plot = pd.DataFrame({"Bronze": Bronze_average, "Silver": Silver_average, "Gold": Silver_average}, index=[0]).T
    plot.columns=["Insurance Plan"]
    st.bar_chart(data=plot, width=700, height=400)
