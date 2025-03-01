Task Manager - System Monitor
Application Description:
Task Manager is a system performance monitoring application that displays real-time usage of CPU, RAM, Disk, and Network. It provides users with a graphical interface featuring dynamic charts, allowing them to set usage limits and receive alerts when these limits are exceeded.

Key Features:
1️⃣ Real-time System Monitoring

Displays CPU, RAM, Disk, and Network usage.
Automatic data updates every 2 seconds.
2️⃣ Alerts for Exceeding Limits

Users can set a threshold for CPU, RAM, Disk, and Network usage.
If any resource surpasses the defined limit, a warning alert is displayed.
3️⃣ View Active Processes

Displays a list of the most resource-intensive background processes with details such as Process ID (PID), Name, CPU usage, and Memory consumption.
Helps users identify processes consuming excessive resources.
4️⃣ Dynamic Graphs

Real-time bar chart updates showing the usage percentage of each resource.
Helps users analyze performance trends effectively.
5️⃣ Light/Dark Mode Switching 🌗

Users can toggle between light and dark modes for a comfortable viewing experience.
How the Application Works:
When launched, the application retrieves system resource data using the psutil library.
Values are displayed in the PyQt GUI, with automatic updates every 2 seconds for accuracy.
If any resource exceeds the user-defined threshold, a popup alert is triggered.
A dedicated button displays active processes, sorting them by CPU usage and showing the top 20 most demanding processes.
The app supports light and dark mode switching for flexible user experience.
Benefits of the Application:
✅ Performance Analysis – Helps users understand resource consumption on their devices.
✅ Efficiency Improvement – Users can terminate unnecessary processes to optimize performance.
✅ Network Monitoring – Tracks data sent and received to avoid excessive internet usage.
✅ Custom Alerts – Prevents overheating or slowdowns by setting appropriate resource limits.

Technologies Used:
📌 Programming Language: Python 🐍
📌 Main Libraries:

PyQt5 → For GUI development
psutil → For retrieving system resource data
Matplotlib → For generating graphs
QTimer → For automatic updates every 2 seconds
🚀 Task Manager is an ideal tool for effortlessly monitoring system performance with a modern design and advanced features!
