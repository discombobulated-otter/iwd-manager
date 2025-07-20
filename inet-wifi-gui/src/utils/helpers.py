def format_ssid(ssid):
    """Format the SSID for display."""
    return ssid.strip().title()

def handle_exception(e):
    """Log and handle exceptions."""
    print(f"An error occurred: {e}")

def is_valid_ssid(ssid):
    """Check if the provided SSID is valid."""
    return isinstance(ssid, str) and len(ssid) > 0

def parse_network_info(network_info):
    """Parse network information into a more usable format."""
    return {
        'ssid': network_info.get('ssid', ''),
        'signal_strength': network_info.get('signal_strength', 0),
        'status': network_info.get('status', 'unknown')
    }