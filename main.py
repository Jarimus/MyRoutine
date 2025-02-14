from kivymd.app import MDApp, Builder
from kivymd.uix.list import MDListItem, MDListItemLeadingIcon, MDListItemHeadlineText, MDListItemSupportingText
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.label import MDLabel
import json


class MainApp(MDApp):

    def on_start(self):
        #super
        super().on_start()

        self.current_weekday = ""
        self.current_time_of_day = ""
        #self.root.ids.rutiini_teksti.text = ""

        if self.settings["theme_style"] == "Light":
                self.root.ids.dark_mode_btn.text = "Pimeätila päälle"

        for day in self.schedule:

            self.root.ids.main_scroll.add_widget(
                MDLabel(
                    text=day,
                    adaptive_height=True,
                    halign="center",
                    font_style = "Headline",
                    role = "small",
                    underline = False,
                )
            )

            for time, description in self.schedule[day].items():

                self.root.ids.main_scroll.add_widget(
                    MDListItem(
                        MDListItemLeadingIcon(
                            icon="calendar-clock"
                        ),
                        MDListItemHeadlineText(
                            text=time
                        ),
                        MDListItemSupportingText(
                            text=description
                        )
                    )
                )

    def build(self):

        self.load_data()

        self.theme_cls.theme_style = self.settings["theme_style"]
        self.theme_cls.primary_palette = self.settings["primary_palette"]

        return Builder.load_file("main.kv")
    

    def toggle_dark_mode(self):
        self.theme_cls.theme_style = (
            "Dark" if self.theme_cls.theme_style == "Light" else "Light"
        )
        self.root.ids.dark_mode_btn.text = "Pimeätila päälle" if self.theme_cls.theme_style == "Light" else "Pimeätila pois"
        self.settings["theme_style"] = self.theme_cls.theme_style
    
    def theme_picker_open(self):

        colors =  ['Aliceblue', 'Antiquewhite', 'Aqua', 'Aquamarine', 'Azure', 'Beige', 'Bisque', 'Black',
                   'Blanchedalmond', 'Blue', 'Blueviolet', 'Brown', 'Burlywood', 'Cadetblue', 'Chartreuse',
                   'Chocolate', 'Coral', 'Cornflowerblue', 'Cornsilk', 'Crimson', 'Cyan', 'Darkblue', 'Darkcyan',
                   'Darkgoldenrod', 'Darkgray', 'Darkgrey', 'Darkgreen', 'Darkkhaki', 'Darkmagenta', 'Darkolivegreen',
                   'Darkorange', 'Darkorchid', 'Darkred', 'Darksalmon', 'Darkseagreen', 'Darkslateblue', 'Darkslategray',
                   'Darkslategrey', 'Darkturquoise', 'Darkviolet', 'Deeppink', 'Deepskyblue', 'Dimgray', 'Dimgrey', 'Dodgerblue',
                   'Firebrick', 'Floralwhite', 'Forestgreen', 'Fuchsia', 'Gainsboro', 'Ghostwhite', 'Gold', 'Goldenrod', 'Gray', 'Grey',
                   'Green', 'Greenyellow', 'Honeydew', 'Hotpink', 'Indianred', 'Indigo', 'Ivory', 'Khaki', 'Lavender', 'Lavenderblush',
                   'Lawngreen', 'Lemonchiffon', 'Lightblue', 'Lightcoral', 'Lightcyan', 'Lightgoldenrodyellow', 'Lightgreen', 'Lightgray',
                   'Lightgrey', 'Lightpink', 'Lightsalmon', 'Lightseagreen', 'Lightskyblue', 'Lightslategray', 'Lightslategrey', 'Lightsteelblue',
                   'Lightyellow', 'Lime', 'Limegreen', 'Linen', 'Magenta', 'Maroon', 'Mediumaquamarine', 'Mediumblue', 'Mediumorchid', 'Mediumpurple',
                   'Mediumseagreen', 'Mediumslateblue', 'Mediumspringgreen', 'Mediumturquoise', 'Mediumvioletred', 'Midnightblue', 'Mintcream', 'Mistyrose',
                   'Moccasin', 'Navajowhite', 'Navy', 'Oldlace', 'Olive', 'Olivedrab', 'Orange', 'Orangered', 'Orchid', 'Palegoldenrod', 'Palegreen', 'Paleturquoise',
                   'Palevioletred', 'Papayawhip', 'Peachpuff', 'Peru', 'Pink', 'Plum', 'Powderblue', 'Purple', 'Red', 'Rosybrown', 'Royalblue', 'Saddlebrown', 'Salmon',
                   'Sandybrown', 'Seagreen', 'Seashell', 'Sienna', 'Silver', 'Skyblue', 'Slateblue', 'Slategray', 'Slategrey', 'Snow', 'Springgreen', 'Steelblue', 'Tan',
                   'Teal', 'Thistle', 'Tomato', 'Turquoise', 'Violet', 'Wheat', 'White', 'Whitesmoke', 'Yellow', 'Yellowgreen']

        menu_items = [
            {
                "text": f"{color}",
                "on_release": lambda x=f"{color}": self.set_palette(x),
                "leading_icon": "check" if self.theme_cls.primary_palette == f"{color}" else "",
            } for color in colors
        ]

        """Opens a list picker to choose a new primary color palette."""
        self.palette_dropdown = MDDropdownMenu(
            caller=self.root.ids.theme_picker_btn, items = menu_items,
            position = "bottom",
            radius = 30
        )
        self.palette_dropdown.open()

    def set_palette(self, color: str):
        self.theme_cls.primary_palette = color
        self.settings["primary_palette"] = self.theme_cls.primary_palette

    def pick_weekday_open(self):

        weekdays = ["Maanantai", "Tiistai", "Keskiviikko", "Torstai", "Perjantai", "Lauantai", "Sunnuntai"]
        menu_items = [
            {
            "text": f"{weekday}",
            "on_release": lambda x=weekday: self.pick_weekday_callback(x),
            "leading_icon": "check" if self.current_weekday == f"{weekday}" else "",
        } for weekday in weekdays
        ]
        self.weekday_dropdown = MDDropdownMenu(
            caller=self.root.ids.weekday_picker_btn,
            items=menu_items,
            position="center",
            radius=30
        )
        self.weekday_dropdown.open()
    
    def pick_weekday_callback(self, weekday: str):
        self.current_weekday = weekday
        self.root.ids.weekday_picker_btn_text.text = weekday
        self.weekday_dropdown.dismiss()

    def pick_time_of_day_open(self):

        tod = ["Aamupäivä", "Iltapäivä"]
        menu_items = [
            {
            "text": f"{time}",
            "on_release": lambda x=time: self.pick_time_of_day_callback(x),
            "leading_icon": "check" if self.current_time_of_day == f"{time}" else "",
        } for time in tod
        ]
        self.time_of_day_dropdown = MDDropdownMenu(
            caller=self.root.ids.time_of_day_picker_btn,
            items=menu_items,
            position="center",
            radius=30
        )

        self.time_of_day_dropdown.open()
    
    def pick_time_of_day_callback(self, tod: str):
        self.current_time_of_day = tod
        self.root.ids.time_of_day_picker_text.text = tod
        self.time_of_day_dropdown.dismiss()

    def save_new_routine(self):
        if self.current_weekday == "" or self.current_time_of_day == "" or self.root.ids.rutiini_teksti.text == "":
            return #pop up notification here
        else:
            self.schedule[self.current_weekday][self.current_time_of_day] = self.root.ids.rutiini_teksti.text

            self.reload_routines()

            self.save_data()

            self.root.ids.rutiini_teksti.text = ""
            self.root.ids.time_of_day_picker_text.text = "Aamupäivä / Iltapäivä"
            self.root.ids.weekday_picker_btn_text.text = "Valitse päivä"
    
    def reload_routines(self):

        self.root.ids.main_scroll.clear_widgets()

        for day in self.schedule:

            self.root.ids.main_scroll.add_widget(
                MDLabel(
                    text=day,
                    adaptive_height=True,
                    halign="center",
                    font_style = "Headline",
                    role = "small",
                    underline = False,
                )
            )

            for time, description in self.schedule[day].items():

                self.root.ids.main_scroll.add_widget(
                    MDListItem(
                        MDListItemLeadingIcon(
                            icon="calendar-clock"
                        ),
                        MDListItemHeadlineText(
                            text=time
                        ),
                        MDListItemSupportingText(
                            text=description
                        )
                    )
                )
        

    def load_data(self):
        try:
            with open("data.json", "r") as file:
                file_data = file.read()
                data = json.loads(file_data)
            self.settings = data["settings"]
            self.schedule = data["schedule"]

        except OSError:
            self.settings = {
                "theme_style": "Dark",
                "primary_palette": "Orange",
            }
                    #Build the schedule from data
            self.schedule = {
                "Maanantai": {
                    "Aamupäivä": "N/A",
                    "Iltapäivä": "N/A"
                },
                "Tiistai": {
                    "Aamupäivä": "N/A",
                    "Iltapäivä": "N/A"
                },
                "Keskiviikko": {
                    "Aamupäivä": "N/A",
                    "Iltapäivä": "N/A"
                },
                "Torstai": {
                    "Aamupäivä": "N/A",
                    "Iltapäivä": "N/A"
                },
                "Perjantai": {
                    "Aamupäivä": "N/A",
                    "Iltapäivä": "N/A"
                },
                "Lauantai": {
                    "Aamupäivä": "N/A",
                    "Iltapäivä": "N/A"
                },
                "Sunnuntai": {
                    "Aamupäivä": "N/A",
                    "Iltapäivä": "N/A"
                },
            }
        

    def save_data(self):
        data = {}
        data["settings"] = self.settings
        data["schedule"] = self.schedule

        with open("data.json", "w") as file:
            file.write(json.dumps(data))




if __name__ == "__main__":
    MainApp().run()