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

# Real-time updating section with a placeholder for the entire dashboard
placeholder = st.empty()

# Initialize map with folium
initial_location = [35.1595, 126.8526]  # Gwangju, South Korea (as in the example image)
map_placeholder = st.empty()

# Generate fake driver information for display
driver_data = [
    {"차량 번호": "180호2274", "운전자 이름": "김*천", "연락처": "010-****-6372", "상태": "정상"},
    {"차량 번호": "180호2274", "운전자 이름": "조*비", "연락처": "010-****-3232", "상태": "정상"},
    {"차량 번호": "180호2274", "운전자 이름": "노*노", "연락처": "010-****-1092", "상태": "정상"},
    {"차량 번호": "180호2274", "운전자 이름": "백*태", "연락처": "010-****-0239", "상태": "정상"},
    {"차량 번호": "180호2274", "운전자 이름": "장*호", "연락처": "010-****-1202", "상태": "정상"},
]

# Display the dashboard
with placeholder.container():
    # Display current time
    now = datetime.now()
    st.markdown("<h1 style='color: black;'>화물 차량 대시보드</h1>", unsafe_allow_html=True)
    st.markdown(f"<p style='color: black;'>현재 시간: {now.strftime('%Y.%m.%d %H:%M:%S')}</p>", unsafe_allow_html=True)

    # Set background color to white for entire container
    st.markdown(
        """
        <style>
            .stApp {
                background-color: white;
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
                    <img src='data:image/png;base64,{icon_truck_base64}' style='width:40px;height:40px;'>
                    <br>트럭 수: <strong>50</strong>
                </div>
                <div style='text-align: center; color: black;'>
                    <img src='data:image/png;base64,{icon_driver_base64}' style='width:40px;height:40px;'>
                    <br>운전자 수: <strong>45</strong>
                </div>
            </div>
        """
        st.markdown(truck_driver_html, unsafe_allow_html=True)

    # Safe Driving Status Graph
    with col2:
        st.markdown("<h2 style='color: black;'>운전 상태</h2>", unsafe_allow_html=True)
        fig, ax = plt.subplots(figsize=(3, 2))
        ax.bar(["Drowsy", "Safe"], [25, 20], color=['#1f77b4', '#17becf'])
        ax.set_facecolor('white')
        fig.patch.set_facecolor('white')  # Set figure background color to white
        ax.tick_params(axis='x', labelsize=8, colors='black')  # Set tick label color to black
        ax.tick_params(axis='y', labelsize=8, colors='black')
        ax.title.set_color('black')
        plt.close(fig)  # Close the figure to prevent warning
        st.pyplot(fig)

    # Safety Score Statistics Pie Chart
    with col3:
        st.markdown("<h2 style='color: black;'>안전 점수 분포</h2>", unsafe_allow_html=True)
        labels = ["80-100", "60-79", "26-59", "0-25"]
        sizes = [8, 15, 5, 2]
        fig, ax = plt.subplots(figsize=(3, 2))
        ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90, colors=['#1f77b4', '#aec7e8', '#17becf', '#9edae5'], textprops={'fontsize': 7, 'color': 'black'})
        ax.axis('equal')
        ax.set_facecolor('white')
        fig.patch.set_facecolor('white')  # Set figure background color to white
        plt.close(fig)  # Close the figure to prevent warning
        st.pyplot(fig)

    # Driving Information Vertical Bar Graph
    with col4:
        st.markdown("<h2 style='color: black;'>운행 정보</h2>", unsafe_allow_html=True)
        fig, ax = plt.subplots(figsize=(3, 2))
        ax.barh(["Today's Distance", "Yesterday's Distance"], [120, 100], color=['#1f77b4', '#17becf'])
        ax.set_facecolor('white')
        fig.patch.set_facecolor('white')  # Set figure background color to white
        ax.tick_params(axis='x', labelsize=8, colors='black')  # Set tick label color to black
        ax.tick_params(axis='y', labelsize=8, colors='black')
        ax.title.set_color('black')
        plt.close(fig)  # Close the figure to prevent warning
        st.pyplot(fig)

    # 운전자 정보 and Map in One Row
    driver_col, map_col = st.columns([1, 2])

    # Driver Information Panel
    with driver_col:
        st.markdown("<h2 style='color: black;'>운전자 정보</h2>", unsafe_allow_html=True)
        for driver in driver_data:
            icon_base64 = icon_normal_base64
            driver_html = f"<div style='display: flex; align-items: center; margin-bottom: 10px; color: black;'>"
            driver_html += f"<img src='data:image/png;base64,{icon_base64}' style='width:30px;height:30px;margin-right:10px;'>"
            driver_html += f"<div><strong>{driver['차량 번호']}</strong><br>{driver['운전자 이름']} ({driver['연락처']})</div></div>"
            st.markdown(driver_html, unsafe_allow_html=True)

    # Real-time Map Update
    with map_col:
        st.markdown("<h2 style='text-align: center; color: black;'>화물 차량 상태 모니터링</h2>", unsafe_allow_html=True)
        folium_map = folium.Map(location=initial_location, zoom_start=12)
        
        # Randomly generate locations around Gwangju for vehicle icons
        for i in range(5):
            random_location = [
                initial_location[0] + np.random.uniform(-0.05, 0.05),
                initial_location[1] + np.random.uniform(-0.05, 0.05)
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

    # 트럭 기사 안전 세부 정보
    st.markdown("<h2 style='color: black;'>트럭 기사 안전운전 세부 조회</h2>", unsafe_allow_html=True)
    safety_col1, safety_col2 = st.columns(2)

    # Left Driver Safety Information
    with safety_col1:
        st.markdown("<h3 style='color: black;'>김*현 | 180호2274 | 대전지점</h3>", unsafe_allow_html=True)
        st.markdown("<p style='color: black;'>주행 거리: 364km</p>", unsafe_allow_html=True)
        st.markdown("<p style='color: black;'>주행 시간: 3시간 40분</p>", unsafe_allow_html=True)
        st.markdown("<p style='color: black;'>안전 점수: 67</p>", unsafe_allow_html=True)
        st.markdown("<p style='color: black;'>졸음 감지: 3회</p>", unsafe_allow_html=True)
        st.markdown("<h3 style='color: black;'>졸음 운전 통계</h3>", unsafe_allow_html=True)
        labels = ["Distance Traveled", "Driving Hours", "Safety Score", "Drowsiness Events"]
        values = [364, 3.67, 67, 3]  # Hours converted to a single float for visualization
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

    # Right Driver Safety Information
    with safety_col2:
        st.markdown("<h3 style='color: black;'>조*비 | 180호3076 | 광주지점</h3>", unsafe_allow_html=True)
        st.markdown("<p style='color: black;'>주행 거리: 413km</p>", unsafe_allow_html=True)
        st.markdown("<p style='color: black;'>주행 시간: 4시간 25분</p>", unsafe_allow_html=True)
        st.markdown("<p style='color: black;'>안전 점수: 76</p>", unsafe_allow_html=True)
        st.markdown("<p style='color: black;'>졸음 감지: 1회</p>", unsafe_allow_html=True)
        st.markdown("<h3 style='color: black;'>졸음 운전 통계</h3>", unsafe_allow_html=True)
        labels = ["Distance Traveled", "Driving Hours", "Safety Score", "Drowsiness Events"]
        values = [413, 4.42, 76, 1]  # Hours converted to a single float for visualization
        fig, ax = plt.subplots(figsize=(5, 3))
        ax.bar(labels, values, color='#aec7e8')
        ax.set_facecolor('white')
        fig.patch.set_facecolor('white')  # Set figure background color to white
        ax.set_xlabel("Category", fontsize=8, color='black')
        ax.set_ylabel("Value", fontsize=8, color='black')
        ax.tick_params(axis='x', labelsize=8, colors='black')
        ax.tick_params(axis='y', labelsize=8, colors='black')
        plt.close(fig)  # Close the figure to prevent warning
        st.pyplot(fig)
