import sys
import psutil
import subprocess
import matplotlib.pyplot as plt
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, QFormLayout, QLineEdit, QMessageBox, QTextEdit, QComboBox
from PyQt5.QtCore import QTimer
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

class SystemControl(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.initTimer()
    
    def initUI(self):
        self.setWindowTitle("System Resource Control")
        self.setGeometry(100, 100, 900, 600)
        
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
        
        form_layout.addRow("CPU Limit (%):", self.cpu_limit)
        form_layout.addRow("RAM Limit (%):", self.ram_limit)
        layout.addLayout(form_layout)
        
        self.process_button = QPushButton("Show Running Processes")
        self.process_button.clicked.connect(self.show_processes)
        layout.addWidget(self.process_button)
        
        self.process_text = QTextEdit()
        self.process_text.setReadOnly(True)
        layout.addWidget(self.process_text)
        
        self.kill_process_button = QPushButton("Kill Selected Process")
        self.kill_process_button.clicked.connect(self.kill_selected_process)
        layout.addWidget(self.kill_process_button)
        
        self.process_selector = QComboBox()
        layout.addWidget(self.process_selector)
        
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
        network_usage = ((net_io.bytes_sent + net_io.bytes_recv) - (self.prev_net_io.bytes_sent + self.prev_net_io.bytes_recv)) / 1024  # KB/s
        self.prev_net_io = net_io
        
        self.cpu_label.setText(f"CPU Usage: {cpu_usage}%")
        self.ram_label.setText(f"RAM Usage: {ram_usage}%")
        self.disk_label.setText(f"Disk Usage: {disk_usage}%")
        self.network_label.setText(f"Network: {network_usage:.2f} KB/s")
        
        self.update_chart(cpu_usage, ram_usage, disk_usage, network_usage)
        self.check_alerts(cpu_usage, ram_usage)
    
    def update_chart(self, cpu, ram, disk, network):
        self.ax.clear()
        labels = ["CPU", "RAM", "Disk", "Network"]
        values = [cpu, ram, disk, network]
        colors = ['red', 'blue', 'green', 'purple']
        
        self.ax.bar(labels, values, color=colors)
        self.ax.set_ylim(0, 100)
        self.ax.set_ylabel("Usage (%) / KB/s")
        self.ax.set_title("System Resource Usage")
        
        self.canvas.draw()
    
    def check_alerts(self, cpu, ram):
        try:
            cpu_limit = float(self.cpu_limit.text())
            ram_limit = float(self.ram_limit.text())
        except ValueError:
            QMessageBox.warning(self, "Input Error", "Please enter valid numeric values for limits.")
            return
        
        alerts = []
        if cpu > cpu_limit:
            alerts.append("High CPU Usage!")
        if ram > ram_limit:
            alerts.append("High RAM Usage!")
        
        if alerts:
            QMessageBox.warning(self, "Resource Alert", "\n".join(alerts))
    
    def show_processes(self):
        self.process_selector.clear()
        processes = [(p.pid, p.name()) for p in psutil.process_iter(['pid', 'name'])]
        
        process_info = "PID | Name\n" + "-"*30 + "\n"
        for pid, name in processes[:20]:  # عرض أول 20 عملية
            process_info += f"{pid} | {name}\n"
            self.process_selector.addItem(f"{pid} - {name}", pid)
        
        self.process_text.setText(process_info)
    
    def kill_selected_process(self):
        selected = self.process_selector.currentData()
        if selected:
            try:
                subprocess.run(["taskkill", "/PID", str(selected), "/F"], shell=True)
                QMessageBox.information(self, "Success", f"Process {selected} killed successfully.")
                self.show_processes()
            except Exception as e:
                QMessageBox.warning(self, "Error", f"Failed to kill process: {e}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    monitor = SystemControl()
    monitor.show()
    sys.exit(app.exec_())
