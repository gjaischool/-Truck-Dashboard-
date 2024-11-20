import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
import numpy as np
import time
import streamlit.components.v1 as components
import folium
import base64
import os
import threading

# Font settings (you can remove this if no font customization is needed)
plt.rcParams['axes.unicode_minus'] = False  # Prevents minus symbol issues

# Page configuration
st.set_page_config(page_title="화물 차량 대시보드", layout="wide", page_icon=None, initial_sidebar_state="auto", menu_items=None)

# Load icons from specified paths
def load_icon_as_base64(path):
    with open(path, "rb") as file:
        return base64.b64encode(file.read()).decode('utf-8')

# Paths to icon files
icon_drowsy_path = "data/DR.png"
icon_normal_path = "data/NO.png"
icon_truck_path = "data/Truck.png"
icon_driver_path = "data/Driver.png"

# Encode the drowsy, normal, truck, and driver icons
icon_drowsy_base64 = load_icon_as_base64(icon_drowsy_path)
icon_normal_base64 = load_icon_as_base64(icon_normal_path)
icon_truck_base64 = load_icon_as_base64(icon_truck_path)
icon_driver_base64 = load_icon_as_base64(icon_driver_path)

# Load CSV data
csv_path = "data/Dashboard_downloadable.csv"  # Updated path to use uploaded CSV file
try:
    df = pd.read_csv(csv_path)
    df.columns = df.columns.str.strip()  # Remove leading/trailing whitespace from column names
except FileNotFoundError:
    st.error("CSV 파일을 찾을 수 없습니다. 파일 경로를 확인해주세요.")
    df = pd.DataFrame()  # Create an empty dataframe to prevent further errors

# Real-time updating section with a placeholder for the entire dashboard
placeholder = st.empty()

# Initialize map with folium
initial_location = [35.1595, 126.8526]  # Gwangju, South Korea (as in the example image)
map_placeholder = st.empty()

# Generate driver information for display using correct English column names
if not df.empty:
    df.columns = df.columns.str.lower().str.replace(' ', '_')  # Normalize column names
    driver_data = df[[
        'car_number', 'name', 'locate', 'driving_distance', 'driving_time', 'safe_score', 'drawniess_detection'
    ]].to_dict(orient='records')
else:
    driver_data = []

# Function to toggle the visibility of the animated text
def toggle_visibility():
    while True:
        st.session_state['show_text'] = not st.session_state.get('show_text', True)
        time.sleep(1)

# Start a separate thread to toggle the visibility of the text
if 'text_thread' not in st.session_state:
    st.session_state['text_thread'] = threading.Thread(target=toggle_visibility, daemon=True)
    st.session_state['text_thread'].start()

# Display the dashboard
while True:
    with placeholder.container():
        # Display current time
        now = datetime.now()
        st.image('data/truck11.jpg', use_container_width=True)
        
        st.markdown(f"<p style='color: black;'>현재 시간: {now.strftime('%Y.%m.%d %H:%M:%S')}</p>", unsafe_allow_html=True)

        # Add new section header for 전체 운전자 통계 with updated color
        st.markdown(
            """
            <div style='background-color: #87CEEB; padding: 10px;'>
                <h2 style='color: black;'>전체 운전자 통계</h2>
            </div>
            """,
            unsafe_allow_html=True
        )

        # Set background color to white for entire container
        st.markdown(
            """
            <style>
                .stApp {
                    background-color: white;
                }
                ::-webkit-scrollbar {
                    width: 12px;
                }
                ::-webkit-scrollbar-track {
                    background: lightgray;
                }
                ::-webkit-scrollbar-thumb {
                    background: gray;
                    border-radius: 10px;
                }
            </style>
            """,
            unsafe_allow_html=True
        )

        # Dashboard Layout with Four Panels in One Row
        col1, col2, col3, col4 = st.columns(4)

        # Cargo Transport Status with Truck and Driver Icons
        with col1:
            st.markdown("<h2 style='color: black;'>차량/운전자 상태</h2>", unsafe_allow_html=True)
            truck_driver_html = f"""
                <div style='display: flex; justify-content: space-around; align-items: center;'>
                    <div style='text-align: center; color: black;'>
                        <img src='data:image/png;base64,{icon_truck_base64}' style='width:80px;height:80px;'>
                        <br><span style='font-size: 1.5em;'>트럭 수: <strong>50</strong></span>
                    </div>
                    <div style='text-align: center; color: black;'>
                        <img src='data:image/png;base64,{icon_driver_base64}' style='width:80px;height:80px;'>
                        <br><span style='font-size: 1.5em;'>운전자 수: <strong>45</strong></span>
                    </div>
                </div>
            """
            st.markdown(truck_driver_html, unsafe_allow_html=True)

        # Safe Driving Status Graph
        with col2:
            st.markdown("<h2 style='color: black;'>운전 상태</h2>", unsafe_allow_html=True)
            drowsy_placeholder = st.empty()
            drowsy, safe = np.random.randint(0, 100, 2)
            fig, ax = plt.subplots(figsize=(4, 3))  # Adjust the figure size for better display
            ax.bar(["Drowsy", "Safe"], [drowsy, safe], color=['#1f77b4', '#17becf'])
            ax.set_ylim(0, 100)  # Set Y-axis limits to reflect percentages
            ax.set_facecolor('white')
            fig.patch.set_facecolor('white')  # Set figure background color to white
            ax.tick_params(axis='x', labelsize=8, colors='black')  # Set tick label color to black
            ax.tick_params(axis='y', labelsize=8, colors='black')
            ax.title.set_color('black')
            drowsy_placeholder.pyplot(fig)
            plt.close(fig)

        # Safety Score Statistics Pie Chart
        with col3:
            st.markdown("<h2 style='color: black;'>안전 점수 분포</h2>", unsafe_allow_html=True)
            score_placeholder = st.empty()
            labels = ["80-100", "60-79", "26-59", "0-25"]
            score_ranges = [np.random.randint(0, 50) for _ in range(4)]
            fig, ax = plt.subplots(figsize=(4, 3))  # Adjust the figure size for better display
            ax.pie(score_ranges, labels=labels, autopct='%1.1f%%', startangle=90, colors=['#1f77b4', '#aec7e8', '#17becf', '#9edae5'], textprops={'fontsize': 7, 'color': 'black'})
            ax.axis('equal')
            ax.set_facecolor('white')
            fig.patch.set_facecolor('white')  # Set figure background color to white
            score_placeholder.pyplot(fig)
            plt.close(fig)

        # Driving Information Vertical Bar Graph
        with col4:
            st.markdown("<h2 style='color: black;'>운행 정보</h2>", unsafe_allow_html=True)
            distance_placeholder = st.empty()
            today_dist, yesterday_dist = np.random.randint(0, 100, 2)
            fig, ax = plt.subplots(figsize=(5, 4))  # Increase the figure size to avoid clipping
            ax.barh(["Today's Distance", "Yesterday's Distance"], [today_dist, yesterday_dist], color=['#1f77b4', '#17becf'])  # Set specific percentages for 'Driving distance'
            ax.set_xlim(0, 100)  # Set X-axis limits to reflect percentages
            ax.set_facecolor('white')
            fig.patch.set_facecolor('white')  # Set figure background color to white
            ax.tick_params(axis='x', labelsize=8, colors='black')
            ax.tick_params(axis='y', labelsize=8, colors='black')
            ax.title.set_color('black')
            distance_placeholder.pyplot(fig)
            plt.close(fig)

        # 운전자 정보 and Map in One Row with scrollbar for long list
        driver_col, map_col = st.columns([1, 2])

        # Driver Information Panel
        with driver_col:
            st.markdown("<h2 style='color: black;'>운전자 정보</h2>", unsafe_allow_html=True)
            driver_info_container = st.container()
            with driver_info_container:
                if driver_data:
                    driver_info_html = "<div style='height: 500px; overflow-y: auto; scrollbar-width: thick; scrollbar-color: gray lightgray;'>"
                    for driver in driver_data:
                        icon_base64 = icon_normal_base64
                        driver_html = f"<div style='display: flex; align-items: center; margin-bottom: 10px; color: black;'>"
                        driver_html += f"<img src='data:image/png;base64,{icon_base64}' style='width:30px;height:30px;margin-right:10px;'>"
                        driver_html += f"<div><strong>{driver['car_number']}</strong><br>{driver['name']} ({driver['locate']})</div></div>"
                        driver_info_html += driver_html
                    driver_info_html += "</div>"
                    st.markdown(driver_info_html, unsafe_allow_html=True)

        # Real-time Map Update
        with map_col:
            st.markdown("<h2 style='text-align: center; color: black;'>화물 차량 상태 모니터링</h2>", unsafe_allow_html=True)
            if st.session_state.get('show_text', True):
                st.markdown("<div style='text-align: center; color: black; font-size: 1em; padding: 5px; border: 1px solid #ccc; display: inline-block;'>직선 구간 3km 이상시에만 졸음 탐지 기능 활성화</div>", unsafe_allow_html=True)
            folium_map = folium.Map(location=initial_location, zoom_start=12)
            
            # Randomly generate locations along highways around Gwangju for vehicle icons
            for i in range(13):
                random_location = [
                    initial_location[0] + np.random.uniform(-0.1, 0.1),
                    initial_location[1] + np.random.uniform(-0.1, 0.1)
                ]
                status_icon = np.random.choice(['졸음', '정상'])
                icon_base64 = {
                    '졸음': icon_drowsy_base64,
                    '정상': icon_normal_base64
                }[status_icon]
                icon_html = f"<img src='data:image/png;base64,{icon_base64}' style='width:60px;height:60px;'>"
                folium.Marker(
                    location=random_location,
                    popup=f"Vehicle {i+1} - Status: {status_icon}",
                    icon=folium.DivIcon(html=icon_html)
                ).add_to(folium_map)
            
            # Display map in Streamlit
            map_html = folium_map._repr_html_()
            components.html(map_html, height=500)

        # 트럭 기사 안전운전 세부 조회 Section with Search Functionality
        st.markdown(
            """
            <div style='background-color: #4682B4; padding: 10px; text-align: left;'>
                <h2 style='color: white;'>트럭 기사 안전운전 세부 조회</h2>
            </div>
            """,
            unsafe_allow_html=True
        )
        search_query = st.text_input("이름 (연락처) 검색", "", help="이름 (연락처)를 입력하세요", max_chars=20, key="search_input")
        search_button = st.button("🔍 검색", key="search_button")
        
        if not df.empty and search_button:
            # Fetch driver data from CSV
            driver_info = df[df['name'].str.contains(search_query, case=False, na=False)]
            
            safety_col1, safety_col2 = st.columns(2)

            if not driver_info.empty:
                for index, row in driver_info.iterrows():
                    with safety_col1:
                        st.markdown(f"<h3 style='color: black;'>{row['name']} | {row['car_number']} | {row['locate']}</h3>", unsafe_allow_html=True)
                        st.markdown(f"<p style='color: black;'>주행 거리: {row['driving_distance']}km</p>", unsafe_allow_html=True)
                        st.markdown(f"<p style='color: black;'>주행 시간: {row['driving_time']}</p>", unsafe_allow_html=True)
                        st.markdown(f"<p style='color: black;'>안전 점수: {row['safe_score']}</p>", unsafe_allow_html=True)
                        st.markdown(f"<p style='color: black;'>졸음 감지: {row['drawniess_detection']}회</p>", unsafe_allow_html=True)
                        st.markdown("<h3 style='color: black;'>졸음 운전 통계</h3>", unsafe_allow_html=True)
                        labels = ["Distance Traveled", "Driving Hours", "Safety Score", "Drowsiness Events"]
                        values = [row['driving_distance'], row['driving_time'], row['safe_score'], row['drawniess_detection']]
                        fig, ax = plt.subplots(figsize=(5, 3))
                        ax.bar(labels, values, color='#1f77b4')
                        ax.set_facecolor('white')
                        fig.patch.set_facecolor('white')  # Set figure background color to white
                        ax.set_xlabel("Category", fontsize=8, color='black')
                        ax.set_ylabel("Value", fontsize=8, color='black')
                        ax.tick_params(axis='x', labelsize=8, colors='black')
                        ax.tick_params(axis='y', labelsize=8, colors='black')
                        plt.close(fig)  # Close the figure to prevent warning
                        st.pyplot(fig)

    # Hide the pink box at the bottom with additional vertical spacing
    st.markdown(
        """
        <div style='height: 1000px;'></div>  <!-- Add vertical spacing to push pink box down -->
        <div style='background-color: white; color: white; padding: 10px;'>
            <pre> </pre>
        </div>
        """,
        unsafe_allow_html=True
    )
    
    # Delay to simulate real-time updates
    time.sleep(5)
