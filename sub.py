import ipaddress
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.core.window import Window
from kivy.graphics import Color, RoundedRectangle
from kivy.metrics import dp

# ================================================
# FIXED WINDOW SETTINGS - NO RESIZE, NO DRAG
# ================================================
Window.size = (350, 550)  # Small calculator size
Window.borderless = False  # Keep window borders
Window.resizable = False   # Disable resizing
Window.always_on_top = False  # Don't force always on top

# Disable window dragging - these are platform specific
# We'll handle it in a different way
import platform
import ctypes
if platform.system() == 'Windows':
    try:
        # Try to remove WS_THICKFRAME and WS_MAXIMIZEBOX styles
        hwnd = ctypes.windll.user32.GetActiveWindow()
        style = ctypes.windll.user32.GetWindowLongW(hwnd, -16)  # GWL_STYLE
        style &= ~0x00040000  # Remove WS_THICKFRAME
        style &= ~0x00010000  # Remove WS_MAXIMIZEBOX
        ctypes.windll.user32.SetWindowLongW(hwnd, -16, style)
    except:
        pass  # If this fails, window will still be non-resizable

Window.clearcolor = (0.08, 0.16, 0.28, 1)  # Dark blue background

# Modern color scheme
COLORS = {
    'primary': (0.15, 0.3, 0.55, 1),     # Light blue
    'dark': (1, 1, 1, 1),                # White text
    'light': (0.95, 0.95, 0.96, 1),      # Very light gray
    'button_bg': (0.1, 0.25, 0.45, 1),   # Darker blue for buttons
    'button_hover': (0.15, 0.35, 0.60, 1), # Lighter blue on hover
    'input_bg': (0.12, 0.22, 0.40, 1),   # Dark blue for inputs
}

class FixedInput(TextInput):
    """TextInput that works properly in fixed window"""
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.multiline = False
        self.font_size = dp(16)
        self.background_color = COLORS['input_bg']
        self.foreground_color = COLORS['dark']
        self.padding = [dp(10), dp(10)]
        self.halign = 'left'
        self.cursor_color = COLORS['light']
        self.cursor_width = dp(2)
        self.size_hint = (1, 0.12)
        self.background_normal = ''
        self.background_active = ''

class CalculatorApp(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(orientation="vertical", padding=dp(15), spacing=dp(10))
        
        # Title
        title_label = Label(
            text="[b]Subnet Calculator[/b]",
            markup=True,
            font_size=dp(18),
            size_hint=(1, 0.08),
            color=COLORS['light']
        )
        self.add_widget(title_label)
        
        # Input section
        input_label = Label(
            text="Enter CIDR notation:",
            font_size=dp(12),
            size_hint=(1, 0.05),
            color=COLORS['light']
        )
        self.add_widget(input_label)
        
        self.input_field = FixedInput(
            hint_text="Example: 192.168.1.0/24",
            size_hint=(1, 0.12)
        )
        self.add_widget(self.input_field)
        
        # Give focus to input field
        self.input_field.focus = True
        
        # Calculate button
        self.calc_button = Button(
            text="Calculate",
            size_hint=(1, 0.1),
            background_color=COLORS['button_bg'],
            color=COLORS['light'],
            font_size=dp(16),
            bold=True
        )
        self.calc_button.bind(on_press=self.calculate)
        self.add_widget(self.calc_button)
        
        # Results section
        results_label = Label(
            text="[b]Results:[/b]",
            markup=True,
            font_size=dp(14),
            size_hint=(1, 0.05),
            color=COLORS['light']
        )
        self.add_widget(results_label)
        
        # Scrollable results area
        scroll_view = ScrollView(size_hint=(1, 0.55))
        self.result_label = TextInput(
            text="Results will appear here",
            halign='left',
            font_size=dp(14),
            multiline=True,
            readonly=True,
            background_color=COLORS['input_bg'],
            foreground_color=COLORS['light'],
            size_hint=(1, 1)
        )
        scroll_view.add_widget(self.result_label)
        self.add_widget(scroll_view)
        
        # Status bar
        status_bar = Label(
            text="Ready",
            font_size=dp(10),
            size_hint=(1, 0.02),
            color=(0.7, 0.7, 0.8, 1)
        )
        self.add_widget(status_bar)

    def calculate(self, instance):
        cidr = self.input_field.text.strip()
        
        if not cidr:
            self.result_label.text = "Please enter a CIDR notation"
            return
        
        try:
            net = ipaddress.ip_network(cidr, strict=False)
            
            # Calculate usable hosts
            if net.prefixlen <= 30:
                usable = net.num_addresses - 2
                hosts = list(net.hosts())
                first_host = hosts[0] if hosts else 'N/A'
                last_host = hosts[-1] if hosts else 'N/A'
            elif net.prefixlen == 31:
                usable = 2
                first_host = net[0]
                last_host = net[1]
            else:  # /32
                usable = 1
                first_host = net[0]
                last_host = net[0]
            
            # Format results for small window
            text = f"""Network Information:
Network: {net.network_address}
Netmask: {net.netmask}
Broadcast: {net.broadcast_address if net.prefixlen <= 30 else 'N/A'}
First Host: {first_host}
Last Host: {last_host}
Usable Hosts: {usable:,}
Prefix: /{net.prefixlen}
Total Addresses: {net.num_addresses:,}

Properties:
Private: {'Yes' if net.is_private else 'No'}
Version: IPv{net.version}

Range:
{net[0]} to {net[-1]}"""
            
            self.result_label.text = text
            
        except ValueError as e:
            error_msg = str(e)
            if "has host bits set" in error_msg:
                self.result_label.text = "Error: Use network address\nExample: 192.168.1.0/24"
            else:
                self.result_label.text = f"Error: {error_msg}"
        except Exception as e:
            self.result_label.text = f"Unexpected error: {e}"

class SubnetCalculatorApp(App):
    def build(self):
        self.title = "Subnet Calculator"
        
        # Set the icon
        try:
            icon_path = 'icon.png'
            self.icon = icon_path
        except:
            pass  # Icon not found, continue without it
        
        # Additional window settings
        Window.minimum_width, Window.minimum_height = 350, 550
        Window.maximum_width, Window.maximum_height = 350, 550
        
        return CalculatorApp()

if __name__ == "__main__":
    # Force window to stay fixed size
    import os
    os.environ['KIVY_WINDOW'] = 'sdl2'
    
    SubnetCalculatorApp().run()