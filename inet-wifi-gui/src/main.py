import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox
from PyQt5.QtCore import QTimer
from ui.main_window import Ui_MainWindow
from backend.wifi_daemon import WifiDaemon

class MainApp(QMainWindow):
    def __init__(self):
        super(MainApp, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.wifi_daemon = WifiDaemon()

        # Connect UI signals to slots
        self.ui.connectButton.clicked.connect(self.connect_to_wifi)
        self.ui.disconnectButton.clicked.connect(self.disconnect_wifi)
        self.ui.refreshButton.clicked.connect(self.refresh_networks)
        self.ui.networkList.itemClicked.connect(self.populate_ssid)

        # Show/hide password logic
        self.ui.showPasswordButton.clicked.connect(self.toggle_password_visibility)
        self._password_visible = False

        self.refresh_networks()

        # Add QTimer for periodic status updates
        self.status_timer = QTimer(self)
        self.status_timer.timeout.connect(self.update_connection_status)
        self.status_timer.start(5000)  # every 5 seconds
        self.update_connection_status()  # initial call

    def connect_to_wifi(self):
        ssid_display = self.ui.ssidInput.text()
        ssid = ssid_display.split(' (')[0].strip() if ' (' in ssid_display else ssid_display.strip()
        password = self.ui.passwordInput.text()
        if not ssid:
            self.statusBar().showMessage("No SSID selected.", 5000)
            return
        if not password:
            self.statusBar().showMessage("Password required.", 5000)
            return
        try:
            self.statusBar().showMessage(f"Connecting to {ssid}...", 5000)
            result = self.wifi_daemon.connect_to_network(ssid, password)
            if result:
                self.statusBar().showMessage(f"Connected to {ssid}.", 5000)
                QMessageBox.information(self, "Success", f"Connected to {ssid}.")
            else:
                self.statusBar().showMessage(f"Failed to connect to {ssid}.", 5000)
                QMessageBox.warning(self, "Error", f"Failed to connect to {ssid}.")
        except Exception as e:
            self.statusBar().showMessage(f"Error: {e}", 5000)
            QMessageBox.critical(self, "Error", f"Exception: {e}")

    def disconnect_wifi(self):
        try:
            self.statusBar().showMessage("Disconnecting...", 5000)
            result = self.wifi_daemon.disconnect()
            if result:
                self.statusBar().showMessage("Disconnected from Wi-Fi network.", 5000)
                QMessageBox.information(self, "Success", "Disconnected from Wi-Fi network.")
            else:
                self.statusBar().showMessage("Failed to disconnect.", 5000)
                QMessageBox.warning(self, "Error", "Failed to disconnect from Wi-Fi network.")
        except Exception as e:
            self.statusBar().showMessage(f"Error: {e}", 5000)
            QMessageBox.critical(self, "Error", f"Exception: {e}")

    def refresh_networks(self):
        try:
            self.statusBar().showMessage("Scanning for networks...", 5000)
            networks = self.wifi_daemon.list_available_networks() or []
            self.ui.networkList.clear()
            for ssid, security, signal in networks:
                display = f"{ssid} ({security}, {signal}%)"
                self.ui.networkList.addItem(display)
            self.statusBar().showMessage(f"Found {len(networks)} networks.", 5000)
        except Exception as e:
            self.statusBar().showMessage(f"Error: {e}", 5000)

    def populate_ssid(self, item):
        display_text = item.text()
        ssid = display_text.split(' (')[0].strip() if ' (' in display_text else display_text.strip()
        self.ui.ssidInput.setText(ssid)

    def toggle_password_visibility(self):
        if self._password_visible:
            self.ui.passwordInput.setEchoMode(self.ui.passwordInput.Password)
            self.ui.showPasswordButton.setText('Show')
            self._password_visible = False
        else:
            self.ui.passwordInput.setEchoMode(self.ui.passwordInput.Normal)
            self.ui.showPasswordButton.setText('Hide')
            self._password_visible = True

    def update_connection_status(self):
        try:
            ssid, signal, security, interface, state = self.wifi_daemon.get_network_info()
            # Determine signal bars
            def signal_to_bars(signal):
                try:
                    val = int(signal)
                except (TypeError, ValueError):
                    return "?"
                if val >= 80:
                    return "█"*4
                elif val >= 60:
                    return "█"*3+"▆"
                elif val >= 40:
                    return "█"*2+"▆▂"
                elif val >= 20:
                    return "█"+"▆▂ "
                else:
                    return "▂   "

            if ssid:
                bars = signal_to_bars(signal)
                msg = f"Connected: {ssid} | Signal: {signal} {bars}"
                self.statusBar().showMessage(msg)
                # Green for connected
                self.statusBar().setStyleSheet("color: black; background: #b6fcb6;")
                tooltip = f"SSID: {ssid}\nSignal: {signal}\nBars: {bars}\nSecurity: {security}\nInterface: {interface}\nState: {state}"
                self.statusBar().setToolTip(tooltip)
            elif state and state.lower() == "connecting":
                self.statusBar().showMessage("Connecting...")
                self.statusBar().setStyleSheet("color: black; background: #fff7b2;")
                self.statusBar().setToolTip("")
            else:
                self.statusBar().showMessage("Not connected to any Wi-Fi network.")
                # Red for not connected
                self.statusBar().setStyleSheet("color: white; background: #fcbbbb;")
                self.statusBar().setToolTip("")
        except Exception as e:
            self.statusBar().showMessage(f"Status error: {e}")
            self.statusBar().setStyleSheet("color: white; background: #fcbbbb;")
            self.statusBar().setToolTip("")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_app = MainApp()
    main_app.show()
    sys.exit(app.exec_())