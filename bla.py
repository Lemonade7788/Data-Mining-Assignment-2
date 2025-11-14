import streamlit as st
import pandas as pd
import plotly.express as px

# Load and clean data
df = pd.read_csv("MFGEmployees4.csv")
df = df.dropna(subset=['DepartmentName', 'AbsentHours', 'Age'])

# Page config
st.set_page_config(layout="wide", page_title="Interactive MFG Dashboard")
st.title("📊 Interactive MFG Employee Dashboard")

# Sidebar controls
st.sidebar.header("🔧 Customize Dashboard")

# Bar chart controls
st.sidebar.subheader("Bar Chart")
bar_title = st.sidebar.text_input("Bar Chart Title", "Top 10 Departments by Employee Count")
bar_color = st.sidebar.color_picker("Bar Color", "#1f77b4")

# Line chart controls
st.sidebar.subheader("Line Chart")
line_title = st.sidebar.text_input("Line Chart Title", "Average Absent Hours per Department")
line_color = st.sidebar.color_picker("Line Color", "#008080")

# Histogram controls
st.sidebar.subheader("Histogram")
hist_title = st.sidebar.text_input("Histogram Title", "Distribution of Employee Ages")
hist_color = st.sidebar.color_picker("Histogram Bar Color", "#FFA500")
hist_bins = st.sidebar.slider("Number of Bins", min_value=5, max_value=30, value=15)

# Bubble chart controls
st.sidebar.subheader("Bubble Chart")
bubble_title = st.sidebar.text_input("Bubble Chart Title", "Absent Hours by Age Group")
bubble_color = st.sidebar.color_picker("Bubble Color", "#636EFA")

# Layout: 2 rows × 2 columns
col1, col2 = st.columns([1, 1])

# 1️⃣ Bar Chart
with col1:
    st.subheader(bar_title)
    dept_count = df['DepartmentName'].value_counts().head(10).reset_index()
    dept_count.columns = ['Department', 'Count']
    fig1 = px.bar(dept_count, x='Department', y='Count',
                  color_discrete_sequence=[bar_color],
                  height=300, labels={'Count': 'Number of Employees'})
    fig1.update_layout(xaxis_tickangle=-45, margin=dict(t=30, b=30))
    st.plotly_chart(fig1, use_container_width=True)

# 2️⃣ Line Chart
with col2:
    st.subheader(line_title)
    avg_absent = df.groupby('DepartmentName')['AbsentHours'].mean().sort_values(ascending=False).head(10).reset_index()
    fig2 = px.line(avg_absent, x='DepartmentName', y='AbsentHours', markers=True,
                   line_shape='linear', color_discrete_sequence=[line_color],
                   height=300, labels={'AbsentHours': 'Avg Absent Hours'})
    fig2.update_layout(xaxis_tickangle=-45, margin=dict(t=30, b=30))
    st.plotly_chart(fig2, use_container_width=True)

# Row 2
col3, col4 = st.columns([1, 1])

# 3️⃣ Histogram
with col3:
    st.subheader(hist_title)
    fig3 = px.histogram(df, x='Age', nbins=hist_bins,
                        height=300, labels={'Age': 'Employee Age'},
                        title=hist_title)
    fig3.update_traces(marker_line_color='black', marker_line_width=1,
                       marker_color=hist_color)
    fig3.update_layout(margin=dict(t=30, b=30))
    st.plotly_chart(fig3, use_container_width=True)

# 4️⃣ Bubble Chart
with col4:
    st.subheader(bubble_title)
    bins = pd.cut(df['Age'], bins=range(int(df['Age'].min()), int(df['Age'].max())+5, 5))
    grouped = df.groupby(bins).agg({'AbsentHours':'mean', 'Age':'count'}).rename(columns={'Age':'Count'}).dropna()
    grouped['Midpoint'] = [interval.mid for interval in grouped.index]
    fig4 = px.scatter(grouped, x='Midpoint', y='AbsentHours', size='Count',
                      height=300, labels={'Midpoint': 'Age Group Midpoint', 'AbsentHours': 'Avg Absent Hours'},
                      color_discrete_sequence=[bubble_color])
    fig4.update_layout(margin=dict(t=30, b=30))
    st.plotly_chart(fig4, use_container_width=True)