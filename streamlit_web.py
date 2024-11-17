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
st.set_page_config(page_title="화물 차량 대시보드", layout="wide")

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

# Infinite loop for updating graphs, tables, and maps in real-time
while True:
    # Simulating data changes for dynamic updating
    data = {
        "차량/운전자 상태": {
            "트럭 수": np.random.randint(50, 70),
            "운전자 수": np.random.randint(45, 55),
            "졸음/알람 앱 설치 수": np.random.randint(50, 60)
        },
        "운전 상태": {
            "현재 운행 중": np.random.randint(20, 30),
            "주의 산만 감지": np.random.randint(0, 5)
        },
        "안전 점수 분포": {
            "80-100": np.random.randint(0, 10),
            "60-79": np.random.randint(10, 20),
            "26-59": np.random.randint(0, 10),
            "0-25": np.random.randint(0, 5)
        },
        "운행 정보": {
            "오늘 주행 거리": np.random.randint(100, 150),
            "어제 주행 거리": np.random.randint(80, 120)
        }
    }

    with placeholder.container():
        # Display current time
        now = datetime.now()
        st.header("화물 차량 대시보드")
        st.write(f"현재 시간: {now.strftime('%Y.%m.%d %H:%M:%S')}")

        # Dashboard Layout with Four Panels in One Row
        col1, col2, col3, col4 = st.columns(4)

        # Cargo Transport Status with Truck and Driver Icons
        with col1:
            st.subheader("차량/운전자 상태")
            truck_driver_html = f"""
                <div style='display: flex; justify-content: space-around; align-items: center;'>
                    <div style='text-align: center; color: white;'>
                        <img src='data:image/png;base64,{icon_truck_base64}' style='width:40px;height:40px;'>
                        <br>트럭 수: <strong>{data['차량/운전자 상태']['트럭 수']}</strong>
                    </div>
                    <div style='text-align: center; color: white;'>
                        <img src='data:image/png;base64,{icon_driver_base64}' style='width:40px;height:40px;'>
                        <br>운전자 수: <strong>{data['차량/운전자 상태']['운전자 수']}</strong>
                    </div>
                </div>
            """
            st.markdown(truck_driver_html, unsafe_allow_html=True)

        # Safe Driving Status Graph
        with col2:
            st.subheader("운전 상태")
            fig, ax = plt.subplots(figsize=(3, 2))
            ax.bar(["Drowsy", "Safe"], [data['운전 상태']['현재 운행 중'], data['운전 상태']['주의 산만 감지']], color=['#1f77b4', '#17becf'])
            ax.set_facecolor('black')
            fig.patch.set_facecolor('black')  # Set figure background color to black
            ax.tick_params(axis='x', labelsize=8, colors='white')  # Set tick label color to white
            ax.tick_params(axis='y', labelsize=8, colors='white')
            ax.title.set_color('white')
            plt.close(fig)  # Close the figure to prevent warning
            st.pyplot(fig)

        # Safety Score Statistics Pie Chart
        with col3:
            st.subheader("안전 점수 분포")
            labels = ["80-100", "60-79", "26-59", "0-25"]
            sizes = [data["안전 점수 분포"][key] for key in labels]
            fig, ax = plt.subplots(figsize=(3, 2))
            ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90, colors=['#1f77b4', '#aec7e8', '#17becf', '#9edae5'], textprops={'fontsize': 7, 'color': 'white'})
            ax.axis('equal')
            ax.set_facecolor('black')
            fig.patch.set_facecolor('black')  # Set figure background color to black
            plt.close(fig)  # Close the figure to prevent warning
            st.pyplot(fig)

        # Driving Information Vertical Bar Graph
        with col4:
            st.subheader("운행 정보")
            fig, ax = plt.subplots(figsize=(3, 2))
            ax.barh(["Today's Distance", "Yesterday's Distance"], [data['운행 정보']['오늘 주행 거리'], data['운행 정보']['어제 주행 거리']], color=['#1f77b4', '#17becf'])
            ax.set_facecolor('black')
            fig.patch.set_facecolor('black')  # Set figure background color to black
            ax.tick_params(axis='x', labelsize=8, colors='white')  # Set tick label color to white
            ax.tick_params(axis='y', labelsize=8, colors='white')
            ax.title.set_color('white')
            plt.close(fig)  # Close the figure to prevent warning
            st.pyplot(fig)

        # 운전자 정보 and Map in One Row
        driver_col, map_col = st.columns([1, 2])

        # Driver Information Panel
        with driver_col:
            st.subheader("운전자 정보")
            for driver in driver_data:
                icon_base64 = icon_normal_base64
                driver_html = f"<div style='display: flex; align-items: center; margin-bottom: 10px; color: white;'>"
                driver_html += f"<img src='data:image/png;base64,{icon_base64}' style='width:30px;height:30px;margin-right:10px;'>"
                driver_html += f"<div><strong>{driver['차량 번호']}</strong><br>{driver['운전자 이름']} ({driver['연락처']})</div></div>"
                st.markdown(driver_html, unsafe_allow_html=True)

        # Real-time Map Update
        with map_col:
            st.markdown("<h2 style='text-align: center; color: white;'>화물 차량 상태 모니터링</h2>", unsafe_allow_html=True)
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
        st.markdown("## 트럭 기사 안전운전 세부 조회")
        safety_col1, safety_col2 = st.columns(2)

        # Left Driver Safety Information
        with safety_col1:
            st.subheader("김*현 | 180호2274 | 대전지점")
            st.metric("주행 거리", "364km")
            st.metric("주행 시간", "3시간 40분")
            st.metric("안전 점수", "67")
            st.metric("졸음 감지", "3회")
            st.subheader("졸음 운전 통계")
            months = ["JAN", "FEB", "MAR", "APR", "MAY", "JUN", "JUL", "AUG", "SEP", "OCT", "NOV", "DEC"]
            drowsiness_counts = np.random.randint(0, 7, len(months))
            fig, ax = plt.subplots(figsize=(5, 3))
            ax.bar(months, drowsiness_counts, color='#1f77b4')
            ax.set_facecolor('black')
            fig.patch.set_facecolor('black')  # Set figure background color to black
            ax.set_xlabel("Month", fontsize=8, color='white')
            ax.set_ylabel("Drowsiness Count", fontsize=8, color='white')
            ax.tick_params(axis='x', labelsize=8, colors='white')
            ax.tick_params(axis='y', labelsize=8, colors='white')
            plt.close(fig)  # Close the figure to prevent warning
            st.pyplot(fig)

        # Right Driver Safety Information
        with safety_col2:
            st.subheader("조*비 | 180호3076 | 광주지점")
            st.metric("주행 거리", "413km")
            st.metric("주행 시간", "4시간 25분")
            st.metric("안전 점수", "76")
            st.metric("졸음 감지", "1회")
            st.subheader("졸음 운전 통계")
            months = ["JAN", "FEB", "MAR", "APR", "MAY", "JUN", "JUL", "AUG", "SEP", "OCT", "NOV", "DEC"]
            drowsiness_counts = np.random.randint(0, 7, len(months))
            fig, ax = plt.subplots(figsize=(5, 3))
            ax.bar(months, drowsiness_counts, color='#aec7e8')
            ax.set_facecolor('black')
            fig.patch.set_facecolor('black')  # Set figure background color to black
            ax.set_xlabel("Month", fontsize=8, color='white')
            ax.set_ylabel("Drowsiness Count", fontsize=8, color='white')
            ax.tick_params(axis='x', labelsize=8, colors='white')
            ax.tick_params(axis='y', labelsize=8, colors='white')
            plt.close(fig)  # Close the figure to prevent warning
            st.pyplot(fig)

    # Pause for a short duration to create real-time effect
    time.sleep(2)
