# i-net WiFi GUI

This project is a graphical user interface (GUI) for managing and interacting with Wi-Fi networks on Linux, built using Python and Qt Designer. The application serves as a front-end for the i-net WiFi Daemon, allowing users to control Wi-Fi functionalities seamlessly.

## Features

- Simple and intuitive GUI to control Wi-Fi daemon functionalities.
- Python backend that interacts with the i-net WiFi Daemon services.
- Built using Qt Designer for a user-friendly interface.
- Easy to run by executing the `main.py` file.

## Installation

1. Clone the repository:
   ```
   git clone <repository-url>
   cd inet-wifi-gui
   ```

2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

## Usage

To run the application, execute the following command:
```
python src/main.py
```

## File Structure

```
inet-wifi-gui
├── src
│   ├── main.py               # Entry point of the application
│   ├── backend
│   │   └── wifi_daemon.py    # Handles interactions with the Wi-Fi daemon
│   ├── ui
│   │   └── main_window.ui     # UI layout created with Qt Designer
│   └── utils
│       └── helpers.py         # Utility functions for the application
├── requirements.txt           # Project dependencies
└── README.md                  # Project documentation
```

## Contributing

Contributions are welcome! Please feel free to submit a pull request or open an issue for any suggestions or improvements.

## License

This project is licensed under the MIT License. See the LICENSE file for details.