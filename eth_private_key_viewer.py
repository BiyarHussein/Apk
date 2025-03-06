from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from eth_account import Account

# Constants
keys_per_page = 10000
first_private_key = 1
last_private_key = int("0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364140", 16)
total_pages = (last_private_key - first_private_key) // keys_per_page + 1


class KeyViewerApp(App):
    def build(self):
        self.layout = BoxLayout(orientation='vertical')

        # Page navigation
        self.page_label = Label(text=f"Page 1 of {total_pages}")
        self.first_button = Button(text="First", size_hint=(0.25, 0.2))
        self.prev_button = Button(text="Previous", size_hint=(0.25, 0.2))
        self.next_button = Button(text="Next", size_hint=(0.25, 0.2))
        self.last_button = Button(text="Last", size_hint=(0.25, 0.2))

        self.first_button.bind(on_press=self.first_page)
        self.prev_button.bind(on_press=self.prev_page)
        self.next_button.bind(on_press=self.next_page)
        self.last_button.bind(on_press=self.last_page)

        # Display private keys
        self.keys_label = Label(text="Generating keys...", font_size=12, size_hint_y=None)
        self.keys_label.bind(size=self.update_text_size)
        self.scroll = ScrollView(size_hint=(1, 1))
        self.scroll.add_widget(self.keys_label)

        # Search Section
        self.result_label = Label(text="Enter a Private Key or Address", size_hint=(1, 0.2))
        self.input_field = TextInput(hint_text="Enter Private Key or Address", multiline=False)
        self.search_button = Button(text="Search", size_hint=(1, 0.2))
        self.search_button.bind(on_press=self.search_key)

        # Add widgets to layout
        self.layout.add_widget(self.page_label)
        self.layout.add_widget(self.scroll)

        # Navigation buttons in one row
        nav_layout = BoxLayout(size_hint=(1, 0.2))
        nav_layout.add_widget(self.first_button)
        nav_layout.add_widget(self.prev_button)
        nav_layout.add_widget(self.next_button)
        nav_layout.add_widget(self.last_button)

        self.layout.add_widget(nav_layout)
        self.layout.add_widget(self.result_label)
        self.layout.add_widget(self.input_field)
        self.layout.add_widget(self.search_button)

        # Load first page
        self.current_page = 1
        self.display_page(self.current_page)

        return self.layout

    def update_text_size(self, instance, value):
        self.keys_label.text_size = (instance.width, None)

    def display_page(self, page):
        """Generate and display private keys for the given page."""
        start_key = (page - 1) * keys_per_page + first_private_key
        end_key = min(start_key + keys_per_page - 1, last_private_key)

        keys_text = f"Displaying Page {page} of {total_pages}\n\n"
        for i in range(start_key, end_key + 1):
            private_key = hex(i)[2:].zfill(64)
            acct = Account.from_key(private_key)
            keys_text += f"{private_key} | {acct.address}\n"

        self.keys_label.text = keys_text
        self.page_label.text = f"Page {self.current_page} of {total_pages}"

    def first_page(self, instance):
        """Go to the first page."""
        self.current_page = 1
        self.display_page(self.current_page)

    def prev_page(self, instance):
        """Go to the previous page."""
        if self.current_page > 1:
            self.current_page -= 1
            self.display_page(self.current_page)

    def next_page(self, instance):
        """Go to the next page."""
        if self.current_page < total_pages:
            self.current_page += 1
            self.display_page(self.current_page)

    def last_page(self, instance):
        """Go to the last page."""
        self.current_page = total_pages
        self.display_page(self.current_page)

    def search_key(self, instance):
        """Search for a private key or address."""
        search_input = self.input_field.text.strip()

        if len(search_input) == 64 and all(c in "0123456789abcdefABCDEF" for c in search_input):
            try:
                acct = Account.from_key("0x" + search_input)
                self.result_label.text = f"Found!\nPrivate Key: {search_input}\nAddress: {acct.address}"
            except Exception as e:
                self.result_label.text = f"Error: {e}"

        elif search_input.lower().startswith("0x") and len(search_input) == 42:
            self.result_label.text = "Address search not available in this version."

        else:
            self.result_label.text = "Invalid input. Enter a valid private key or Ethereum address."


if __name__ == "__main__":
    KeyViewerApp().run()