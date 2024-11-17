화물 차량 대시보드 웹(Truck Dashboard)

This project is a real-time dashboard to monitor truck activities using Streamlit. It provides various features such as displaying the number of trucks and drivers, driver safety information, and drowsiness detection status, along with visual graphs and a dynamic map for monitoring truck locations.


Features

Real-Time Data Update: The dashboard continuously updates information every few seconds to show the latest status of trucks and drivers.

Visual Graphs: The dashboard includes various visual representations, such as bar charts and pie charts, for easier understanding of driver and truck statuses.

Driver Information: Displays detailed driver information, including name, contact, and current status.

Dynamic Map: Uses Folium to provide real-time geographic tracking of trucks, highlighting their locations and indicating driver statuses (e.g., drowsy or safe).



Installation and Setup

To set up and run this project locally, follow the instructions below:



Prerequisites

Python 3.7 or later should be installed.

Pip (Python's package manager) should be installed.



Step 1: Clone the Repository

First, clone this GitHub repository to your local machine using the following command:

git clone <repository-url>
cd <repository-name>



Step 2: Install Required Packages

This project requires several Python libraries to run properly. To install these dependencies, you need to run the following command:

pip install -r requirements.txt



The requirements.txt file should contain:

streamlit
pandas
matplotlib
folium



Step 3: Set Up Data Directory

The project requires specific icons to be displayed in the dashboard. Ensure that your directory structure looks like this:

project/
|
├── streamlit_app.py          # Main script file
├── requirements.txt          # Python dependencies
├── README.md                 # Project description (this file)
├── data/                     # Directory containing icons
│   ├── DR.png                # Icon for drowsy driving
│   ├── NO.png                # Icon for normal driving
│   ├── Truck.png             # Icon for trucks
│   └── Driver.png            # Icon for drivers
└── .gitignore                # Git ignore rules



Step 4: Running the Dashboard

To start the dashboard, simply run the following command in the project directory:

streamlit run streamlit_app.py

This command will open the Streamlit dashboard in your default web browser. You will see a real-time dashboard that visualizes the latest truck and driver status.



Dashboard Overview

Header: Displays the current time and title "화물 차량 대시보드".

Truck/Driver Status: Shows the number of trucks and drivers available.

Driving Status: Graph representing drowsy vs. safe driving conditions.

Safety Score Distribution: A pie chart visualizing the distribution of driver safety scores.

Driving Information: Shows the distance driven today and yesterday for the fleet.

Driver Information: Displays individual driver details, including vehicle number, name, and contact information.

Map Section: Displays a map of Gwangju, South Korea, with truck markers indicating their current status.



Code Structure and Logic

Libraries and Configuration:

The application uses streamlit, pandas, matplotlib, folium, and others for data visualization.

Icons are loaded from the data/ directory and converted to base64 strings for embedding in HTML components.



Dashboard Layout:

The dashboard is organized into sections (columns) for presenting truck status, driver status, graphs, and maps.

Real-Time Updates:

The dashboard has a continuous loop (while True:) that updates driver and truck status with randomly generated data to simulate real-time changes.

Graphs and Charts:

matplotlib is used to render bar and pie charts representing truck data and driver statuses.

Charts are styled with a black background and white text to improve readability.

Interactive Map:

folium is used to generate a real-time map of Gwangju, South Korea, with markers representing truck locations and driver statuses.

Customization and Enhancements

Data Integration: Replace the current randomly generated data with actual data from APIs or a database.

User Authentication: Implement user authentication using streamlit-auth to make the dashboard secure.

Alert System: Add alerts for drowsy drivers, such as notifications or warning sounds.

Deployment: Deploy the app using services like Streamlit Cloud, Heroku, or AWS to share it with a larger audience.



Contributing

If you'd like to contribute to this project, feel free to create an issue or open a pull request. Any improvements or bug fixes are welcome.

License

This project is open-source and available under the MIT License. Please see the LICENSE file for more details.

