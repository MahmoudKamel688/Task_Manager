import sys
import psutil
import matplotlib.pyplot as plt
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, QMessageBox, QLineEdit, QFormLayout, QTextEdit, QComboBox
from PyQt5.QtCore import QTimer
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

class SystemMonitor(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.initTimer()
    
    def initUI(self):
        self.setWindowTitle("System Monitor")
        self.setGeometry(100, 100, 800, 600)
        
        layout = QVBoxLayout()
        
        self.cpu_label = QLabel("CPU Usage: 0%")
        self.ram_label = QLabel("RAM Usage: 0%")
        self.disk_label = QLabel("Disk Usage: 0%")
        self.network_label = QLabel("Network: 0 KB/s")
        
        layout.addWidget(self.cpu_label)
        layout.addWidget(self.ram_label)
        layout.addWidget(self.disk_label)
        layout.addWidget(self.network_label)
        
        form_layout = QFormLayout()
        self.cpu_limit = QLineEdit("80")
        self.ram_limit = QLineEdit("80")
        self.disk_limit = QLineEdit("80")
        self.network_limit = QLineEdit("1024")
        
        form_layout.addRow("CPU Limit (%):", self.cpu_limit)
        form_layout.addRow("RAM Limit (%):", self.ram_limit)
        form_layout.addRow("Disk Limit (%):", self.disk_limit)
        form_layout.addRow("Network Limit (KB/s):", self.network_limit)
        layout.addLayout(form_layout)
        
        self.mode_selector = QComboBox()
        self.mode_selector.addItems(["Light Mode", "Dark Mode"])
        self.mode_selector.currentIndexChanged.connect(self.change_mode)
        layout.addWidget(self.mode_selector)
        
        self.refresh_button = QPushButton("Refresh")
        self.refresh_button.clicked.connect(self.update_stats)
        layout.addWidget(self.refresh_button)
        
        self.process_button = QPushButton("Show Running Processes")
        self.process_button.clicked.connect(self.show_processes)
        layout.addWidget(self.process_button)
        
        self.process_text = QTextEdit()
        self.process_text.setReadOnly(True)
        layout.addWidget(self.process_text)
        
        self.figure, self.ax = plt.subplots()
        self.canvas = FigureCanvas(self.figure)
        layout.addWidget(self.canvas)
        
        self.setLayout(layout)
        self.prev_net_io = psutil.net_io_counters()
        self.update_stats()
    
    def initTimer(self):
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_stats)
        self.timer.start(2000)  # تحديث تلقائي كل 2 ثانية
    
    def update_stats(self):
        cpu_usage = psutil.cpu_percent()
        ram_usage = psutil.virtual_memory().percent
        disk_usage = psutil.disk_usage('/').percent
        net_io = psutil.net_io_counters()
        network_usage = ((net_io.bytes_sent + net_io.bytes_recv) - (self.prev_net_io.bytes_sent + self.prev_net_io.bytes_recv)) / 2  # KB/s
        self.prev_net_io = net_io
        
        self.cpu_label.setText(f"CPU Usage: {cpu_usage}%")
        self.ram_label.setText(f"RAM Usage: {ram_usage}%")
        self.disk_label.setText(f"Disk Usage: {disk_usage}%")
        self.network_label.setText(f"Network: {network_usage:.2f} KB/s")
        
        self.update_chart(cpu_usage, ram_usage, disk_usage, network_usage)
        self.check_alerts(cpu_usage, ram_usage, disk_usage, network_usage)
    
    def update_chart(self, cpu, ram, disk, network):
        self.ax.clear()
        labels = ["CPU", "RAM", "Disk", "Network"]
        values = [cpu, ram, disk, network]
        colors = ['red', 'blue', 'green', 'purple']
        
        self.ax.bar(labels, values, color=colors)
        self.ax.set_ylim(0, max(100, network * 2))
        self.ax.set_ylabel("Usage (%) / KB/s")
        self.ax.set_title("System Resource Usage")
        
        self.canvas.draw()
    
    def check_alerts(self, cpu, ram, disk, network):
        try:
            cpu_limit = float(self.cpu_limit.text())
            ram_limit = float(self.ram_limit.text())
            disk_limit = float(self.disk_limit.text())
            network_limit = float(self.network_limit.text())
        except ValueError:
            QMessageBox.warning(self, "Input Error", "Please enter valid numeric values for limits.")
            return
        
        alerts = []
        if cpu > cpu_limit:
            alerts.append("High CPU Usage!")
        if ram > ram_limit:
            alerts.append("High RAM Usage!")
        if disk > disk_limit:
            alerts.append("High Disk Usage!")
        if network > network_limit:
            alerts.append("High Network Usage!")
        
        if alerts:
            QMessageBox.warning(self, "Resource Alert", "\n".join(alerts))
    
    def show_processes(self):
        processes = [(p.pid, p.name(), p.cpu_percent(), p.memory_info().rss / (1024 * 1024)) for p in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_info'])]
        processes.sort(key=lambda x: x[2], reverse=True)
        
        process_info = "PID | Name | CPU% | Memory (MB)\n" + "-"*40 + "\n"
        for pid, name, cpu, mem in processes[:20]:  # عرض أول 20 عملية
            process_info += f"{pid} | {name} | {cpu:.2f}% | {mem:.2f} MB\n"
        
        self.process_text.setText(process_info)
    
    def change_mode(self):
        mode = self.mode_selector.currentText()
        if mode == "Dark Mode":
            self.setStyleSheet("background-color: #2E2E2E; color: white;")
        else:
            self.setStyleSheet("background-color: white; color: black;")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    monitor = SystemMonitor()
    monitor.show()
    sys.exit(app.exec_())
