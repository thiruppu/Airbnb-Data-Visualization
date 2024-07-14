import streamlit as st
import pandas as pd
import plotly.express as px

# Set page configuration to wide
st.set_page_config(layout="wide")

# Load data
st_data = pd.read_csv('project04_st.csv')

# Convert host_host_id to string
st_data["host_host_id"] = st_data["host_host_id"].astype(str)

# Extract unique years and months
year = st_data["review_year"].unique()
month = st_data["review_month"].unique()

# Convert unique years and months to lists and sort them
year_list = sorted(list(year))
month_list = sorted(list(month))

# Define function to generate total reviews by year chart
def total_review_by_year():
    grouped_sum = st_data.groupby("review_year")[["number_of_reviews"]].sum().reset_index()
    grouped_sum_chart = px.line(grouped_sum, x="review_year", y="number_of_reviews", title="Total reviews by year")
    return grouped_sum_chart

# Define function to generate total reviews by month chart
def total_review_by_month():
    grouped_sum = st_data.groupby("review_month")[["number_of_reviews"]].sum().reset_index()
    grouped_sum_map_chart = px.bar(grouped_sum, x="review_month", y="number_of_reviews", title="Total reviews by month")
    return grouped_sum_map_chart    

# Define function to generate overall reviews for a selected year
def overall_reviews(select_year):
    selected_year = st_data[st_data["review_year"] == select_year]
    combined = selected_year.groupby("review_month")[["number_of_reviews"]].sum().reset_index()
    combined_overview = px.bar(combined, x="review_month", y="number_of_reviews", title=f"Total reviews by month for {select_year}",color_discrete_sequence=px.colors.sequential.Bluered)
    return combined_overview

# Define function to get top hosts
def top_hosts():
    filtered_data = st_data[st_data["number_of_reviews"] > 0]
    host = filtered_data[["number_of_reviews", "host_host_id"]]
    host_sorted = host.sort_values(by="number_of_reviews", ascending=False)
    host_sorted_1 = host_sorted.head(10).reset_index(drop=True)
    return host_sorted_1

# Sidebar navigation
st.sidebar.title("Navigation")
page = st.sidebar.selectbox("Select Page", ["About", "Main Menu"])

# About page
if page == "About":
    st.title("Airbnb Data Visualization")
    st.markdown("""
    This project aims to analyze and visualize Airbnb listing data to provide insights into trends, host performance, and review patterns. The key features of this project include:
    
    1. **MongoDB Connection and Data Retrieval**: Establish a connection to the MongoDB Atlas database and retrieve the Airbnb dataset. Perform queries and data retrieval operations to extract the necessary information for your analysis.
    2. **Data Cleaning and Preparation**: Clean the Airbnb dataset by handling missing values, removing duplicates, and transforming data types as necessary. Prepare the dataset for EDA and visualization tasks, ensuring data integrity and consistency.
    3. **Geospatial Visualization**: Develop a Streamlit web application that utilizes the geospatial data from the Airbnb dataset to create interactive maps. Visualize the distribution of listings across different locations, allowing users to explore prices, ratings, and other relevant factors.
    4. **Price Analysis and Visualization**: Use the cleaned data to analyze and visualize how prices vary across different locations, property types, and seasons. Create dynamic plots and charts that enable users to explore price trends, outliers, and correlations with other variables.
    5. **Availability Analysis by Season**: Analyze the availability of Airbnb listings based on seasonal variations. Visualize the occupancy rates, booking patterns, and demand fluctuations throughout the year using line charts, heatmaps, or other suitable visualizations.
    6. **Location-Based Insights**: Investigate how the price of listings varies across different locations. Use MongoDB queries and data aggregation techniques to extract relevant information for specific regions or neighborhoods. Visualize these insights on interactive maps or create dashboards in tools like Tableau or Power BI.
    7. **Interactive Visualizations**: Develop dynamic and interactive visualizations that allow users to filter and drill down into the data based on their preferences. Enable users to interact with the visualizations to explore specific regions, property types, or time periods of interest.
    8. **Dashboard Creation**: Utilize Tableau or Power BI to create a comprehensive dashboard that presents key insights from your analysis. Combine different visualizations, such as maps, charts, and tables, to provide a holistic view of the Airbnb dataset and its patterns.
    
    
    
    This project utilizes various technologies and libraries to achieve its goals:
    
    - **Python**: For data manipulation and analysis.
    - **Pandas**: For data handling and transformation.
    - **Plotly**: For creating interactive charts.
    - **Streamlit**: For building the web app and displaying the visualizations.
    - **Power BI**: For advanced and comprehensive data visualization.
    
    Feel free to explore the visualizations and insights provided by this project.
    """)

# Main Menu page
elif page == "Main Menu":
    st.title("Airbnb Data Visualization")
    
    col1, col2 = st.columns(2)

    with col1:
        # Display total reviews by year chart
        st.subheader("Total Reviews by Year")
        review_by_year = total_review_by_year()
        st.plotly_chart(review_by_year)

    with col2:
        # Display total reviews by month chart
        st.subheader("Total Reviews by Month")
        review_by_month = total_review_by_month()
        st.plotly_chart(review_by_month)


    # Select year and display overall reviews for that year
    st.subheader("Overall Reviews for Selected Year")
    select_year = st.selectbox("Select Year", year_list)
    submit_button = st.button("Submit")

    if submit_button:
        overall = overall_reviews(select_year)
        st.plotly_chart(overall)
    st.subheader("Top 10 Hosts based on Customer Reviews")
    col3,col4,col5=st.columns(3)
    
    with col4:
        # Display top 10 hosts
        
        top_ten_hosts = top_hosts()
        st.dataframe(top_ten_hosts)