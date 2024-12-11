import pyshark
import nmap
import os

if not os.path.exists("captures"):
    os.makedirs("captures")
if not os.path.exists("scans"):
    os.makedirs("scans")


class CaptureConfig:
    def __init__(self, interface=None, packets=None, ipv4=None, json=False, ek=False):
        self.interface = interface
        self.packets = packets
        self.ipv4 = ipv4
        self.json = json
        self.ek = ek


class ScanConfig:
    def __init__(self, target, ports, arguments, verbose_level):
        self.target = target
        self.ports = ports
        self.arguments = arguments
        self.verbose_level = verbose_level


class Interpreter:
    def __init__(self):
        self.capture_configs = {}
        self.scan_configs = {}

    def add_capture_config(self, name, config):
        self.capture_configs[name] = config

    def add_scan_config(self, name, config):
        self.scan_configs[name] = config

    def run_capture(self, config_name):
        config = self.capture_configs.get(config_name)
        print(f"Interface: {config.interface}")
        print(f"Ip filter: {config.ipv4}")
        print(f"Ek output format: {config.ek}")
        print(f"Json output format: {config.json}")
        print(f"Number of packets going to be captured: {config.packets}")
        cap = pyshark.LiveCapture(interface=config.interface, output_file=f"captures/{config_name}.pcap")
        cap_save = pyshark.LiveCapture(interface=config.interface, output_file=f"captures/{config_name}.pcap")
        output_file = "captures/capture.txt"
        if config.ek:
            output_file = f'captures/{config_name}.ek'
        if config.json:
            output_file = f'captures/{config_name}.json'

        if not config:
            print(f"Capture config {config_name} not found")
            return
            # Validate that 'interface' exists
        if not config.interface:
            print("Error: Interface must be specified for capture")
            return
        if not config.packets:
            print("Error: Number of packets must be specified for capture")
            return
        if (config.json == True) and (config.ek == True):
            print("Error: Either 'json' or 'ek' can be True, but not both.")
            return
        if config.ipv4 is not None:
            display_filter = f'ip.addr == {config.ipv4}'

        print(f"Running capture on {config.interface} for {config.packets} packets")
        if (config.ipv4 is not None) and config.json:
            cap = pyshark.LiveCapture(interface=config.interface, display_filter=display_filter, use_json=True)
        if (config.ipv4 is not None) and config.ek:
            cap = pyshark.LiveCapture(interface=config.interface, display_filter=display_filter, use_ek=True)
        if config.ipv4 is not None:
            cap = pyshark.LiveCapture(interface=config.interface, display_filter=display_filter)
        if (config.ipv4 is not None) or config.json or config.ek:
            cap_save.sniff(packet_count=config.packets)
            cap_save.close()

        cap.sniff(packet_count=config.packets)
        cap.close()

        with open(output_file, "w") as file:
            for packet in cap:
                file.write(str(packet) + "\n" + "This is a new packet" + "\n")  # Write packet details to the file

        print(f"Capture completed. Results saved to {output_file}")

    def run_scan(self, config_name):
        config = self.scan_configs.get(config_name)
        print(f"Target: {config.target}")
        print(f"Ports: {config.ports}")
        print(f"Arguments: {config.arguments}")
        print(f"Verbose level: {config.verbose_level}")
        output_file = f'scans/{config_name}.txt'
        print(f"Output file: {output_file}")
        if not config:
            print(f"Scan config {config_name} not found")
            return

            # Build the verbosity argument with the correct format
        verbosity = 'v' * min(config.verbose_level, 5)  # Limit to 5 'v' for verbosity level
        print(f"Running Nmap scan on {config.target} with ports {config.ports}")
        nm = nmap.PortScanner()
        nm.scan(hosts=config.target,
                arguments=f'-{verbosity} -p {config.ports} -sT -oN scans/{config_name} {config.arguments}')

        with open(output_file, "w") as file:
            for host in nm.all_hosts():
                file.write(f'Host: {host}, Status: {nm[host].state()} + "\n"')
                for proto in nm[host].all_protocols():
                    file.write(f'Protocol: {proto}, Ports: {nm[host][proto]} + "\n"')

    def interpret_file(self, file_path):
        with open(file_path, 'r') as f:
            lines = f.readlines()

        current_capture_config = None
        current_scan_config = None
        current_capture_name = None
        current_scan_name = None

        for line in lines:
            line = line.strip()

            # Parse capture_config
            if line.startswith("config_capture"):
                current_capture_name = line.split(":")[1].strip()
                current_capture_config = {}
            elif current_capture_config is not None:
                if ":" in line:
                    key, value = line.split(":", 1)
                    key = key.strip()
                    value = value.strip() if value else None  # Set value to None if it's empty

                    # Convert numeric values to appropriate types
                    if key == "packets" and value.isdigit():
                        value = int(value)
                    if key == "ipv4" and value is not None:
                        value = str(value)

                    elif key == "json" or key == "ek":
                        value = value.lower() == "true"  # Convert "True"/"False" strings to boolean

                    current_capture_config[key] = value

                elif line == "":
                    self.add_capture_config(current_capture_name, CaptureConfig(**current_capture_config))
                    current_capture_config = None

            # Parse scan_config
            elif line.startswith("config_scan"):
                current_scan_name = line.split(":")[1].strip()
                current_scan_config = {}
            elif current_scan_config is not None:
                if ":" in line:
                    key, value = line.split(":", 1)
                    key = key.strip()
                    value = value.strip()  # Set value to None if it's empty

                    # Convert numeric values to appropriate types
                    if key == "target":
                        value = str(value)
                    if key == "ports":
                        value = str(value)
                    if key == "arguments":
                        value = str(value)
                    if key == "verbose_level":
                        value = int(value)

                    current_scan_config[key] = value

                elif line == "":
                    self.add_scan_config(current_scan_name, ScanConfig(**current_scan_config))
                    current_scan_config = None

            # Execute capture
            elif line.startswith("capture"):
                capture_name = line.split(":")[1].strip()
                self.run_capture(capture_name)

            # Execute scan
            elif line.startswith("scan"):
                scan_name = line.split(":")[1].strip()
                self.run_scan(scan_name)


# Example usage
interpreter = Interpreter()

# Load and interpret the program file
interpreter.interpret_file("programs/program.ns")

# You can then run capture and scan commands based on your configurations
