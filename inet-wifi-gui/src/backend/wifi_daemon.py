import subprocess
import re

class WifiDaemon:
    def __init__(self):
        # Initialize the Wi-Fi daemon connection
        pass

    def connect_to_network(self, ssid, password):
        # Connect to the specified Wi-Fi network using iwctl
        try:
            result = subprocess.run([
                "iwctl", "--passphrase", password, "station", "wlan0", "connect", ssid
            ], text=True, capture_output=True, check=True)
            return result.returncode == 0
        except Exception as e:
            print(f"Error connecting to network {ssid}: {e}")
            return False

    def disconnect(self):
        # Disconnect from the current Wi-Fi network using iwctl
        try:
            result = subprocess.run([
                "iwctl", "station", "wlan0", "disconnect"
            ], text=True, capture_output=True, check=True)
            return result.returncode == 0
        except Exception as e:
            print(f"Error disconnecting from network: {e}")
            return False

    def get_network_info(self):
        # Retrieve information about the current Wi-Fi network using iwctl
        try:
            result = subprocess.run([
                "iwctl", "station", "wlan0", "show"
            ], text=True, capture_output=True, check=True)
            output = result.stdout
            # Remove ANSI color codes
            output = re.sub(r'\x1b\[[0-9;]*m', '', output)
            ssid = None
            signal = None
            security = None
            interface = None
            state = None
            for line in output.splitlines():
                if 'Connected network' in line:
                    ssid = line.split(':', 1)[-1].strip()
                if 'Signal strength' in line:
                    signal = line.split(':', 1)[-1].strip()
                if 'Security' in line:
                    security = line.split(':', 1)[-1].strip()
                if 'Interface' in line:
                    interface = line.split(':', 1)[-1].strip()
                if 'State' in line:
                    state = line.split(':', 1)[-1].strip()
            return ssid, signal, security, interface, state
        except Exception as e:
            print(f"Error getting network info: {e}")
            return None, None, None, None, None

    def list_available_networks(self):
        # List all available Wi-Fi networks using iwctl
        try:
            result = subprocess.run([
                "iwctl", "station", "wlan0", "get-networks"
            ], text=True, capture_output=True, check=True)
            output = result.stdout
            # Remove ANSI color codes
            output = re.sub(r'\x1b\[[0-9;]*m', '', output)
            networks = []
            header_found = False
            for line in output.splitlines():
                line_strip = line.strip()
                if (
                    not line_strip or
                    line_strip.startswith('SSID') or
                    line_strip.startswith('--') or
                    line_strip.startswith('>') or
                    line_strip.lower().startswith('network') or
                    'available' in line_strip.lower() or
                    re.match(r'^[^\w]+$', line_strip) or
                    len(line_strip.split()) < 2
                ):
                    continue
                # Find header to determine columns
                if not header_found and 'Security' in line_strip and 'Signal' in line_strip:
                    header_found = True
                    continue
                # Parse columns: SSID, Security, Signal
                parts = line_strip.split()
                if len(parts) >= 3:
                    ssid = ' '.join(parts[:-2]).lstrip('>')
                    security = parts[-2]
                    signal = parts[-1]
                    networks.append((ssid.strip(), security, signal))
            return networks
        except Exception as e:
            print(f"Error scanning networks: {e}")
            return []

    def signal_strength(self):
        # Get the signal strength of the current connection
        pass