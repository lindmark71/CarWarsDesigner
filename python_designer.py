""" Python_Designer"""

#pylint: disable=attribute-defined-outside-init
#pylint: disable=line-too-long
#pylint: disable=too-many-arguments
#pylint: disable=too-many-positional-arguments
#pylint: disable=too-many-public-methods
#pylint: disable=too-many-branches
#pylint: disable=too-many-instance-attributes
#pylint: disable=too-many-locals
#pylint: disable=too-many-lines
#pylint: disable=too-many-statements
#pylint: disable=unused-argument
#pylint: disable=unused-wildcard-import
#pylint: disable=wildcard-import

#pylint: disable=fixme
#pylint: disable=missing-function-docstring
#pylint: disable=unused-import
#pylint: disable=unused-variable
#pylint: disable=c-extension-no-member
#pylint: disable=invalid-name

import os
import math
import tkinter as tk
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from tkinter import filedialog
import re
import json
from datetime import datetime
import webbrowser
from fpdf import FPDF

class Python_Designer():
    """Python_Designer class"""
    def __init__(self):
        """ Initial class, establish TKinter usage, labels, dropdowns and buttons"""
        self.datestamp: str = "08_04_2026"

        self.weapon_dropdown_objects = []
        self.weapon_qty_entry_objects = []
        self.weapon_qty_up_button_objects = []
        self.weapon_qty_down_button_objects = []
        
        # This is where your delete button list tracker belongs:
        self.weapon_delete_button_objects = []
        self.weapon_dropdown_string_vars = []
        self.weapon_qty_string_vars = []
        self.weapon_ammo_qty_string_vars = []
        self.weapon_extra_mag_qty_string_vars = []
        self.weapon_mount_dropdown_string_vars = []
        self.weapon_ammo_qty_entry_objects = []
        self.weapon_ammo_qty_up_button_objects = []
        self.weapon_ammo_qty_down_button_objects = []
        self.weapon_extra_mag_qty_entry_objects = []
        self.weapon_extra_mag_qty_up_button_objects = []
        self.weapon_extra_mag_qty_down_button_objects = []
        self.weapon_mount_dropdown_objects = []
        self.weapon_link_up_button_objects = []
        self.weapon_link_down_button_objects = []
        self.weapon_cost_label_objects = []
        self.weapon_weight_label_objects = []
        self.weapon_spaces_label_objects = []
        self.weapon_dp_label_objects = []
        self.weapon_to_hit_label_objects = []
        self.weapon_damage_label_objects = []
        self.weapon_delete_button_objects = []
        self.sub_weapon_dropdown_objects = []
        self.sub_weapon_dropdown_string_vars = []

        self.accessory_dropdown_string_vars = []
        self.accessory_qty_string_vars = []


        self.weapon_rows_count             = 0#10
        self.link_rows_count               = 0#10
        self.bt_rows_count                 = 0#10
        self.accessory_rows_count          = 0#30
        self.component_armor_rows_count    = 0# 5
        self.rocket_booster_rows_count     = 0# 5
        self.personal_equipment_rows_count = 0#10

        #forced column widths
        self.grid_col_item_forced_width                 = 250
        self.grid_col_qty_forced_width                  = 0
        self.grid_left_up_button_forced_width           = 0
        self.grid_left_down_button_forced_width         = 0
        self.grid_right_qty_forced_width                = 0
        self.grid_right_up_button_forced_width          = 0
        self.grid_right_down_button_forced_width        = 0
        self.grid_col_weapon_ammo_entry_forced_width    = 0
        self.grid_col_weapon_ammo_qty_up_forced_width   = 0
        self.grid_col_weapon_ammo_qty_down_forced_width = 0
        self.grid_col_extra_mag_entry_forced_width      = 0
        self.grid_col_extra_mag_qty_up_forced_width     = 0
        self.grid_col_extra_mag_qty_down_forced_width   = 0
        self.grid_col_cost_forced_width                 = 0
        self.grid_col_weight_forced_width               = 0
        self.grid_col_spaces_forced_width               = 0
        self.grid_col_dp_forced_width                   = 0
        self.grid_col_max_weight_forced_width           = 0
        self.grid_col_power_factors_forced_width        = 0
        self.grid_col_base_mpg_forced_width             = 0
        self.grid_col_test_track_forced_width           = 0
        self.grid_col_test_track_numbers_forced_width   = 0
        self.grid_col_last_column_forced_width          = 0


        self.set_columns()
        self.root = tk.Tk()
        self.root.state('zoomed')
        self.root.title(f"Python Car Wars Designer: Version {self.datestamp}") # Sets window title
        self.root.geometry("1600x800") # Sets window size
        self.current_file_path: str = ""
        self.is_cycle: bool = False
        self.is_loading: bool = False
        self.is_init: bool = True #There are whole slew of steps that don't need to happen if
                                   #we're just initializing the layout.  Turn off recalculate

        #Add drop down menus
        self.load_menus()

        for index in range(1, self.weapon_rows_count + 1):
            setattr(self, f"selected_sub_weapon_{index}", None)
            setattr(self, f"sub_weapon_dropdown_{index}", None)
            setattr(self, f"selected_sub_weapon_{index}_canvas", None)
            setattr(self, f"sub_weapon_dropdown_{index}_canvas", None)
            setattr(self, f"weapon_armor_facing_{index}", None)
            setattr(self, f"weapon_armor_facing_{index}_dropdown", None)
        
        self.gas_tank_dropdown = None     
        self.hc_adjusted: float = 0.0
        self.age_value: int = 0

        self.canvas_type = None
        self.main_frame = Frame(self.root)
        self.main_frame.pack(fill=BOTH, expand=1)
        # create a canvas
        self.my_canvas = Canvas(self.main_frame)
        self.my_canvas.pack(side=LEFT, fill=BOTH, expand=1)
        #add a scroll bar to the canvas
        self.my_scrollbar = Scrollbar(self.main_frame, orient=VERTICAL, command=self.my_canvas.yview)
        self.my_scrollbar.pack(side=RIGHT, fill=Y)
        self.horizontal_scrollbar = Scrollbar(self.main_frame, orient=HORIZONTAL, command=self.my_canvas.xview)
        self.horizontal_scrollbar.pack(side=BOTTOM, fill=X)
        #configure the canvas to have a scroll bar
        self.my_canvas.configure(yscrollcommand=self.my_scrollbar.set, xscrollcommand=self.horizontal_scrollbar.set)
        self.my_canvas.bind('<Configure>', lambda e: self.my_canvas.configure(scrollregion = self.my_canvas.bbox("all")))

        #create another frame inside the canvas
        self.second_frame = Frame(self.my_canvas)
        #add the new frame to a window in the canvas
        self.my_canvas.create_window((0,0), window=self.second_frame, anchor="nw")

        # Locate this existing line in your __init__:
        self.my_canvas.bind('<Configure>', lambda e: self.my_canvas.configure(scrollregion = self.my_canvas.bbox("all")))
        # 3. BINDINGS PASS: Link mouse wheel rotations across all operating systems
        # Windows & macOS mouse wheel events
        self.my_canvas.bind_all("<MouseWheel>", self._on_mouse_wheel_unified)
        
        # Linux mouse wheel up/down events
        self.my_canvas.bind_all("<Button-4>", self._on_mouse_wheel_unified)
        self.my_canvas.bind_all("<Button-5>", self._on_mouse_wheel_unified)

        # Create the weapons framework partition
        self.weapon_container_frame = tk.Frame(self.second_frame, bg=self.second_frame.cget('bg'))
        self.weapon_container_frame.grid(row=114, column=0, columnspan=30, sticky="nsew")

        # Create the standalone Accessories framework partition row
        self.accessory_container_frame = tk.Frame(self.second_frame, bg=self.second_frame.cget('bg'))
        self.accessory_container_frame.grid(row=116, column=0, columnspan=30, sticky="nsew")


        # Build column index lists to pass configurations cleanly
        column_indices = [
            (self.grid_col_item,                 self.grid_col_item_forced_width),
            (self.grid_col_qty,                  self.grid_col_qty_forced_width),
            (self.grid_left_up_button,           self.grid_left_up_button_forced_width),
            (self.grid_left_down_button,         self.grid_left_down_button_forced_width),
            (self.grid_right_qty,                self.grid_right_qty_forced_width),
            (self.grid_right_up_button,          self.grid_right_up_button_forced_width),
            (self.grid_right_down_button,        self.grid_right_down_button_forced_width),
            (self.grid_col_weapon_ammo_entry,    self.grid_col_weapon_ammo_entry_forced_width),
            (self.grid_col_weapon_ammo_qty_up,   self.grid_col_weapon_ammo_qty_up_forced_width),
            (self.grid_col_weapon_ammo_qty_down, self.grid_col_weapon_ammo_qty_down_forced_width),
            (self.grid_col_extra_mag_entry,      self.grid_col_extra_mag_entry_forced_width),
            (self.grid_col_extra_mag_qty_up,     self.grid_col_extra_mag_qty_up_forced_width),
            (self.grid_col_extra_mag_qty_down,   self.grid_col_extra_mag_qty_down_forced_width),
            (self.grid_col_cost,                 self.grid_col_cost_forced_width),
            (self.grid_col_weight,               self.grid_col_weight_forced_width),
            (self.grid_col_spaces,               self.grid_col_spaces_forced_width),
            (self.grid_col_dp,                   self.grid_col_dp_forced_width),
            (self.grid_col_max_weight,           self.grid_col_max_weight_forced_width),
            (self.grid_col_power_factors,        self.grid_col_power_factors_forced_width),
            (self.grid_col_base_mpg,             self.grid_col_base_mpg_forced_width),
            (self.grid_col_test_track,           self.grid_col_test_track_forced_width),
            (self.grid_col_test_track_numbers,   self.grid_col_test_track_numbers_forced_width),
            (self.grid_col_last_column,          self.grid_col_last_column_forced_width)
        ]

        # Apply minsize configurations globally
        for idx, width in column_indices:
            self.second_frame.columnconfigure(index=idx, minsize=width)
            self.weapon_container_frame.columnconfigure(index=idx, minsize=width)
        # PLACE THE BUTTON: Give it a high columnspan so it skips the wide first column boundaries!
        self.add_weapon_btn = tk.Button(
            self.weapon_container_frame, 
            text="➕ Add Weapon Row", 
            command=self.add_new_weapon_row_tactical,
            bg="#e1f5fe"
        )
        # We set columnspan=5 and move it to column 1 to completely avoid the 300-pixel zone
        self.add_weapon_btn.grid(row=0, column=self.grid_col_item, columnspan=1, sticky="w", padx=5, pady=5)

        # Build the layout placement action button matching application styling choices
        self.add_accessory_btn = tk.Button(
            self.accessory_container_frame,
            text="➕ Add Accessory Row",
            command=self.add_new_accessory_row,
            bg="#e1f5fe"  # Subtle brownish-grey theme distinct from weapons block
        )

        self.add_accessory_btn.grid(row=0, column=0, columnspan=1, sticky="w", padx=5, pady=5)

        # Start tracking count at 0 instead of drawing all 30 at startup
        self.accessory_rows_count = 0  

        self.add_labels_canvas(canvas_type=self.second_frame)
        self.add_dropdowns_canvas(canvas_type=self.second_frame)
        self.add_buttons_canvas(canvas_type=self.second_frame)

        #######################WEAPONS SECTION########################
        #This is required before any weapon row actions can occur
        #for index in range(1, self.weapon_rows_count + 1):
        #    weapon_options_list: list = self.get_weapon_options_alt()
        #    self.add_labels_buttons_weapon_row_unified(row_number=index, canvas_type=self.weapon_container_frame)
        #    self.add_dropdown_weapon_alt_unified(row_number=index, canvas_type=self.weapon_container_frame)        
        #######################WEAPONS SECTION########################


        # Add this inside __init__() to replace the previous dropdown variables
        #self.link_dropdown_sources = [None] * self.link_rows_count
        #self.link_dropdown_targets = [None] * self.link_rows_count
        #self.link_selections = [[] for _ in range(self.link_rows_count)]  # Holds lists of chosen actions
        #self.link_entry_vars = [tk.StringVar(value="No items linked") for _ in range(self.link_rows_count)]
        #self.link_entry_fields = [None] * self.link_rows_count

        # Add this inside __init__() near your Link row variables
        #self.bt_rows_count = 10
        #self.bt_selections = [[] for _ in range(self.bt_rows_count)]  # Holds lists of chosen actions for Bumper Triggers
        #self.bt_entry_vars = [tk.StringVar(value="No items linked") for _ in range(self.bt_rows_count)]
        #self.bt_entry_fields = [None] * self.bt_rows_count

        # Added facing tracking variables for each bumper trigger row
        #self.selected_bt_facing = [tk.StringVar(value="Front") for _ in range(self.bt_rows_count)]
        #self.add_labels_buttons_link_rows(canvas_type=self.second_frame)
        #self.add_labels_buttons_bumper_trigger_rows(canvas_type=self.second_frame)
        #self.add_labels_buttons_accessories_1_canvas(canvas_type=self.second_frame)
        #self.add_labels_buttons_accessories_2_canvas(canvas_type=self.second_frame)
        #self.add_labels_buttons_accessories_3_canvas(canvas_type=self.second_frame)
        #self.add_labels_buttons_accessories_4_canvas(canvas_type=self.second_frame)
        #self.add_labels_buttons_accessories_5_canvas(canvas_type=self.second_frame)
        #self.add_labels_buttons_accessories_6_canvas(canvas_type=self.second_frame)
        #self.add_labels_buttons_accessories_7_canvas(canvas_type=self.second_frame)
        #self.add_labels_buttons_accessories_8_canvas(canvas_type=self.second_frame)
        #self.add_labels_buttons_accessories_9_canvas(canvas_type=self.second_frame)
        #self.add_labels_buttons_accessories_10_canvas(canvas_type=self.second_frame)
        #self.add_labels_buttons_accessories_11_canvas(canvas_type=self.second_frame)
        #self.add_labels_buttons_accessories_12_canvas(canvas_type=self.second_frame)
        #self.add_labels_buttons_accessories_13_canvas(canvas_type=self.second_frame)
        #self.add_labels_buttons_accessories_14_canvas(canvas_type=self.second_frame)
        #self.add_labels_buttons_accessories_15_canvas(canvas_type=self.second_frame)
        #self.add_labels_buttons_accessories_16_canvas(canvas_type=self.second_frame)
        #self.add_labels_buttons_accessories_17_canvas(canvas_type=self.second_frame)
        #self.add_labels_buttons_accessories_18_canvas(canvas_type=self.second_frame)
        #self.add_labels_buttons_accessories_19_canvas(canvas_type=self.second_frame)
        #self.add_labels_buttons_accessories_20_canvas(canvas_type=self.second_frame)
        #self.add_labels_buttons_accessories_21_canvas(canvas_type=self.second_frame)
        #self.add_labels_buttons_accessories_22_canvas(canvas_type=self.second_frame)
        #self.add_labels_buttons_accessories_23_canvas(canvas_type=self.second_frame)
        #self.add_labels_buttons_accessories_24_canvas(canvas_type=self.second_frame)
        #self.add_labels_buttons_accessories_25_canvas(canvas_type=self.second_frame)
        #self.add_labels_buttons_accessories_26_canvas(canvas_type=self.second_frame)
        #self.add_labels_buttons_accessories_27_canvas(canvas_type=self.second_frame)
        #self.add_labels_buttons_accessories_28_canvas(canvas_type=self.second_frame)
        #self.add_labels_buttons_accessories_29_canvas(canvas_type=self.second_frame)
        #self.add_labels_buttons_accessories_30_canvas(canvas_type=self.second_frame)
        #self.add_dropdown_weapons(canvas_type=self.second_frame)
        #self.add_component_armor_rows(canvas_type=self.second_frame)
        #self.get_component_armor_facing_dictionaries()
        #self.add_dropdown_component_armor_canvas(canvas_type=self.second_frame)
        #self.get_rocket_booster_facing_dictionaries()
        #self.add_row_rocket_boosters(canvas_type=self.second_frame)
        #self.load_accessories_processing_list()
        #self.add_labels_buttons_personal_equipment(canvas_type=self.second_frame)
        self.canvas_type = self.second_frame
        self.hide_electric_engine_options()
        self.hide_gas_engine_options()
        self.is_init = False

    def load_menus(self):
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        file_menu = tk.Menu(menubar, tearoff=0)  # tearoff=0 prevents detaching the menu
        edit_menu = tk.Menu(menubar, tearoff=0)
        help_menu = tk.Menu(menubar, tearoff=0)

        menubar.add_cascade(label="File", menu=file_menu)
        menubar.add_cascade(label="Edit", menu=edit_menu)
        menubar.add_cascade(label="Help", menu=help_menu)

        file_menu.add_command(label="New", command=self.menu_file_new)
        file_menu.add_command(label="Open", command=self.menu_file_open)
        file_menu.add_command(label="Print", command=self.menu_file_print)
        file_menu.add_command(label="Save", command=self.menu_file_save)
        file_menu.add_command(label="Save As", command=self.menu_file_save_as)
        file_menu.add_separator()  # Add a visual separator
        file_menu.add_command(label="Exit", command=self.menu_file_exit)

        help_menu.add_command(label="How Does This Work?", command=self.menu_help_how_does_this_work)
        help_menu.add_command(label="What's New", command=self.menu_help_whats_new)
        help_menu.add_command(label="What's Next", command=self.menu_help_whats_next)
        help_menu.add_command(label="About", command=self.menu_help_about)

    def menu_file_new(self, *args):
        # 1. Reset all your core vehicle configuration values safely
        self.selected_body.set('Body')
        self.selected_modifications.set('No Mods')
        self.selected_chassis.set('Chassis')
        self.selected_suspension.set('Suspension')
        self.selected_engine.set('Engine')
        self.var_engine_gas_super_charger.set(0)
        self.var_engine_gas_vp_turbo.set(0)
        self.var_engine_gas_tube_headers.set(0)
        self.var_engine_gas_blue_print.set(0)
        self.var_engine_gas_turbo.set(0)
        self.var_engine_electric_super_conductors.set(0)
        self.var_engine_electric_platnium_catalysts.set(0)
        self.var_engine_electric_extra_power_cells.set(0)
        self.selected_gas_tank.set('Gas Tank')
        self.var_gas_gallon_qty.set(0)
        self.var_front_tire_qty.set(0)
        self.var_rear_tire_qty.set(0)
        self.var_driver_gunner_qty.set(0)
        self.var_passenger_qty.set(0)
        self.var_outer_armor_qty.set(0)
        self.var_inner_armor_qty.set(0)
        self.var_front_tire_steelbelting.set(0)
        self.var_front_tire_radial.set(0)
        self.var_front_tire_fireproof.set(0)
        self.var_front_tire_offroad.set(0)
        self.var_front_tire_racing_slick.set(0)
        self.var_rear_tire_steelbelting.set(0)
        self.var_rear_tire_radial.set(0)
        self.var_rear_tire_fireproof.set(0)
        self.var_rear_tire_offroad.set(0)
        self.var_rear_tire_racing_slick.set(0)
        self.selected_front_tire.set('Tires')
        self.selected_rear_tire.set('Tires')
        self.selected_outer_armor.set('Outer Armor')
        self.selected_inner_armor.set('Inner Armor')

        # 2. Reset the text tracking parameters across all 30 Accessory rows
        for i in range(1, 31):
            getattr(self, f"selected_accessories_{i}").set('Accessory')
            getattr(self, f"var_accessories_{i}_qty").set(0)

        # 3. Reset the component armor values back to pristine baselines
        for i in range(1, 6):
            getattr(self, f"selected_component_armor_{i}").set('Component armor')
            getattr(self, f"selected_component_armor_facing_{i}").set('Facing')
            getattr(self, f"var_component_armor_spaces_qty_{i}").set(0)
            getattr(self, f"var_component_armor_count_qty_{i}").set(0)

       # =====================================================================
        # THE NEW ATOMIC RESET WEAPONS STEP
        # =====================================================================
        # 1. Completely destroy the weapon frame container and all widgets inside it!
        if hasattr(self, 'weapon_container_frame') and self.weapon_container_frame is not None:
            self.weapon_container_frame.grid_forget()
            self.weapon_container_frame.destroy()

        # 2. Re-create a clean, empty canvas sub-frame in its place
        self.weapon_container_frame = tk.Frame(self.second_frame, bg=self.second_frame.cget('bg'))
        self.weapon_container_frame.grid(row=112, column=0, columnspan=10, sticky="nsew", padx=5, pady=5)

        # 3. Clean up the underlying data memory values
        self.weapon_rows_count = 0  # Set weapon count back to zero!

        # 4. Draw the standalone "Add Weapon Row" trigger button onto the fresh frame
        self.add_weapon_btn = tk.Button(
            self.weapon_container_frame, 
            text="➕ Add Weapon Row", 
            command=self.add_new_weapon_row_tactical,
            bg="#e1f5fe"
        )

        # 4. IRONCLAD WEAPON COLUMN PURGE (Hunts down dynamic stacked dropdowns)
        # This scans every child widget inside self.second_frame that is sitting 
        # in Column 0 from Row 112 onwards (the weapons section layout zone).
        # It maps them to find the true originals, and destroys the dynamic duplicates!
        #all_column_zero_menus = []
        #for child in self.second_frame.winfo_children():
        #    try:
        #        widget_class = child.winfo_class()
        #        if widget_class in ['Menubutton', 'TMenubutton', 'Combobox']:
        #            grid_info = child.grid_info()
        #            col = grid_info.get("column", -1)
        #            row = grid_info.get("row", -1)
        #            
        #            if row >= 112 and col == 0:
        #                all_column_zero_menus.append((row, child))
        #    except Exception:
        #        pass

        # Sort widgets vertically by their row position to safely separate originals from duplicates
        #all_column_zero_menus.sort(key=lambda x: x[0])

        # Track how many primary category dropdowns we expect to keep
        #processed_primary_rows = {}
        
        #for row, widget in all_column_zero_menus:
        #    # The first dropdown found on a unique row number is your original category selection box.
        #    # Any subsequent dropdown on that exact same row is a dynamic sub-weapon box!
        #    if row not in processed_primary_rows:
        #        processed_primary_rows[row] = widget
        #    else:
        #        try:
        #            widget.grid_forget() # Un-map placement path
        #            widget.destroy()     # Delete the ghost sub-dropdown from memory entirely
        #        except Exception:
        #            pass

        # 5. Clear variable tracking attributes and restore baseline data column labels
        #for index in range(1, self.weapon_rows_count + 1):
        #    getattr(self, f"selected_weapon_alt_{index}").set('Weapon')
        #    getattr(self, f"weapon_armor_facing_{index}").set('Facing')
        #    getattr(self, f"var_sub_weapon_{index}_qty").set(0)
        #    getattr(self, f"var_sub_weapon_ammo_{index}_qty").set(0)
        #    getattr(self, f"var_sub_weapon_extra_mags_{index}_qty").set(0)

            # Nullify secondary canvas reference markers completely to clear layout memory
        #    for var_suffix in ["", "_canvas"]:
        #        setattr(self, f"selected_sub_weapon_{index}{var_suffix}", None)
        #        setattr(self, f"sub_weapon_dropdown_{index}{var_suffix}", None)

            # Force statistic string labels back to pure zero baseline footprints
        #    getattr(self, f"label_sub_weapon_{index}_cost").configure(text="0")
        #    getattr(self, f"label_sub_weapon_{index}_weight").configure(text="0")
        ##    getattr(self, f"label_sub_weapon_{index}_space").configure(text="0")
        #    getattr(self, f"label_sub_weapon_{index}_shots").configure(text="0")
        #    getattr(self, f"label_sub_weapon_{index}_ammo_cost").configure(text="0")
        #    getattr(self, f"label_sub_weapon_{index}_ammo_weight").configure(text="0")
        #    getattr(self, f"label_sub_weapon_{index}_tohit").configure(text="")
        #    getattr(self, f"label_sub_weapon_{index}_damage").configure(text="")

        # 6. Synchronize screen layout bounds tracking pass
        self.root.update_idletasks()
        self.my_canvas.configure(scrollregion=self.my_canvas.bbox("all"))
        self.recalculate()

    def menu_file_open(self, *args):
        self.current_file_path = filedialog.askopenfilename()  # Open file selection dialog
        self.load_record(self.current_file_path)

    def menu_file_save(self, *args):
        if self.current_file_path == "":
            self.current_file_path = filedialog.asksaveasfilename()  # Open file selection dialog
        self.save_record(self.current_file_path)
        messagebox.showinfo("File Save", f"{self.current_file_path} saved.")

    def menu_file_save_as(self, *args):
        self.current_file_path = filedialog.asksaveasfilename()  # Open file selection dialog
        self.save_record(self.current_file_path)
        messagebox.showinfo("File Save As", f"{self.current_file_path} saved.")

    def menu_file_print(self, *args):
        output_dict: dict = {}
        output_dict["Body"] = ""
        var_sloped_armor: int = int(self.var_sloped_armor.get())
        if var_sloped_armor == 1: #include the sloped reference
            output_dict["Body"] += "Sloped "
        local_mod: str = str(self.selected_modifications.get())
        if local_mod not in ["No Mods", "Modifications"]:
            output_dict["Body"] += local_mod + " "
        output_dict["Body"] += str(self.selected_body.get())
        output_dict["Body_Name"] = str(self.selected_body.get())
        if int(self.var_six_wheel_chassis.get()) == 1:
            output_dict["Body"] += " with six wheel chassis"
        output_dict["Chassis"] = str(self.selected_chassis.get())
        output_dict["Suspension"] = str(self.selected_suspension.get())
        output_dict["Engine"] = str(self.selected_engine.get())
        if self.label_engine_type.cget("text") == "Gas":
            if self.var_engine_gas_super_charger.get() == 1:
                output_dict["Engine"] += ", " + "SuperCharger"
            if self.var_engine_gas_vp_turbo.get() == 1:
                output_dict["Engine"] += ", " + "Variable Pitch Turbo Charger"
            if self.var_engine_gas_tube_headers.get() == 1:
                output_dict["Engine"] += ", " + "Tubular Headers"
            if self.var_engine_gas_blue_print.get() == 1:
                output_dict["Engine"] += ", " + "Blueprinting"
            if self.var_engine_gas_turbo.get() == 1:
                output_dict["Engine"] += ", " + "TurboCharger"
            output_dict["GasTank"] = str(self.selected_gas_tank.get())
            output_dict["GasQty"] = str(self.var_gas_gallon_qty.get())
            output_dict["GasDp"] = str(self.label_gas_tank_dp.cget("text"))
        else:
            if self.var_engine_electric_super_conductors.get() == 1:
                output_dict["Engine"] += ", " + "Super Conductors"
            if self.var_engine_electric_platnium_catalysts.get():
                output_dict["Engine"] += ", " + "Platnium Catalysts"
            if self.var_engine_electric_extra_power_cells.get() == 1:
                output_dict["Engine"] += ", " + "Extra Power Cells"

        output_dict["Total_Cost"] = str(self.label_total_cost.cget("text"))
        output_dict["Total_Weight"] = str(self.label_total_weight.cget("text"))
        output_dict["Total_Space"] = str(self.label_total_space.cget("text"))
        output_dict["Final_Engine_MPG"] = str(self.label_final_engine_mpg.cget("text"))
        output_dict["Total_Power_Factors"] = str(self.label_total_power_factors.cget("text"))
        output_dict["Top_Speed"] = str(self.label_top_speed.cget("text"))
        output_dict["Max_Weight_Top_Speed"] = str(self.label_max_weight_top_speed.cget("text"))
        output_dict["Accel"] = str(self.label_accel.cget("text"))
        output_dict["Max_Accel"] = str(self.label_max_accel.cget("text"))
        output_dict["HC"] = str(self.label_max_hc.cget("text"))
        output_dict["MPG"] = str(self.label_final_engine_mpg.cget("text"))
        output_dict["Range"] = str(self.label_range.cget("text"))
        output_dict["Engine_Type"] = str(self.label_engine_type.cget("text"))
        output_dict["Engine_DP"] = str(self.label_engine_dp.cget("text"))
        output_dict["Outer_Armor_Name"] = str(self.selected_outer_armor.get())
        output_dict["Inner_Armor_Name"] = str(self.selected_inner_armor.get())

        if self.var_front_tire_qty.get() > 0: #only list front tires if they exist
            output_dict["front_tire_dp"] = str(self.label_front_tire_dp.cget("text"))
            output_dict["front_tire_qty"] = str(self.var_front_tire_qty.get())
            output_dict["front_tire"] = ""
            if self.var_front_tire_steelbelting.get() == 1:
                output_dict["front_tire"] += "Steelbelted" + " "
            if self.var_front_tire_radial.get() == 1:
                output_dict["front_tire"] += "Radial" + " "
            if self.var_front_tire_fireproof.get() == 1:
                output_dict["front_tire"] += "Fireproof" + " "
            if self.var_front_tire_offroad.get() == 1:
                output_dict["front_tire"] += "OffRoad" + " "
            if self.var_front_tire_racing_slick.get() == 1:
                output_dict["front_tire"] += "Racing Slicks" + " "
            output_dict["front_tire"] += str(self.selected_front_tire.get())
        if self.var_rear_tire_qty.get() > 0: #only list rear tires if they exist
            output_dict["rear_tire_dp"] = str(self.label_rear_tire_dp.cget("text"))
            output_dict["rear_tire_qty"] = str(self.var_rear_tire_qty.get())
            output_dict["rear_tire"] = ""
            if self.var_rear_tire_steelbelting.get() == 1:
                output_dict["rear_tire"] += "Steelbelted" + " "
            if self.var_rear_tire_radial.get() == 1:
                output_dict["rear_tire"] += "Radial" + " "
            if self.var_rear_tire_fireproof.get() == 1:
                output_dict["rear_tire"] += "Fireproof" + " "
            if self.var_rear_tire_offroad.get() == 1:
                output_dict["rear_tire"] += "OffRoad" + " "
            if self.var_rear_tire_racing_slick.get() == 1:
                output_dict["rear_tire"] += "Racing Slicks" + " "
            output_dict["rear_tire"] += str(self.selected_rear_tire.get())
        if self.var_driver_gunner_qty.get() > 0:
            output_dict["driver_gunner"] = str(self.var_driver_gunner_qty.get())
        if self.var_passenger_qty.get() > 0:
            output_dict["passenger"] = str(self.var_passenger_qty.get())

        output_dict["armor_outer_front_qty"]  = str(self.var_outer_front_armor_allocation_qty.get())
        output_dict["armor_outer_back_qty"]   = str(self.var_outer_back_armor_allocation_qty.get())
        output_dict["armor_outer_left_qty"]   = str(self.var_outer_left_armor_allocation_qty.get())
        output_dict["armor_outer_right_qty"]  = str(self.var_outer_right_armor_allocation_qty.get())
        output_dict["armor_outer_top_qty"]    = str(self.var_outer_top_armor_allocation_qty.get())
        output_dict["armor_outer_bottom_qty"] = str(self.var_outer_underbody_armor_allocation_qty.get())

        output_dict["armor_inner_front_qty"]  = str(self.var_inner_front_armor_allocation_qty.get())
        output_dict["armor_inner_back_qty"]   = str(self.var_inner_back_armor_allocation_qty.get())
        output_dict["armor_inner_left_qty"]   = str(self.var_inner_left_armor_allocation_qty.get())
        output_dict["armor_inner_right_qty"]  = str(self.var_inner_right_armor_allocation_qty.get())
        output_dict["armor_inner_top_qty"]    = str(self.var_inner_top_armor_allocation_qty.get())
        output_dict["armor_inner_bottom_qty"] = str(self.var_inner_underbody_armor_allocation_qty.get())

        for index in range(1, self.weapon_rows_count + 1):
            # Safely fetch the main conditional canvas attribute
            canvas_attr = getattr(self, f"selected_sub_weapon_{index}_canvas", None)
            
            if canvas_attr is not None:
                output_dict[f"weapon_{index}_qty"]    = getattr(self, f"var_sub_weapon_{index}_qty").get()
                output_dict[f"weapon_{index}_name"]   = canvas_attr.get()
                output_dict[f"weapon_{index}_facing"] = getattr(self, f"weapon_armor_facing_{index}").get()
                output_dict[f"weapon_{index}_to_hit"] = getattr(self, f"label_sub_weapon_{index}_tohit").cget("text")
                output_dict[f"weapon_{index}_damage"] = getattr(self, f"label_sub_weapon_{index}_damage").cget("text")
                output_dict[f"weapon_{index}_ammo"]   = getattr(self, f"var_sub_weapon_ammo_{index}_qty").get()
                output_dict[f"weapon_{index}_dp"]     = getattr(self, f"label_hidden_sub_weapon_{index}_dp").cget("text")
                output_dict[f"weapon_type_{index}"]   = str(getattr(self, f"selected_weapon_alt_{index}").get())
            else:
                output_dict[f"weapon_{index}_qty"]    = ""
                output_dict[f"weapon_{index}_name"]   = ""
                output_dict[f"weapon_{index}_facing"] = ""
                output_dict[f"weapon_{index}_to_hit"] = ""
                output_dict[f"weapon_{index}_damage"] = ""
                output_dict[f"weapon_{index}_ammo"]   = ""
                output_dict[f"weapon_{index}_dp"]     = ""
                output_dict[f"weapon_type_{index}"]   = ""


        #if self.selected_sub_weapon_1_canvas is not None:
        #    output_dict["weapon_1_qty"]    = self.var_sub_weapon_1_qty.get()
        #    output_dict["weapon_1_name"]   = self.selected_sub_weapon_1_canvas.get()
        #    output_dict["weapon_1_facing"] = self.weapon_armor_facing_1.get()
        #    output_dict["weapon_1_to_hit"] = self.label_sub_weapon_1_tohit.cget("text")
        #    output_dict["weapon_1_damage"] = self.label_sub_weapon_1_damage.cget("text")
        #    output_dict["weapon_1_ammo"]   = self.var_sub_weapon_ammo_1_qty.get()
        #    output_dict["weapon_1_dp"]     = self.label_hidden_sub_weapon_1_dp.cget("text")
        #else:
        #    output_dict["weapon_1_qty"]    = ""
        #    output_dict["weapon_1_name"]   = ""
        #    output_dict["weapon_1_facing"] = ""
        #    output_dict["weapon_1_to_hit"] = ""
        #    output_dict["weapon_1_damage"] = ""
        #    output_dict["weapon_1_ammo"]   = ""
        #    output_dict["weapon_1_dp"]     = ""
        #if self.selected_sub_weapon_2_canvas is not None:
        #    output_dict["weapon_2_qty"]    = self.var_sub_weapon_2_qty.get()
        #    output_dict["weapon_2_name"]   = self.selected_sub_weapon_2_canvas.get()
        #    output_dict["weapon_2_facing"] = self.weapon_armor_facing_2.get()
        #    output_dict["weapon_2_to_hit"] = self.label_sub_weapon_2_tohit.cget("text")
        #    output_dict["weapon_2_damage"] = self.label_sub_weapon_2_damage.cget("text")
        #    output_dict["weapon_2_ammo"]   = self.var_sub_weapon_ammo_2_qty.get()
        #    output_dict["weapon_2_dp"]     = self.label_hidden_sub_weapon_2_dp.cget("text")
        #else:
        #    output_dict["weapon_2_qty"]    = ""
        #    output_dict["weapon_2_name"]   = ""
        #    output_dict["weapon_2_facing"] = ""
        #    output_dict["weapon_2_to_hit"] = ""
        #    output_dict["weapon_2_damage"] = ""
        #    output_dict["weapon_2_ammo"]   = ""
        #    output_dict["weapon_2_dp"]     = ""
        #if self.selected_sub_weapon_3_canvas is not None:
        #    output_dict["weapon_3_qty"]    = self.var_sub_weapon_3_qty.get()
        #    output_dict["weapon_3_name"]   = self.selected_sub_weapon_3_canvas.get()
        #    output_dict["weapon_3_facing"] = self.weapon_armor_facing_3.get()
        #    output_dict["weapon_3_to_hit"] = self.label_sub_weapon_3_tohit.cget("text")
        #    output_dict["weapon_3_damage"] = self.label_sub_weapon_3_damage.cget("text")
        #    output_dict["weapon_3_ammo"]   = self.var_sub_weapon_ammo_3_qty.get()
        #    output_dict["weapon_3_dp"]     = self.label_hidden_sub_weapon_3_dp.cget("text")
        #else:
        #    output_dict["weapon_3_qty"]    = ""
        #    output_dict["weapon_3_name"]   = ""
        #    output_dict["weapon_3_facing"] = ""
        #    output_dict["weapon_3_to_hit"] = ""
        #    output_dict["weapon_3_damage"] = ""
        #    output_dict["weapon_3_ammo"]   = ""
        #    output_dict["weapon_3_dp"]     = ""
        #if self.selected_sub_weapon_4_canvas is not None:
        #    output_dict["weapon_4_qty"]    = self.var_sub_weapon_4_qty.get()
        #    output_dict["weapon_4_name"]   = self.selected_sub_weapon_4_canvas.get()
        #    output_dict["weapon_4_facing"] = self.weapon_armor_facing_4.get()
        #    output_dict["weapon_4_to_hit"] = self.label_sub_weapon_4_tohit.cget("text")
        #    output_dict["weapon_4_damage"] = self.label_sub_weapon_4_damage.cget("text")
        #    output_dict["weapon_4_ammo"]   = self.var_sub_weapon_ammo_4_qty.get()
        #    output_dict["weapon_4_dp"]     = self.label_hidden_sub_weapon_4_dp.cget("text")
        #else:
        #    output_dict["weapon_4_qty"]    = ""
        #    output_dict["weapon_4_name"]   = ""
        #    output_dict["weapon_4_facing"] = ""
        #    output_dict["weapon_4_to_hit"] = ""
        #    output_dict["weapon_4_damage"] = ""
        #    output_dict["weapon_4_ammo"]   = ""
        #    output_dict["weapon_4_dp"]     = ""
        #if self.selected_sub_weapon_5_canvas is not None:
        #    output_dict["weapon_5_qty"]    = self.var_sub_weapon_5_qty.get()
        #    output_dict["weapon_5_name"]   = self.selected_sub_weapon_5_canvas.get()
        #    output_dict["weapon_5_facing"] = self.weapon_armor_facing_5.get()
        #    output_dict["weapon_5_to_hit"] = self.label_sub_weapon_5_tohit.cget("text")
        #    output_dict["weapon_5_damage"] = self.label_sub_weapon_5_damage.cget("text")
        #    output_dict["weapon_5_ammo"]   = self.var_sub_weapon_ammo_5_qty.get()
        #    output_dict["weapon_5_dp"]     = self.label_hidden_sub_weapon_5_dp.cget("text")
        #else:
        #    output_dict["weapon_5_qty"]    = ""
        #    output_dict["weapon_5_name"]   = ""
        #    output_dict["weapon_5_facing"] = ""
        #    output_dict["weapon_5_to_hit"] = ""
        #    output_dict["weapon_5_damage"] = ""
        #    output_dict["weapon_5_ammo"]   = ""
        #    output_dict["weapon_5_dp"]     = ""
        #if self.selected_sub_weapon_6_canvas is not None:
        #    output_dict["weapon_6_qty"]    = self.var_sub_weapon_6_qty.get()
        #    output_dict["weapon_6_name"]   = self.selected_sub_weapon_6_canvas.get()
        #    output_dict["weapon_6_facing"] = self.weapon_armor_facing_6.get()
        #    output_dict["weapon_6_to_hit"] = self.label_sub_weapon_6_tohit.cget("text")
        #    output_dict["weapon_6_damage"] = self.label_sub_weapon_6_damage.cget("text")
        #    output_dict["weapon_6_ammo"]   = self.var_sub_weapon_ammo_6_qty.get()
        #    output_dict["weapon_6_dp"]     = self.label_hidden_sub_weapon_6_dp.cget("text")
        #else:
        #    output_dict["weapon_6_qty"]    = ""
        #    output_dict["weapon_6_name"]   = ""
        #    output_dict["weapon_6_facing"] = ""
        #    output_dict["weapon_6_to_hit"] = ""
        #    output_dict["weapon_6_damage"] = ""
        #    output_dict["weapon_6_ammo"]   = ""
        #    output_dict["weapon_6_dp"]     = ""
        #if self.selected_sub_weapon_7_canvas is not None:
        #    output_dict["weapon_7_qty"]    = self.var_sub_weapon_7_qty.get()
        #    output_dict["weapon_7_name"]   = self.selected_sub_weapon_7_canvas.get()
        #    output_dict["weapon_7_facing"] = self.weapon_armor_facing_7.get()
        #    output_dict["weapon_7_to_hit"] = self.label_sub_weapon_7_tohit.cget("text")
        #    output_dict["weapon_7_damage"] = self.label_sub_weapon_7_damage.cget("text")
        #    output_dict["weapon_7_ammo"]   = self.var_sub_weapon_ammo_7_qty.get()
        #    output_dict["weapon_7_dp"]     = self.label_hidden_sub_weapon_7_dp.cget("text")
        #else:
        #    output_dict["weapon_7_qty"]    = ""
        #    output_dict["weapon_7_name"]   = ""
        #    output_dict["weapon_7_facing"] = ""
        #    output_dict["weapon_7_to_hit"] = ""
        #    output_dict["weapon_7_damage"] = ""
        #    output_dict["weapon_7_ammo"]   = ""
        #    output_dict["weapon_7_dp"]     = ""
        #if self.selected_sub_weapon_8_canvas is not None:
        #    output_dict["weapon_8_qty"]    = self.var_sub_weapon_8_qty.get()
        #    output_dict["weapon_8_name"]   = self.selected_sub_weapon_8_canvas.get()
        #    output_dict["weapon_8_facing"] = self.weapon_armor_facing_8.get()
        #    output_dict["weapon_8_to_hit"] = self.label_sub_weapon_8_tohit.cget("text")
        #    output_dict["weapon_8_damage"] = self.label_sub_weapon_8_damage.cget("text")
        #    output_dict["weapon_8_ammo"]   = self.var_sub_weapon_ammo_8_qty.get()
        #    output_dict["weapon_8_dp"]     = self.label_hidden_sub_weapon_8_dp.cget("text")
        #else:
        #    output_dict["weapon_8_qty"]    = ""
        #    output_dict["weapon_8_name"]   = ""
        #    output_dict["weapon_8_facing"] = ""
        #    output_dict["weapon_8_to_hit"] = ""
        #    output_dict["weapon_8_damage"] = ""
        #    output_dict["weapon_8_ammo"]   = ""
        #    output_dict["weapon_8_dp"]     = ""
        #if self.selected_sub_weapon_9_canvas is not None:
        #    output_dict["weapon_9_qty"]    = self.var_sub_weapon_9_qty.get()
        #    output_dict["weapon_9_name"]   = self.selected_sub_weapon_9_canvas.get()
        #    output_dict["weapon_9_facing"] = self.weapon_armor_facing_9.get()
        #    output_dict["weapon_9_to_hit"] = self.label_sub_weapon_9_tohit.cget("text")
        #    output_dict["weapon_9_damage"] = self.label_sub_weapon_9_damage.cget("text")
        #    output_dict["weapon_9_ammo"]   = self.var_sub_weapon_ammo_9_qty.get()
        #    output_dict["weapon_9_dp"]     = self.label_hidden_sub_weapon_9_dp.cget("text")
        #else:
        #    output_dict["weapon_9_qty"]    = ""
        #    output_dict["weapon_9_name"]   = ""
        #    output_dict["weapon_9_facing"] = ""
        #    output_dict["weapon_9_to_hit"] = ""
        #    output_dict["weapon_9_damage"] = ""
        #    output_dict["weapon_9_ammo"]   = ""
        #    output_dict["weapon_9_dp"]     = ""
        #if self.selected_sub_weapon_10_canvas is not None:
        #    output_dict["weapon_10_qty"]    = self.var_sub_weapon_10_qty.get()
        #    output_dict["weapon_10_name"]   = self.selected_sub_weapon_10_canvas.get()
        #    output_dict["weapon_10_facing"] = self.weapon_armor_facing_10.get()
        #    output_dict["weapon_10_to_hit"] = self.label_sub_weapon_10_tohit.cget("text")
        #    output_dict["weapon_10_damage"] = self.label_sub_weapon_10_damage.cget("text")
        #    output_dict["weapon_10_ammo"]   = self.var_sub_weapon_ammo_10_qty.get()
        #    output_dict["weapon_10_dp"]     = self.label_hidden_sub_weapon_10_dp.cget("text")
        #else:
        #    output_dict["weapon_10_qty"]    = ""
        #    output_dict["weapon_10_name"]   = ""
        #    output_dict["weapon_10_facing"] = ""
        #    output_dict["weapon_10_to_hit"] = ""
        #    output_dict["weapon_10_damage"] = ""
        #    output_dict["weapon_10_ammo"]   = ""
        #    output_dict["weapon_10_dp"]     = ""

        #output_dict["weapon_type_1"] = str(self.selected_weapon_alt_1.get())
        #output_dict["weapon_type_2"] = str(self.selected_weapon_alt_2.get())
        #output_dict["weapon_type_3"] = str(self.selected_weapon_alt_3.get())
        #output_dict["weapon_type_4"] = str(self.selected_weapon_alt_4.get())
        #output_dict["weapon_type_5"] = str(self.selected_weapon_alt_5.get())
        #output_dict["weapon_type_6"] = str(self.selected_weapon_alt_6.get())
        #output_dict["weapon_type_7"] = str(self.selected_weapon_alt_7.get())
        #output_dict["weapon_type_8"] = str(self.selected_weapon_alt_8.get())
        #output_dict["weapon_type_9"] = str(self.selected_weapon_alt_9.get())
        #output_dict["weapon_type_10"] = str(self.selected_weapon_alt_10.get())

        output_dict["accessory_1_qty"]   = str(self.var_accessories_1_qty.get())
        output_dict["accessory_1_name"]  = str(self.selected_accessories_1.get())
        output_dict["accessory_2_qty"]   = str(self.var_accessories_2_qty.get())
        output_dict["accessory_2_name"]  = str(self.selected_accessories_2.get())
        output_dict["accessory_3_qty"]   = str(self.var_accessories_3_qty.get())
        output_dict["accessory_3_name"]  = str(self.selected_accessories_3.get())
        output_dict["accessory_4_qty"]   = str(self.var_accessories_4_qty.get())
        output_dict["accessory_4_name"]  = str(self.selected_accessories_4.get())
        output_dict["accessory_5_qty"]   = str(self.var_accessories_5_qty.get())
        output_dict["accessory_5_name"]  = str(self.selected_accessories_5.get())
        output_dict["accessory_6_qty"]   = str(self.var_accessories_6_qty.get())
        output_dict["accessory_6_name"]  = str(self.selected_accessories_6.get())
        output_dict["accessory_7_qty"]   = str(self.var_accessories_7_qty.get())
        output_dict["accessory_7_name"]  = str(self.selected_accessories_7.get())
        output_dict["accessory_8_qty"]   = str(self.var_accessories_8_qty.get())
        output_dict["accessory_8_name"]  = str(self.selected_accessories_8.get())
        output_dict["accessory_9_qty"]   = str(self.var_accessories_9_qty.get())
        output_dict["accessory_9_name"]  = str(self.selected_accessories_9.get())
        output_dict["accessory_10_qty"]  = str(self.var_accessories_10_qty.get())
        output_dict["accessory_10_name"] = str(self.selected_accessories_10.get())
        output_dict["accessory_11_qty"]  = str(self.var_accessories_11_qty.get())
        output_dict["accessory_11_name"] = str(self.selected_accessories_11.get())
        output_dict["accessory_12_qty"]  = str(self.var_accessories_12_qty.get())
        output_dict["accessory_12_name"] = str(self.selected_accessories_12.get())
        output_dict["accessory_13_qty"]  = str(self.var_accessories_13_qty.get())
        output_dict["accessory_13_name"] = str(self.selected_accessories_13.get())
        output_dict["accessory_14_qty"]  = str(self.var_accessories_14_qty.get())
        output_dict["accessory_14_name"] = str(self.selected_accessories_14.get())
        output_dict["accessory_15_qty"]  = str(self.var_accessories_15_qty.get())
        output_dict["accessory_15_name"] = str(self.selected_accessories_15.get())
        output_dict["accessory_16_qty"]  = str(self.var_accessories_16_qty.get())
        output_dict["accessory_16_name"] = str(self.selected_accessories_16.get())
        output_dict["accessory_17_qty"]  = str(self.var_accessories_17_qty.get())
        output_dict["accessory_17_name"] = str(self.selected_accessories_17.get())
        output_dict["accessory_18_qty"]  = str(self.var_accessories_18_qty.get())
        output_dict["accessory_18_name"] = str(self.selected_accessories_18.get())
        output_dict["accessory_19_qty"]  = str(self.var_accessories_19_qty.get())
        output_dict["accessory_19_name"] = str(self.selected_accessories_19.get())
        output_dict["accessory_20_qty"]  = str(self.var_accessories_20_qty.get())
        output_dict["accessory_20_name"] = str(self.selected_accessories_20.get())
        output_dict["accessory_21_qty"]  = str(self.var_accessories_21_qty.get())
        output_dict["accessory_21_name"] = str(self.selected_accessories_21.get())
        output_dict["accessory_22_qty"]  = str(self.var_accessories_22_qty.get())
        output_dict["accessory_22_name"] = str(self.selected_accessories_22.get())
        output_dict["accessory_23_qty"]  = str(self.var_accessories_23_qty.get())
        output_dict["accessory_23_name"] = str(self.selected_accessories_23.get())
        output_dict["accessory_24_qty"]  = str(self.var_accessories_24_qty.get())
        output_dict["accessory_24_name"] = str(self.selected_accessories_24.get())
        output_dict["accessory_25_qty"]  = str(self.var_accessories_25_qty.get())
        output_dict["accessory_25_name"] = str(self.selected_accessories_25.get())
        output_dict["accessory_26_qty"]  = str(self.var_accessories_26_qty.get())
        output_dict["accessory_26_name"] = str(self.selected_accessories_26.get())
        output_dict["accessory_27_qty"]  = str(self.var_accessories_27_qty.get())
        output_dict["accessory_27_name"] = str(self.selected_accessories_27.get())
        output_dict["accessory_28_qty"]  = str(self.var_accessories_28_qty.get())
        output_dict["accessory_28_name"] = str(self.selected_accessories_28.get())
        output_dict["accessory_29_qty"]  = str(self.var_accessories_29_qty.get())
        output_dict["accessory_29_name"] = str(self.selected_accessories_29.get())
        output_dict["accessory_30_qty"]  = str(self.var_accessories_30_qty.get())
        output_dict["accessory_30_name"] = str(self.selected_accessories_30.get())

        output_dict["ca_1_facing"] = str(self.selected_component_armor_facing_1.get())
        output_dict["ca_1_type"]   = str(self.selected_component_armor_1.get())
        output_dict["ca_1_dp"]     = str(self.var_component_armor_count_qty_1.get())
        output_dict["ca_2_facing"] = str(self.selected_component_armor_facing_2.get())
        output_dict["ca_2_type"]   = str(self.selected_component_armor_2.get())
        output_dict["ca_2_dp"]     = str(self.var_component_armor_count_qty_2.get())
        output_dict["ca_3_facing"] = str(self.selected_component_armor_facing_3.get())
        output_dict["ca_3_type"]   = str(self.selected_component_armor_3.get())
        output_dict["ca_3_dp"]     = str(self.var_component_armor_count_qty_3.get())
        output_dict["ca_4_facing"] = str(self.selected_component_armor_facing_4.get())
        output_dict["ca_4_type"]   = str(self.selected_component_armor_4.get())
        output_dict["ca_4_dp"]     = str(self.var_component_armor_count_qty_4.get())
        output_dict["ca_5_facing"] = str(self.selected_component_armor_facing_5.get())
        output_dict["ca_5_type"]   = str(self.selected_component_armor_5.get())
        output_dict["ca_5_dp"]     = str(self.var_component_armor_count_qty_5.get())
        output_dict["pe_name_1"]   = str(self.selected_personal_equipment_1.get())
        output_dict["pe_qty_1"]    = int(self.var_personal_equipment_1_qty.get())
        output_dict["pe_name_2"]   = str(self.selected_personal_equipment_2.get())
        output_dict["pe_qty_2"]    = int(self.var_personal_equipment_2_qty.get())
        output_dict["pe_name_3"]   = str(self.selected_personal_equipment_3.get())
        output_dict["pe_qty_3"]    = int(self.var_personal_equipment_3_qty.get())
        output_dict["pe_name_4"]   = str(self.selected_personal_equipment_4.get())
        output_dict["pe_qty_4"]    = int(self.var_personal_equipment_4_qty.get())
        output_dict["pe_name_5"]   = str(self.selected_personal_equipment_5.get())
        output_dict["pe_qty_5"]    = int(self.var_personal_equipment_5_qty.get())
        output_dict["pe_name_6"]   = str(self.selected_personal_equipment_6.get())
        output_dict["pe_qty_6"]    = int(self.var_personal_equipment_6_qty.get())
        output_dict["pe_name_7"]   = str(self.selected_personal_equipment_7.get())
        output_dict["pe_qty_7"]    = int(self.var_personal_equipment_7_qty.get())
        output_dict["pe_name_8"]   = str(self.selected_personal_equipment_8.get())
        output_dict["pe_qty_8"]    = int(self.var_personal_equipment_8_qty.get())
        output_dict["pe_name_9"]   = str(self.selected_personal_equipment_9.get())
        output_dict["pe_qty_9"]    = int(self.var_personal_equipment_9_qty.get())
        output_dict["pe_name_10"]   = str(self.selected_personal_equipment_10.get())
        output_dict["pe_qty_10"]    = int(self.var_personal_equipment_10_qty.get())

        # Insert inside menu_file_print() before self.make_pdf call
        output_dict["links"] = []
        for i in range(self.link_rows_count):
            chosen_items = self.link_selections[i]
            if chosen_items:
                output_dict["links"].append({
                    "link_index": i + 1,
                    "items": chosen_items  # This exports a python list: ["Weapon 1: Machine Gun (Front)", "Weapon 2: Machine Gun (Front)"]
                })

        self.make_pdf(input_dict=output_dict)

    def menu_file_exit(self, *args):
        response = messagebox.askquestion('Exit Application', 'Do you really want to exit?')
        if response == 'yes':
            self.root.quit()

    def menu_help_how_does_this_work(self, *args):
        display_info: str = "How Does This Work?\n"
        display_info += "Welcome to the Python Car Wars Designer tool.\n"
        display_info += "\n"
        display_info += "Using dropdown list boxes, select vehicle body, modifications, chassis and suspension.\n"
        display_info += "\n"
        display_info += "Select engine and modifications, tires, crew, armor selections and allocations,\n"
        display_info += "\n"
        display_info += "Select weapons, count, ammo, extra magazines and facings.\n"
        display_info += "\n"
        display_info += "Select accessories.  Commonly used ones are towards the top of the list.\n"
        display_info += "\n"
        display_info += "Select component armor.  Select number of spaces protected, armor count, and facing.\n"
        display_info += "\n"
        display_info += "Select rocket boosters.  Confirm the accelration value is correct.\n"
        display_info += "\n"
        display_info += "Select personal equipent.\n"
        display_info += "\n"
        display_info += "Use 'File New' to start over.\n"
        display_info += "\n"
        display_info += "Use 'File Save' to save your progress to the current file.\n"
        display_info += "\n"
        display_info += "Use 'File Save As' to save your progress to a new file.\n"

        messagebox.showinfo("How Does This Work?", display_info)

    def menu_help_about(self, *args):
        messagebox.showinfo("About", f"Python Designer {self.datestamp}")

    def menu_help_whats_new(self, *args):
        display_info: str = "What's New with the Python Designer:\n"
        display_info += "\n"
        display_info += "1) Weapon listings have had their ToHit and Damage values displayed.\n"
        display_info += "\n"
        display_info += "2) The 'grenade equivalent' setting for personal equipment has been installed.\n"
        display_info += "\n"
        display_info += "3) A declaration that a design is overweight has been added to the Design Validity section.\n"
        display_info += "\n"
        display_info += "4) A bug appeared in the formatting of decimal values.  A new function was installed to formalize how numbers were presented.\n"
        display_info += "\n"
        display_info += "5) Prices for ranged personal weapons with a cost per shot have been adjusted to presume they are fully loaded.\n"
        display_info += "\n"
        display_info += "6) Every Accessory that, by game law, has a maximum allowed quantity is now being checked and reported as an invalid design if the amount selected exceeds that maximum limit.\n"
        display_info += "\n"
        display_info += "7) Updates to data formatting and position placement have improved the UI experience.\n"
        display_info += "\n"
        display_info += "8) Off-Road tires should increase the HC by 1 if on all tires, when off-road.  That has been included now.\n"
        display_info += "\n"
        display_info += "8) A disconnect between weapon rows 3 and 4 has been resolved\n"
        display_info += "\n"
        display_info += "9) The File->Print menu option now generated a PDF file for the current status of a design.\n"
        display_info += "\n"
        display_info += "10) Vans over a certain weight lose one point of HC automatically.  Calculate for this.\n"
        display_info += "\n"
        messagebox.showinfo("What's New", display_info)

    def menu_help_whats_next(self, *args):
        display_info: str = "What's Next with the Python Designer:\n"
        display_info += "\n"
        display_info += "1) What is next?  Trucks?  Planes?  Boats?  What would you like to see?\n"
        display_info += "\n"
        messagebox.showinfo("What's Next", display_info)

    def load_record(self, path: str):
        file_input_list: list = []
        file_incoming_entry: str = ""
        with open(path, "r", encoding="UTF-8") as input_file:
            file_incoming_entry = input_file.readline()

        for index in range(1, self.weapon_rows_count + 1):
            # Safe initialization for the weapon name StringVar
            if not hasattr(self, f"selected_sub_weapon_{index}_canvas") or getattr(self, f"selected_sub_weapon_{index}_canvas") is None:
                setattr(self, f"selected_sub_weapon_{index}_canvas", tk.StringVar(value="Weapon"))
                
            # Safe initialization for the sub-weapon quantity IntVar
            if not hasattr(self, f"var_sub_weapon_{index}_qty") or getattr(self, f"var_sub_weapon_{index}_qty") is None:
                setattr(self, f"var_sub_weapon_{index}_qty", tk.IntVar(value=0))
            
            # Safe initialization for the ammunition quantity IntVar
            if not hasattr(self, f"var_sub_weapon_ammo_{index}_qty") or getattr(self, f"var_sub_weapon_ammo_{index}_qty") is None:
                setattr(self, f"var_sub_weapon_ammo_{index}_qty", tk.IntVar(value=0))


        string_of_dicts_cleaned = re.sub(r"'(?=[^:]*:)", '"', file_incoming_entry)
        string_of_dicts_cleaned = re.sub(r"(?<=:)'", '"', string_of_dicts_cleaned)
        file_input_list = json.loads(string_of_dicts_cleaned)

        dict_list = file_input_list[0]

        self.selected_body.set(                           dict_list['self.selected_body'])
        self.selected_modifications.set(                  dict_list['self.selected_modifications'])
        self.selected_chassis.set(                        dict_list['self.selected_chassis'])
        self.selected_suspension.set(                     dict_list['self.selected_suspension'])
        self.selected_engine.set(                         dict_list['self.selected_engine'])
        self.var_engine_gas_super_charger.set(            dict_list['self.var_engine_gas_super_charger'])
        self.var_engine_gas_vp_turbo.set(                 dict_list['self.var_engine_gas_vp_turbo'])
        self.var_engine_gas_tube_headers.set(             dict_list['self.var_engine_gas_tube_headers'])
        self.var_engine_gas_blue_print.set(               dict_list['self.var_engine_gas_blue_print'])
        self.var_engine_gas_turbo.set(                    dict_list['self.var_engine_gas_turbo'])
        self.var_engine_electric_super_conductors.set(    dict_list['self.var_engine_electric_super_conductors'])
        self.var_engine_electric_platnium_catalysts.set(  dict_list['self.var_engine_electric_platnium_catalysts'])
        self.var_engine_electric_extra_power_cells.set(   dict_list['self.var_engine_electric_extra_power_cells'])
        self.selected_gas_tank.set(                       dict_list['self.selected_gas_tank'])
        self.var_gas_gallon_qty.set(                      dict_list['self.var_gas_gallon_qty'])
        self.var_front_tire_qty.set(                      dict_list['self.var_front_tire_qty'])
        self.var_rear_tire_qty.set(                       dict_list['self.var_rear_tire_qty'])
        self.var_driver_gunner_qty.set(                   dict_list['self.var_driver_gunner_qty'])
        self.var_passenger_qty.set(                       dict_list['self.var_passenger_qty'])
        self.var_outer_armor_qty.set(                     dict_list['self.var_outer_armor_qty'])
        self.var_inner_armor_qty.set(                     dict_list['self.var_inner_armor_qty'])
        self.var_front_tire_steelbelting.set(             dict_list['self.var_front_tire_steelbelting'])
        self.var_front_tire_radial.set(                   dict_list['self.var_front_tire_radial'])
        self.var_front_tire_fireproof.set(                dict_list['self.var_front_tire_fireproof'])
        self.var_front_tire_offroad.set(                  dict_list['self.var_front_tire_offroad'])
        self.var_front_tire_racing_slick.set(             dict_list['self.var_front_tire_racing_slick'])
        self.var_rear_tire_steelbelting.set(              dict_list['self.var_rear_tire_steelbelting'])
        self.var_rear_tire_radial.set(                    dict_list['self.var_rear_tire_radial'])
        self.var_rear_tire_fireproof.set(                 dict_list['self.var_rear_tire_fireproof'])
        self.var_rear_tire_offroad.set(                   dict_list['self.var_rear_tire_offroad'])
        self.var_rear_tire_racing_slick.set(              dict_list['self.var_rear_tire_racing_slick'])
        self.selected_front_tire.set(                     dict_list['self.selected_front_tire'])
        self.selected_rear_tire.set(                      dict_list['self.selected_rear_tire'])
        self.selected_outer_armor.set(                    dict_list['self.selected_outer_armor'])
        self.selected_inner_armor.set(                    dict_list['self.selected_inner_armor'])

        # --- FIXED RESTORE WEAPONS WITH REBUILT INTERACTIVE DROPDOWNS ---
        # 1. ACTIVATE LOGICAL LOADING SAFEGUARDS
        self.is_loading = True

        for index in range(1, self.weapon_rows_count + 1):
            self.add_labels_buttons_weapon_row_unified(row_number = index, canvas_type=self.weapon_container_frame)

            # Update values for existing Tkinter variables using .set()
            getattr(self, f"selected_weapon_alt_{index}").set(dict_list[f"self.selected_weapon_alt_{index}"])
            selected_category: str = getattr(self, f"selected_weapon_alt_{index}").get()
            dropdown_list = self.get_weapon_sub_list(category=selected_category)

            self.add_dropdown_sub_weapon_unified(row_number = index, canvas_type=self.weapon_container_frame, dropdown_list=dropdown_list)

            #This canvas (aka self.selected_sub_weapon_1_canvas needs to exist first before a .set can be called on it
            getattr(self, f"selected_sub_weapon_{index}_canvas").set(dict_list[f"self.selected_sub_weapon_{index}_canvas"])
            
            # Reassign or load raw dictionary data directly into the attributes
            # --- FIXED PATHWAY FOR AMMO QUANTITY TRACKING VARIABLES ---
            # 1. Main Weapon/Ammo Quantity
            qty_var = getattr(self, f"var_sub_weapon_{index}_qty", None)
            if qty_var and hasattr(qty_var, "set"):
                qty_var.set(dict_list.get(f"self.var_sub_weapon_{index}_qty", 0))
            elif qty_var is None:
                # Fallback block if variable names use alternate tracking keys
                alt_qty_var = getattr(self, f"selected_weapon_qty_{index}", None)
                if alt_qty_var and hasattr(alt_qty_var, "set"):
                    alt_qty_var.set(dict_list.get(f"self.var_sub_weapon_{index}_qty", 0))

            # 2. Ammo Count Capacity / Reserve Settings (if tracked separately)
            ammo_var = getattr(self, f"var_sub_weapon_ammo_{index}_qty", None)
            if ammo_var and hasattr(ammo_var, "set"):
                ammo_var.set(dict_list.get(f"self.var_sub_weapon_ammo_{index}_qty", 0))
            #getattr(self, f"var_sub_weapon_{index}_qty").set(dict_list.get(f"self.var_sub_weapon_{index}_qty", 0))
            #getattr(self, f"var_sub_weapon_ammo_{index}_qty").set(dict_list.get(f"self.var_sub_weapon_ammo_{index}_qty", 0))

            tohit_widget = getattr(self, f"label_sub_weapon_{index}_tohit", None)
            if tohit_widget is not None:
                tohit_widget.configure(text=dict_list.get(f"self.label_sub_weapon_{index}_tohit", ""))            
            #setattr(self, f"label_sub_weapon_{index}_tohit", dict_list[f"self.label_sub_weapon_{index}_tohit"])
            
            damage_widget = getattr(self, f"label_sub_weapon_{index}_damage", None)
            if damage_widget is not None:
                damage_widget.configure(text=dict_list.get(f"self.label_sub_weapon_{index}_damage", ""))
            #setattr(self, f"label_sub_weapon_{index}_damage", dict_list[f"self.label_sub_weapon_{index}_damage"])

            #setattr(self, f"var_sub_weapon_ammo_{index}_qty", dict_list[f"self.var_sub_weapon_ammo_{index}_qty"])

            dp_widget = getattr(self, f"label_hidden_sub_weapon_{index}_dp", None)
            if dp_widget is not None:
                dp_widget.configure(text=dict_list.get(f"self.label_hidden_sub_weapon_{index}_dp", "0"))
            #setattr(self, f"label_hidden_sub_weapon_{index}_dp", dict_list[f"self.label_hidden_sub_weapon_{index}_dp"])

            # Dynamic lookup for extra magazine variable and dictionary states
            mag_var = getattr(self, f"var_sub_weapon_extra_mags_{index}_qty", None)
            if mag_var and hasattr(mag_var, "set"):
                mag_var.set(dict_list.get(f"self.var_sub_weapon_extra_mags_{index}_qty", 0))

            # --- Change this old fallback block inside your load_record loop: ---
            # if hasattr(self, "on_select_weapon_alt_unified_canvas"):
            #     self.on_select_weapon_alt_unified_canvas(index, self.second_frame)
            # elif hasattr(self, "on_weapon_select"):
            #     ...

            # --- To this explicit forced evaluation: ---
            self.update_weapon_row_statistics_forced(index)

        #self.selected_weapon_alt_1.set(dict_list["self.selected_weapon_alt_1"])
        #self.selected_sub_weapon_1_canvas.set(dict_list['self.selected_sub_weapon_1_canvas'])
        #self.var_sub_weapon_1_qty         = dict_list['self.var_sub_weapon_1_qty']
        #self.weapon_armor_facing_1        = dict_list['self.weapon_armor_facing_1']
        #self.label_sub_weapon_1_tohit     = dict_list['self.label_sub_weapon_1_tohit']
        #self.label_sub_weapon_1_damage    = dict_list['self.label_sub_weapon_1_damage']
        #self.var_sub_weapon_ammo_1_qty    = dict_list['self.var_sub_weapon_ammo_1_qty']
        #self.label_hidden_sub_weapon_1_dp = dict_list['self.label_hidden_sub_weapon_1_dp']
                    
        # 2. DEACTIVATE PROTECTION FLAG
        
        self.is_loading = False
        # =====================================================================
        # 2. CALCULATION SYNC PASS: Force your unified traces to process values
        # =====================================================================
        for index in range(1, self.weapon_rows_count + 1):
            # Check if an extra magazines text tracking variable exists
            mag_attr = f"var_sub_weapon_extra_mags_{index}_qty"
            if hasattr(self, mag_attr) and getattr(self, mag_attr) is not None:
                # Forcefully kick-run the calculations engine for this row
                if hasattr(self, "on_select_sub_weapon_unified"):
                    self.on_select_sub_weapon_unified(row_number=index)

        # --- RESTORE ACCESSORIES (1 to 30) ---
        for i in range(1, 31):
            attr_name = f"selected_accessories_{i}"
            key = f"self.{attr_name}"
            if key in dict_list and hasattr(self, attr_name) and getattr(self, attr_name):
                getattr(self, attr_name).set(dict_list[key])

        # --- RESTORE COMPONENT ARMOR (1 to 5) ---
        for i in range(1, 6):
            for suffix in ["", "_points"]:
                attr_name = f"selected_component_armor_{i}{suffix}"
                key = f"self.{attr_name}"
                if key in dict_list and hasattr(self, attr_name) and getattr(self, attr_name):
                    getattr(self, attr_name).set(dict_list[key])

        # --- RESTORE ROCKET BOOSTERS (1 to 5) ---
        for i in range(1, 6):
            qty_attr = f"var_rocket_booster_pounds_qty_{i}"
            face_attr = f"selected_rocket_booster_facing_{i}"
        
            if f"self.{qty_attr}" in dict_list and hasattr(self, qty_attr) and getattr(self, qty_attr):
                getattr(self, qty_attr).set(dict_list[f"self.{qty_attr}"])
            if f"self.{face_attr}" in dict_list and hasattr(self, face_attr) and getattr(self, face_attr):
                getattr(self, face_attr).set(dict_list[f"self.{face_attr}"])

        # --- RESTORE PERSONAL EQUIPMENT (1 to 10) ---
        for i in range(1, 11):
            for suffix in ["", "_qty"]:
                attr_name = f"selected_personal_equipment_{i}{suffix}"
                key = f"self.{attr_name}"
                if key in dict_list and hasattr(self, attr_name) and getattr(self, attr_name):
                    getattr(self, attr_name).set(dict_list[key])

        # --- RESTORE LINKS & BUMPER TRIGGERS (1 to 10) ---
        for i in range(self.link_rows_count):
            key = f"self.link_selections_{i}"
            if key in dict_list:
                raw_val = dict_list[key]
                self.link_selections[i] = raw_val.split("||") if raw_val else []
                self.link_entry_vars[i].set(", ".join(self.link_selections[i]) if self.link_selections[i] else "No items linked")

        for i in range(self.bt_rows_count):
            sel_key = f"self.bt_selections_{i}"
            face_key = f"self.selected_bt_facing_{i}"
        
            if face_key in dict_list:
                self.selected_bt_facing[i].set(dict_list[face_key])
            if sel_key in dict_list:
                raw_val = dict_list[sel_key]
                self.bt_selections[i] = raw_val.split("||") if raw_val else []
            self.bt_entry_vars[i].set(", ".join(self.bt_selections[i]) if self.bt_selections[i] else "No items linked")

        self.var_six_wheel_chassis.set(                   dict_list['self.var_six_wheel_chassis'])
        self.var_sloped_armor.set(                        dict_list['self.var_sloped_armor'])
        self.var_outer_front_armor_allocation_qty.set(    dict_list['self.var_outer_front_armor_allocation_qty'])
        self.var_outer_back_armor_allocation_qty.set(     dict_list['self.var_outer_back_armor_allocation_qty'])
        self.var_outer_left_armor_allocation_qty.set(     dict_list['self.var_outer_left_armor_allocation_qty'])
        self.var_outer_right_armor_allocation_qty.set(    dict_list['self.var_outer_right_armor_allocation_qty'])
        self.var_outer_top_armor_allocation_qty.set(      dict_list['self.var_outer_top_armor_allocation_qty'])
        self.var_outer_underbody_armor_allocation_qty.set(dict_list['self.var_outer_underbody_armor_allocation_qty'])
        self.var_inner_front_armor_allocation_qty.set(    dict_list['self.var_inner_front_armor_allocation_qty'])
        self.var_inner_back_armor_allocation_qty.set(     dict_list['self.var_inner_back_armor_allocation_qty'])
        self.var_inner_left_armor_allocation_qty.set(     dict_list['self.var_inner_left_armor_allocation_qty'])
        self.var_inner_right_armor_allocation_qty.set(    dict_list['self.var_inner_right_armor_allocation_qty'])
        self.var_inner_top_armor_allocation_qty.set(      dict_list['self.var_inner_top_armor_allocation_qty'])
        self.var_inner_underbody_armor_allocation_qty.set(dict_list['self.var_inner_underbody_armor_allocation_qty'])
        
        self.is_init = False
        self.is_loading = False
        
        # Run a synchronous screen refresh pass
        self.root.update_idletasks()
        self.recalculate()

    def save_record(self, path: str):
        file_output_list = []
        entry_dict: dict = {}
        entry_dict["total_cost"]                                    = self.label_total_cost.cget("text") #This value needs to be saved to identify uploaded files to the webserver
        entry_dict["top_speed"]                                     = self.label_top_speed.cget("text")
        entry_dict["accel"]                                         = self.label_accel.cget("text")
        entry_dict["max_accel"]                                     = self.label_max_accel.cget("text")
        entry_dict["hc"]                                            = self.label_hc.cget("text")
        entry_dict["max_hc"]                                        = self.label_max_hc.cget("text")
        entry_dict["front_tire_dp"]                                 = self.label_front_tire_dp.cget("text")
        entry_dict["rear_tire_dp"]                                  = self.label_rear_tire_dp.cget("text")
        entry_dict["engine_dp"]                                     = self.label_engine_dp.cget("text")
        entry_dict["gas_tank_dp"]                                   = self.label_gas_tank_dp.cget("text")
        entry_dict["self.selected_body"]                            = self.selected_body.get()
        entry_dict["self.selected_modifications"]                   = self.selected_modifications.get()
        entry_dict["self.selected_chassis"]                         = self.selected_chassis.get()
        entry_dict["self.selected_suspension"]                      = self.selected_suspension.get()
        entry_dict["self.selected_engine"]                          = self.selected_engine.get()
        entry_dict["self.var_engine_gas_super_charger"]             = self.var_engine_gas_super_charger.get()
        entry_dict["self.var_engine_gas_vp_turbo"]                  = self.var_engine_gas_vp_turbo.get()
        entry_dict["self.var_engine_gas_tube_headers"]              = self.var_engine_gas_tube_headers.get()
        entry_dict["self.var_engine_gas_blue_print"]                = self.var_engine_gas_blue_print.get()
        entry_dict["self.var_engine_gas_turbo"]                     = self.var_engine_gas_turbo.get()
        entry_dict["self.var_engine_electric_super_conductors"]     = self.var_engine_electric_super_conductors.get()
        entry_dict["self.var_engine_electric_platnium_catalysts"]   = self.var_engine_electric_platnium_catalysts.get()
        entry_dict["self.var_engine_electric_extra_power_cells"]    = self.var_engine_electric_extra_power_cells.get()
        entry_dict["self.selected_gas_tank"]                        = self.selected_gas_tank.get()
        entry_dict["self.var_gas_gallon_qty"]                       = self.var_gas_gallon_qty.get()
        entry_dict["self.var_front_tire_qty"]                       = self.var_front_tire_qty.get()
        entry_dict["self.var_rear_tire_qty"]                        = self.var_rear_tire_qty.get()
        entry_dict["self.var_driver_gunner_qty"]                    = self.var_driver_gunner_qty.get()
        entry_dict["self.var_passenger_qty"]                        = self.var_passenger_qty.get()
        entry_dict["self.var_outer_armor_qty"]                      = self.var_outer_armor_qty.get()
        entry_dict["self.var_inner_armor_qty"]                      = self.var_inner_armor_qty.get()
        entry_dict["self.var_front_tire_steelbelting"]              = self.var_front_tire_steelbelting.get()
        entry_dict["self.var_front_tire_radial"]                    = self.var_front_tire_radial.get()
        entry_dict["self.var_front_tire_fireproof"]                 = self.var_front_tire_fireproof.get()
        entry_dict["self.var_front_tire_offroad"]                   = self.var_front_tire_offroad.get()
        entry_dict["self.var_front_tire_racing_slick"]              = self.var_front_tire_racing_slick.get()
        entry_dict["self.var_rear_tire_steelbelting"]               = self.var_rear_tire_steelbelting.get()
        entry_dict["self.var_rear_tire_radial"]                     = self.var_rear_tire_radial.get()
        entry_dict["self.var_rear_tire_fireproof"]                  = self.var_rear_tire_fireproof.get()
        entry_dict["self.var_rear_tire_offroad"]                    = self.var_rear_tire_offroad.get()
        entry_dict["self.var_rear_tire_racing_slick"]               = self.var_rear_tire_racing_slick.get()
        entry_dict["self.selected_front_tire"]                      = self.selected_front_tire.get()
        entry_dict["self.selected_rear_tire"]                       = self.selected_rear_tire.get()
        entry_dict["self.selected_outer_armor"]                     = self.selected_outer_armor.get()
        entry_dict["self.selected_inner_armor"]                     = self.selected_inner_armor.get()

        # =====================================================================
        # EXPLICIT RESTORATION: WEAPON ROW 1 ONLY (ZERO LOOP DISCONNECTS)
        # =====================================================================
        for index in range(1, self.weapon_rows_count + 1):
            entry_dict[f"self.selected_weapon_alt_{index}"] = getattr(self, f"selected_weapon_alt_{index}").get()
            entry_dict[f"self.var_sub_weapon_{index}_qty"] = getattr(self, f"var_sub_weapon_{index}_qty").get()
            
            # Verify the sub-weapon canvas object wrapper has drawn before extracting text values
            canvas_attr = getattr(self, f"selected_sub_weapon_{index}_canvas", None)
            if canvas_attr is not None:
                if hasattr(canvas_attr, "get"):
                    entry_dict[f"self.selected_sub_weapon_{index}_canvas"] = canvas_attr.get()
                else:
                    entry_dict[f"self.selected_sub_weapon_{index}_canvas"] = str(canvas_attr)
            else:
                entry_dict[f"self.selected_sub_weapon_{index}_canvas"] = "None"
                
            # Target the explicit facing layout variable tracker assigned on Page 1
            entry_dict[f"self.weapon_armor_facing_{index}"] = getattr(self, f"weapon_armor_facing_{index}").get()
            
            # Save static text stats for formatting parity checks
            entry_dict[f"self.label_sub_weapon_{index}_tohit"] = getattr(self, f"label_sub_weapon_{index}_tohit").cget("text")
            entry_dict[f"self.label_sub_weapon_{index}_damage"] = getattr(self, f"label_sub_weapon_{index}_damage").cget("text")
            try:
                entry_dict[f"self.var_sub_weapon_ammo_{index}_qty"] = getattr(self, f"var_sub_weapon_ammo_{index}_qty").get()
            except tk.TclError:
                entry_dict[f"self.var_sub_weapon_ammo_{index}_qty"] = 0
            entry_dict[f"self.label_hidden_sub_weapon_{index}_dp"] = getattr(self, f"label_hidden_sub_weapon_{index}_dp").cget("text")

            # 🎯 ADD THIS CRITICAL LINE TO SAVE EXTRA MAGS:
            mag_attr = f"var_sub_weapon_extra_mags_{index}_qty"
            if hasattr(self, mag_attr) and getattr(self, mag_attr) is not None:
                try:
                    entry_dict[f"self.{mag_attr}"] = getattr(self, mag_attr).get()
                except (tk.TclError, ValueError):
                    entry_dict[f"self.{mag_attr}"] = 0
            else:
                entry_dict[f"self.{mag_attr}"] = 0

        #entry_dict["self.selected_weapon_alt_1"] = self.selected_weapon_alt_1.get()
        #entry_dict["self.var_sub_weapon_1_qty"] = self.var_sub_weapon_1_qty.get()
        
        # Verify the sub-weapon canvas object wrapper has drawn before extracting text values
        #if self.selected_sub_weapon_1_canvas is not None:
        #    if hasattr(self.selected_sub_weapon_1_canvas, "get"):
        #        entry_dict["self.selected_sub_weapon_1_canvas"] = self.selected_sub_weapon_1_canvas.get()
        #    else:
        #        entry_dict["self.selected_sub_weapon_1_canvas"] = str(self.selected_sub_weapon_1_canvas)
        #else:
        #    entry_dict["self.selected_sub_weapon_1_canvas"] = "None"
            
        # Target the explicit facing layout variable tracker assigned on Page 1
        #entry_dict["self.weapon_armor_facing_1"] = self.weapon_armor_facing_1.get()
        
        # Save static text stats for formatting parity checks
        #entry_dict["self.label_sub_weapon_1_tohit"] = self.label_sub_weapon_1_tohit.cget("text")
        #entry_dict["self.label_sub_weapon_1_damage"] = self.label_sub_weapon_1_damage.cget("text")
        #entry_dict["self.var_sub_weapon_ammo_1_qty"] = self.var_sub_weapon_ammo_1_qty.get()
        #entry_dict["self.label_hidden_sub_weapon_1_dp"] = self.label_hidden_sub_weapon_1_dp.cget("text")
                
        # --- ACCESSORIES (1 to 30) ---
        for i in range(1, 31):
            # FIX: Corrected variable lookup syntax, and targeting both names AND our updated unified quantity integer variables
            for suffix in ["", "_qty"]:
                attr_name = f"selected_accessories_{i}" if suffix == "" else f"var_accessories_{i}_qty"
                if hasattr(self, attr_name) and getattr(self, attr_name):
                    entry_dict[f"self.{attr_name}"] = getattr(self, attr_name).get()

        # --- COMPONENT ARMOR (1 to 5) ---
        for i in range(1, 6):
            for suffix in ["", "_points"]:
                attr_name = f"selected_component_armor_{i}{suffix}"
                if hasattr(self, attr_name) and getattr(self, attr_name):
                    entry_dict[f"self.{attr_name}"] = getattr(self, attr_name).get()

        # --- ROCKET BOOSTERS (1 to 5) ---
        for i in range(1, 6):
            qty_attr = f"var_rocket_booster_pounds_qty_{i}"
            face_attr = f"selected_rocket_booster_facing_{i}"
            if hasattr(self, qty_attr) and getattr(self, qty_attr):
                entry_dict[f"self.{qty_attr}"] = getattr(self, qty_attr).get()
            if hasattr(self, face_attr) and getattr(self, face_attr):
                entry_dict[f"self.{face_attr}"] = getattr(self, face_attr).get()

        # --- PERSONAL EQUIPMENT (1 to 10) ---
        for i in range(1, 11):
            for suffix in ["", "_qty"]:
                attr_name = f"selected_personal_equipment_{i}{suffix}"
                if hasattr(self, attr_name) and getattr(self, attr_name):
                    entry_dict[f"self.{attr_name}"] = getattr(self, attr_name).get()

        # --- LINKS & BUMPER TRIGGERS (1 to 10) ---
        for i in range(self.link_rows_count):
            entry_dict[f"self.link_selections_{i}"] = "||".join(self.link_selections[i])
        
        for i in range(self.bt_rows_count):
            entry_dict[f"self.bt_selections_{i}"] = "||".join(self.bt_selections[i])
            entry_dict[f"self.selected_bt_facing_{i}"] = self.selected_bt_facing[i].get()

        # -------------------------------------            
        entry_dict["self.var_six_wheel_chassis"]                    = self.var_six_wheel_chassis.get()
        entry_dict["self.var_sloped_armor"]                         = self.var_sloped_armor.get()
        entry_dict["self.var_outer_front_armor_allocation_qty"]     = self.var_outer_front_armor_allocation_qty.get()
        entry_dict["self.var_outer_back_armor_allocation_qty"]      = self.var_outer_back_armor_allocation_qty.get()
        entry_dict["self.var_outer_left_armor_allocation_qty"]      = self.var_outer_left_armor_allocation_qty.get()
        entry_dict["self.var_outer_right_armor_allocation_qty"]     = self.var_outer_right_armor_allocation_qty.get()
        entry_dict["self.var_outer_top_armor_allocation_qty"]       = self.var_outer_top_armor_allocation_qty.get()
        entry_dict["self.var_outer_underbody_armor_allocation_qty"] = self.var_outer_underbody_armor_allocation_qty.get()
        entry_dict["self.var_inner_front_armor_allocation_qty"]     = self.var_inner_front_armor_allocation_qty.get()
        entry_dict["self.var_inner_back_armor_allocation_qty"]      = self.var_inner_back_armor_allocation_qty.get()
        entry_dict["self.var_inner_left_armor_allocation_qty"]      = self.var_inner_left_armor_allocation_qty.get()
        entry_dict["self.var_inner_right_armor_allocation_qty"]     = self.var_inner_right_armor_allocation_qty.get()
        entry_dict["self.var_inner_top_armor_allocation_qty"]       = self.var_inner_top_armor_allocation_qty.get()
        entry_dict["self.var_inner_underbody_armor_allocation_qty"] = self.var_inner_underbody_armor_allocation_qty.get()
        file_output_list.append(entry_dict)
        with open(self.current_file_path, "w", encoding="UTF-8") as output_file:
            output_file.write(str(file_output_list))

    def add_labels_canvas(self, canvas_type):
        tk.Label(canvas_type, text="Python Car Wars Designer", anchor="w").grid(row = self.grid_row_form_total, column = self.grid_col_item, sticky="w")
        tk.Label(canvas_type, text="Total:", anchor="w").grid(row = self.grid_row_form_total, column = self.grid_col_qty, sticky="w", columnspan=3)
        self.label_total_cost          = tk.Label(canvas_type, text="0", anchor="w")
        self.label_total_cost.grid(row=self.grid_row_form_header, column=self.grid_col_cost, sticky="w")
        self.label_total_weight        = tk.Label(canvas_type, text="0", anchor="w")
        self.label_total_weight.grid(row=self.grid_row_form_header, column=self.grid_col_weight, sticky="w")
        self.label_total_space         = tk.Label(canvas_type, text="0", anchor="w")
        self.label_total_space.grid(row=self.grid_row_form_header, column=self.grid_col_spaces, sticky="w")
        self.label_max_weight          = tk.Label(canvas_type, text="0", anchor="w")
        self.label_max_weight.grid(row=self.grid_row_form_header, column=self.grid_col_max_weight, sticky="w")
        self.label_total_power_factors = tk.Label(canvas_type, text="0", anchor="w")
        self.label_total_power_factors.grid(row=self.grid_row_form_header, column=self.grid_col_power_factors, sticky="w")
        self.label_final_engine_mpg    = tk.Label(canvas_type, text="0", anchor="w")
        self.label_final_engine_mpg.grid(row=self.grid_row_form_header, column=self.grid_col_base_mpg, sticky="w")

        tk.Label(canvas_type, text="Design Validity",                   anchor="w").grid(column=self.grid_col_item,                 row=self.grid_row_red_alert,                 sticky="w")
        tk.Label(canvas_type, text="Item",                              anchor="w").grid(column=self.grid_col_item,                 row=self.grid_row_form_header,               sticky="w")
        tk.Label(canvas_type, text="Qty",                               anchor="w").grid(column=self.grid_col_qty,                  row=self.grid_row_form_header,               sticky="w")
        tk.Label(canvas_type, text="Cost",                              anchor="w").grid(column=self.grid_col_cost,                 row=self.grid_row_form_total,                sticky="w")
        tk.Label(canvas_type, text="Weight",                            anchor="w").grid(column=self.grid_col_weight,               row=self.grid_row_form_total,                sticky="w")
        tk.Label(canvas_type, text="Spaces",                            anchor="w").grid(column=self.grid_col_spaces,               row=self.grid_row_form_total,                sticky="w", columnspan=2)
        tk.Label(canvas_type, text="DP",                                anchor="w").grid(column=self.grid_col_dp,                   row=self.grid_row_form_total,                sticky="w")
        tk.Label(canvas_type, text="Max Weight: ",                      anchor="w").grid(column=self.grid_col_max_weight,           row=self.grid_row_form_total,                sticky="w")
        tk.Label(canvas_type, text="Power Factors",                     anchor="w").grid(column=self.grid_col_power_factors,        row=self.grid_row_form_total,                sticky="w")
        tk.Label(canvas_type, text="Base MPG",                          anchor="w").grid(column=self.grid_col_base_mpg,             row=self.grid_row_form_total,                sticky="w")
        tk.Label(canvas_type, text="Range",                             anchor="w").grid(column=self.grid_col_base_mpg,             row=self.grid_row_body_modification,         sticky="w")
        tk.Label(canvas_type, text="Test Track",                        anchor="w").grid(column=self.grid_col_test_track,           row=self.grid_row_form_total,                sticky="w")
        tk.Label(canvas_type, text="Top Speed",                         anchor="w").grid(column=self.grid_col_test_track,           row=self.grid_row_form_header,               sticky="w")
        tk.Label(canvas_type, text="Acceleration",                      anchor="w").grid(column=self.grid_col_test_track,           row=self.grid_row_body,                      sticky="w")
        tk.Label(canvas_type, text="HC",                                anchor="w").grid(column=self.grid_col_test_track,           row=self.grid_row_body_modification,         sticky="w")
        tk.Label(canvas_type, text="Fully Loaded",                      anchor="w").grid(column=self.grid_col_test_track,           row=self.grid_row_chassis,                   sticky="w")
        tk.Label(canvas_type, text="Top Speed",                         anchor="w").grid(column=self.grid_col_test_track,           row=self.grid_row_suspension,                sticky="w")
        tk.Label(canvas_type, text="Acceleration",                      anchor="w").grid(column=self.grid_col_test_track,           row=self.grid_row_engine,                    sticky="w")
        tk.Label(canvas_type, text="HC",                                anchor="w").grid(column=self.grid_col_test_track,           row=self.grid_row_engine_mods_header,        sticky="w")
        tk.Label(canvas_type, text="Crew",                              anchor="w").grid(column=self.grid_col_item,                 row=self.grid_row_crew_header,               sticky="w")
        tk.Label(canvas_type, text="Crew: Driver/Gunners : Passengers", anchor="w").grid(column=self.grid_col_item,                 row=self.grid_row_crew_header,               sticky="w")
        #tk.Label(canvas_type, text="Accessories",                       anchor="w").grid(column=self.grid_col_item,                 row=self.grid_row_accessories_header,        sticky="w")
        #tk.Label(canvas_type, text="Notes",                             anchor="w").grid(column=self.grid_col_max_weight,           row=self.grid_row_accessories_header,        sticky="w")
        #tk.Label(canvas_type, text="Component Armor",                   anchor="w").grid(column=self.grid_col_item,                 row=self.grid_row_component_header,          sticky="w")
        #tk.Label(canvas_type, text="Spaces",                            anchor="w").grid(column=self.grid_col_qty,                  row=self.grid_row_component_header,          sticky="w", columnspan=3)
        #tk.Label(canvas_type, text="Pts",                               anchor="w").grid(column=self.grid_right_qty,                row=self.grid_row_component_header,          sticky="w")
        #tk.Label(canvas_type, text="Armor Location",                    anchor="w").grid(column=self.grid_col_max_weight,           row=self.grid_row_component_header,          sticky="w")
        #tk.Label(canvas_type, text="Rocker Boosters",                   anchor="w").grid(column=self.grid_col_item,                 row=self.grid_row_rocket_booster_header,     sticky="w")
        #tk.Label(canvas_type, text="Lbs",                               anchor="w").grid(column=self.grid_col_qty,                  row=self.grid_row_rocket_booster_header,     sticky="w")
        #tk.Label(canvas_type, text="Facing",                            anchor="w").grid(column=self.grid_col_max_weight,           row=self.grid_row_rocket_booster_header,     sticky="w")
        #tk.Label(canvas_type, text="Thrust MPH",                        anchor="w").grid(column=self.grid_col_power_factors,        row=self.grid_row_rocket_booster_header,     sticky="w")
        tk.Label(canvas_type, text="Unassigned:",                       anchor="w").grid(column=self.grid_col_spaces,               row=self.grid_row_armor_header,               sticky="w")
        tk.Label(canvas_type, text="Front:",                            anchor="w").grid(column=self.grid_col_dp,                   row=self.grid_row_armor_header,               sticky="w")
        tk.Label(canvas_type, text="Back:",                             anchor="w").grid(column=self.grid_col_max_weight,           row=self.grid_row_armor_header,               sticky="w")
        tk.Label(canvas_type, text="Left:",                             anchor="w").grid(column=self.grid_col_power_factors,        row=self.grid_row_armor_header,               sticky="w")
        tk.Label(canvas_type, text="Right:",                            anchor="w").grid(column=self.grid_col_base_mpg,             row=self.grid_row_armor_header,               sticky="w")
        tk.Label(canvas_type, text="Top:",                              anchor="w").grid(column=self.grid_col_test_track,           row=self.grid_row_armor_header,               sticky="w")
        tk.Label(canvas_type, text="Underbody:",                        anchor="w").grid(column=self.grid_col_test_track_numbers,   row=self.grid_row_armor_header,               sticky="w")
        #tk.Label(canvas_type, text="Personal Equipment",                anchor="w").grid(column=self.grid_col_item,                 row=self.grid_row_personal_equipment_header, sticky="w")
        #tk.Label(canvas_type, text="Qty",                               anchor="w").grid(column=self.grid_col_qty,                  row=self.grid_row_personal_equipment_header, sticky="w")
        #tk.Label(canvas_type, text="Cost",                              anchor="w").grid(column=self.grid_col_cost,                 row=self.grid_row_personal_equipment_header, sticky="w")
        #tk.Label(canvas_type, text="Weight",                            anchor="w").grid(column=self.grid_col_weight,               row=self.grid_row_personal_equipment_header, sticky="w")
        #tk.Label(canvas_type, text="GE",                                anchor="w").grid(column=self.grid_col_spaces,               row=self.grid_row_personal_equipment_header, sticky="w")
        #tk.Label(canvas_type, text="To-Hit",                            anchor="w").grid(column=self.grid_col_dp,                   row=self.grid_row_personal_equipment_header, sticky="w")
        #tk.Label(canvas_type, text="Damage",                            anchor="w").grid(column=self.grid_col_max_weight,           row=self.grid_row_personal_equipment_header, sticky="w")
        #tk.Label(canvas_type, text="Shots",                             anchor="w").grid(column=self.grid_col_power_factors,        row=self.grid_row_personal_equipment_header, sticky="w")
        #tk.Label(canvas_type, text="CPS",                               anchor="w").grid(column=self.grid_col_base_mpg,             row=self.grid_row_personal_equipment_header, sticky="w")
        #tk.Label(canvas_type, text="WPS",                               anchor="w").grid(column=self.grid_col_test_track,           row=self.grid_row_personal_equipment_header, sticky="w")
        #tk.Label(canvas_type, text="Notes",                             anchor="w").grid(column=self.grid_col_test_track_numbers,   row=self.grid_row_personal_equipment_header, sticky="w")

        self.label_body_selected = tk.Label(canvas_type, text="0", anchor="w")
        self.label_body_cost = tk.Label(canvas_type, text="0", anchor="w")
        self.label_body_cost.grid(column=self.grid_col_cost, row=self.grid_row_body, sticky="w")
        self.label_body_weight = tk.Label(canvas_type, text="0", anchor="w")
        self.label_body_weight.grid(column=self.grid_col_weight , row=self.grid_row_body, sticky="w")
        self.label_body_spaces = tk.Label(canvas_type, text="0", anchor="w")
        self.label_body_spaces.grid(column=self.grid_col_spaces, row=self.grid_row_body, sticky="w")
        self.label_hidden_cargo_spaces = tk.Label(canvas_type, text="0", anchor="w")

        self.label_body_max_weight = tk.Label(canvas_type, text="0", anchor="w")
        #self.label_body_max_weight.grid(column=self.grid_col_dp, row=self.grid_row_form_total, sticky="w")
        self.hidden_body_cycle = tk.Label(canvas_type, text="0", anchor="w")
        self.label_hidden_body_armor_cost = tk.Label(canvas_type, text="0", anchor="w")
        self.label_hidden_body_armor_weight = tk.Label(canvas_type, text="0", anchor="w")
        self.label_hidden_body_hc = tk.Label(canvas_type, text="0", anchor="w")

        self.label_modificiation_cost = tk.Label(canvas_type, text="0", anchor="w")
        self.label_modificiation_cost.grid(column=self.grid_col_cost,row=self.grid_row_body_modification, sticky="w")
        self.label_modificiation_weight = tk.Label(canvas_type, text="0", anchor="w")
        self.label_modificiation_weight.grid(column=self.grid_col_weight ,row=self.grid_row_body_modification, sticky="w")
        self.label_modificiation_space = tk.Label(canvas_type, text="0", anchor="w")
        self.label_modificiation_space.grid(column=self.grid_col_spaces,row=self.grid_row_body_modification, sticky="w")
        self.label_hidden_modification_cargo_space = tk.Label(canvas_type, text="0", anchor="w")

        self.var_six_wheel_chassis = tk.IntVar(value=0)
        self.check_six_wheel_chassis = tk.Checkbutton(canvas_type, text="Six Wheel Chassis", variable=self.var_six_wheel_chassis, command=self.var_six_wheel_chassis_changed, anchor="w")
        self.check_six_wheel_chassis.grid(column=self.grid_col_qty,row=self.grid_row_chassis, sticky="w", columnspan=6)

        self.var_sloped_armor = tk.IntVar(value=0)
        self.check_sloped_armor = tk.Checkbutton(canvas_type, text="Sloped Armor", variable=self.var_sloped_armor, command=self.var_sloped_armor_changed, anchor="w")
        self.check_sloped_armor.grid(column=self.grid_col_item,row=self.grid_row_sloped_armor, sticky="w")

        self.label_chassis_cost = tk.Label(canvas_type, text="0", anchor="w")
        self.label_chassis_cost.grid(column=self.grid_col_cost, row=self.grid_row_chassis, sticky="w")

        self.label_suspension_cost = tk.Label(canvas_type, text="0", anchor="w")
        self.label_suspension_cost.grid(column=self.grid_col_cost, row=self.grid_row_suspension, sticky="w")

        self.label_engine_cost = tk.Label(canvas_type, text="0", anchor="w")
        self.label_engine_cost.grid(column=self.grid_col_cost,row=self.grid_row_engine, sticky="w")
        self.label_engine_weight = tk.Label(canvas_type, text="0", anchor="w")
        self.label_engine_weight.grid(column=self.grid_col_weight ,row=self.grid_row_engine, sticky="w")
        self.label_engine_space = tk.Label(canvas_type, text="0", anchor="w")
        self.label_engine_space.grid(column=self.grid_col_spaces,row=self.grid_row_engine, sticky="w")
        self.label_engine_dp = tk.Label(canvas_type, text="0", anchor="w")
        self.label_engine_dp.grid(column=self.grid_col_dp,row=self.grid_row_engine, sticky="w")
        self.label_engine_pf = tk.Label(canvas_type, text="0", anchor="w")
        self.label_engine_pf.grid(column=self.grid_col_power_factors,row=self.grid_row_engine, sticky="w")
        self.label_engine_mpg = tk.Label(canvas_type, text="0", anchor="w")
        self.label_engine_mpg.grid(column=self.grid_col_base_mpg,row=self.grid_row_engine, sticky="w")
        self.label_engine_type = tk.Label(canvas_type, text="0", anchor="w")
        self.label_range = tk.Label(canvas_type, text="0", anchor="w")
        self.label_range.grid(column=self.grid_col_base_mpg, row=self.grid_row_chassis, sticky="w")
        self.label_top_speed = tk.Label(canvas_type, text="0", anchor="w")
        self.label_top_speed.grid(column=self.grid_col_test_track_numbers, row=self.grid_row_form_header, sticky="w")
        self.label_accel = tk.Label(canvas_type, text="0", anchor="w")
        self.label_accel.grid(column=self.grid_col_test_track_numbers, row=self.grid_row_body, sticky="w")
        self.label_hc = tk.Label(canvas_type, text="0", anchor="w")
        self.label_hc.grid(column=self.grid_col_test_track_numbers, row=self.grid_row_body_modification, sticky="w")
        self.label_max_weight_top_speed = tk.Label(canvas_type, text="0", anchor="w")
        self.label_max_weight_top_speed.grid(column=self.grid_col_test_track_numbers, row=self.grid_row_suspension, sticky="w")
        self.label_max_accel = tk.Label(canvas_type, text="0", anchor="w")
        self.label_max_accel.grid(column=self.grid_col_test_track_numbers, row=self.grid_row_engine, sticky="w")
        self.label_max_hc = tk.Label(canvas_type, text="0", anchor="w")
        self.label_max_hc.grid(column=self.grid_col_test_track_numbers, row=self.grid_row_engine_mods_header, sticky="w")

        tk.Label(canvas_type, text="Engine Modifications", anchor="w").grid(column=self.grid_col_item, row=self.grid_row_engine_mods_header, sticky="w") # Place the label in the window

        self.label_gas_header = tk.Label(canvas_type, text="Gas", anchor="w")
        self.label_gas_header.grid(column=self.grid_col_item, row=self.grid_row_gas_engine_mods, sticky="w") # Place the label in the window

        self.var_engine_gas_super_charger = tk.IntVar(value=0)
        self.check_engine_gas_super_charger = tk.Checkbutton(canvas_type, text="Super Charger", variable=self.var_engine_gas_super_charger, command=self.var_engine_gas_super_charger_changed, anchor="w")
        self.check_engine_gas_super_charger.grid(column=self.grid_col_qty,row=self.grid_row_gas_engine_mods, sticky="w", columnspan=6)
        self.check_engine_gas_super_charger.config(state="disabled")

        self.var_engine_gas_vp_turbo = tk.IntVar(value=0)
        self.check_engine_gas_vp_turbo = tk.Checkbutton(canvas_type, text="VP Turbo", variable=self.var_engine_gas_vp_turbo, command=self.var_engine_gas_vp_turbo_changed, anchor="w")
        self.check_engine_gas_vp_turbo.grid(column=self.grid_col_cost,row=self.grid_row_gas_engine_mods, sticky="w", columnspan=6)
        self.check_engine_gas_vp_turbo.config(state="disabled")

        self.var_engine_gas_tube_headers = tk.IntVar(value=0)
        self.check_engine_gas_tube_headers = tk.Checkbutton(canvas_type, text="Tube Headers", variable=self.var_engine_gas_tube_headers, command=self.var_engine_gas_tube_headers_changed, anchor="w")
        self.check_engine_gas_tube_headers.grid(column=self.grid_col_dp,row=self.grid_row_gas_engine_mods, sticky="w", columnspan=3)
        self.check_engine_gas_tube_headers.config(state="disabled")

        self.var_engine_gas_blue_print = tk.IntVar(value=0)
        self.check_engine_gas_blue_print = tk.Checkbutton(canvas_type, text="Blue Print", variable=self.var_engine_gas_blue_print, command=self.var_engine_gas_blue_print_changed, anchor="w")
        self.check_engine_gas_blue_print.grid(column=self.grid_col_power_factors,row=self.grid_row_gas_engine_mods, sticky="w")
        self.check_engine_gas_blue_print.config(state="disabled")

        self.var_engine_gas_turbo = tk.IntVar(value=0)
        self.check_engine_gas_turbo = tk.Checkbutton(canvas_type, text="Turbo", variable=self.var_engine_gas_turbo, command=self.var_engine_gas_turbo_changed, anchor="w")
        self.check_engine_gas_turbo.grid(column=self.grid_col_base_mpg,row=self.grid_row_gas_engine_mods, sticky="w")
        self.check_engine_gas_turbo.config(state="disabled")

        self.label_electric_header = tk.Label(canvas_type, text="Electric")
        self.label_electric_header.grid(column=self.grid_col_item, row=self.grid_row_electric_mods, sticky="w")

        self.var_engine_electric_super_conductors = tk.IntVar(value=0)
        self.check_engine_electric_super_conductors = tk.Checkbutton(canvas_type, text="Super Conductors", variable=self.var_engine_electric_super_conductors, command=self.recalculate, anchor="w")
        self.check_engine_electric_super_conductors.grid(column=self.grid_col_qty,row=self.grid_row_electric_mods, sticky="w", columnspan=6)
        self.check_engine_electric_super_conductors.config(state="disabled")

        self.var_engine_electric_platnium_catalysts = tk.IntVar(value=0)
        self.check_engine_electric_platnium_catalysts = tk.Checkbutton(canvas_type, text="Platnium Catalysts", variable=self.var_engine_electric_platnium_catalysts, command=self.recalculate, anchor="w")
        self.check_engine_electric_platnium_catalysts.grid(column=self.grid_col_cost,row=self.grid_row_electric_mods, sticky="w", columnspan=3)
        self.check_engine_electric_platnium_catalysts.config(state="disabled")

        self.var_engine_electric_extra_power_cells = tk.IntVar(value=0)
        self.check_engine_electric_extra_power_cells = tk.Checkbutton(canvas_type, text="Extra Power Cells", variable=self.var_engine_electric_extra_power_cells, command=self.recalculate, anchor="w")
        self.check_engine_electric_extra_power_cells.grid(column=self.grid_col_max_weight,row=self.grid_row_electric_mods, sticky="w", columnspan=6)
        self.check_engine_electric_extra_power_cells.config(state="disabled")

        self.label_engine_mod_cost = tk.Label(canvas_type, text="0", anchor="w")
        self.label_engine_mod_cost.grid(column=self.grid_col_cost,row=self.grid_row_engine_mods_header, sticky="w")
        self.label_engine_mod_weight = tk.Label(canvas_type, text="0", anchor="w")
        self.label_engine_mod_weight.grid(column=self.grid_col_weight ,row=self.grid_row_engine_mods_header, sticky="w")
        self.label_engine_mod_space = tk.Label(canvas_type, text="0", anchor="w")
        self.label_engine_mod_space.grid(column=self.grid_col_spaces,row=self.grid_row_engine_mods_header, sticky="w")
        self.label_engine_mod_dp = tk.Label(canvas_type, text="0", anchor="w")
        self.label_engine_mod_dp.grid(column=self.grid_col_dp,row=self.grid_row_engine_mods_header, sticky="w")
        self.label_engine_mod_pf = tk.Label(canvas_type, text="0", anchor="w")
        self.label_engine_mod_pf.grid(column=self.grid_col_power_factors,row=self.grid_row_engine_mods_header, sticky="w")
        self.label_engine_mod_mpg = tk.Label(canvas_type, text="0", anchor="w")
        self.label_engine_mod_mpg.grid(column=self.grid_col_base_mpg,row=self.grid_row_engine_mods_header, sticky="w")

        self.label_hidden_gas_tank_cost = tk.Label(canvas_type, text="0", anchor="w")
        self.label_hidden_gas_tank_weight = tk.Label(canvas_type, text="0", anchor="w")
        self.label_hidden_gas_tank_dp = tk.Label(canvas_type, text="0", anchor="w")
        self.label_gas_tank_cost = tk.Label(canvas_type, text="0", anchor="w")
        self.label_gas_tank_cost.grid(column=self.grid_col_cost,row=self.grid_row_gas_tank, sticky="w")
        self.label_gas_tank_weight = tk.Label(canvas_type, text="0", anchor="w")
        self.label_gas_tank_weight.grid(column=self.grid_col_weight ,row=self.grid_row_gas_tank, sticky="w")
        self.label_gas_tank_space = tk.Label(canvas_type, text="0", anchor="w")
        self.label_gas_tank_space.grid(column=self.grid_col_spaces,row=self.grid_row_gas_tank, sticky="w")
        self.label_gas_tank_dp = tk.Label(canvas_type, text="0", anchor="w")
        self.label_gas_tank_dp.grid(column=self.grid_col_dp,row=self.grid_row_gas_tank, sticky="w")

        self.var_gas_gallon_qty = tk.IntVar(value=0)
        self.entry_gas_gallon_qty = ttk.Entry(canvas_type, textvariable=self.var_gas_gallon_qty, width=3)
        self.entry_gas_gallon_qty.grid(column=self.grid_col_qty,row=self.grid_row_gas_tank, sticky="w")
        self.var_gas_gallon_qty.trace_add("write", self.on_changed_entry_gas_gallon_qty)
        self.var_front_tire_qty = tk.IntVar(value=0)
        self.entry_front_tire_qty = ttk.Entry(canvas_type, textvariable=self.var_front_tire_qty, width=3)
        self.entry_front_tire_qty.grid(column=self.grid_col_qty,row=self.grid_row_front_tire, sticky="w")
        self.var_front_tire_qty.trace_add("write", self.on_changed_front_tire_qty)
        self.var_rear_tire_qty = tk.IntVar(value=0)
        self.entry_rear_tire_qty = ttk.Entry(canvas_type, textvariable=self.var_rear_tire_qty, width=3)
        self.entry_rear_tire_qty.grid(column=self.grid_col_qty,row=self.grid_row_rear_tire, sticky="w")
        self.var_rear_tire_qty.trace_add("write", self.on_changed_rear_tire_qty)
        self.var_driver_gunner_qty = tk.IntVar(value=0)
        self.entry_driver_gunner_qty = ttk.Entry(canvas_type, textvariable=self.var_driver_gunner_qty, width=3)
        self.entry_driver_gunner_qty.grid(column=self.grid_col_qty,row=self.grid_row_crew_header, sticky="w")
        self.var_driver_gunner_qty.trace_add("write", self.on_changed_driver_gunner_qty)
        self.var_passenger_qty = tk.IntVar(value=0)
        self.entry_passenger_qty = ttk.Entry(canvas_type, textvariable=self.var_passenger_qty, width=3)
        self.entry_passenger_qty.grid(column=self.grid_right_qty,row=self.grid_row_crew_header, sticky="w")
        self.var_passenger_qty.trace_add("write", self.on_changed_driver_gunner_qty)
        self.var_outer_armor_qty = tk.IntVar(value=0)
        self.entry_outer_armor_qty = ttk.Entry(canvas_type, textvariable=self.var_outer_armor_qty, width=3)
        self.entry_outer_armor_qty.grid(column=self.grid_col_qty,row=self.grid_row_outer_armor, sticky="w")
        self.var_outer_armor_qty.trace_add("write", self.on_changed_outer_armor_qty)
        self.var_inner_armor_qty = tk.IntVar(value=0)
        self.entry_inner_armor_qty = ttk.Entry(canvas_type, textvariable=self.var_inner_armor_qty, width=3)
        self.entry_inner_armor_qty.grid(column=self.grid_col_qty,row=self.grid_row_inner_armor, sticky="w")
        self.var_inner_armor_qty.trace_add("write", self.on_changed_inner_armor_qty)

        self.label_hidden_front_tire_cost = tk.Label(canvas_type, text="0", anchor="w")
        self.label_hidden_front_tire_weight = tk.Label(canvas_type, text="0", anchor="w")
        self.label_hidden_front_tire_dp = tk.Label(canvas_type, text="0", anchor="w")
        self.label_front_tire_cost = tk.Label(canvas_type, text="0", anchor="w")
        self.label_front_tire_cost.grid(column=self.grid_col_cost,row=self.grid_row_front_tire, sticky="w")
        self.label_front_tire_weight = tk.Label(canvas_type, text="0", anchor="w")
        self.label_front_tire_weight.grid(column=self.grid_col_weight ,row=self.grid_row_front_tire, sticky="w")
        self.label_front_tire_dp = tk.Label(canvas_type, text="0", anchor="w")
        self.label_front_tire_dp.grid(column=self.grid_col_dp,row=self.grid_row_front_tire, sticky="w")

        self.var_front_tire_steelbelting = tk.IntVar(value=0)
        self.check_front_tire_steelbelting = tk.Checkbutton(canvas_type, text="Steelbelting", variable=self.var_front_tire_steelbelting, command=self.var_front_tire_steelbelting_changed, anchor="w")
        self.check_front_tire_steelbelting.grid(column=self.grid_col_max_weight,row=self.grid_row_front_tire, sticky="w")

        self.var_front_tire_radial = tk.IntVar(value=0)
        self.check_front_tire_radial = tk.Checkbutton(canvas_type, text="Radial", variable=self.var_front_tire_radial, command=self.var_front_tire_radial_changed, anchor="w")
        self.check_front_tire_radial.grid(column=self.grid_col_power_factors,row=self.grid_row_front_tire, sticky="w")

        self.var_front_tire_fireproof = tk.IntVar(value=0)
        self.check_front_tire_fireproof = tk.Checkbutton(canvas_type, text="Fireproof", variable=self.var_front_tire_fireproof, command=self.var_front_tire_fireproof_changed, anchor="w")
        self.check_front_tire_fireproof.grid(column=self.grid_col_base_mpg,row=self.grid_row_front_tire, sticky="w")

        self.var_front_tire_offroad = tk.IntVar(value=0)
        self.check_front_tire_offroad = tk.Checkbutton(canvas_type, text="OffRoad", variable=self.var_front_tire_offroad, command=self.var_front_tire_offroad_changed, anchor="w")
        self.check_front_tire_offroad.grid(column=self.grid_col_test_track,row=self.grid_row_front_tire, sticky="w")

        self.var_front_tire_racing_slick = tk.IntVar(value=0)
        self.check_front_tire_racing_slick = tk.Checkbutton(canvas_type, text="Racing Slicks", variable=self.var_front_tire_racing_slick, command=self.var_front_tire_racing_slick_changed, anchor="w")
        self.check_front_tire_racing_slick.grid(column=self.grid_col_test_track_numbers,row=self.grid_row_front_tire, sticky="w")

        self.label_hidden_rear_tire_cost = tk.Label(canvas_type, text="0", anchor="w")
        self.label_hidden_rear_tire_weight = tk.Label(canvas_type, text="0", anchor="w")
        self.label_hidden_rear_tire_dp = tk.Label(canvas_type, text="0", anchor="w")
        self.label_rear_tire_cost = tk.Label(canvas_type, text="0", anchor="w")
        self.label_rear_tire_cost.grid(column=self.grid_col_cost,row=self.grid_row_rear_tire, sticky="w")
        self.label_rear_tire_weight = tk.Label(canvas_type, text="0", anchor="w")
        self.label_rear_tire_weight.grid(column=self.grid_col_weight ,row=self.grid_row_rear_tire, sticky="w")
        self.label_rear_tire_dp = tk.Label(canvas_type, text="0", anchor="w")
        self.label_rear_tire_dp.grid(column=self.grid_col_dp,row=self.grid_row_rear_tire, sticky="w")

        self.var_rear_tire_steelbelting = tk.IntVar(value=0)
        self.check_rear_tire_steelbelting = tk.Checkbutton(canvas_type, text="Steelbelting", variable=self.var_rear_tire_steelbelting, command=self.var_rear_tire_steelbelting_changed, anchor="w")
        self.check_rear_tire_steelbelting.grid(column=self.grid_col_max_weight,row=self.grid_row_rear_tire, sticky="w")

        self.var_rear_tire_radial = tk.IntVar(value=0)
        self.check_rear_tire_radial = tk.Checkbutton(canvas_type, text="Radial", variable=self.var_rear_tire_radial, command=self.var_rear_tire_radial_changed, anchor="w")
        self.check_rear_tire_radial.grid(column=self.grid_col_power_factors,row=self.grid_row_rear_tire, sticky="w")

        self.var_rear_tire_fireproof = tk.IntVar(value=0)
        self.check_rear_tire_fireproof = tk.Checkbutton(canvas_type, text="Fireproof", variable=self.var_rear_tire_fireproof, command=self.var_rear_tire_fireproof_changed, anchor="w")
        self.check_rear_tire_fireproof.grid(column=self.grid_col_base_mpg,row=self.grid_row_rear_tire, sticky="w")

        self.var_rear_tire_offroad = tk.IntVar(value=0)
        self.check_rear_tire_offroad = tk.Checkbutton(canvas_type, text="OffRoad", variable=self.var_rear_tire_offroad, command=self.var_rear_tire_offroad_changed, anchor="w")
        self.check_rear_tire_offroad.grid(column=self.grid_col_test_track,row=self.grid_row_rear_tire, sticky="w")

        self.var_rear_tire_racing_slick = tk.IntVar(value=0)
        self.check_rear_tire_racing_slick = tk.Checkbutton(canvas_type, text="Racing Slicks", variable=self.var_rear_tire_racing_slick, command=self.var_rear_tire_racing_slick_changed, anchor="w")
        self.check_rear_tire_racing_slick.grid(column=self.grid_col_test_track_numbers,row=self.grid_row_rear_tire, sticky="w")

        self.label_driver_gunner_weight = tk.Label(canvas_type, text="0", anchor="w")
        self.label_driver_gunner_weight.grid(column=self.grid_col_weight ,row=self.grid_row_crew_header, sticky="w")
        self.label_driver_gunner_space = tk.Label(canvas_type, text="0", anchor="w")
        self.label_driver_gunner_space.grid(column=self.grid_col_spaces,row=self.grid_row_crew_header, sticky="w")

        self.label_armor_header = tk.Label(canvas_type, text="Armor", anchor="w")
        self.label_armor_header.grid(column=self.grid_col_item, row=self.grid_row_armor_header, sticky="w")

        self.label_outer_armor_cost = tk.Label(canvas_type, text="0", anchor="w")
        self.label_outer_armor_cost.grid(column=self.grid_col_cost,row=self.grid_row_outer_armor, sticky="w")
        self.label_outer_armor_weight = tk.Label(canvas_type, text="0", anchor="w")
        self.label_outer_armor_weight.grid(column=self.grid_col_weight ,row=self.grid_row_outer_armor, sticky="w")
        self.label_inner_armor_cost = tk.Label(canvas_type, text="0", anchor="w")
        self.label_inner_armor_cost.grid(column=self.grid_col_cost,row=self.grid_row_inner_armor, sticky="w")
        self.label_inner_armor_weight = tk.Label(canvas_type, text="0", anchor="w")
        self.label_inner_armor_weight.grid(column=self.grid_col_weight ,row=self.grid_row_inner_armor, sticky="w")

        self.label_hidden_outer_armor_selection = tk.Label(canvas_type, text="0", anchor="w")
        self.label_hidden_outer_armor_cost = tk.Label(canvas_type, text="0", anchor="w")
        self.label_hidden_outer_armor_weight = tk.Label(canvas_type, text="0", anchor="w")
        self.label_hidden_inner_armor_selection = tk.Label(canvas_type, text="0", anchor="w")
        self.label_hidden_inner_armor_cost = tk.Label(canvas_type, text="0", anchor="w")
        self.label_hidden_inner_armor_weight = tk.Label(canvas_type, text="0", anchor="w")

        self.label_outer_unassigned_armor_qty = tk.Label(canvas_type, text="0", anchor="w")
        self.label_outer_unassigned_armor_qty.grid(column=self.grid_col_spaces,row=self.grid_row_outer_armor, sticky="w")

        self.label_inner_unassigned_armor_qty = tk.Label(canvas_type, text="0", anchor="w")
        self.label_inner_unassigned_armor_qty.grid(column=self.grid_col_spaces,row=self.grid_row_inner_armor, sticky="w")

        self.var_outer_front_armor_allocation_qty = tk.IntVar(value=0)
        self.entry_outer_front_armor_allocation_qty = ttk.Entry(canvas_type, textvariable=self.var_outer_front_armor_allocation_qty, width=3)
        self.entry_outer_front_armor_allocation_qty.grid(column=self.grid_col_dp,row=self.grid_row_outer_armor, sticky="w")
        self.var_outer_front_armor_allocation_qty.trace_add("write", self.on_changed_entry_outer_armor_allocation_qty)

        self.var_outer_back_armor_allocation_qty = tk.IntVar(value=0)
        self.entry_outer_back_armor_allocation_qty = ttk.Entry(canvas_type, textvariable=self.var_outer_back_armor_allocation_qty, width=3)
        self.entry_outer_back_armor_allocation_qty.grid(column=self.grid_col_max_weight,row=self.grid_row_outer_armor, sticky="w")
        self.var_outer_back_armor_allocation_qty.trace_add("write", self.on_changed_entry_outer_armor_allocation_qty)

        self.var_outer_left_armor_allocation_qty = tk.IntVar(value=0)
        self.entry_outer_left_armor_allocation_qty = ttk.Entry(canvas_type, textvariable=self.var_outer_left_armor_allocation_qty, width=3)
        self.entry_outer_left_armor_allocation_qty.grid(column=self.grid_col_power_factors,row=self.grid_row_outer_armor, sticky="w")
        self.var_outer_left_armor_allocation_qty.trace_add("write", self.on_changed_entry_outer_armor_allocation_qty)

        self.var_outer_right_armor_allocation_qty = tk.IntVar(value=0)
        self.entry_outer_right_armor_allocation_qty = ttk.Entry(canvas_type, textvariable=self.var_outer_right_armor_allocation_qty, width=3)
        self.entry_outer_right_armor_allocation_qty.grid(column=self.grid_col_base_mpg,row=self.grid_row_outer_armor, sticky="w")
        self.var_outer_right_armor_allocation_qty.trace_add("write", self.on_changed_entry_outer_armor_allocation_qty)

        self.var_outer_top_armor_allocation_qty = tk.IntVar(value=0)
        self.entry_outer_top_armor_allocation_qty = ttk.Entry(canvas_type, textvariable=self.var_outer_top_armor_allocation_qty, width=3)
        self.entry_outer_top_armor_allocation_qty.grid(column=self.grid_col_test_track,row=self.grid_row_outer_armor, sticky="w")
        self.var_outer_top_armor_allocation_qty.trace_add("write", self.on_changed_entry_outer_armor_allocation_qty)

        self.var_outer_underbody_armor_allocation_qty = tk.IntVar(value=0)
        self.entry_outer_underbody_armor_allocation_qty = ttk.Entry(canvas_type, textvariable=self.var_outer_underbody_armor_allocation_qty, width=3)
        self.entry_outer_underbody_armor_allocation_qty.grid(column=self.grid_col_test_track_numbers,row=self.grid_row_outer_armor, sticky="w")
        self.var_outer_underbody_armor_allocation_qty.trace_add("write", self.on_changed_entry_outer_armor_allocation_qty)

        self.var_inner_front_armor_allocation_qty = tk.IntVar(value=0)
        self.entry_inner_front_armor_allocation_qty = ttk.Entry(canvas_type, textvariable=self.var_inner_front_armor_allocation_qty, width=3)
        self.entry_inner_front_armor_allocation_qty.grid(column=self.grid_col_dp,row=self.grid_row_inner_armor, sticky="w")
        self.var_inner_front_armor_allocation_qty.trace_add("write", self.on_changed_entry_inner_armor_allocation_qty)

        self.var_inner_back_armor_allocation_qty = tk.IntVar(value=0)
        self.entry_inner_back_armor_allocation_qty = ttk.Entry(canvas_type, textvariable=self.var_inner_back_armor_allocation_qty, width=3)
        self.entry_inner_back_armor_allocation_qty.grid(column=self.grid_col_max_weight,row=self.grid_row_inner_armor, sticky="w")
        self.var_inner_back_armor_allocation_qty.trace_add("write", self.on_changed_entry_inner_armor_allocation_qty)

        self.var_inner_left_armor_allocation_qty = tk.IntVar(value=0)
        self.entry_inner_left_armor_allocation_qty = ttk.Entry(canvas_type, textvariable=self.var_inner_left_armor_allocation_qty, width=3)
        self.entry_inner_left_armor_allocation_qty.grid(column=self.grid_col_power_factors,row=self.grid_row_inner_armor, sticky="w")
        self.var_inner_left_armor_allocation_qty.trace_add("write", self.on_changed_entry_inner_armor_allocation_qty)

        self.var_inner_right_armor_allocation_qty = tk.IntVar(value=0)
        self.entry_inner_right_armor_allocation_qty = ttk.Entry(canvas_type, textvariable=self.var_inner_right_armor_allocation_qty, width=3)
        self.entry_inner_right_armor_allocation_qty.grid(column=self.grid_col_base_mpg,row=self.grid_row_inner_armor, sticky="w")
        self.var_inner_right_armor_allocation_qty.trace_add("write", self.on_changed_entry_inner_armor_allocation_qty)

        self.var_inner_top_armor_allocation_qty = tk.IntVar(value=0)
        self.entry_inner_top_armor_allocation_qty = ttk.Entry(canvas_type, textvariable=self.var_inner_top_armor_allocation_qty, width=3)
        self.entry_inner_top_armor_allocation_qty.grid(column=self.grid_col_test_track, row=self.grid_row_inner_armor, sticky="w")
        self.var_inner_top_armor_allocation_qty.trace_add("write", self.on_changed_entry_inner_armor_allocation_qty)

        self.var_inner_underbody_armor_allocation_qty = tk.IntVar(value=0)
        self.entry_inner_underbody_armor_allocation_qty = ttk.Entry(canvas_type, textvariable=self.var_inner_underbody_armor_allocation_qty, width=3)
        self.entry_inner_underbody_armor_allocation_qty.grid(column=self.grid_col_test_track_numbers,row=self.grid_row_inner_armor, sticky="w")
        self.var_inner_underbody_armor_allocation_qty.trace_add("write", self.on_changed_entry_inner_armor_allocation_qty)

        self.label_hidden_front_tire_hc     = tk.Label(canvas_type, text="0", anchor="w")
        self.label_hidden_rear_tire_hc      = tk.Label(canvas_type, text="0", anchor="w")

        self.label_hidden_accessories_hc_1  = tk.Label(canvas_type, text="0", anchor="w")
        self.label_hidden_accessories_hc_2  = tk.Label(canvas_type, text="0", anchor="w")
        self.label_hidden_accessories_hc_3  = tk.Label(canvas_type, text="0", anchor="w")
        self.label_hidden_accessories_hc_4  = tk.Label(canvas_type, text="0", anchor="w")
        self.label_hidden_accessories_hc_5  = tk.Label(canvas_type, text="0", anchor="w")
        self.label_hidden_accessories_hc_6  = tk.Label(canvas_type, text="0", anchor="w")
        self.label_hidden_accessories_hc_7  = tk.Label(canvas_type, text="0", anchor="w")
        self.label_hidden_accessories_hc_8  = tk.Label(canvas_type, text="0", anchor="w")
        self.label_hidden_accessories_hc_9  = tk.Label(canvas_type, text="0", anchor="w")
        self.label_hidden_accessories_hc_10 = tk.Label(canvas_type, text="0", anchor="w")
        self.label_hidden_accessories_hc_11 = tk.Label(canvas_type, text="0", anchor="w")
        self.label_hidden_accessories_hc_12 = tk.Label(canvas_type, text="0", anchor="w")
        self.label_hidden_accessories_hc_13 = tk.Label(canvas_type, text="0", anchor="w")
        self.label_hidden_accessories_hc_14 = tk.Label(canvas_type, text="0", anchor="w")
        self.label_hidden_accessories_hc_15 = tk.Label(canvas_type, text="0", anchor="w")
        self.label_hidden_accessories_hc_16 = tk.Label(canvas_type, text="0", anchor="w")
        self.label_hidden_accessories_hc_17 = tk.Label(canvas_type, text="0", anchor="w")
        self.label_hidden_accessories_hc_18 = tk.Label(canvas_type, text="0", anchor="w")
        self.label_hidden_accessories_hc_19 = tk.Label(canvas_type, text="0", anchor="w")
        self.label_hidden_accessories_hc_20 = tk.Label(canvas_type, text="0", anchor="w")
        self.label_hidden_accessories_hc_21 = tk.Label(canvas_type, text="0", anchor="w")
        self.label_hidden_accessories_hc_22 = tk.Label(canvas_type, text="0", anchor="w")
        self.label_hidden_accessories_hc_23 = tk.Label(canvas_type, text="0", anchor="w")
        self.label_hidden_accessories_hc_24 = tk.Label(canvas_type, text="0", anchor="w")
        self.label_hidden_accessories_hc_25 = tk.Label(canvas_type, text="0", anchor="w")
        self.label_hidden_accessories_hc_26 = tk.Label(canvas_type, text="0", anchor="w")
        self.label_hidden_accessories_hc_27 = tk.Label(canvas_type, text="0", anchor="w")
        self.label_hidden_accessories_hc_28 = tk.Label(canvas_type, text="0", anchor="w")
        self.label_hidden_accessories_hc_29 = tk.Label(canvas_type, text="0", anchor="w")
        self.label_hidden_accessories_hc_30 = tk.Label(canvas_type, text="0", anchor="w")

        self.label_valid_spaces = tk.Label(canvas_type, text="", anchor="w")
        self.label_valid_spaces.grid(column=self.grid_col_qty, row=self.grid_row_red_alert, sticky="w")
        self.label_valid_weight = tk.Label(canvas_type, text="", anchor="w")
        self.label_valid_weight.grid(column=self.grid_col_cost, row=self.grid_row_red_alert, sticky="w")
        self.label_valid_accessories = tk.Label(canvas_type, text="", anchor="w")
        self.label_valid_accessories.grid(column=self.grid_col_weight, row=self.grid_row_red_alert, sticky="w")

    def on_changed_entry_outer_armor_allocation_qty(self, *args):
        try:
            armor_qty:                      int = int(val) if (val := str(self.var_outer_armor_qty.get()).strip()).isdigit() else 0
        except tk.TclError:
            armor_qty = 0
        try:
            front_armor_allocation_qty:     int = int(val) if (val := str(self.var_outer_front_armor_allocation_qty.get()).strip()).isdigit() else 0
        except tk.TclError:
            front_armor_allocation_qty = 0
        try:
            back_armor_allocation_qty:      int = int(val) if (val := str(self.var_outer_back_armor_allocation_qty.get()).strip()).isdigit() else 0
        except tk.TclError:
            back_armor_allocation_qty = 0
        try:
            left_armor_allocation_qty:      int = int(val) if (val := str(self.var_outer_left_armor_allocation_qty.get()).strip()).isdigit() else 0
        except tk.TclError:
            left_armor_allocation_qty = 0
        try:
            right_armor_allocation_qty:     int = int(val) if (val := str(self.var_outer_right_armor_allocation_qty.get()).strip()).isdigit() else 0
        except tk.TclError:
            right_armor_allocation_qty = 0
        try:
            top_armor_allocation_qty:       int = int(val) if (val := str(self.var_outer_top_armor_allocation_qty.get()).strip()).isdigit() else 0
        except tk.TclError:
            top_armor_allocation_qty = 0
        try:
            underbody_armor_allocation_qty: int = int(val) if (val := str(self.var_outer_underbody_armor_allocation_qty.get()).strip()).isdigit() else 0
        except tk.TclError:
            underbody_armor_allocation_qty = 0
        try:
            unassigned_armor_qty:           int = armor_qty - front_armor_allocation_qty - back_armor_allocation_qty - left_armor_allocation_qty - right_armor_allocation_qty - top_armor_allocation_qty - underbody_armor_allocation_qty
        except tk.TclError:
            unassigned_armor_qty = 0
        self.label_outer_unassigned_armor_qty.configure(text=str(unassigned_armor_qty))

    def on_changed_entry_inner_armor_allocation_qty(self, *args):
        try:
            armor_qty:                      int = int(val) if (val := str(self.var_inner_armor_qty.get())).strip().isdigit() else 0
        except tk.TclError:
            armor_qty = 0
        try:
            front_armor_allocation_qty:     int = int(val) if (val := str(self.var_inner_front_armor_allocation_qty.get())).strip().isdigit() else 0
        except tk.TclError:
            front_armor_allocation_qty = 0
        try:
            back_armor_allocation_qty:      int = int(val) if (val := str(self.var_inner_back_armor_allocation_qty.get())).strip().isdigit() else 0
        except tk.TclError:
            back_armor_allocation_qty = 0
        try:
            left_armor_allocation_qty:      int = int(val) if (val := str(self.var_inner_left_armor_allocation_qty.get())).strip().isdigit() else 0
        except tk.TclError:
            left_armor_allocation_qty = 0
        try:
            right_armor_allocation_qty:     int = int(val) if (val := str(self.var_inner_right_armor_allocation_qty.get())).strip().isdigit() else 0
        except tk.TclError:
            right_armor_allocation_qty = 0
        try:
            top_armor_allocation_qty:       int = int(val) if (val := str(self.var_inner_top_armor_allocation_qty.get())).strip().isdigit() else 0
        except tk.TclError:
            top_armor_allocation_qty = 0
        try:
            underbody_armor_allocation_qty: int = int(val) if (val := str(self.var_inner_underbody_armor_allocation_qty.get())).strip().isdigit() else 0
        except tk.TclError:
            underbody_armor_allocation_qty = 0
        try:
            unassigned_armor_qty:           int = armor_qty - front_armor_allocation_qty - back_armor_allocation_qty - left_armor_allocation_qty - right_armor_allocation_qty - top_armor_allocation_qty - underbody_armor_allocation_qty
        except tk.TclError:
            unassigned_armor_qty = 0
        self.label_inner_unassigned_armor_qty.configure(text=str(unassigned_armor_qty))

    def add_buttons_canvas(self, canvas_type):
        """ Add buttons for the user to select up and down values"""
        up_arrow = "\u2191"
        down_arrow = "\u2193"
        self.button_gas_qty_up = tk.Button(canvas_type, text=up_arrow, command=self.on_button_gas_qty_up)
        self.button_gas_qty_up.grid(column=self.grid_left_up_button,row=self.grid_row_gas_tank, sticky="w")
        self.button_gas_qty_down = tk.Button(canvas_type, text=down_arrow, command=self.on_button_gas_qty_down)
        self.button_gas_qty_down.grid(column=self.grid_left_down_button,row=self.grid_row_gas_tank, sticky="w")
        self.button_front_tire_qty_up = tk.Button(canvas_type, text=up_arrow, command=self.on_button_front_tire_qty_up)
        self.button_front_tire_qty_up.grid(column=self.grid_left_up_button,row=self.grid_row_front_tire, sticky="w")
        self.button_front_tire_qty_down = tk.Button(canvas_type, text=down_arrow, command=self.on_button_front_tire_qty_down)
        self.button_front_tire_qty_down.grid(column=self.grid_left_down_button,row=self.grid_row_front_tire, sticky="w")
        self.button_rear_tire_qty_up = tk.Button(canvas_type, text=up_arrow, command=self.on_button_rear_tire_qty_up)
        self.button_rear_tire_qty_up.grid(column=self.grid_left_up_button,row=self.grid_row_rear_tire, sticky="w")
        self.button_rear_tire_qty_down = tk.Button(canvas_type, text=down_arrow, command=self.on_button_rear_tire_qty_down)
        self.button_rear_tire_qty_down.grid(column=self.grid_left_down_button,row=self.grid_row_rear_tire, sticky="w")
        self.button_driver_gunner_qty_up = tk.Button(canvas_type, text=up_arrow, command=self.on_button_driver_gunner_qty_up)
        self.button_driver_gunner_qty_up.grid(column=self.grid_left_up_button,row=self.grid_row_crew_header, sticky="w")
        self.button_driver_gunner_qty_down = tk.Button(canvas_type, text=down_arrow, command=self.on_button_driver_gunner_qty_down)
        self.button_driver_gunner_qty_down.grid(column=self.grid_left_down_button,row=self.grid_row_crew_header, sticky="w")
        self.button_passenger_qty_up = tk.Button(canvas_type, text=up_arrow, command=self.on_button_passenger_qty_up)
        self.button_passenger_qty_up.grid(column=self.grid_right_up_button,row=self.grid_row_crew_header, sticky="w")
        self.button_passenger_qty_down = tk.Button(canvas_type, text=down_arrow, command=self.on_button_passenger_qty_down)
        self.button_passenger_qty_down.grid(column=self.grid_right_down_button,row=self.grid_row_crew_header, sticky="w")

        self.button_outer_armor_qty_up = tk.Button(canvas_type, text=up_arrow, command=self.on_button_outer_armor_qty_up)
        self.button_outer_armor_qty_up.grid(column=self.grid_left_up_button,row=self.grid_row_outer_armor, sticky="w")
        self.button_outer_armor_qty_down = tk.Button(canvas_type, text=down_arrow, command=self.on_button_outer_armor_qty_down)
        self.button_outer_armor_qty_down.grid(column=self.grid_left_down_button,row=self.grid_row_outer_armor, sticky="w")
        self.button_inner_armor_qty_up = tk.Button(canvas_type, text=up_arrow, command=self.on_button_inner_armor_qty_up)
        self.button_inner_armor_qty_up.grid(column=self.grid_left_up_button,row=self.grid_row_inner_armor, sticky="w")
        self.button_inner_armor_qty_down = tk.Button(canvas_type, text=down_arrow, command=self.on_button_inner_armor_qty_down)
        self.button_inner_armor_qty_down.grid(column=self.grid_left_down_button,row=self.grid_row_inner_armor, sticky="w")

        #self.button_accessories_1_qty_up = tk.Button(canvas_type, text=up_arrow, command=self.on_button_accessories_1_qty_up)
        #self.button_accessories_1_qty_up.grid(column=self.grid_left_up_button,row=self.grid_row_accessories_1, sticky="w")
        #self.button_accessories_1_qty_down = tk.Button(canvas_type, text=down_arrow, command=self.on_button_accessories_1_qty_down)
        #self.button_accessories_1_qty_down.grid(column=self.grid_left_down_button,row=self.grid_row_accessories_1, sticky="w")

        #self.button_accessories_2_qty_up = tk.Button(canvas_type, text=up_arrow, command=self.on_button_accessories_2_qty_up)
        #self.button_accessories_2_qty_up.grid(column=self.grid_left_up_button,row=self.grid_row_accessories_2, sticky="w")
        #self.button_accessories_2_qty_down = tk.Button(canvas_type, text=down_arrow, command=self.on_button_accessories_2_qty_down)
        #self.button_accessories_2_qty_down.grid(column=self.grid_left_down_button,row=self.grid_row_accessories_2, sticky="w")

        #self.button_accessories_3_qty_up = tk.Button(canvas_type, text=up_arrow, command=self.on_button_accessories_3_qty_up)
        #self.button_accessories_3_qty_up.grid(column=self.grid_left_up_button,row=self.grid_row_accessories_3, sticky="w")
        #self.button_accessories_3_qty_down = tk.Button(canvas_type, text=down_arrow, command=self.on_button_accessories_3_qty_down)
        #self.button_accessories_3_qty_down.grid(column=self.grid_left_down_button,row=self.grid_row_accessories_3, sticky="w")

        #self.button_accessories_4_qty_up = tk.Button(canvas_type, text=up_arrow, command=self.on_button_accessories_4_qty_up)
        #self.button_accessories_4_qty_up.grid(column=self.grid_left_up_button,row=self.grid_row_accessories_4, sticky="w")
        #self.button_accessories_4_qty_down = tk.Button(canvas_type, text=down_arrow, command=self.on_button_accessories_4_qty_down)
        #self.button_accessories_4_qty_down.grid(column=self.grid_left_down_button,row=self.grid_row_accessories_4, sticky="w")

        #self.button_accessories_5_qty_up = tk.Button(canvas_type, text=up_arrow, command=self.on_button_accessories_5_qty_up)
        #self.button_accessories_5_qty_up.grid(column=self.grid_left_up_button,row=self.grid_row_accessories_5, sticky="w")
        #self.button_accessories_5_qty_down = tk.Button(canvas_type, text=down_arrow, command=self.on_button_accessories_5_qty_down)
        #self.button_accessories_5_qty_down.grid(column=self.grid_left_down_button,row=self.grid_row_accessories_5, sticky="w")

        #self.button_accessories_6_qty_up = tk.Button(canvas_type, text=up_arrow, command=self.on_button_accessories_6_qty_up)
        #self.button_accessories_6_qty_up.grid(column=self.grid_left_up_button,row=self.grid_row_accessories_6, sticky="w")
        #self.button_accessories_6_qty_down = tk.Button(canvas_type, text=down_arrow, command=self.on_button_accessories_6_qty_down)
        #self.button_accessories_6_qty_down.grid(column=self.grid_left_down_button,row=self.grid_row_accessories_6, sticky="w")

        #self.button_accessories_7_qty_up = tk.Button(canvas_type, text=up_arrow, command=self.on_button_accessories_7_qty_up)
        #self.button_accessories_7_qty_up.grid(column=self.grid_left_up_button,row=self.grid_row_accessories_7, sticky="w")
        #self.button_accessories_7_qty_down = tk.Button(canvas_type, text=down_arrow, command=self.on_button_accessories_7_qty_down)
        #self.button_accessories_7_qty_down.grid(column=self.grid_left_down_button,row=self.grid_row_accessories_7, sticky="w")

        #self.button_accessories_8_qty_up = tk.Button(canvas_type, text=up_arrow, command=self.on_button_accessories_8_qty_up)
        #self.button_accessories_8_qty_up.grid(column=self.grid_left_up_button,row=self.grid_row_accessories_8, sticky="w")
        #self.button_accessories_8_qty_down = tk.Button(canvas_type, text=down_arrow, command=self.on_button_accessories_8_qty_down)
        #self.button_accessories_8_qty_down.grid(column=self.grid_left_down_button,row=self.grid_row_accessories_8, sticky="w")

        #self.button_accessories_9_qty_up = tk.Button(canvas_type, text=up_arrow, command=self.on_button_accessories_9_qty_up)
        #self.button_accessories_9_qty_up.grid(column=self.grid_left_up_button,row=self.grid_row_accessories_9, sticky="w")
        #self.button_accessories_9_qty_down = tk.Button(canvas_type, text=down_arrow, command=self.on_button_accessories_9_qty_down)
        #self.button_accessories_9_qty_down.grid(column=self.grid_left_down_button,row=self.grid_row_accessories_9, sticky="w")

        #self.button_accessories_10_qty_up = tk.Button(canvas_type, text=up_arrow, command=self.on_button_accessories_10_qty_up)
        #self.button_accessories_10_qty_up.grid(column=self.grid_left_up_button,row=self.grid_row_accessories_10, sticky="w")
        #self.button_accessories_10_qty_down = tk.Button(canvas_type, text=down_arrow, command=self.on_button_accessories_10_qty_down)
        #self.button_accessories_10_qty_down.grid(column=self.grid_left_down_button,row=self.grid_row_accessories_10, sticky="w")

        #self.button_accessories_11_qty_up = tk.Button(canvas_type, text=up_arrow, command=self.on_button_accessories_11_qty_up)
        #self.button_accessories_11_qty_up.grid(column=self.grid_left_up_button,row=self.grid_row_accessories_11, sticky="w")
        #self.button_accessories_11_qty_down = tk.Button(canvas_type, text=down_arrow, command=self.on_button_accessories_11_qty_down)
        #self.button_accessories_11_qty_down.grid(column=self.grid_left_down_button,row=self.grid_row_accessories_11, sticky="w")

        #self.button_accessories_12_qty_up = tk.Button(canvas_type, text=up_arrow, command=self.on_button_accessories_12_qty_up)
        #self.button_accessories_12_qty_up.grid(column=self.grid_left_up_button,row=self.grid_row_accessories_12, sticky="w")
        #self.button_accessories_12_qty_down = tk.Button(canvas_type, text=down_arrow, command=self.on_button_accessories_12_qty_down)
        #self.button_accessories_12_qty_down.grid(column=self.grid_left_down_button,row=self.grid_row_accessories_12, sticky="w")

        #self.button_accessories_13_qty_up = tk.Button(canvas_type, text=up_arrow, command=self.on_button_accessories_13_qty_up)
        #self.button_accessories_13_qty_up.grid(column=self.grid_left_up_button,row=self.grid_row_accessories_13, sticky="w")
        #self.button_accessories_13_qty_down = tk.Button(canvas_type, text=down_arrow, command=self.on_button_accessories_13_qty_down)
        #self.button_accessories_13_qty_down.grid(column=self.grid_left_down_button,row=self.grid_row_accessories_13, sticky="w")

        #self.button_accessories_14_qty_up = tk.Button(canvas_type, text=up_arrow, command=self.on_button_accessories_14_qty_up)
        #self.button_accessories_14_qty_up.grid(column=self.grid_left_up_button,row=self.grid_row_accessories_14, sticky="w")
        #self.button_accessories_14_qty_down = tk.Button(canvas_type, text=down_arrow, command=self.on_button_accessories_14_qty_down)
        #self.button_accessories_14_qty_down.grid(column=self.grid_left_down_button,row=self.grid_row_accessories_14, sticky="w")

        #self.button_accessories_15_qty_up = tk.Button(canvas_type, text=up_arrow, command=self.on_button_accessories_15_qty_up)
        #self.button_accessories_15_qty_up.grid(column=self.grid_left_up_button,row=self.grid_row_accessories_15, sticky="w")
        #self.button_accessories_15_qty_down = tk.Button(canvas_type, text=down_arrow, command=self.on_button_accessories_15_qty_down)
        #self.button_accessories_15_qty_down.grid(column=self.grid_left_down_button,row=self.grid_row_accessories_15, sticky="w")

        #self.button_accessories_16_qty_up = tk.Button(canvas_type, text=up_arrow, command=self.on_button_accessories_16_qty_up)
        #self.button_accessories_16_qty_up.grid(column=self.grid_left_up_button,row=self.grid_row_accessories_16, sticky="w")
        #self.button_accessories_16_qty_down = tk.Button(canvas_type, text=down_arrow, command=self.on_button_accessories_16_qty_down)
        #self.button_accessories_16_qty_down.grid(column=self.grid_left_down_button,row=self.grid_row_accessories_16, sticky="w")

        #self.button_accessories_17_qty_up = tk.Button(canvas_type, text=up_arrow, command=self.on_button_accessories_17_qty_up)
        #self.button_accessories_17_qty_up.grid(column=self.grid_left_up_button,row=self.grid_row_accessories_17, sticky="w")
        #self.button_accessories_17_qty_down = tk.Button(canvas_type, text=down_arrow, command=self.on_button_accessories_17_qty_down)
        #self.button_accessories_17_qty_down.grid(column=self.grid_left_down_button,row=self.grid_row_accessories_17, sticky="w")

        #self.button_accessories_18_qty_up = tk.Button(canvas_type, text=up_arrow, command=self.on_button_accessories_18_qty_up)
        #self.button_accessories_18_qty_up.grid(column=self.grid_left_up_button,row=self.grid_row_accessories_18, sticky="w")
        #self.button_accessories_18_qty_down = tk.Button(canvas_type, text=down_arrow, command=self.on_button_accessories_18_qty_down)
        #self.button_accessories_18_qty_down.grid(column=self.grid_left_down_button,row=self.grid_row_accessories_18, sticky="w")

        #self.button_accessories_19_qty_up = tk.Button(canvas_type, text=up_arrow, command=self.on_button_accessories_19_qty_up)
        #self.button_accessories_19_qty_up.grid(column=self.grid_left_up_button,row=self.grid_row_accessories_19, sticky="w")
        #self.button_accessories_19_qty_down = tk.Button(canvas_type, text=down_arrow, command=self.on_button_accessories_19_qty_down)
        #self.button_accessories_19_qty_down.grid(column=self.grid_left_down_button,row=self.grid_row_accessories_19, sticky="w")

        #self.button_accessories_20_qty_up = tk.Button(canvas_type, text=up_arrow, command=self.on_button_accessories_20_qty_up)
        #self.button_accessories_20_qty_up.grid(column=self.grid_left_up_button,row=self.grid_row_accessories_20, sticky="w")
        #self.button_accessories_20_qty_down = tk.Button(canvas_type, text=down_arrow, command=self.on_button_accessories_20_qty_down)
        #self.button_accessories_20_qty_down.grid(column=self.grid_left_down_button,row=self.grid_row_accessories_20, sticky="w")

        #self.button_accessories_21_qty_up = tk.Button(canvas_type, text=up_arrow, command=self.on_button_accessories_21_qty_up)
        #self.button_accessories_21_qty_up.grid(column=self.grid_left_up_button,row=self.grid_row_accessories_21, sticky="w")
        #self.button_accessories_21_qty_down = tk.Button(canvas_type, text=down_arrow, command=self.on_button_accessories_21_qty_down)
        #self.button_accessories_21_qty_down.grid(column=self.grid_left_down_button,row=self.grid_row_accessories_21, sticky="w")

        #self.button_accessories_22_qty_up = tk.Button(canvas_type, text=up_arrow, command=self.on_button_accessories_22_qty_up)
        #self.button_accessories_22_qty_up.grid(column=self.grid_left_up_button,row=self.grid_row_accessories_22, sticky="w")
        #self.button_accessories_22_qty_down = tk.Button(canvas_type, text=down_arrow, command=self.on_button_accessories_22_qty_down)
        #self.button_accessories_22_qty_down.grid(column=self.grid_left_down_button,row=self.grid_row_accessories_22, sticky="w")

        #self.button_accessories_23_qty_up = tk.Button(canvas_type, text=up_arrow, command=self.on_button_accessories_23_qty_up)
        #self.button_accessories_23_qty_up.grid(column=self.grid_left_up_button,row=self.grid_row_accessories_23, sticky="w")
        #self.button_accessories_23_qty_down = tk.Button(canvas_type, text=down_arrow, command=self.on_button_accessories_23_qty_down)
        #self.button_accessories_23_qty_down.grid(column=self.grid_left_down_button,row=self.grid_row_accessories_23, sticky="w")

        #self.button_accessories_24_qty_up = tk.Button(canvas_type, text=up_arrow, command=self.on_button_accessories_24_qty_up)
        #self.button_accessories_24_qty_up.grid(column=self.grid_left_up_button,row=self.grid_row_accessories_24, sticky="w")
        #self.button_accessories_24_qty_down = tk.Button(canvas_type, text=down_arrow, command=self.on_button_accessories_24_qty_down)
        #self.button_accessories_24_qty_down.grid(column=self.grid_left_down_button,row=self.grid_row_accessories_24, sticky="w")

        #self.button_accessories_25_qty_up = tk.Button(canvas_type, text=up_arrow, command=self.on_button_accessories_25_qty_up)
        #self.button_accessories_25_qty_up.grid(column=self.grid_left_up_button,row=self.grid_row_accessories_25, sticky="w")
        #self.button_accessories_25_qty_down = tk.Button(canvas_type, text=down_arrow, command=self.on_button_accessories_25_qty_down)
        #self.button_accessories_25_qty_down.grid(column=self.grid_left_down_button,row=self.grid_row_accessories_25, sticky="w")

        #self.button_accessories_26_qty_up = tk.Button(canvas_type, text=up_arrow, command=self.on_button_accessories_26_qty_up)
        #self.button_accessories_26_qty_up.grid(column=self.grid_left_up_button,row=self.grid_row_accessories_26, sticky="w")
        #self.button_accessories_26_qty_down = tk.Button(canvas_type, text=down_arrow, command=self.on_button_accessories_26_qty_down)
        #self.button_accessories_26_qty_down.grid(column=self.grid_left_down_button,row=self.grid_row_accessories_26, sticky="w")

        #self.button_accessories_27_qty_up = tk.Button(canvas_type, text=up_arrow, command=self.on_button_accessories_27_qty_up)
        #self.button_accessories_27_qty_up.grid(column=self.grid_left_up_button,row=self.grid_row_accessories_27, sticky="w")
        #self.button_accessories_27_qty_down = tk.Button(canvas_type, text=down_arrow, command=self.on_button_accessories_27_qty_down)
        #self.button_accessories_27_qty_down.grid(column=self.grid_left_down_button,row=self.grid_row_accessories_27, sticky="w")

        #self.button_accessories_28_qty_up = tk.Button(canvas_type, text=up_arrow, command=self.on_button_accessories_28_qty_up)
        #self.button_accessories_28_qty_up.grid(column=self.grid_left_up_button,row=self.grid_row_accessories_28, sticky="w")
        #self.button_accessories_28_qty_down = tk.Button(canvas_type, text=down_arrow, command=self.on_button_accessories_28_qty_down)
        #self.button_accessories_28_qty_down.grid(column=self.grid_left_down_button,row=self.grid_row_accessories_28, sticky="w")

        #self.button_accessories_29_qty_up = tk.Button(canvas_type, text=up_arrow, command=self.on_button_accessories_29_qty_up)
        #self.button_accessories_29_qty_up.grid(column=self.grid_left_up_button,row=self.grid_row_accessories_29, sticky="w")
        #self.button_accessories_29_qty_down = tk.Button(canvas_type, text=down_arrow, command=self.on_button_accessories_29_qty_down)
        #self.button_accessories_29_qty_down.grid(column=self.grid_left_down_button,row=self.grid_row_accessories_29, sticky="w")

        #self.button_accessories_30_qty_up = tk.Button(canvas_type, text=up_arrow, command=self.on_button_accessories_30_qty_up)
        #self.button_accessories_30_qty_up.grid(column=self.grid_left_up_button,row=self.grid_row_accessories_30, sticky="w")
        #self.button_accessories_30_qty_down = tk.Button(canvas_type, text=down_arrow, command=self.on_button_accessories_30_qty_down)
        #self.button_accessories_30_qty_down.grid(column=self.grid_left_down_button,row=self.grid_row_accessories_30, sticky="w")

    def set_columns(self):
        self.grid_row_red_alert          = 0
        self.grid_row_form_total         = self.grid_row_red_alert + 1
        self.grid_row_form_header        = self.grid_row_form_total + 1
        self.grid_row_body               = self.grid_row_form_header + 1
        self.grid_row_body_modification  = self.grid_row_body + 1
        self.grid_row_chassis            = self.grid_row_body_modification + 1
        self.grid_row_suspension         = self.grid_row_chassis + 1
        self.grid_row_engine             = self.grid_row_suspension  + 1
        self.grid_row_engine_mods_header = self.grid_row_engine + 1
        self.grid_row_gas_engine_mods    = self.grid_row_engine_mods_header + 1
        self.grid_row_electric_mods      = self.grid_row_gas_engine_mods + 1
        #self.grid_row_fuel_injection     = 9
        self.grid_row_gas_tank           = self.grid_row_electric_mods + 1
        self.grid_row_front_tire         = self.grid_row_gas_tank + 1
        self.grid_row_rear_tire          = self.grid_row_front_tire + 1
        self.grid_row_crew_header        = self.grid_row_rear_tire + 1
        self.grid_row_armor_header       = self.grid_row_crew_header + 1
        self.grid_row_outer_armor        = self.grid_row_armor_header + 1
        self.grid_row_inner_armor        = self.grid_row_outer_armor + 1
        self.grid_row_sloped_armor       = self.grid_row_inner_armor + 1
        self.grid_row_weapon_alt_1       = self.grid_row_sloped_armor + 1
        self.grid_row_sub_weapon_alt_1   = self.grid_row_weapon_alt_1 + 1
        #self.grid_row_weapon_alt_2       = self.grid_row_sub_weapon_alt_1 + 1
        #self.grid_row_sub_weapon_alt_2   = self.grid_row_weapon_alt_2 + 1
        #self.grid_row_weapon_alt_3       = self.grid_row_sub_weapon_alt_2 + 1
        #self.grid_row_sub_weapon_alt_3   = self.grid_row_weapon_alt_3 + 1
        #self.grid_row_weapon_alt_4       = self.grid_row_sub_weapon_alt_3 + 1
        #self.grid_row_sub_weapon_alt_4   = self.grid_row_weapon_alt_4 + 1
        #self.grid_row_weapon_alt_5       = self.grid_row_sub_weapon_alt_4 + 1
        #self.grid_row_sub_weapon_alt_5   = self.grid_row_weapon_alt_5 + 1
        #self.grid_row_weapon_alt_6       = self.grid_row_sub_weapon_alt_5 + 1
        #self.grid_row_sub_weapon_alt_6   = self.grid_row_weapon_alt_6 + 1
        #self.grid_row_weapon_alt_7       = self.grid_row_sub_weapon_alt_6 + 1
        #self.grid_row_sub_weapon_alt_7   = self.grid_row_weapon_alt_7 + 1
        #self.grid_row_weapon_alt_8       = self.grid_row_sub_weapon_alt_7 + 1
        #self.grid_row_sub_weapon_alt_8   = self.grid_row_weapon_alt_8 + 1
        #self.grid_row_weapon_alt_9       = self.grid_row_sub_weapon_alt_8 + 1
        #self.grid_row_sub_weapon_alt_9   = self.grid_row_weapon_alt_9 + 1
        #self.grid_row_weapon_alt_10      = self.grid_row_sub_weapon_alt_9 + 1
        #self.grid_row_sub_weapon_alt_10  = self.grid_row_weapon_alt_10 + 1
        #self.grid_row_links_header       = self.grid_row_sub_weapon_alt_10 + 1
        #self.grid_row_link_1             = self.grid_row_links_header + 1
        #self.grid_row_link_2             = self.grid_row_link_1 + 1
        #self.grid_row_link_3             = self.grid_row_link_2 + 1
        #self.grid_row_link_4             = self.grid_row_link_3 + 1
        #self.grid_row_link_5             = self.grid_row_link_4 + 1
        #self.grid_row_link_6             = self.grid_row_link_5 + 1
        #self.grid_row_link_7             = self.grid_row_link_6 + 1
        #self.grid_row_link_8             = self.grid_row_link_7 + 1
        #self.grid_row_link_9             = self.grid_row_link_8 + 1
        #self.grid_row_link_10            = self.grid_row_link_9 + 1

        # Add this code inside your def set_columns(self): method
        #self.grid_row_bumper_trigger_header = self.grid_row_link_10 + 1

        # Automatically calculate rows 1 through 10 dynamically
        #for i in range(1, 11):
        #    setattr(self, f"grid_row_bumper_trigger_row_{i}", self.grid_row_bumper_trigger_header + i)

        # CRUCIAL: Make sure to update your subsequent accessory header to sit cleanly below this new block
        #self.grid_row_accessories_header = getattr(self, f"grid_row_bumper_trigger_row_{self.link_rows_count}") + 1

        #self.grid_row_accessories_header = self.grid_row_link_10 + 1
        #self.grid_row_accessories_1      = self.grid_row_accessories_header + 1
        #self.grid_row_accessories_2      = self.grid_row_accessories_1 + 1
        #self.grid_row_accessories_3      = self.grid_row_accessories_2 + 1
        #self.grid_row_accessories_4      = self.grid_row_accessories_3 + 1
        #self.grid_row_accessories_5      = self.grid_row_accessories_4 + 1
        #self.grid_row_accessories_6      = self.grid_row_accessories_5 + 1
        #self.grid_row_accessories_7      = self.grid_row_accessories_6 + 1
        #self.grid_row_accessories_8      = self.grid_row_accessories_7 + 1
        #self.grid_row_accessories_9      = self.grid_row_accessories_8 + 1
        #self.grid_row_accessories_10      = self.grid_row_accessories_9 + 1
        #self.grid_row_accessories_11      = self.grid_row_accessories_10 + 1
        #self.grid_row_accessories_12      = self.grid_row_accessories_11 + 1
        #self.grid_row_accessories_13      = self.grid_row_accessories_12 + 1
        #self.grid_row_accessories_14      = self.grid_row_accessories_13 + 1
        #self.grid_row_accessories_15      = self.grid_row_accessories_14 + 1
        ##self.grid_row_accessories_16      = self.grid_row_accessories_15 + 1
        #self.grid_row_accessories_17      = self.grid_row_accessories_16 + 1
        #self.grid_row_accessories_18      = self.grid_row_accessories_17 + 1
        #self.grid_row_accessories_19      = self.grid_row_accessories_18 + 1
        #self.grid_row_accessories_20      = self.grid_row_accessories_19 + 1
        #self.grid_row_accessories_21      = self.grid_row_accessories_20 + 1
        #self.grid_row_accessories_22      = self.grid_row_accessories_21 + 1
        #self.grid_row_accessories_23      = self.grid_row_accessories_22 + 1
        #self.grid_row_accessories_24      = self.grid_row_accessories_23 + 1
        #self.grid_row_accessories_25      = self.grid_row_accessories_24 + 1
        #self.grid_row_accessories_26      = self.grid_row_accessories_25 + 1
        #self.grid_row_accessories_27      = self.grid_row_accessories_26 + 1
        #self.grid_row_accessories_28      = self.grid_row_accessories_27 + 1
        #self.grid_row_accessories_29      = self.grid_row_accessories_28 + 1
        #self.grid_row_accessories_30      = self.grid_row_accessories_29 + 1
        #self.grid_row_component_header    = self.grid_row_accessories_30 + 1
        #self.grid_row_component_armor_1   = self.grid_row_component_header + 1
        #self.grid_row_component_armor_2   = self.grid_row_component_armor_1 + 1
        #self.grid_row_component_armor_3   = self.grid_row_component_armor_2 + 1
        #self.grid_row_component_armor_4   = self.grid_row_component_armor_3 + 1
        #self.grid_row_component_armor_5   = self.grid_row_component_armor_4 + 1
        #self.grid_row_rocket_booster_header = self.grid_row_component_armor_5 + 1
        #self.grid_row_rocket_booster_1    = self.grid_row_rocket_booster_header + 1
        #self.grid_row_rocket_booster_2    = self.grid_row_rocket_booster_1 + 1
        #self.grid_row_rocket_booster_3    = self.grid_row_rocket_booster_2 + 1
        #self.grid_row_rocket_booster_4    = self.grid_row_rocket_booster_3 + 1
        #self.grid_row_rocket_booster_5    = self.grid_row_rocket_booster_4 + 1
        #self.grid_row_alt_ge_equivalent   = self.grid_row_rocket_booster_5 + 1
        #self.grid_row_personal_equipment_header = self.grid_row_alt_ge_equivalent + 1
        #self.grid_row_personal_equipment_1 = self.grid_row_personal_equipment_header + 1
        #self.grid_row_personal_equipment_2 = self.grid_row_personal_equipment_1 + 1
        #self.grid_row_personal_equipment_3 = self.grid_row_personal_equipment_2 + 1
        #self.grid_row_personal_equipment_4 = self.grid_row_personal_equipment_3 + 1
        #self.grid_row_personal_equipment_5 = self.grid_row_personal_equipment_4 + 1
        #self.grid_row_personal_equipment_6 = self.grid_row_personal_equipment_5 + 1
        #self.grid_row_personal_equipment_7 = self.grid_row_personal_equipment_6 + 1
        #self.grid_row_personal_equipment_8 = self.grid_row_personal_equipment_7 + 1
        #self.grid_row_personal_equipment_9 = self.grid_row_personal_equipment_8 + 1
        #self.grid_row_personal_equipment_10 = self.grid_row_personal_equipment_9 + 1
        self.grid_col_item                 = 0
        self.grid_col_qty                  = self.grid_col_item + 1
        self.grid_left_up_button           = self.grid_col_qty + 1
        self.grid_left_down_button         = self.grid_left_up_button + 1
        self.grid_right_qty                = self.grid_left_down_button + 1
        self.grid_right_up_button          = self.grid_right_qty + 1
        self.grid_right_down_button        = self.grid_right_up_button + 1
        self.grid_col_weapon_ammo_entry    = self.grid_right_down_button + 1
        self.grid_col_weapon_ammo_qty_up   = self.grid_col_weapon_ammo_entry + 1
        self.grid_col_weapon_ammo_qty_down = self.grid_col_weapon_ammo_qty_up + 1
        self.grid_col_extra_mag_entry      = self.grid_col_weapon_ammo_qty_down + 1
        self.grid_col_extra_mag_qty_up     = self.grid_col_extra_mag_entry + 1
        self.grid_col_extra_mag_qty_down   = self.grid_col_extra_mag_qty_up + 1
        self.grid_col_cost                 = self.grid_col_extra_mag_qty_down + 1
        self.grid_col_weight               = self.grid_col_cost + 1
        self.grid_col_spaces               = self.grid_col_weight + 1
        self.grid_col_dp                   = self.grid_col_spaces + 1
        self.grid_col_max_weight           = self.grid_col_dp + 1
        self.grid_col_power_factors        = self.grid_col_max_weight + 1
        self.grid_col_base_mpg             = self.grid_col_power_factors + 1
        self.grid_col_test_track           = self.grid_col_base_mpg + 1
        self.grid_col_test_track_numbers   = self.grid_col_test_track + 1
        self.grid_col_last_column          = self.grid_col_test_track_numbers + 1

    def add_dropdowns_canvas(self, canvas_type):
        self.get_body_dictionaries()
        self.get_modifications_dictionaries()
        self.get_chassis_dictionaries()
        self.get_suspension_dictionaries()
        self.get_engines_dictionaries()
        self.get_gas_tank_dictionaries()
        self.get_tires_dictionaries()
        self.get_weapon_dictionaries_alt()
        self.get_accessories_dictionaries()
        self.get_outer_armor_dictionaries()
        self.get_inner_armor_dictionaries()
        self.get_personal_equipment_dictionaries()
        self.add_dropdown_body_canvas(canvas_type=canvas_type)
        self.add_dropdown_modifications_canvas(canvas_type=canvas_type)
        self.add_dropdown_chassis_canvas(canvas_type=canvas_type)
        self.add_dropdown_suspension_canvas(canvas_type=canvas_type)
        self.add_dropdown_engines_canvas(canvas_type=canvas_type)
        self.add_dropdown_gas_tank_canvas(canvas_type=canvas_type)
        self.add_dropdown_front_tires_canvas(canvas_type=canvas_type)
        self.add_dropdown_rear_tires_canvas(canvas_type=canvas_type)
        self.add_dropdown_outer_armor_canvas(canvas_type=canvas_type)
        self.add_dropdown_inner_armor_canvas(canvas_type=canvas_type)
        #self.add_dropdown_accessories_canvas(canvas_type=canvas_type)
        #self.add_dropdown_personal_equipment_canvas(canvas_type=canvas_type)

    def add_dropdown_accessories_canvas(self, canvas_type):
        self.add_dropdown_accessories_1_canvas(canvas_type=canvas_type)
        self.add_dropdown_accessories_2_canvas(canvas_type=canvas_type)
        self.add_dropdown_accessories_3_canvas(canvas_type=canvas_type)
        self.add_dropdown_accessories_4_canvas(canvas_type=canvas_type)
        self.add_dropdown_accessories_5_canvas(canvas_type=canvas_type)
        self.add_dropdown_accessories_6_canvas(canvas_type=canvas_type)
        self.add_dropdown_accessories_7_canvas(canvas_type=canvas_type)
        self.add_dropdown_accessories_8_canvas(canvas_type=canvas_type)
        self.add_dropdown_accessories_9_canvas(canvas_type=canvas_type)
        self.add_dropdown_accessories_10_canvas(canvas_type=canvas_type)
        self.add_dropdown_accessories_11_canvas(canvas_type=canvas_type)
        self.add_dropdown_accessories_12_canvas(canvas_type=canvas_type)
        self.add_dropdown_accessories_13_canvas(canvas_type=canvas_type)
        self.add_dropdown_accessories_14_canvas(canvas_type=canvas_type)
        self.add_dropdown_accessories_15_canvas(canvas_type=canvas_type)
        self.add_dropdown_accessories_16_canvas(canvas_type=canvas_type)
        self.add_dropdown_accessories_17_canvas(canvas_type=canvas_type)
        self.add_dropdown_accessories_18_canvas(canvas_type=canvas_type)
        self.add_dropdown_accessories_19_canvas(canvas_type=canvas_type)
        self.add_dropdown_accessories_20_canvas(canvas_type=canvas_type)
        self.add_dropdown_accessories_21_canvas(canvas_type=canvas_type)
        self.add_dropdown_accessories_22_canvas(canvas_type=canvas_type)
        self.add_dropdown_accessories_23_canvas(canvas_type=canvas_type)
        self.add_dropdown_accessories_24_canvas(canvas_type=canvas_type)
        self.add_dropdown_accessories_25_canvas(canvas_type=canvas_type)
        self.add_dropdown_accessories_26_canvas(canvas_type=canvas_type)
        self.add_dropdown_accessories_27_canvas(canvas_type=canvas_type)
        self.add_dropdown_accessories_28_canvas(canvas_type=canvas_type)
        self.add_dropdown_accessories_29_canvas(canvas_type=canvas_type)
        self.add_dropdown_accessories_30_canvas(canvas_type=canvas_type)

    def add_dropdown_body_canvas(self, canvas_type):
        self.selected_body = tk.StringVar()
        self.selected_body.set("Body") # Set default option

        # Options for the dropdown
        #options = ["Body", "Body", "Light Cycle", "Medium Cycle", "Heavy Cycle", "Light SideCar",
        options = ["Body", "Light Cycle", "Medium Cycle", "Heavy Cycle", "Light SideCar",
                   "Heavy SideCar", "Light Trike", "Medium Trike", "Heavy Trike",
                    "x-Hvy Trike", "Rev. Light Trike", "Rev. Medium Trike", "Rev. Heavy Trike",
                    "Rev. X-Hvy Trike", "Subcompact", "Compact", "Mid-Sized",
                    "Sedan", "Luxury", "Station Wagon", "Pickup",
                    "Pickup, 1 Spc Ext. Cab", "Pickup, 2 Spc Ext. Cab", "Camper", "Van",
                    "Formula One/Indy", "Can-Am", "Sprint", "Funny Car", "Dragster"]
        # Create the dropdown widget
        self.body_dropdown = ttk.OptionMenu(canvas_type, self.selected_body, "Body", *options)
        self.body_dropdown.grid(column=self.grid_col_item, row=self.grid_row_body, sticky="w")
        self.selected_body.trace_add("write", self.on_select_body)

    def add_dropdown_modifications_canvas(self, canvas_type):
        self.selected_modifications = tk.StringVar()
        self.selected_modifications.set("Modifications") # Set default option
        # Options for the dropdown
        options = ["No Mods"
                   , "No Mods"
                   , "CA Frame"
                   , "Streamlined"
                   , "CA/Streamlined"]
        # Create the dropdown widget
        self.modification_dropdown = ttk.OptionMenu(canvas_type, self.selected_modifications, "Modifications", *options)
        self.modification_dropdown.grid(column=self.grid_col_item, row=self.grid_row_body_modification, sticky="w")
        self.selected_modifications.trace_add("write", self.on_select_modification)

    def add_dropdown_chassis_canvas(self, canvas_type):
        self.selected_chassis = tk.StringVar()
        self.selected_chassis.set("Chassis")
        # Options for the dropdown
        options = ["Chassis"
                   , "Cycle Chassis"
                   , "Light Chassis"
                   , "Standard Chassis"
                   , "Heavy Chassis"
                   , "Ext Heavy Chassis"]
        # Create the dropdown widget
        self.chassis_dropdown = ttk.OptionMenu(canvas_type, self.selected_chassis, "Chassis", *options)
        self.chassis_dropdown.grid(column=self.grid_col_item, row=self.grid_row_chassis, sticky="w")
        self.selected_chassis.trace_add("write", self.on_select_chassis)

    def add_dropdown_suspension_canvas(self, canvas_type):
        self.selected_suspension = tk.StringVar()
        self.selected_suspension.set("Suspension")
        options = ["Suspension", "Cycle Light Suspension", "Cycle Improved Suspension", "Cycle - Heavy Suspension", "Cycle - OR Suspension", "Light Suspension", "Improved Suspension", "Heavy Suspension", "Off-Road Suspension", "Racing Suspension"]
          # Create the dropdown widget
        self.suspension_dropdown = ttk.OptionMenu(canvas_type, self.selected_suspension, "Suspension", *options)
        self.suspension_dropdown.grid(column=self.grid_col_item, row=self.grid_row_suspension, sticky="w")
        self.selected_suspension.trace_add("write", self.on_select_suspension)

    def add_dropdown_engines_canvas(self, canvas_type):
        self.selected_engine = tk.StringVar()
        self.selected_engine.set("Engine")
        options = ["Engine", "10 cid IC Engine", "30 cid IC Engine",  "50 cid IC Engine",  "100 cid IC Engine",
                   "150 cid IC Engine",  "200 cid IC Engine",  "250 cid IC Engine",  "300 cid IC Engine",
                   "350 cid IC Engine",  "400 cid IC Engine",  "450 cid IC Engine",  "500 cid IC Engine",
                   "700 cid IC Engine", "Small Cycle Power Plant", "Medium Cycle Power Plant", "Large Cycle Power Plant",
                   "Super Cycle Power Plant", "Super Trike Power Plant", "Small Electric Power Plant",
                   "Medium Electric Power Plant", "Large Electric Power Plant", "Super Power Plant",
                   "Sport Power Plant", "ThunderCat Power Plant"]
          # Create the dropdown widget
        self.engine_dropdown = ttk.OptionMenu(canvas_type, self.selected_engine, "Engine", *options)
        self.engine_dropdown.grid(column=self.grid_col_item, row=self.grid_row_engine, sticky="w")
        self.selected_engine.trace_add("write", self.on_select_engines)

    def add_dropdown_gas_tank_canvas(self, canvas_type):
        self.selected_gas_tank = tk.StringVar()
        self.selected_gas_tank.set("Gas Tank")
        options = ["Gas Tank"
                   , "Gas Tank"
                   , "Electric"
                   , "Economy Gas Tank"
                   , "Hvy-Duty Gas Tank"
                   , "Racing Gas Tank"
                   , "Duelling Gas Tank"]
        # Create the dropdown widget
        self.gas_tank_dropdown = ttk.OptionMenu(canvas_type, self.selected_gas_tank, "Gas Tank", *options)
        self.gas_tank_dropdown.grid(column=self.grid_col_item, row=self.grid_row_gas_tank, sticky="w")
        self.selected_gas_tank.trace_add("write", self.on_select_gas_tank)

    def add_dropdown_front_tires_canvas(self, canvas_type):
        self.selected_front_tire = tk.StringVar()
        self.selected_front_tire.set("Tires")
        options = ["Tires"
                   , "Standard Tires"
                   , "Heavy Duty Tires"
                   , "PR Tires"
                   , "Solid Tires"
                   , "Plasticore Tires"]
        # Create the dropdown widget
        self.front_tires_dropdown = ttk.OptionMenu(canvas_type, self.selected_front_tire, "Tires", *options)
        self.front_tires_dropdown.grid(column=self.grid_col_item, row=self.grid_row_front_tire, sticky="w")
        self.selected_front_tire.trace_add("write", self.on_select_front_tires)

    def add_dropdown_rear_tires_canvas(self, canvas_type):
        self.selected_rear_tire = tk.StringVar()
        self.selected_rear_tire.set("Tires")
        options = ["Tires"
                   , "Standard Tires"
                   , "Heavy Duty Tires"
                   , "PR Tires"
                   , "Solid Tires"
                   , "Plasticore Tires"]
        # Create the dropdown widget
        self.rear_tires_dropdown = ttk.OptionMenu(canvas_type, self.selected_rear_tire, "Tires", *options)
        self.rear_tires_dropdown.grid(column=self.grid_col_item, row=self.grid_row_rear_tire, sticky="w")
        self.selected_rear_tire.trace_add("write", self.on_select_rear_tires)

    def add_dropdown_outer_armor_canvas(self, canvas_type):
        self.selected_outer_armor = tk.StringVar()
        self.selected_outer_armor.set("Outer Armor")
        options = self.get_outer_armor_options()
        # Create the dropdown widget
        self.outer_armor_dropdown = ttk.OptionMenu(canvas_type, self.selected_outer_armor, "Outer Armor", *options) #filled elsewhere
        self.outer_armor_dropdown.grid(column=self.grid_col_item, row=self.grid_row_outer_armor, sticky="w")
        self.selected_outer_armor.trace_add("write", self.on_select_outer_armor)

    def add_dropdown_inner_armor_canvas(self, canvas_type):
        self.selected_inner_armor = tk.StringVar()
        self.selected_inner_armor.set("Inner Armor")
        options = self.get_inner_armor_options()
        # Create the dropdown widget
        self.inner_armor_dropdown = ttk.OptionMenu(canvas_type, self.selected_inner_armor, "Inner Armor", *options) #filled elsewhere
        self.inner_armor_dropdown.grid(column=self.grid_col_item, row=self.grid_row_inner_armor, sticky="w")
        self.selected_inner_armor.trace_add("write", self.on_select_inner_armor)

    def add_dropdown_personal_equipment_canvas(self, canvas_type):
        self.add_dropdown_personal_equipment_1_canvas(canvas_type)
        self.add_dropdown_personal_equipment_2_canvas(canvas_type)
        self.add_dropdown_personal_equipment_3_canvas(canvas_type)
        self.add_dropdown_personal_equipment_4_canvas(canvas_type)
        self.add_dropdown_personal_equipment_5_canvas(canvas_type)
        self.add_dropdown_personal_equipment_6_canvas(canvas_type)
        self.add_dropdown_personal_equipment_7_canvas(canvas_type)
        self.add_dropdown_personal_equipment_8_canvas(canvas_type)
        self.add_dropdown_personal_equipment_9_canvas(canvas_type)
        self.add_dropdown_personal_equipment_10_canvas(canvas_type)

    def on_select_body(self, *args):
        selected_value = self.selected_body.get()
        for entry in self.body_list: #list of dictionaries
            body_type: str = entry.get("Body")
            if selected_value == body_type: #found what we're looking for
                self.is_cycle = entry.get("Cycle")
                if selected_value in ("Subcompact", "Formula One/Indy"):
                    self.label_hidden_body_hc.configure(text="1")
                else:
                    self.label_hidden_body_hc.configure(text="0")
                self.hc_addition()
                self.label_body_selected.configure(text=body_type)
                self.label_body_cost.configure(text=entry.get("Cost"))
                self.label_body_weight.configure(text=entry.get("Weight"))
                self.label_body_max_weight.configure(text=entry.get("Total Weight"))
                self.label_max_weight.configure(text=str(entry.get("Total Weight")))
                self.label_body_spaces.configure(text=entry.get("Total Spaces"))
                self.label_hidden_cargo_spaces.configure(text=entry.get("Cargo Spaces"))
                self.label_hidden_body_armor_cost.configure(text=entry.get("Armor Cost/Point"))
                self.label_hidden_body_armor_weight.configure(text=entry.get("Armor Weight/Point"))
                self.hidden_body_cycle.configure(text=entry.get("Cycle")) #Use this when calculating tire weight, cycles get half weight
                #self.on_select_carb() #recalculate fuel injection options, this calls self.recalculate()
                self.on_select_chassis()
                self.recalculate()
                return #exit now

    def on_select_modification(self, *args):
        selected_value = self.selected_modifications.get()
        for entry in self.modifications_list:
            modification_type: str = entry.get("Modification")
            if selected_value == modification_type: # get the values in the body lines for final adjustment
                body_cost: int = self.label_body_cost.cget("text")
                body_weight: int = self.label_body_weight.cget("text")
                body_spaces: int = self.label_body_spaces.cget("text")
                cargo_spaces: int = self.label_hidden_cargo_spaces.cget("text")
                modification_cost: int = int(float(entry.get("Cost")) * body_cost)
                modification_weight: int = int(float(entry.get("Weight")) * body_weight)
                local_sloped_armor = self.var_sloped_armor.get() * 0.1
                streamline_spaces: float = float(entry.get("Spaces"))
                total_spaces: float = local_sloped_armor + streamline_spaces
                if total_spaces == 0.2: #both have been selected, adjust
                    total_spaces = 0.15
                modification_spaces: int = math.ceil(total_spaces * body_spaces)
                modification_cargo_spaces: int = math.ceil(total_spaces * cargo_spaces)
                self.label_modificiation_cost.configure(text=str(modification_cost))
                self.label_modificiation_weight.configure(text=str(modification_weight))
                self.label_modificiation_space.configure(text=str(modification_spaces))
                self.label_hidden_modification_cargo_space.configure(text=str(modification_cargo_spaces))
                self.recalculate()
                return #exit now
        #If we're here, there's no modification selected, but check to see if we're sloped
        sloped = self.var_sloped_armor.get()
        body_spaces: int = self.label_body_spaces.cget("text")
        total_spaces = self.var_sloped_armor.get() * 0.1
        modification_spaces: int = math.ceil(total_spaces * body_spaces)
        self.label_modificiation_space.configure(text=str(modification_spaces))
        self.recalculate()

    def on_select_chassis(self, *args):
        selected_value = self.selected_chassis.get()
        for entry in self.chassis_list:
            chassis_type: str = entry.get("Chassis")
            if selected_value == chassis_type: # get the values in the body lines for final adjustment
                body_cost: int = self.label_body_cost.cget("text")
                body_max_weight: int = self.label_body_max_weight.cget("text")
                chassis_cost: int = math.ceil(entry.get("Cost") * body_cost)
                chassis_max_weight = int(body_max_weight * float(entry.get("Max Weight")))
                self.label_chassis_cost.configure(text=str(chassis_cost))
                self.label_max_weight.configure(text=str(chassis_max_weight))
                body_selected: str = self.label_body_selected.cget("text")
                if body_selected in ["Pickup", "Pickup, 1 Spc Ext. Cab", "Pickup, 2 Spc Ext. Cab", "Camper", "Van"]:
                    if chassis_type == "Ext Heavy Chassis":
                        self.var_six_wheel_chassis.set(1)
                self.recalculate()
                return #exit now

    def var_six_wheel_chassis_changed(self, *args):
        self.recalculate()

    def var_sloped_armor_changed(self, *args):
        self.on_select_outer_armor()
        self.on_select_inner_armor()
        self.on_select_modification()
        self.recalculate()

    def on_select_suspension(self, *args):
        selected_value = self.selected_suspension.get()
        for entry in self.suspension_list:
            suspension_type: str = entry.get("Suspension")
            if selected_value == suspension_type: # get the values in the body lines for final adjustment
                body_cost: int = self.label_body_cost.cget("text")
                suspension_cost: int = math.ceil(float(entry.get("Cost")) * body_cost)
                hc_value: int = int(entry.get("HC"))
                self.label_hc.configure(text=str(hc_value))
                self.hc_addition()
                self.label_suspension_cost.configure(text=str(suspension_cost)) # we will want to show the proper HC
                self.recalculate()
                return #exit now

    def on_select_engines(self, *args):
        selected_value = self.selected_engine.get()
        for entry in self.engine_list:
            engine_type: str = entry.get("Engine")
            if selected_value == engine_type: # get the values in the body lines for final adjustment
                self.label_engine_cost.configure(text=entry.get("Cost"))
                self.label_engine_weight.configure(text=entry.get("Weight"))
                self.label_engine_space.configure(text=entry.get("Spaces"))
                self.label_engine_dp.configure(text=entry.get("DP"))
                self.label_engine_pf.configure(text=entry.get("Power Factors"))
                self.label_engine_mpg.configure(text=entry.get("Base MPG"))
                self.label_engine_type.configure(text=entry.get("Type"))
                if self.label_engine_type.cget("text") == "Gas":
                    self.hide_electric_engine_options()
                    self.show_gas_engine_options()
                else:
                    self.show_electric_engine_options()
                    self.hide_gas_engine_options()
                self.recalculate()
                return #exit now

    def var_engine_gas_super_charger_changed(self, *args):
        self.recalculate()

    def var_engine_gas_vp_turbo_changed(self, *args):
        self.var_engine_gas_turbo.set(0) # turn off the Turbo if VP Turbo is selected
        self.recalculate()

    def var_engine_gas_turbo_changed(self, *args):
        self.var_engine_gas_vp_turbo.set(0) # turn off the VP turbo if Turbo is selected
        self.recalculate()

    def var_engine_gas_tube_headers_changed(self, *args):
        self.recalculate()

    def var_engine_gas_blue_print_changed(self, *args):
        self.recalculate()

    def on_select_gas_tank(self, *args):
        selected_value = self.selected_gas_tank.get()
        for entry in self.gas_tank_list:
            gas_tank_type: str = entry.get("Gas Tank")
            if selected_value == gas_tank_type: # get the values in the body lines for final adjustment
                gas_gallon_qty: int = int(self.entry_gas_gallon_qty.get())
                gas_tank_cost = entry.get("Cost")
                gas_tank_weight = entry.get("Weight")
                gas_tank_dp = entry.get("DP")
                self.label_hidden_gas_tank_cost.configure(text=str(gas_tank_cost))
                self.label_hidden_gas_tank_weight.configure(text=str(gas_tank_weight))
                self.label_hidden_gas_tank_dp.configure(text=str(gas_tank_dp))

                if gas_gallon_qty > 0 and gas_tank_cost > 0:
                    new_gas_tank_cost = (gas_tank_cost + 40) * gas_gallon_qty
                    new_gas_tank_weight = (gas_tank_weight + 5) * gas_gallon_qty

                    self.label_gas_tank_cost.configure(text=str(new_gas_tank_cost))
                    self.label_gas_tank_weight.configure(text=str(new_gas_tank_weight))
                    self.label_gas_tank_dp.configure(text=str(gas_tank_dp))
                    self.recalculate()
                else: #zero out the numbers
                    self.label_gas_tank_cost.configure(text=str(0))
                    self.label_gas_tank_weight.configure(text=str(0))
                    self.label_gas_tank_dp.configure(text=str(0))

                return #exit now

    def on_changed_entry_gas_gallon_qty(self, *args):
        gas_gallon_qty = self.var_gas_gallon_qty.get()
        if gas_gallon_qty > 0:
            gas_tank_cost = int(self.label_hidden_gas_tank_cost.cget("text"))
            gas_tank_weight = int(self.label_hidden_gas_tank_weight.cget("text"))
            gas_tank_dp = int(self.label_hidden_gas_tank_dp.cget("text"))
            gas_tank_cost = (gas_tank_cost + 40) * gas_gallon_qty
            gas_tank_weight = (gas_tank_weight + 5) * gas_gallon_qty
            gas_tank_spaces = math.ceil((gas_gallon_qty - 5) / 15)
            self.label_gas_tank_cost.configure(text=str(gas_tank_cost))
            self.label_gas_tank_weight.configure(text=str(gas_tank_weight))
            self.label_gas_tank_dp.configure(text=str(gas_tank_dp))
            self.label_gas_tank_space.configure(text=str(gas_tank_spaces))
        else:
            self.label_gas_tank_cost.configure(text=str(0))
            self.label_gas_tank_weight.configure(text=str(0))
            self.label_gas_tank_dp.configure(text=str(0))
            self.label_gas_tank_space.configure(text=str(0))
        self.recalculate()

    def on_changed_front_tire_qty(self, *args):
        front_tire_qty = self.var_front_tire_qty.get()
        self.var_front_tire_qty.set(value=front_tire_qty)
        self.front_tire_adjustment()
        self.recalculate()

    def on_changed_rear_tire_qty(self, *args):
        rear_tire_qty = self.var_rear_tire_qty.get()
        self.var_rear_tire_qty.set(value=rear_tire_qty)
        self.rear_tire_adjustment()
        self.recalculate()

    def on_changed_driver_gunner_qty(self, *args):
        driver_gunner_qty = self.var_driver_gunner_qty.get()
        passenger_qty = self.var_passenger_qty.get()
        self.var_driver_gunner_qty.set(value=driver_gunner_qty)
        self.label_driver_gunner_weight.configure(text=str(150*(driver_gunner_qty + passenger_qty)))
        self.label_driver_gunner_space.configure(text=str(driver_gunner_qty * 2 + passenger_qty))
        self.recalculate()

    def on_changed_outer_armor_qty(self, *args):
        body_armor_cost:    float = float(self.label_hidden_body_armor_cost.cget("text")) #this could be a decimal
        body_armor_weight:  float = float(self.label_hidden_body_armor_weight.cget("text")) #this could be a decimal
        outer_armor_cost:   float = float(self.label_hidden_outer_armor_cost.cget("text"))
        outer_armor_weight: float = float(self.label_hidden_outer_armor_weight.cget("text"))
        try:
            outer_armor_qty: int = int(val) if (val := str(self.var_outer_armor_qty.get()).strip()).isdigit() else 0
        except tk.TclError:
            outer_armor_qty = 0
        self.var_outer_armor_qty.set(value=outer_armor_qty)
        total_armor_cost = outer_armor_cost * outer_armor_qty * body_armor_cost
        self.label_outer_armor_cost.configure(text=self.float_to_str(total_armor_cost))
        self.label_outer_armor_weight.configure(text=self.float_to_str(outer_armor_weight * outer_armor_qty * body_armor_weight))
        self.on_changed_entry_outer_armor_allocation_qty(None)
        self.recalculate()

    def on_changed_inner_armor_qty(self, *args):
        body_armor_cost:    float = float(self.label_hidden_body_armor_cost.cget("text")) #this could be a decimal
        body_armor_weight:  float = float(self.label_hidden_body_armor_weight.cget("text")) #this could be a decimal
        inner_armor_cost:   float = float(self.label_hidden_inner_armor_cost.cget("text"))
        inner_armor_weight: float = float(self.label_hidden_inner_armor_weight.cget("text"))
        try:
            inner_armor_qty = self.var_inner_armor_qty.get()
        except tk.TclError:
            inner_armor_qty = 0
        self.var_inner_armor_qty.set(value=inner_armor_qty)
        total_armor_cost = inner_armor_cost * inner_armor_qty * body_armor_cost
        printed_armor_cost: str = self.float_to_str(total_armor_cost)
        self.label_inner_armor_cost.configure(text=printed_armor_cost)
        printed_armor_weight: str = self.float_to_str(inner_armor_weight * inner_armor_qty * body_armor_weight)
        self.label_inner_armor_weight.configure(text=self.float_to_str(printed_armor_weight))
        self.on_changed_entry_inner_armor_allocation_qty(None)
        self.recalculate()

    def var_front_tire_steelbelting_changed(self, *args):
        self.on_select_front_tires()

    def var_front_tire_radial_changed(self, *args):
        self.var_front_tire_racing_slick.set(0) #turn off slicks if radials are selected
        self.var_front_tire_offroad.set(0)      #turn off off-road if radials are selected
        self.on_select_front_tires()

    def var_front_tire_fireproof_changed(self, *args):
        self.on_select_front_tires()

    def var_front_tire_offroad_changed(self, *args):
        self.var_front_tire_racing_slick.set(0) #turn off slicks if offroad are selected
        self.var_front_tire_radial.set(0)      #turn off radials if offroad are selected
        self.on_select_front_tires()

    def var_front_tire_racing_slick_changed(self, *args):
        self.var_front_tire_offroad.set(0)      #turn off offroad if racing slicks are selected
        self.var_front_tire_radial.set(0)      #turn off radials if racing slicks are selected
        self.on_select_front_tires()

    def on_select_front_tires(self, *args):
        selected_value = self.selected_front_tire.get()
        for entry in self.tires_list:
            tire_type: str = entry.get("Tires")
            if selected_value == tire_type: # get the values in the body lines for final adjustment
                tire_cost = int(entry.get("Cost"))
                tire_weight = int(entry.get("Weight"))
                tire_dp = int(entry.get("DP"))
                self.label_hidden_front_tire_cost.configure(text=str(tire_cost))
                self.label_hidden_front_tire_weight.configure(text=str(tire_weight))
                self.label_hidden_front_tire_dp.configure(text=str(tire_dp))
                self.front_tire_adjustment()
                self.recalculate()
                return #exit now

    def var_rear_tire_steelbelting_changed(self, *args):
        self.on_select_rear_tires()

    def var_rear_tire_radial_changed(self, *args):
        self.var_rear_tire_racing_slick.set(0) #turn off slicks if radials are selected
        self.var_rear_tire_offroad.set(0)      #turn off off-road if radials are selected
        self.on_select_rear_tires()

    def var_rear_tire_fireproof_changed(self, *args):
        self.on_select_rear_tires()

    def var_rear_tire_offroad_changed(self, *args):
        self.var_rear_tire_racing_slick.set(0) #turn off slicks if offroad are selected
        self.var_rear_tire_radial.set(0)      #turn off radials if offroad are selected
        self.on_select_rear_tires()

    def var_rear_tire_racing_slick_changed(self, *args):
        self.var_rear_tire_offroad.set(0)      #turn off offroad if racing slicks are selected
        self.var_rear_tire_radial.set(0)      #turn off radials if racing slicks are selected
        self.on_select_rear_tires()

    def on_select_rear_tires(self, *args):
        selected_value = self.selected_rear_tire.get()
        for entry in self.tires_list:
            tire_type: str = entry.get("Tires")
            if selected_value == tire_type: # get the values in the body lines for final adjustment
                tire_cost = int(entry.get("Cost"))
                tire_weight = int(entry.get("Weight"))
                tire_dp = int(entry.get("DP"))
                self.label_hidden_rear_tire_cost.configure(text=str(tire_cost))
                self.label_hidden_rear_tire_weight.configure(text=str(tire_weight))
                self.label_hidden_rear_tire_dp.configure(text=str(tire_dp))
                self.rear_tire_adjustment()

                self.recalculate()
                return #exit now

    def on_select_outer_armor(self, *args):
        selected_value = self.selected_outer_armor.get()
        for entry in self.outer_armor_list:
        #  "Weight": "0",   "Abbr": "None"}
            armor_type: str = entry.get("Outer Armor")
            if selected_value == armor_type:
                self.label_hidden_outer_armor_selection.configure(text=armor_type)
                outer_armor_cost = float(entry.get("Cost"))
                sloped_armor_adjustment = self.var_sloped_armor.get()
                outer_armor_cost = outer_armor_cost + outer_armor_cost * sloped_armor_adjustment * 0.1
                outer_armor_weight = float(entry.get("Weight"))
                self.label_hidden_outer_armor_cost.configure(text=str(outer_armor_cost))
                self.label_hidden_outer_armor_weight.configure(text=str(outer_armor_weight))
                body_armor_cost:    float = float(self.label_hidden_body_armor_cost.cget("text")) #this could be a decimal
                body_armor_weight:  float = float(self.label_hidden_body_armor_weight.cget("text")) #this could be a decimal
                outer_armor_qty = self.var_outer_armor_qty.get()
                total_armor_cost = outer_armor_cost * outer_armor_qty * body_armor_cost
                self.label_outer_armor_cost.configure(text=self.float_to_str(total_armor_cost))
                self.label_outer_armor_weight.configure(text=self.float_to_str(outer_armor_weight * outer_armor_qty * body_armor_weight))
                self.recalculate()

    def on_select_inner_armor(self, *args):
        selected_value = self.selected_inner_armor.get()
        for entry in self.inner_armor_list:
        #  "Weight": "0",   "Abbr": "None"}
            armor_type: str = entry.get("Inner Armor")
            if selected_value == armor_type:
                self.label_hidden_inner_armor_selection.configure(text=armor_type)
                inner_armor_cost = float(entry.get("Cost"))
                sloped_armor_adjustment = self.var_sloped_armor.get()
                inner_armor_cost = inner_armor_cost + inner_armor_cost * sloped_armor_adjustment * 0.1
                inner_armor_weight = float(entry.get("Weight"))
                self.label_hidden_inner_armor_cost.configure(text=str(inner_armor_cost))
                self.label_hidden_inner_armor_weight.configure(text=str(inner_armor_weight))
                body_armor_cost:    float = float(self.label_hidden_body_armor_cost.cget("text")) #this could be a decimal
                body_armor_weight:  float = float(self.label_hidden_body_armor_weight.cget("text")) #this could be a decimal
                inner_armor_qty = self.var_inner_armor_qty.get()
                printed_armor_cost: str = self.float_to_str(inner_armor_cost * inner_armor_qty * body_armor_cost)
                self.label_inner_armor_cost.configure(text=printed_armor_cost)
                printed_armor_weight: str = self.float_to_str(inner_armor_weight * inner_armor_qty * body_armor_weight)
                self.label_inner_armor_weight.configure(text=self.float_to_str(printed_armor_weight))
                self.recalculate()

    def recalculate(self):
        """Recalculate all the labels for cost, weight and space.  Expect this to be done each time something changes"""
        if self.is_init is True:
            return #we don't need to run recalculate if were still intializing
        engine_type: str = self.label_engine_type.cget("text")
        if engine_type == "Gas":
            self.check_engine_gas_super_charger.config(state="normal")
            self.check_engine_gas_vp_turbo.config(state="normal")
            self.check_engine_gas_tube_headers.config(state="normal")
            self.check_engine_gas_blue_print.config(state="normal")
            self.check_engine_gas_turbo.config(state="normal")
            self.var_engine_electric_super_conductors.set(0)
            self.var_engine_electric_platnium_catalysts.set(0)
            self.var_engine_electric_extra_power_cells.set(0)
            self.check_engine_electric_super_conductors.config(state="disabled")
            self.check_engine_electric_platnium_catalysts.config(state="disabled")
            self.check_engine_electric_extra_power_cells.config(state="disabled")
        elif engine_type == "Electric": #electric options
            self.var_engine_gas_super_charger.set(0)
            self.check_engine_gas_super_charger.config(state="disabled")

            self.var_engine_gas_vp_turbo.set(0)
            self.check_engine_gas_vp_turbo.config(state="disabled")

            self.var_engine_gas_tube_headers.set(0)
            self.check_engine_gas_tube_headers.config(state="disabled")

            self.var_engine_gas_blue_print.set(0)
            self.check_engine_gas_blue_print.config(state="disabled")

            self.var_engine_gas_turbo.set(0)
            self.check_engine_gas_turbo.config(state="disabled")

            self.check_engine_electric_super_conductors.config(state="normal")
            self.check_engine_electric_platnium_catalysts.config(state="normal")
            self.check_engine_electric_extra_power_cells.config(state="normal")
        else: #turn off everything
            self.var_engine_gas_super_charger.set(0)
            self.check_engine_gas_super_charger.config(state="disabled")

            self.var_engine_gas_vp_turbo.set(0)
            self.check_engine_gas_vp_turbo.config(state="disabled")

            self.var_engine_gas_tube_headers.set(0)
            self.check_engine_gas_tube_headers.config(state="disabled")

            self.var_engine_gas_blue_print.set(0)
            self.check_engine_gas_blue_print.config(state="disabled")

            self.var_engine_gas_turbo.set(0)
            self.check_engine_gas_turbo.config(state="disabled")

            self.var_engine_electric_super_conductors.set(0)
            self.var_engine_electric_platnium_catalysts.set(0)
            self.var_engine_electric_extra_power_cells.set(0)
            self.check_engine_electric_super_conductors.config(state="disabled")
            self.check_engine_electric_platnium_catalysts.config(state="disabled")
            self.check_engine_electric_extra_power_cells.config(state="disabled")
            #########################

        body_cost:              int = int(self.label_body_cost.cget("text"))
        body_weight:            int = int(self.label_body_weight.cget("text"))
        body_spaces:            int = int(self.label_body_spaces.cget("text"))
        modificiation_cost:     int = int(self.label_modificiation_cost.cget("text"))
        modificiation_weight:   int = int(self.label_modificiation_weight.cget("text"))
        modificiation_space:    int = int(self.label_modificiation_space.cget("text"))
        chassis_cost:           int = int(self.label_chassis_cost.cget("text"))
        six_wheel_chassis_cost: int = int(self.var_six_wheel_chassis.get()) * 100
        suspension_cost:        int = int(self.label_suspension_cost.cget("text"))
        engine_cost:            int = int(self.label_engine_cost.cget("text"))
        engine_weight:          int = int(self.label_engine_weight.cget("text"))
        engine_space:           int = int(self.label_engine_space.cget("text"))
        engine_power_factors:   int = int(self.label_engine_pf.cget("text"))
        engine_mpg:             int = int(self.label_engine_mpg.cget("text"))

        engine_mod_cost, engine_mod_weight, engine_mod_space, engine_mod_power_factors, engine_mod_mpg, engine_mod_dp, engine_mod_accel = self.engine_mods_recalc()

        self.label_engine_mod_cost.configure(text=str(engine_mod_cost))
        self.label_engine_mod_weight.configure(text=str(engine_mod_weight))
        self.label_engine_mod_space.configure(text=str(engine_mod_space))
        self.label_engine_mod_dp.configure(text=str(engine_mod_dp))
        self.label_engine_mod_pf.configure(text=str(engine_mod_power_factors))
        self.label_engine_mod_mpg.configure(text=str(engine_mod_mpg))

        gas_tank_cost   = int(self.label_gas_tank_cost.cget("text"))
        gas_tank_weight = int(self.label_gas_tank_weight.cget("text"))
        gas_tank_space  = int(self.label_gas_tank_space.cget("text"))

        front_tire_cost   = int(self.label_front_tire_cost.cget("text"))
        front_tire_weight = int(self.label_front_tire_weight.cget("text"))
        rear_tire_cost    = int(self.label_rear_tire_cost.cget("text"))
        rear_tire_weight  = int(self.label_rear_tire_weight.cget("text"))

        driver_gunner_weight: int = int(self.label_driver_gunner_weight.cget("text"))
        driver_gunner_space:  int = int(self.label_driver_gunner_space.cget("text"))

        outer_armor_cost:   float = float(self.label_outer_armor_cost.cget("text"))
        outer_armor_weight: float = float(self.label_outer_armor_weight.cget("text"))
        inner_armor_cost:   float = float(self.label_inner_armor_cost.cget("text"))
        inner_armor_weight: float = float(self.label_inner_armor_weight.cget("text"))

        # This single loop processes all 10 weapon rows automatically
        weapons_data = []
        
        loop_max = len(self.weapon_cost_label_objects)
        for loop_index in range(0, loop_max):
            weapon_cost_obj = self.weapon_cost_label_objects[loop_index]
            weapon_weight_obj = self.weapon_weight_label_objects[loop_index]
            weapon_space_obj = self.weapon_spaces_label_objects[loop_index]
            weapon_cost_str = weapon_cost_obj.cget("text")
            weapon_weight_str = weapon_weight_obj.cget("text")
            weapon_space_str = weapon_space_obj.cget("text")

            wpn_stats = {
                "cost":        float(weapon_cost_str),
                "weight":      float(weapon_weight_str),
                "space":       float(weapon_space_str),
            } #mag cost and weight is already include in the ammo cost and weight, don't include it here as well
            weapons_data.append(wpn_stats)

        #active_links_cost = 0
        #for i in range(self.link_rows_count):
        #    total_items_linked = 0
            
        #    for item_str in self.link_selections[i]:
        #        # Look for a number inside a '(Qty: X)' pattern
        #        if "(Qty:" in item_str:
        #            try:
        #                # Extract the text between '(Qty:' and the closing ')'
        #                qty_part = item_str.split("(Qty:")[1].split(")")[0].strip()
        #                total_items_linked += int(qty_part)
        #            except (IndexError, ValueError):
        #                total_items_linked += 1 # Safety fallback if parsing fails
        #        else:
        #            total_items_linked += 1 # Accessories / Boosters count as 1 item
            
            # A link is mathematically valid and charged $50 if managing 2 or more absolute units
        #    if total_items_linked >= 2:
        #        active_links_cost += 50

        #active_bt_cost = 0
        #for i in range(self.bt_rows_count):
        #    total_items_triggered = 0
            
        #    for item_str in self.bt_selections[i]:
        #        if "(Qty:" in item_str:
        #            try:
        #                qty_part = item_str.split("(Qty:")[1].split(")")[0].strip()
        #                total_items_triggered += int(qty_part)
        #            except (IndexError, ValueError):
        #                total_items_triggered += 1
        #        else:
        #            total_items_triggered += 1 # Accessories / Boosters / Links count as 1
            
        #    # A bumper trigger is active and charged $50 if it triggers 1 or more total units
        #    if total_items_triggered >= 1:
        #        active_bt_cost += 50

        # This single loop processes all 30 accessory slots automatically
        #accessories_data = []
        
        #for i in range(1, 31):
        #    acc_stats = {
        #        "cost":   self._safe_parse_label(f"label_accessories_{i}_cost", float),
        #        "weight": self._safe_parse_label(f"label_accessories_{i}_weight", float),
        #        "space":  self._safe_parse_label(f"label_accessories_{i}_space", float)
        #    }
        #    accessories_data.append(acc_stats)

        # This single loop processes all 5 component armor configurations automatically
        #component_armor_data = []
        
        #for i in range(1, 6):
        #    ca_stats = {
        #        "cost":   self._safe_parse_label(f"label_component_armor_{i}_cost", float),
        #        "weight": self._safe_parse_label(f"label_component_armor_{i}_weight", float),
        #        "space":  self._safe_parse_label(f"label_component_armor_{i}_space", float)
        #    }
        #    component_armor_data.append(ca_stats)

        # This single loop processes all 5 rocket booster clusters automatically
        #rocket_booster_data = []
        
        #for i in range(1, 6):
        #    rb_stats = {
        #        "cost":   self._safe_parse_label(f"label_rocket_booster_{i}_cost", float),
        #        "weight": self._safe_parse_label(f"label_rocket_booster_{i}_weight", float),
        #        "space":  self._safe_parse_label(f"label_rocket_booster_{i}_space", float)
        #    }
        #    rocket_booster_data.append(rb_stats)

        # This single loop processes all 10 personal equipment listings automatically
        #personal_equipment_data = []
        
        #for i in range(1, 11):
        #    pe_stats = {
        #        "cost":   self._safe_parse_label(f"label_personal_equipment_{i}_cost", float),
        #        "weight": self._safe_parse_label(f"label_personal_equipment_{i}_weight", float),
        #        "space":  self._safe_parse_label(f"label_personal_equipment_{i}_space", float)
        #    }
        #    personal_equipment_data.append(pe_stats)


        cost_list: list = []
        cost_list.append(body_cost)
        cost_list.append(modificiation_cost)
        cost_list.append(chassis_cost)
        cost_list.append(six_wheel_chassis_cost)
        cost_list.append(suspension_cost)
        cost_list.append(engine_cost)
        cost_list.append(engine_mod_cost)
        #cost_list.append(engine_carb_cost)
        cost_list.append(gas_tank_cost)
        cost_list.append(front_tire_cost)
        cost_list.append(rear_tire_cost)
        cost_list.append(outer_armor_cost)
        cost_list.append(inner_armor_cost)

        # Instantly sum up your grand totals for the whole car
        total_weapon_cost   = sum(w["cost"] for w in weapons_data)
        cost_list.append(total_weapon_cost)
        #cost_list.append(active_links_cost)
        #cost_list.append(active_bt_cost)

        # Sum up accessory totals for the vehicle instantly
        #total_accessory_cost   = sum(a["cost"] for a in accessories_data)
        #cost_list.append(total_accessory_cost)

        # Sum up component armor totals instantly
        #total_component_armor_cost   = sum(c["cost"] for c in component_armor_data)
        #cost_list.append(total_component_armor_cost)

        # Sum up rocket booster totals instantly
        #total_rocket_booster_cost   = sum(r["cost"] for r in rocket_booster_data)
        #cost_list.append(total_rocket_booster_cost)

        # Sum up personal equipment totals instantly
        #total_personal_equipment_cost   = sum(p["cost"] for p in personal_equipment_data)
        #cost_list.append(total_personal_equipment_cost)

        weight_list: list = []
        weight_list.append(body_weight)
        weight_list.append(modificiation_weight)
        weight_list.append(engine_weight)
        weight_list.append(engine_mod_weight)
        weight_list.append(gas_tank_weight)
        weight_list.append(front_tire_weight)
        weight_list.append(rear_tire_weight)
        weight_list.append(outer_armor_weight)
        weight_list.append(inner_armor_weight)
        weight_list.append(driver_gunner_weight)
        #weight_list.append(passenger_weight)
        total_weapon_weight = sum(w["weight"] for w in weapons_data)
        weight_list.append(total_weapon_weight)
        #weight_list.append(total_ammo_weight)
        #total_accessory_weight = sum(a["weight"] for a in accessories_data)
        #weight_list.append(total_accessory_weight)

        #total_component_armor_weight = sum(c["weight"] for c in component_armor_data)
        #weight_list.append(total_component_armor_weight)

        #total_rocket_booster_weight = sum(r["weight"] for r in rocket_booster_data)
        #weight_list.append(total_rocket_booster_weight)

        #total_personal_equipment_weight = sum(p["weight"] for p in personal_equipment_data)
        #weight_list.append(total_personal_equipment_weight)

        space_list: list = []
        space_list.append(modificiation_space)
        space_list.append(engine_space)
        space_list.append(engine_mod_space)
        space_list.append(gas_tank_space)
        space_list.append(driver_gunner_space)
        #space_list.append(passenger_space)
        total_weapon_space  = sum(w["space"] for w in weapons_data)
        space_list.append(total_weapon_space)
        #total_accessory_space  = sum(a["space"] for a in accessories_data)
        #space_list.append(total_accessory_space)

        #total_component_armor_space  = sum(c["space"] for c in component_armor_data)
        #space_list.append(total_component_armor_space)

        #total_rocket_booster_space  = sum(r["space"] for r in rocket_booster_data)
        #space_list.append(total_rocket_booster_space)

        #total_personal_equipment_space  = sum(p["space"] for p in personal_equipment_data)
        #space_list.append(total_personal_equipment_space) #it's not likely that personal equipment *has* vehicle spaces, but it's here

        total_cost:   int = sum(cost_list)
        total_weight: int = sum(weight_list)
        total_spaces: int = body_spaces - sum(space_list)
        total_power_factors: int = engine_power_factors + engine_mod_power_factors# + engine_carb_power_factors
        total_mpg: int = engine_mpg + engine_mod_mpg

        top_speed: int = 0
        accel: int = 0
        max_accel: int = 0
        mile_range: int = 0
        if engine_type == "Gas":
            gas_gallon_qty = self.var_gas_gallon_qty.get()
            mile_range = total_mpg * gas_gallon_qty
            top_speed = (240 * total_power_factors) / (total_power_factors + total_weight)
        elif engine_type == "Electric":
            top_speed = (360 * total_power_factors) / (total_power_factors + total_weight)
            mile_range = 200
        else:
            top_speed = 0
        if "Streamlined" in self.selected_modifications.get():
            top_speed = top_speed * 1.1 #10% increase
        top_speed = math.floor(top_speed / 2.5) * 2.5 # round to the nearest 2.5 value

        max_weight_top_speed: int = 0
        max_weight = int(self.label_max_weight.cget("text"))
        if engine_type == "Gas":
            max_weight_top_speed = (240 * total_power_factors) / (total_power_factors + max_weight)
        elif engine_type == "Electric":
            max_weight_top_speed = (360 * total_power_factors) / (total_power_factors + max_weight)
        else:
            max_weight_top_speed = 0
        if "Streamlined" in self.selected_modifications.get():
            max_weight_top_speed = max_weight_top_speed * 1.1 #10% increase
        max_weight_top_speed = math.floor(max_weight_top_speed / 2.5) * 2.5 # round to the nearest 2.5 value

        if total_power_factors >= max_weight:
            max_accel = 15 + engine_mod_accel
        elif total_power_factors * 2 >= max_weight:
            max_accel = 10 + engine_mod_accel
        elif total_power_factors * 3 >= max_weight:
            max_accel = 5 + engine_mod_accel
        else:
            max_accel = 0

        if total_power_factors >= total_weight:
            accel = 15 + engine_mod_accel
        elif total_power_factors * 2 >= total_weight:
            accel = 10 + engine_mod_accel
        elif total_power_factors * 3 >= total_weight:
            accel = 5 + engine_mod_accel
        else:
            accel = 0

        self.label_range.configure(text=str(mile_range))

        #run decimal conversions here
        self.label_total_cost.configure(text=self.float_to_str(total_cost))
        self.label_total_weight.configure(text=self.float_to_str(total_weight))
        self.label_total_space.configure(text=self.float_to_str(total_spaces))
        self.label_final_engine_mpg.configure(text=self.float_to_str(total_mpg))
        self.label_total_power_factors.configure(text=self.float_to_str(total_power_factors))
        self.label_top_speed.configure(text=self.float_to_str(top_speed))
        self.label_max_weight_top_speed.configure(text=self.float_to_str(max_weight_top_speed))
        self.label_accel.configure(text=self.float_to_str(accel))
        self.label_max_accel.configure(text=self.float_to_str(max_accel))

        facings_text: str = self.facing_compilations()
        self.label_valid_spaces.configure(text=facings_text)
        weight_text: str = ""
        space_text: str = ""
        if total_weight > max_weight:
            weight_text = "DESIGN OVER WEIGHT"
        self.label_valid_weight.configure(text=weight_text)
        if total_spaces < 0.0:
            space_text = "DESIGN HAS TOO MANY SPACES USED"
            self.label_valid_spaces.configure(text=space_text)
        self.update_link_dropdowns()

    def float_to_str(self, input_value: float) -> str:
        """Given a float input, determine the best format for display the value as a string"""
        return_string: str = ""
        if isinstance(input_value, str): #this should be a float, but whatever
            return_string = input_value
        else:
            if input_value.is_integer():
                return_string = str(int(input_value))
            else:
                return_string = f"{input_value:.2f}"
                return_number = float(return_string)
                if return_number == 0.01:
                    return_number = 0
                if return_number.is_integer():
                    return_string = str(int(return_number))
        return return_string

    def engine_mods_recalc(self):
        engine_cost = int(self.label_engine_cost.cget("text"))
        engine_power_factors = int(self.label_engine_pf.cget("text"))
        engine_weight = int(self.label_engine_weight.cget("text"))
        engine_dp = int(self.label_engine_dp.cget("text"))
        engine_mod_cost:          float = 0.0
        engine_mod_weight:        float = 0.0
        engine_mod_space:         float = 0.0
        engine_mod_power_factors: float = 0.0
        engine_mod_mpg:           float = 0.0
        engine_mod_accel:         float = 0.0
        engine_mod_dp:            float = 0.0
        total_engine_mod_pf:      float = 0.0
        total_engine_mod_cost:    float = 0.0

        if self.var_engine_gas_super_charger.get() == 1:
            engine_mod_space = engine_mod_space + 1
            engine_mod_weight = engine_weight * 0.2
            engine_mod_power_factors = engine_power_factors * 0.4
            engine_mod_cost = 3000 + engine_mod_power_factors
            total_engine_mod_cost = total_engine_mod_cost + engine_mod_cost
            total_engine_mod_pf = total_engine_mod_pf + engine_mod_power_factors
            engine_mod_accel = engine_mod_accel + 5
            engine_mod_mpg = engine_mod_mpg - 1
        if self.var_engine_gas_vp_turbo.get() == 1:
            engine_mod_power_factors = engine_power_factors * 0.25
            engine_mod_cost = 2000 + engine_mod_power_factors
            total_engine_mod_pf = total_engine_mod_pf + engine_mod_power_factors
            engine_mod_accel = engine_mod_accel + 5
            total_engine_mod_cost = total_engine_mod_cost + engine_mod_cost
        if self.var_engine_gas_tube_headers.get() == 1:
            engine_mod_cost = engine_cost * 0.2
            engine_mod_power_factors = engine_power_factors * 0.05
            total_engine_mod_pf = total_engine_mod_pf + engine_mod_power_factors
            total_engine_mod_cost = total_engine_mod_cost + engine_mod_cost
        if self.var_engine_gas_blue_print.get() == 1:
            engine_mod_cost = engine_cost * 0.5
            engine_mod_power_factors = engine_power_factors * 0.1
            total_engine_mod_pf = total_engine_mod_pf + engine_mod_power_factors
            total_engine_mod_cost = total_engine_mod_cost + engine_mod_cost
        if self.var_engine_gas_turbo.get() == 1:
            engine_mod_power_factors = engine_power_factors * 0.25
            engine_mod_cost = 1000 + engine_mod_power_factors
            total_engine_mod_pf = total_engine_mod_pf + engine_mod_power_factors
            engine_mod_accel = engine_mod_accel + 5
            total_engine_mod_cost = total_engine_mod_cost + engine_mod_cost
        if self.var_engine_electric_super_conductors.get() == 1:
            engine_mod_cost = engine_cost * 0.5
            total_engine_mod_pf = total_engine_mod_pf + engine_power_factors * 0.1
            total_engine_mod_cost = total_engine_mod_cost + engine_mod_cost
        if self.var_engine_electric_platnium_catalysts.get() == 1:
            engine_mod_cost = engine_cost * 0.2
            total_engine_mod_pf = total_engine_mod_pf + engine_power_factors * 0.05
            total_engine_mod_cost = total_engine_mod_cost + engine_mod_cost
        if self.var_engine_electric_extra_power_cells.get() == 1:
            engine_mod_cost = engine_cost * 0.25
            engine_mod_weight = engine_weight * 0.25
            engine_mod_dp = engine_mod_dp + 0.1
            engine_mod_space = engine_mod_space + 0.1
            total_engine_mod_cost = total_engine_mod_cost + engine_mod_cost

        engine_mod_dp = engine_mod_dp * engine_dp

        return int(total_engine_mod_cost), int(engine_mod_weight), int(engine_mod_space), int(total_engine_mod_pf), int(engine_mod_mpg), int(engine_mod_dp), int(engine_mod_accel)

    def on_button_gas_qty_up(self, *args):
        gas_gallon_qty = self.var_gas_gallon_qty.get()
        gas_gallon_qty = gas_gallon_qty + 1
        self.var_gas_gallon_qty.set(value=gas_gallon_qty)

        if gas_gallon_qty > 0:
            gas_tank_cost = int(self.label_hidden_gas_tank_cost.cget("text"))
            gas_tank_weight = int(self.label_hidden_gas_tank_weight.cget("text"))
            gas_tank_dp = int(self.label_hidden_gas_tank_dp.cget("text"))
            gas_tank_cost = (gas_tank_cost + 40) * gas_gallon_qty
            gas_tank_weight = (gas_tank_weight + 5) * gas_gallon_qty
            self.label_gas_tank_cost.configure(text=str(gas_tank_cost))
            self.label_gas_tank_weight.configure(text=str(gas_tank_weight))
            self.label_gas_tank_dp.configure(text=str(gas_tank_dp))
        self.recalculate()

    def on_button_gas_qty_down(self, *args):
        gas_gallon_qty = self.var_gas_gallon_qty.get()
        gas_gallon_qty = max(gas_gallon_qty - 1, 0)
        self.var_gas_gallon_qty.set(value=gas_gallon_qty)

        if gas_gallon_qty > 0:
            gas_tank_cost = int(self.label_hidden_gas_tank_cost.cget("text"))
            gas_tank_weight = int(self.label_hidden_gas_tank_weight.cget("text"))
            gas_tank_dp = int(self.label_hidden_gas_tank_dp.cget("text"))
            gas_tank_cost = (gas_tank_cost + 40) * gas_gallon_qty
            gas_tank_weight = (gas_tank_weight + 5) * gas_gallon_qty
            self.label_gas_tank_cost.configure(text=str(gas_tank_cost))
            self.label_gas_tank_weight.configure(text=str(gas_tank_weight))
            self.label_gas_tank_dp.configure(text=str(gas_tank_dp))
        else:
            self.label_gas_tank_cost.configure(text=str(0))
            self.label_gas_tank_weight.configure(text=str(0))
            self.label_gas_tank_dp.configure(text=str(0))
        self.recalculate()

    def on_button_front_tire_qty_up(self, *args):
        front_tire_qty = self.var_front_tire_qty.get()
        front_tire_qty = front_tire_qty + 1
        self.var_front_tire_qty.set(value=front_tire_qty)
        #self.front_tire_adjustment()
        self.recalculate()

    def on_button_front_tire_qty_down(self, *args):
        front_tire_qty = self.var_front_tire_qty.get()
        front_tire_qty = max(front_tire_qty - 1, 0)
        self.var_front_tire_qty.set(value=front_tire_qty)
        #self.front_tire_adjustment()
        self.recalculate()

    def on_button_rear_tire_qty_up(self, *args):
        rear_tire_qty = self.var_rear_tire_qty.get()
        rear_tire_qty = rear_tire_qty + 1
        self.var_rear_tire_qty.set(value=rear_tire_qty)
        #self.rear_tire_adjustment()
        self.recalculate()

    def on_button_rear_tire_qty_down(self, *args):
        rear_tire_qty = self.var_rear_tire_qty.get()
        rear_tire_qty = max(rear_tire_qty - 1, 0)
        self.var_rear_tire_qty.set(value=rear_tire_qty)
        #self.rear_tire_adjustment()
        self.recalculate()

    def on_button_driver_gunner_qty_up(self, *args):
        driver_gunner_qty = self.var_driver_gunner_qty.get()
        driver_gunner_qty = driver_gunner_qty + 1
        self.var_driver_gunner_qty.set(value=driver_gunner_qty)

    def on_button_driver_gunner_qty_down(self, *args):
        driver_gunner_qty = self.var_driver_gunner_qty.get()
        driver_gunner_qty = max(driver_gunner_qty - 1, 0)
        self.var_driver_gunner_qty.set(value=driver_gunner_qty)

    def on_button_passenger_qty_up(self, *args):
        passenger_qty = self.var_passenger_qty.get()
        passenger_qty = passenger_qty + 1
        self.var_passenger_qty.set(value=passenger_qty)

    def on_button_passenger_qty_down(self, *args):
        passenger_qty = self.var_passenger_qty.get()
        passenger_qty = max(passenger_qty - 1, 0)
        self.var_passenger_qty.set(value=passenger_qty)

    def on_button_outer_armor_qty_up(self, *args):
        body_armor_cost:    float = float(self.label_hidden_body_armor_cost.cget("text")) #this could be a decimal
        body_armor_weight:  float = float(self.label_hidden_body_armor_weight.cget("text")) #this could be a decimal
        outer_armor_cost:   float = float(self.label_hidden_outer_armor_cost.cget("text"))
        sloped_armor_adjustment = self.var_sloped_armor.get()
        outer_armor_cost = outer_armor_cost + outer_armor_cost * sloped_armor_adjustment * 0.1
        outer_armor_weight: float = float(self.label_hidden_outer_armor_weight.cget("text"))
        outer_armor_qty: int = int(self.var_outer_armor_qty.get())
        outer_armor_qty = outer_armor_qty + 1
        self.var_outer_armor_qty.set(value=outer_armor_qty)
        total_armor_cost = outer_armor_cost * outer_armor_qty * body_armor_cost
        self.label_outer_armor_cost.configure(text=self.float_to_str(total_armor_cost))
        self.label_outer_armor_weight.configure(text=self.float_to_str(outer_armor_weight * outer_armor_qty * body_armor_weight))
        self.recalculate()

    def on_button_outer_armor_qty_down(self, *args):
        body_armor_cost:   float = float(self.label_hidden_body_armor_cost.cget("text")) #this could be a decimal
        body_armor_weight: float = float(self.label_hidden_body_armor_weight.cget("text")) #this could be a decimal
        outer_armor_cost:   float = float(self.label_hidden_outer_armor_cost.cget("text"))
        sloped_armor_adjustment = self.var_sloped_armor.get()
        outer_armor_cost = outer_armor_cost + outer_armor_cost * sloped_armor_adjustment * 0.1
        outer_armor_weight: float = float(self.label_hidden_outer_armor_weight.cget("text"))
        outer_armor_qty: int = int(self.var_outer_armor_qty.get())
        outer_armor_qty = max(outer_armor_qty - 1, 0)
        self.var_outer_armor_qty.set(value=outer_armor_qty)
        total_armor_cost = outer_armor_cost * outer_armor_qty * body_armor_cost
        self.label_outer_armor_cost.configure(text=self.float_to_str(total_armor_cost))
        self.label_outer_armor_weight.configure(text=self.float_to_str(outer_armor_weight * outer_armor_qty * body_armor_weight))
        self.recalculate()

    def on_button_inner_armor_qty_up(self, *args):
        body_armor_cost:   float = float(self.label_hidden_body_armor_cost.cget("text")) #this could be a decimal
        body_armor_weight: float = float(self.label_hidden_body_armor_weight.cget("text")) #this could be a decimal
        inner_armor_cost:   float = float(self.label_hidden_inner_armor_cost.cget("text"))
        sloped_armor_adjustment = self.var_sloped_armor.get()
        inner_armor_cost = inner_armor_cost + inner_armor_cost * sloped_armor_adjustment * 0.1
        inner_armor_weight: float = float(self.label_hidden_inner_armor_weight.cget("text"))
        inner_armor_qty = self.var_inner_armor_qty.get()
        inner_armor_qty = inner_armor_qty + 1
        self.var_inner_armor_qty.set(value=inner_armor_qty)
        total_armor_cost = inner_armor_cost * inner_armor_qty * body_armor_cost
        self.label_inner_armor_cost.configure(text=self.float_to_str(total_armor_cost))
        self.label_inner_armor_weight.configure(text=self.float_to_str(inner_armor_weight * inner_armor_qty * body_armor_weight))
        self.recalculate()

    def on_button_inner_armor_qty_down(self, *args):
        body_armor_cost:   float = float(self.label_hidden_body_armor_cost.cget("text")) #this could be a decimal
        body_armor_weight: float = float(self.label_hidden_body_armor_weight.cget("text")) #this could be a decimal
        inner_armor_cost:   float = float(self.label_hidden_inner_armor_cost.cget("text"))
        sloped_armor_adjustment = self.var_sloped_armor.get()
        inner_armor_cost = inner_armor_cost + inner_armor_cost * sloped_armor_adjustment * 0.1
        inner_armor_weight: float = float(self.label_hidden_inner_armor_weight.cget("text"))
        inner_armor_qty = self.var_inner_armor_qty.get()
        inner_armor_qty = max(inner_armor_qty - 1, 0)
        self.var_inner_armor_qty.set(value=inner_armor_qty)
        total_armor_cost = inner_armor_cost * inner_armor_qty * body_armor_cost
        self.label_inner_armor_cost.configure(text=self.float_to_str(total_armor_cost))
        self.label_inner_armor_weight.configure(text=self.float_to_str(inner_armor_weight * inner_armor_qty * body_armor_weight))
        self.recalculate()

    def front_tire_adjustment(self):
        front_tire_qty = self.var_front_tire_qty.get()
        if front_tire_qty > 0:
            tire_cost:   int = int(self.label_hidden_front_tire_cost.cget("text"))
            tire_weight: int = int(self.label_hidden_front_tire_weight.cget("text"))
            tire_dp:     int = int(self.label_hidden_front_tire_dp.cget("text"))

            hidden_body_cycle: int = self.hidden_body_cycle.cget("text")
            var_front_tire_steelbelting: int = self.var_front_tire_steelbelting.get()
            var_front_tire_radial:       int = self.var_front_tire_radial.get()
            var_front_tire_fireproof:    int = self.var_front_tire_fireproof.get()
            var_front_tire_offroad:      int = self.var_front_tire_offroad.get()
            var_front_tire_racing_slick: int = self.var_front_tire_racing_slick.get()
            if hidden_body_cycle == 1:
                tire_weight = tire_weight / 2
            tire_cost_adjustment: float = 0.0
            tire_weight_adjustment: float = 0.0
            tire_dp_adjustment: float = 0.0
            tire_dp_adjustment_raw: int = 0
            #radials only add HC if all four tires are radials.  Slicks add +1 for each matched pair
            tire_hc_adjustment = self.calculate_tire_hc_adjustment(front=True)
            self.label_hidden_front_tire_hc.configure(text=str(tire_hc_adjustment))

            self.hc_addition()
            tire_weight_adjustment_raw: int = 0
            if var_front_tire_steelbelting == 1:
            #Steelbelting .5 .5 .25 0
                tire_cost_adjustment   = tire_cost_adjustment   + 0.5
                tire_weight_adjustment = tire_weight_adjustment + 0.5
                tire_dp_adjustment     = tire_dp_adjustment     + 0.25
            if var_front_tire_radial       == 1:
            #Radial	1.5 .2 -1 1
                tire_cost_adjustment   = tire_cost_adjustment   + 1.5
                tire_weight_adjustment = tire_weight_adjustment + 0.2
                tire_dp_adjustment_raw = tire_dp_adjustment_raw - 1
                tire_hc_adjustment     = tire_hc_adjustment     + 0.5 #radials on front and back required, check if tire quantity is 4, then adjust to +1
            if var_front_tire_fireproof    == 1:
            #Fireproof 1 0 0 0
                tire_cost_adjustment   = tire_cost_adjustment   + 1.0
            if var_front_tire_offroad      == 1:
            #Off-Road .2 +5 0 +1
                tire_cost_adjustment   = tire_cost_adjustment   + 0.2
                tire_weight_adjustment_raw = tire_weight_adjustment_raw + 5
                tire_hc_adjustment     = tire_hc_adjustment     + 0.5 #off-road on front and back required, check if tire quantity is 4, then adjust to +1
            if var_front_tire_racing_slick == 1:
            #Racing Slick 3 1 +1 +2
                tire_cost_adjustment   = tire_cost_adjustment   + 3.0
                tire_weight_adjustment = tire_weight_adjustment + 1
                tire_dp_adjustment_raw = tire_dp_adjustment_raw - 1
                tire_hc_adjustment     = tire_hc_adjustment     + 1.0 #radials on front and back required, check if tire quantity is 4, then adjust to +1

            tire_cost = (tire_cost + tire_cost * tire_cost_adjustment) * front_tire_qty
            tire_weight = ((tire_weight + tire_weight * tire_weight_adjustment) + tire_weight_adjustment_raw) * front_tire_qty
            tire_dp = tire_dp + tire_dp * tire_dp_adjustment + tire_dp_adjustment_raw

            self.label_front_tire_cost.configure(text=str(int(tire_cost)))
            self.label_front_tire_weight.configure(text=str(int(tire_weight)))
            self.label_front_tire_dp.configure(text=str(int(tire_dp)))
        else:
            self.label_front_tire_cost.configure(text=str(0))
            self.label_front_tire_weight.configure(text=str(0))
            self.label_front_tire_dp.configure(text=str(0))
            self.label_hidden_front_tire_hc.configure(text=str(0))
            self.hc_addition()

    def rear_tire_adjustment(self):
        rear_tire_qty = self.var_rear_tire_qty.get()
        if rear_tire_qty > 0:
            tire_cost:   int = int(self.label_hidden_rear_tire_cost.cget("text"))
            tire_weight: int = int(self.label_hidden_rear_tire_weight.cget("text"))
            tire_dp:     int = int(self.label_hidden_rear_tire_dp.cget("text"))

            hidden_body_cycle: int = self.hidden_body_cycle.cget("text")
            var_rear_tire_steelbelting: int = self.var_rear_tire_steelbelting.get()
            var_rear_tire_radial:       int = self.var_rear_tire_radial.get()
            var_rear_tire_fireproof:    int = self.var_rear_tire_fireproof.get()
            var_rear_tire_offroad:      int = self.var_rear_tire_offroad.get()
            var_rear_tire_racing_slick: int = self.var_rear_tire_racing_slick.get()
            if hidden_body_cycle == 1:
                tire_weight = tire_weight / 2
            tire_cost_adjustment: float = 0.0
            tire_weight_adjustment: float = 0.0
            tire_dp_adjustment: float = 0.0
            tire_dp_adjustment_raw: int = 0
            #radials only add HC if all four tires are radials.  Slicks add +1 for each matched pair
            tire_hc_adjustment: float = float(rear_tire_qty * var_rear_tire_radial * 0.25) + (rear_tire_qty * var_rear_tire_racing_slick * 0.5)
            self.label_hidden_rear_tire_hc.configure(text=str(tire_hc_adjustment))
            #radials only add HC if all four tires are radials.  Slicks add +1 for each matched pair
            tire_hc_adjustment = self.calculate_tire_hc_adjustment(front=False)
            self.label_hidden_rear_tire_hc.configure(text=str(tire_hc_adjustment))

            self.hc_addition()
            tire_weight_adjustment_raw: int = 0
            if var_rear_tire_steelbelting == 1:
            #Steelbelting .5 .5 .25 0
                tire_cost_adjustment   = tire_cost_adjustment   + 0.5
                tire_weight_adjustment = tire_weight_adjustment + 0.5
                tire_dp_adjustment     = tire_dp_adjustment     + 0.25
            if var_rear_tire_radial       == 1:
            #Radial	1.5 .2 -1 1
                tire_cost_adjustment   = tire_cost_adjustment   + 1.5
                tire_weight_adjustment = tire_weight_adjustment + 0.2
                tire_dp_adjustment_raw = tire_dp_adjustment_raw - 1
                tire_hc_adjustment     = tire_hc_adjustment     + 0.5 #radials on front and back required, check if tire quantity is 4, then adjust to +1
            if var_rear_tire_fireproof    == 1:
            #Fireproof 1 0 0 0
                tire_cost_adjustment   = tire_cost_adjustment   + 1.0
            if var_rear_tire_offroad      == 1:
            #Off-Road .2 +5 0 +1
                tire_cost_adjustment   = tire_cost_adjustment   + 0.2
                tire_weight_adjustment_raw = tire_weight_adjustment_raw + 5
                tire_hc_adjustment     = tire_hc_adjustment     + 0.5 #off-road on front and back required, check if tire quantity is 4, then adjust to +1
            if var_rear_tire_racing_slick == 1:
            #Racing Slick 3 1 +1 +2
                tire_cost_adjustment   = tire_cost_adjustment   + 3.0
                tire_weight_adjustment = tire_weight_adjustment + 1
                tire_dp_adjustment_raw = tire_dp_adjustment_raw - 1
                tire_hc_adjustment     = tire_hc_adjustment     + 1.0 #radials on front and back required, check if tire quantity is 4, then adjust to +1

            tire_cost = (tire_cost + tire_cost * tire_cost_adjustment) * rear_tire_qty
            tire_weight = ((tire_weight + tire_weight * tire_weight_adjustment) + tire_weight_adjustment_raw) * rear_tire_qty
            tire_dp = tire_dp + tire_dp * tire_dp_adjustment + tire_dp_adjustment_raw

            self.label_rear_tire_cost.configure(text=str(int(tire_cost)))
            self.label_rear_tire_weight.configure(text=str(int(tire_weight)))
            self.label_rear_tire_dp.configure(text=str(int(tire_dp)))
        else:
            self.label_rear_tire_cost.configure(text=str(0))
            self.label_rear_tire_weight.configure(text=str(0))
            self.label_rear_tire_dp.configure(text=str(0))
            self.label_hidden_rear_tire_hc.configure(text=str(0))
            self.hc_addition()

    def calculate_tire_hc_adjustment(self, front: bool) -> float:
        """Calculate the HC contribution for the tire settings"""
        hc_tire_count: int = 0
        hc_partial_tire_count: int = 0
        if front:
            local_tire_qty          = self.var_front_tire_qty.get()
            local_tire_radial       = self.var_front_tire_radial.get()
            local_tire_racing_slick = self.var_front_tire_racing_slick.get()
            local_tire_off_road     = self.var_front_tire_offroad.get()
        else:
            local_tire_qty          = self.var_rear_tire_qty.get()
            local_tire_radial       = self.var_rear_tire_radial.get()
            local_tire_racing_slick = self.var_rear_tire_racing_slick.get()
            local_tire_off_road     = self.var_rear_tire_offroad.get()
        body_type: str = self.selected_body.get()
        if body_type in ["Light Cycle", "Medium Cycle", "Heavy Cycle"]: # two wheels
            hc_tire_count = 2
            hc_partial_tire_count = 1
        elif body_type in ["Light SideCar", "Heavy SideCar"]: # one wheel
            hc_tire_count = 1
            hc_partial_tire_count = 1
        elif body_type in ["Light Trike", "Medium Trike", "Heavy Trike", "x-Hvy Trike"]:
            hc_tire_count = 3
            if front:
                hc_partial_tire_count = 1
            else:
                hc_partial_tire_count = 2
        elif body_type in ["Rev. Light Trike", "Rev. Medium Trike", "Rev. Heavy Trike", "Rev. X-Hvy Trike"]:
            hc_tire_count = 3
            if front:
                hc_partial_tire_count = 2
            else:
                hc_partial_tire_count = 1
        else:
            hc_tire_count = 4
            hc_partial_tire_count = 2
            six_wheel_status: int = int(self.var_six_wheel_chassis.get())
            if six_wheel_status == 1: #change the formula to account for six wheels
                hc_tire_count = 6
                if front:
                    hc_partial_tire_count = 2
                else:
                    hc_partial_tire_count = 4

        radial_tire_count:   int = local_tire_qty * local_tire_radial
        slick_tire_count:    int = local_tire_qty * local_tire_racing_slick
        off_road_tire_count: int = local_tire_qty * local_tire_off_road
        tire_hc_adjustment: float = 0.0
        if radial_tire_count == hc_tire_count: #full load
            tire_hc_adjustment = tire_hc_adjustment + 1
        elif radial_tire_count >= hc_partial_tire_count: #just the front two tires, partial credit
            tire_hc_adjustment = tire_hc_adjustment + 0.5
        if slick_tire_count == hc_tire_count: #full load
            tire_hc_adjustment = tire_hc_adjustment + 2
        elif slick_tire_count >= hc_partial_tire_count: #just the front two tires, partial credit
            tire_hc_adjustment = tire_hc_adjustment + 1
        if off_road_tire_count == hc_tire_count: #full load
            tire_hc_adjustment = tire_hc_adjustment + 1
        elif off_road_tire_count >= hc_partial_tire_count:
            tire_hc_adjustment = tire_hc_adjustment + 0.5 # partial load
        return tire_hc_adjustment

    def hc_addition(self):
        addition_list: list = []
        body_type: str = self.selected_body.get()
        if body_type in ["Pickup", "Pickup, 1 Spc Ext. Cab", "Pickup, 2 Spc Ext. Cab", "Camper", "Van"]:
            total_weight: float = float(self.label_total_weight.cget("text"))
            if total_weight >= 5500:
                self.label_hidden_body_hc.configure(text="-1")
            else:
                self.label_hidden_body_hc.configure(text="0")

        addition_list.append(int(self.label_hidden_body_hc.cget("text")))
        addition_list.append(int(self.label_hc.cget("text")))
        addition_list.append(float(self.label_hidden_front_tire_hc.cget("text")))
        addition_list.append(float(self.label_hidden_rear_tire_hc.cget("text")))
        addition_list.append(float(self.label_hidden_accessories_hc_1.cget("text")))
        addition_list.append(float(self.label_hidden_accessories_hc_2.cget("text")))
        addition_list.append(float(self.label_hidden_accessories_hc_3.cget("text")))
        addition_list.append(float(self.label_hidden_accessories_hc_4.cget("text")))
        addition_list.append(float(self.label_hidden_accessories_hc_5.cget("text")))
        addition_list.append(float(self.label_hidden_accessories_hc_6.cget("text")))
        addition_list.append(float(self.label_hidden_accessories_hc_7.cget("text")))
        addition_list.append(float(self.label_hidden_accessories_hc_8.cget("text")))
        addition_list.append(float(self.label_hidden_accessories_hc_9.cget("text")))
        addition_list.append(float(self.label_hidden_accessories_hc_10.cget("text")))
        addition_list.append(float(self.label_hidden_accessories_hc_11.cget("text")))
        addition_list.append(float(self.label_hidden_accessories_hc_12.cget("text")))
        addition_list.append(float(self.label_hidden_accessories_hc_13.cget("text")))
        addition_list.append(float(self.label_hidden_accessories_hc_14.cget("text")))
        addition_list.append(float(self.label_hidden_accessories_hc_15.cget("text")))
        addition_list.append(float(self.label_hidden_accessories_hc_16.cget("text")))
        addition_list.append(float(self.label_hidden_accessories_hc_17.cget("text")))
        addition_list.append(float(self.label_hidden_accessories_hc_18.cget("text")))
        addition_list.append(float(self.label_hidden_accessories_hc_19.cget("text")))
        addition_list.append(float(self.label_hidden_accessories_hc_20.cget("text")))
        addition_list.append(float(self.label_hidden_accessories_hc_21.cget("text")))
        addition_list.append(float(self.label_hidden_accessories_hc_22.cget("text")))
        addition_list.append(float(self.label_hidden_accessories_hc_23.cget("text")))
        addition_list.append(float(self.label_hidden_accessories_hc_24.cget("text")))
        addition_list.append(float(self.label_hidden_accessories_hc_25.cget("text")))
        addition_list.append(float(self.label_hidden_accessories_hc_26.cget("text")))
        addition_list.append(float(self.label_hidden_accessories_hc_27.cget("text")))
        addition_list.append(float(self.label_hidden_accessories_hc_28.cget("text")))
        addition_list.append(float(self.label_hidden_accessories_hc_29.cget("text")))
        addition_list.append(float(self.label_hidden_accessories_hc_30.cget("text")))
        local_total = sum(addition_list)
        self.label_max_hc.configure(text=str(local_total))

    def get_body_dictionaries(self):
        self.body_list = []
        entry_dict: dict = {'Body': "Body",                   'Cost': 0,    'Weight': 0,    'Total Weight': 0,    'Total Spaces': 0,  'Cargo Spaces': 0,  'Armor Cost/Point': 0,  'Armor Weight/Point': 0,  'To-Hit Mod (side)': 0,  'Max Turret':-1, "Cycle": 0}
        self.body_list.append(entry_dict)
        entry_dict: dict = {'Body': "Light Cycle",            'Cost': 200,  'Weight': 250,  'Total Weight': 800,  'Total Spaces': 4,  'Cargo Spaces': 0,  'Armor Cost/Point': 10, 'Armor Weight/Point': 4,  'To-Hit Mod (side)': -2, 'Max Turret':-1, "Cycle": 1}
        self.body_list.append(entry_dict)
        entry_dict: dict = {'Body': "Medium Cycle",           'Cost': 300,  'Weight': 300,  'Total Weight': 1100, 'Total Spaces': 5,  'Cargo Spaces': 0,  'Armor Cost/Point': 11, 'Armor Weight/Point': 5,  'To-Hit Mod (side)': -2, 'Max Turret':-1, "Cycle": 1}
        self.body_list.append(entry_dict)
        entry_dict: dict = {'Body': "Heavy Cycle",            'Cost': 400,  'Weight': 350,  'Total Weight': 1300, 'Total Spaces': 7,  'Cargo Spaces': 0,  'Armor Cost/Point': 12, 'Armor Weight/Point': 6,  'To-Hit Mod (side)': -2, 'Max Turret':-1, "Cycle": 1}
        self.body_list.append(entry_dict)
        entry_dict: dict = {'Body': "Light SideCar",          'Cost': 300,  'Weight': 200,  'Total Weight': 400,  'Total Spaces': 2,  'Cargo Spaces': 0,  'Armor Cost/Point': 5,  'Armor Weight/Point': 5,  'To-Hit Mod (side)': -2, 'Max Turret':-1, "Cycle": 1}
        self.body_list.append(entry_dict)
        entry_dict: dict = {'Body': "Heavy SideCar",          'Cost': 450,  'Weight': 350,  'Total Weight': 750,  'Total Spaces': 3,  'Cargo Spaces': 0,  'Armor Cost/Point': 5,  'Armor Weight/Point': 6,  'To-Hit Mod (side)': -2, 'Max Turret':-1, "Cycle": 1}
        self.body_list.append(entry_dict)
        entry_dict: dict = {'Body': "Light Trike",            'Cost': 250,  'Weight': 300,  'Total Weight': 1600, 'Total Spaces': 8,  'Cargo Spaces': 0,  'Armor Cost/Point': 11, 'Armor Weight/Point': 5,  'To-Hit Mod (side)': -2, 'Max Turret':0,  "Cycle": 1}
        self.body_list.append(entry_dict)
        entry_dict: dict = {'Body': "Medium Trike",           'Cost': 300,  'Weight': 500,  'Total Weight': 2100, 'Total Spaces': 10, 'Cargo Spaces': 0,  'Armor Cost/Point': 12, 'Armor Weight/Point': 6,  'To-Hit Mod (side)': -1, 'Max Turret':1,  "Cycle": 1}
        self.body_list.append(entry_dict)
        entry_dict: dict = {'Body': "Heavy Trike",            'Cost': 400,  'Weight': 700,  'Total Weight': 2800, 'Total Spaces': 12, 'Cargo Spaces': 0,  'Armor Cost/Point': 14, 'Armor Weight/Point': 7,  'To-Hit Mod (side)': -1, 'Max Turret':2,  "Cycle": 1}
        self.body_list.append(entry_dict)
        entry_dict: dict = {'Body': "x-Hvy Trike",            'Cost': 550,  'Weight': 950,  'Total Weight': 3500, 'Total Spaces': 14, 'Cargo Spaces': 0,  'Armor Cost/Point': 16, 'Armor Weight/Point': 8,  'To-Hit Mod (side)': 0,  'Max Turret':2,  "Cycle": 1}
        self.body_list.append(entry_dict)
        entry_dict: dict = {'Body': "Rev. Light Trike",       'Cost': 375,  'Weight': 300,  'Total Weight': 1600, 'Total Spaces': 7,  'Cargo Spaces': 0,  'Armor Cost/Point': 11, 'Armor Weight/Point': 5,  'To-Hit Mod (side)': -2, 'Max Turret':0,  "Cycle": 1}
        self.body_list.append(entry_dict)
        entry_dict: dict = {'Body': "Rev. Medium Trike",      'Cost': 450,  'Weight': 500,  'Total Weight': 2100, 'Total Spaces': 9,  'Cargo Spaces': 0,  'Armor Cost/Point': 12, 'Armor Weight/Point': 6,  'To-Hit Mod (side)': -1, 'Max Turret':1,  "Cycle": 1}
        self.body_list.append(entry_dict)
        entry_dict: dict = {'Body': "Rev. Heavy Trike",       'Cost': 600,  'Weight': 700,  'Total Weight': 2800, 'Total Spaces': 11, 'Cargo Spaces': 0,  'Armor Cost/Point': 14, 'Armor Weight/Point': 7,  'To-Hit Mod (side)': -1, 'Max Turret':2,  "Cycle": 1}
        self.body_list.append(entry_dict)
        entry_dict: dict = {'Body': "Rev. X-Hvy Trike",       'Cost': 825,  'Weight': 950,  'Total Weight': 3500, 'Total Spaces': 13, 'Cargo Spaces': 0,  'Armor Cost/Point': 16, 'Armor Weight/Point': 8,  'To-Hit Mod (side)': 0,  'Max Turret':2,  "Cycle": 1}
        self.body_list.append(entry_dict)
        entry_dict: dict = {'Body': "Subcompact",             'Cost': 300,  'Weight': 1000, 'Total Weight': 2300, 'Total Spaces': 7,  'Cargo Spaces': 0,  'Armor Cost/Point': 11, 'Armor Weight/Point': 5,  'To-Hit Mod (side)': -1, 'Max Turret':0,  "Cycle": 0}
        self.body_list.append(entry_dict)
        entry_dict: dict = {'Body': "Compact",                'Cost': 400,  'Weight': 1300, 'Total Weight': 3700, 'Total Spaces': 10, 'Cargo Spaces': 0,  'Armor Cost/Point': 13, 'Armor Weight/Point': 6,  'To-Hit Mod (side)': -1, 'Max Turret':1,  "Cycle": 0}
        self.body_list.append(entry_dict)
        entry_dict: dict = {'Body': "Mid-Sized",              'Cost': 600,  'Weight': 1600, 'Total Weight': 4800, 'Total Spaces': 13, 'Cargo Spaces': 0,  'Armor Cost/Point': 16, 'Armor Weight/Point': 8,  'To-Hit Mod (side)': 0,  'Max Turret':2,  "Cycle": 0}
        self.body_list.append(entry_dict)
        entry_dict: dict = {'Body': "Sedan",                  'Cost': 700,  'Weight': 1700, 'Total Weight': 5100, 'Total Spaces': 16, 'Cargo Spaces': 0,  'Armor Cost/Point': 18, 'Armor Weight/Point': 9,  'To-Hit Mod (side)': 0,  'Max Turret':2,  "Cycle": 0}
        self.body_list.append(entry_dict)
        entry_dict: dict = {'Body': "Luxury",                 'Cost': 800,  'Weight': 1800, 'Total Weight': 5500, 'Total Spaces': 19, 'Cargo Spaces': 0,  'Armor Cost/Point': 20, 'Armor Weight/Point': 10, 'To-Hit Mod (side)': 0,  'Max Turret':2,  "Cycle": 0}
        self.body_list.append(entry_dict)
        entry_dict: dict = {'Body': "Station Wagon",          'Cost': 800,  'Weight': 1800, 'Total Weight': 5500, 'Total Spaces': 14, 'Cargo Spaces': 7,  'Armor Cost/Point': 20, 'Armor Weight/Point': 10, 'To-Hit Mod (side)': 0,  'Max Turret':2,  "Cycle": 0}
        self.body_list.append(entry_dict)
        entry_dict: dict = {'Body': "Pickup",                 'Cost': 900,  'Weight': 2100, 'Total Weight': 6500, 'Total Spaces': 13, 'Cargo Spaces': 11, 'Armor Cost/Point': 22, 'Armor Weight/Point': 11, 'To-Hit Mod (side)': 0,  'Max Turret':2,  "Cycle": 0}
        self.body_list.append(entry_dict)
        entry_dict: dict = {'Body': "Pickup, 1 Spc Ext. Cab", 'Cost': 1900, 'Weight': 2200, 'Total Weight': 6500, 'Total Spaces': 14, 'Cargo Spaces': 10, 'Armor Cost/Point': 22, 'Armor Weight/Point': 11, 'To-Hit Mod (side)': 0,  'Max Turret':2,  "Cycle": 0}
        self.body_list.append(entry_dict)
        entry_dict: dict = {'Body': "Pickup, 2 Spc Ext. Cab", 'Cost': 2400, 'Weight': 2350, 'Total Weight': 6500, 'Total Spaces': 16, 'Cargo Spaces': 12, 'Armor Cost/Point': 24, 'Armor Weight/Point': 12, 'To-Hit Mod (side)': 0,  'Max Turret':2,  "Cycle": 0}
        self.body_list.append(entry_dict)
        entry_dict: dict = {'Body': "Camper",                 'Cost': 1400, 'Weight': 2300, 'Total Weight': 6500, 'Total Spaces': 17, 'Cargo Spaces': 7,  'Armor Cost/Point': 30, 'Armor Weight/Point': 14, 'To-Hit Mod (side)': 0,  'Max Turret':3,  "Cycle": 0}
        self.body_list.append(entry_dict)
        entry_dict: dict = {'Body': "Van",                    'Cost': 1000, 'Weight': 2000, 'Total Weight': 6000, 'Total Spaces': 24, 'Cargo Spaces': 6,  'Armor Cost/Point': 30, 'Armor Weight/Point': 14, 'To-Hit Mod (side)': 0,  'Max Turret':3,  "Cycle": 0}
        self.body_list.append(entry_dict)
        entry_dict: dict = {'Body': "Formula One/Indy",       'Cost': 6500, 'Weight': 600,  'Total Weight': 4000, 'Total Spaces': 15, 'Cargo Spaces': 0,  'Armor Cost/Point': 22, 'Armor Weight/Point': 10, 'To-Hit Mod (side)': 0,  'Max Turret':2,  "Cycle": 0}
        self.body_list.append(entry_dict)
        entry_dict: dict = {'Body': "Can-Am",                 'Cost': 6500, 'Weight': 800,  'Total Weight': 4500, 'Total Spaces': 18, 'Cargo Spaces': 0,  'Armor Cost/Point': 24, 'Armor Weight/Point': 12, 'To-Hit Mod (side)': 0,  'Max Turret':2,  "Cycle": 0}
        self.body_list.append(entry_dict)
        entry_dict: dict = {'Body': "Sprint",                 'Cost': 5600, 'Weight': 300,  'Total Weight': 3200, 'Total Spaces': 10, 'Cargo Spaces': 0,  'Armor Cost/Point': 15, 'Armor Weight/Point': 7,  'To-Hit Mod (side)': 0,  'Max Turret':2,  "Cycle": 0}
        self.body_list.append(entry_dict)
        entry_dict: dict = {'Body': "Funny Car",              'Cost': 6600, 'Weight': 700,  'Total Weight': 4500, 'Total Spaces': 20, 'Cargo Spaces': 0,  'Armor Cost/Point': 26, 'Armor Weight/Point': 13, 'To-Hit Mod (side)': 0,  'Max Turret':2,  "Cycle": 0}
        self.body_list.append(entry_dict)
        entry_dict: dict = {'Body': "Dragster",               'Cost': 6200, 'Weight': 600,  'Total Weight': 4000, 'Total Spaces': 16, 'Cargo Spaces': 0,  'Armor Cost/Point': 20, 'Armor Weight/Point': 8,  'To-Hit Mod (side)': 0,  'Max Turret':2,  "Cycle": 0}
        self.body_list.append(entry_dict)

    def get_modifications_dictionaries(self):
        self.modifications_list = []
        entry_dict: dict = {'Modification': "No Mods", 'Cost': 0, 'Weight': 0, 'Spaces': 0, 'Cargo Spaces': 0}
        self.modifications_list.append(entry_dict)
        entry_dict: dict = {'Modification': "CA Frame", 'Cost': 4, 'Weight': -0.5, 'Spaces': 0, 'Cargo Spaces': 0}
        self.modifications_list.append(entry_dict)
        entry_dict: dict = {'Modification': "Streamlined", 'Cost': .5, 'Weight': 0, 'Spaces': 0.1, 'Cargo Spaces': 0.1}
        self.modifications_list.append(entry_dict)
        entry_dict: dict = {'Modification': "CA/Streamlined", 'Cost': 5, 'Weight': -0.5, 'Spaces':0.1, 'Cargo Spaces': 0.1}
        self.modifications_list.append(entry_dict)

    def get_chassis_dictionaries(self):
        self.chassis_list = []
        entry_dict: dict = {'Chassis': "Chassis", 'Cost': 0, 'Max Weight': 1}
        self.chassis_list.append(entry_dict)
        entry_dict: dict = {'Chassis': "Cycle Chassis", 'Cost': 0, 'Max Weight': 1}
        self.chassis_list.append(entry_dict)
        entry_dict: dict = {'Chassis': "Light Chassis", 'Cost': -0.2, 'Max Weight': 0.9}
        self.chassis_list.append(entry_dict)
        entry_dict: dict = {'Chassis': "Standard Chassis", 'Cost': 0, 'Max Weight': 1}
        self.chassis_list.append(entry_dict)
        entry_dict: dict = {'Chassis': "Heavy Chassis", 'Cost': 0.5, 'Max Weight': 1.1}
        self.chassis_list.append(entry_dict)
        entry_dict: dict = {'Chassis': "Ext Heavy Chassis", 'Cost': 1.0, 'Max Weight': 1.2}
        self.chassis_list.append(entry_dict)

    def get_suspension_dictionaries(self):
        self.suspension_list = []
        entry_dict: dict = {'Suspension': "Suspension", 'Cost': 0, 'HC': 0, "Van HC": -6, "Sub HC": -6}
        self.suspension_list.append(entry_dict)
        entry_dict: dict = {'Suspension': "Cycle Light Suspension",    'Cost': 0,   'HC': 0, "Van HC": -6, "Sub HC": -6}
        self.suspension_list.append(entry_dict)
        entry_dict: dict = {'Suspension': "Cycle Improved Suspension", 'Cost': 1,   'HC': 1, "Van HC": -6, "Sub HC": -6}
        self.suspension_list.append(entry_dict)
        entry_dict: dict = {'Suspension': "Cycle - Heavy Suspension",  'Cost': 2,   'HC': 2, "Van HC": -6, "Sub HC": -6}
        self.suspension_list.append(entry_dict)
        entry_dict: dict = {'Suspension': "Cycle - OR Suspension",     'Cost': 3,   'HC': 2, "Van HC": -6, "Sub HC": -6}
        self.suspension_list.append(entry_dict)
        entry_dict: dict = {'Suspension': "Light Suspension",          'Cost': 0,   'HC': 1, "Van HC": 0,  "Sub HC": 2}
        self.suspension_list.append(entry_dict)
        entry_dict: dict = {'Suspension': "Improved Suspension",       'Cost': 1,   'HC': 2, "Van HC": 1,  "Sub HC": 3}
        self.suspension_list.append(entry_dict)
        entry_dict: dict = {'Suspension': "Heavy Suspension",          'Cost': 1.5, 'HC': 3, "Van HC": 2,  "Sub HC": 4}
        self.suspension_list.append(entry_dict)
        entry_dict: dict = {'Suspension': "Off-Road Suspension",       'Cost': 5,   'HC': 2, "Van HC": 1,  "Sub HC": 3}
        self.suspension_list.append(entry_dict)
        entry_dict: dict = {'Suspension': "Racing Suspension",         'Cost': 0,   'HC': 5, "Van HC": -6, "Sub HC": -6}
        self.suspension_list.append(entry_dict)

    def get_engines_dictionaries(self):
        self.engine_list = []
        entry_dict: dict = {'Engine': "Engine", 'Cost': 0, 'Weight': 0, 'Spaces': 0, "DP": 0, "Power Factors": 0, "Base MPG": 0, "Type": "None"}
        self.engine_list.append(entry_dict)
        entry_dict: dict = {'Engine': "10 cid IC Engine",            'Cost': 400,   'Weight': 60,   'Spaces': 1,  "DP": 1,  "Power Factors": 300,   "Base MPG": 80, "Type": "Gas"}
        self.engine_list.append(entry_dict)
        entry_dict: dict = {'Engine': "30 cid IC Engine",            'Cost': 750,   'Weight': 115,  'Spaces': 1,  "DP": 2,  "Power Factors": 500,   "Base MPG": 70, "Type": "Gas"}
        self.engine_list.append(entry_dict)
        entry_dict: dict = {'Engine': "50 cid IC Engine",            'Cost': 1250,  'Weight': 150,  'Spaces': 1,  "DP": 3,  "Power Factors": 700,   "Base MPG": 60, "Type": "Gas"}
        self.engine_list.append(entry_dict)
        entry_dict: dict = {'Engine': "100 cid IC Engine",           'Cost': 2500,  'Weight': 265,  'Spaces': 2,  "DP": 6,  "Power Factors": 1300,  "Base MPG": 50, "Type": "Gas"}
        self.engine_list.append(entry_dict)
        entry_dict: dict = {'Engine': "150 cid IC Engine",           'Cost': 4000,  'Weight': 375,  'Spaces': 3,  "DP": 9,  "Power Factors": 1900,  "Base MPG": 45, "Type": "Gas"}
        self.engine_list.append(entry_dict)
        entry_dict: dict = {'Engine': "200 cid IC Engine",           'Cost': 5500,  'Weight': 480,  'Spaces': 4,  "DP": 12, "Power Factors": 2500,  "Base MPG": 35, "Type": "Gas"}
        self.engine_list.append(entry_dict)
        entry_dict: dict = {'Engine': "250 cid IC Engine",           'Cost': 6500,  'Weight': 715,  'Spaces': 5,  "DP": 14, "Power Factors": 3200,  "Base MPG": 28, "Type": "Gas"}
        self.engine_list.append(entry_dict)
        entry_dict: dict = {'Engine': "300 cid IC Engine",           'Cost': 7800,  'Weight': 825,  'Spaces': 6,  "DP": 16, "Power Factors": 4000,  "Base MPG": 22, "Type": "Gas"}
        self.engine_list.append(entry_dict)
        entry_dict: dict = {'Engine': "350 cid IC Engine",           'Cost': 9500,  'Weight': 975,  'Spaces': 7,  "DP": 19, "Power Factors": 5000,  "Base MPG": 18, "Type": "Gas"}
        self.engine_list.append(entry_dict)
        entry_dict: dict = {'Engine': "400 cid IC Engine",           'Cost': 10500, 'Weight': 1050, 'Spaces': 8,  "DP": 22, "Power Factors": 6300,  "Base MPG": 15, "Type": "Gas"}
        self.engine_list.append(entry_dict)
        entry_dict: dict = {'Engine': "450 cid IC Engine",           'Cost': 11700, 'Weight': 1125, 'Spaces': 9,  "DP": 24, "Power Factors": 7800,  "Base MPG": 13, "Type": "Gas"}
        self.engine_list.append(entry_dict)
        entry_dict: dict = {'Engine': "500 cid IC Engine",           'Cost': 13000, 'Weight': 1200, 'Spaces': 10, "DP": 26, "Power Factors": 9500,  "Base MPG": 12, "Type": "Gas"}
        self.engine_list.append(entry_dict)
        entry_dict: dict = {'Engine': "700 cid IC Engine",           'Cost': 19000, 'Weight': 1275, 'Spaces': 14, "DP": 30, "Power Factors": 13000, "Base MPG": 10, "Type": "Gas"}
        self.engine_list.append(entry_dict)
        entry_dict: dict = {'Engine': "Small Cycle Power Plant",     'Cost': 500,   'Weight': 100,  'Spaces': 1,  "DP": 2,  "Power Factors": 400,   "Base MPG": 0, "Type": "Electric"}
        self.engine_list.append(entry_dict)
        entry_dict: dict = {'Engine': "Medium Cycle Power Plant",    'Cost': 1000,  'Weight': 150,  'Spaces': 1,  "DP": 3,  "Power Factors": 600,   "Base MPG": 0, "Type": "Electric"}
        self.engine_list.append(entry_dict)
        entry_dict: dict = {'Engine': "Large Cycle Power Plant",     'Cost': 1500,  'Weight': 175,  'Spaces': 2,  "DP": 4,  "Power Factors": 800,   "Base MPG": 0, "Type": "Electric"}
        self.engine_list.append(entry_dict)
        entry_dict: dict = {'Engine': "Super Cycle Power Plant",     'Cost': 2000,  'Weight': 200,  'Spaces': 2,  "DP": 5,  "Power Factors": 1000,  "Base MPG": 0, "Type": "Electric"}
        self.engine_list.append(entry_dict)
        entry_dict: dict = {'Engine': "Super Trike Power Plant",     'Cost': 3000,  'Weight': 250,  'Spaces': 3,  "DP": 6,  "Power Factors": 1200,  "Base MPG": 0, "Type": "Electric"}
        self.engine_list.append(entry_dict)
        entry_dict: dict = {'Engine': "Small Electric Power Plant",  'Cost': 500,   'Weight': 500,  'Spaces': 3,  "DP": 5,  "Power Factors": 800,   "Base MPG": 0, "Type": "Electric"}
        self.engine_list.append(entry_dict)
        entry_dict: dict = {'Engine': "Medium Electric Power Plant", 'Cost': 1000,  'Weight': 700,  'Spaces': 4,  "DP": 8,  "Power Factors": 1400,  "Base MPG": 0, "Type": "Electric"}
        self.engine_list.append(entry_dict)
        entry_dict: dict = {'Engine': "Large Electric Power Plant",  'Cost': 2000,  'Weight': 900,  'Spaces': 5,  "DP": 10, "Power Factors": 2000,  "Base MPG": 0, "Type": "Electric"}
        self.engine_list.append(entry_dict)
        entry_dict: dict = {'Engine': "Super Power Plant",           'Cost': 3000,  'Weight': 1100, 'Spaces': 6,  "DP": 12, "Power Factors": 2600,  "Base MPG": 0, "Type": "Electric"}
        self.engine_list.append(entry_dict)
        entry_dict: dict = {'Engine': "Sport Power Plant",           'Cost': 6000,  'Weight': 1000, 'Spaces': 6,  "DP": 12, "Power Factors": 3000,  "Base MPG": 0, "Type": "Electric"}
        self.engine_list.append(entry_dict)
        entry_dict: dict = {'Engine': "ThunderCat Power Plant",      'Cost': 12000, 'Weight': 2000, 'Spaces': 8,  "DP": 15, "Power Factors": 6700,  "Base MPG": 0, "Type": "Electric"}
        self.engine_list.append(entry_dict)

    def get_gas_tank_dictionaries(self):
        self.gas_tank_list = []
        entry_dict: dict = {"Gas Tank": "Gas Tank",          "Cost": 0,  "Weight": 0,  "DP": 0}
        self.gas_tank_list.append(entry_dict)
        entry_dict: dict = {"Gas Tank": "Electric",          "Cost": 0,  "Weight": 0,  "DP": 0}
        self.gas_tank_list.append(entry_dict)
        entry_dict: dict = {"Gas Tank": "Economy Gas Tank",  "Cost": 2,  "Weight": 1,  "DP": 2}
        self.gas_tank_list.append(entry_dict)
        entry_dict: dict = {"Gas Tank": "Hvy-Duty Gas Tank", "Cost": 5,  "Weight": 2,  "DP": 4}
        self.gas_tank_list.append(entry_dict)
        entry_dict: dict = {"Gas Tank": "Racing Gas Tank",   "Cost": 10, "Weight": 5,  "DP": 4}
        self.gas_tank_list.append(entry_dict)
        entry_dict: dict = {"Gas Tank": "Duelling Gas Tank", "Cost": 25, "Weight": 10, "DP": 8}
        self.gas_tank_list.append(entry_dict)

    def get_tires_dictionaries(self):
        self.tires_list = []
        entry_dict: dict = {"Tires": "Tires",            "Cost": 0,    "Weight": 0,   "DP": 0}
        self.tires_list.append(entry_dict)
        entry_dict: dict = {"Tires": "Standard Tires",   "Cost": 50,   "Weight": 30,  "DP": 4}
        self.tires_list.append(entry_dict)
        entry_dict: dict = {"Tires": "Heavy Duty Tires", "Cost": 100,  "Weight": 40,  "DP": 6}
        self.tires_list.append(entry_dict)
        entry_dict: dict = {"Tires": "PR Tires",         "Cost": 200,  "Weight": 50,  "DP": 9}
        self.tires_list.append(entry_dict)
        entry_dict: dict = {"Tires": "Solid Tires",      "Cost": 500,  "Weight": 75,  "DP": 12}
        self.tires_list.append(entry_dict)
        entry_dict: dict = {"Tires": "Plasticore Tires", "Cost": 1000, "Weight": 150, "DP": 25}
        self.tires_list.append(entry_dict)

    def get_accessories_dictionaries(self):
        self.accessories_list = []
        entry_dict: dict = {"Accessory Name": "Accessory",                                    "Cost": "0",     "Space": "0",    "Weight": "0",     "DP": "",   "Notes": "", "Turret Size": -2, "Cycle Only": 0}
        self.accessories_list.append(entry_dict)
        entry_dict: dict = {"Accessory Name": "Active Suspension",                            "Cost": "4000",  "Space": "1",	"Weight": "100",   "DP": "",   "Notes": "+1 Added to HC", "Turret Size":  -2, "Cycle Only": 0}
        self.accessories_list.append(entry_dict)
        entry_dict: dict = {"Accessory Name": "Anti-Lock Brakes",                             "Cost": "1000",  "Space": "",	    "Weight": "",      "DP": "",   "Notes": "No tire dam from hvy braking. Braking hazards -D1for bad road surfaces", "Turret Size": -2, "Cycle Only": 0}
        self.accessories_list.append(entry_dict)
        entry_dict: dict = {"Accessory Name": "Blow Through Concealment",                     "Cost": "100",   "Space": "",	    "Weight": "10",    "DP": "",   "Notes": "EACH!", "Turret Size":  -2, "Cycle Only": 0}
        self.accessories_list.append(entry_dict)
        entry_dict: dict = {"Accessory Name": "Bumper Spikes",                                "Cost": "150",   "Space": "",	    "Weight": "70",    "DP": "",   "Notes": "1D in collisions", "Turret Size":  -2, "Cycle Only": 0}
        self.accessories_list.append(entry_dict)
        entry_dict: dict = {"Accessory Name": "Bumper Trigger",                               "Cost": "50",    "Space": "",	    "Weight": "",      "DP": "",   "Notes": "", "Turret Size":  -2, "Cycle Only": 0}
        self.accessories_list.append(entry_dict)
        entry_dict: dict = {"Accessory Name": "Cyberlink",                                    "Cost": "16000", "Space": "1",	"Weight": "100",   "DP": "",   "Notes": " +3 to hit", "Turret Size":  -2, "Cycle Only": 0}
        self.accessories_list.append(entry_dict)
        entry_dict: dict = {"Accessory Name": "Fire Extinguisher (FE)",                       "Cost": "300",   "Space": "1",    "Weight": "150",   "DP": "",   "Notes": "Will put out fire on 1 - 3 (1 - 2 with gas) on 1D6", "Turret Size":  -2, "Cycle Only": 0}
        self.accessories_list.append(entry_dict)
        entry_dict: dict = {"Accessory Name": "Fire Retardant Insulators",                    "Cost": "150",   "Space": "1",	"Weight": "25",    "DP": "",   "Notes": " PER SPACE PROTECTED", "Turret Size":  -2, "Cycle Only": 0}
        self.accessories_list.append(entry_dict)
        entry_dict: dict = {"Accessory Name": "Heavy-duty Brakes",                            "Cost": "600",   "Space": "",	    "Weight": "",      "DP": "",   "Notes": "One purchase per vehicle", "Turret Size":  -2, "Cycle Only": 0}
        self.accessories_list.append(entry_dict)
        entry_dict: dict = {"Accessory Name": "Heavy-duty Shock Absorbers",                   "Cost": "2400",  "Space": "",	    "Weight": "30",    "DP": "",   "Notes": "Reduce All Road Hazards by D1, D0 do not force Control Rolls; one purchase only", "Turret Size":  -2, "Cycle Only": 0}
        self.accessories_list.append(entry_dict)
        entry_dict: dict = {"Accessory Name": "Hi-Res Computer",                              "Cost": "4000",  "Space": "",    	"Weight": "",      "DP": "",   "Notes": " +2 To Hit for ONE location", "Turret Size":  -2, "Cycle Only": 0}
        self.accessories_list.append(entry_dict)
        entry_dict: dict = {"Accessory Name": "Hi-Res SWC (HRSWC)",                           "Cost": "2500",  "Space": "",	    "Weight": "",      "DP": "",   "Notes": " +2 To Hit for One Weapon System for One Location", "Turret Size":  -2, "Cycle Only": 0}
        self.accessories_list.append(entry_dict)
        entry_dict: dict = {"Accessory Name": "High Torque Motors (HTM)",                     "Cost": "600",   "Space": "",	    "Weight": "",      "DP": "",   "Notes": "Adds 5 to acceleration when engaged; Top speed reduced by 1/4; buy just one", "Turret Size":  -2, "Cycle Only": 0}
        self.accessories_list.append(entry_dict)
        entry_dict: dict = {"Accessory Name": "HTMs, Heavy Duty (HDHTM)",                     "Cost": "1200",  "Space": "",	    "Weight": "",      "DP": "",   "Notes": "Doubles base accel. When engaged; Top speed reduced 1/3; buy just one", "Turret Size":  -2, "Cycle Only": 0}
        self.accessories_list.append(entry_dict)
        entry_dict: dict = {"Accessory Name": "Improved FE (IFE)",                            "Cost": "500",   "Space": "1",	"Weight": "200",   "DP": "",   "Notes": "Will put out fire on 1 - 4 (1 - 3 with gas) on 1D6", "Turret Size":  -2, "Cycle Only": 0}
        self.accessories_list.append(entry_dict)
        entry_dict: dict = {"Accessory Name": "Link",                                         "Cost": "50",    "Space": "",	    "Weight": "",      "DP": "",   "Notes": "", "Turret Size":  -2, "Cycle Only": 0}
        self.accessories_list.append(entry_dict)
        entry_dict: dict = {"Accessory Name": "Ramplate",                                     "Cost": "0",     "Space": "",	    "Weight": "0",     "DP": "",   "Notes": "", "Turret Size":  -2, "Cycle Only": 0}
        self.accessories_list.append(entry_dict)
        entry_dict: dict = {"Accessory Name": "Single-Weapon Computer",                       "Cost": "500",   "Space": "",	    "Weight": "",      "DP": "",   "Notes": " +1 to hit with one weapon system for one location", "Turret Size":  -2, "Cycle Only": 0}
        self.accessories_list.append(entry_dict)
        entry_dict: dict = {"Accessory Name": "Smart Link",                                   "Cost": "500",   "Space": "",	    "Weight": "",      "DP": "",   "Notes": "Allows weapons in one location to be aimed and fired with others (same weapon)", "Turret Size":  -2, "Cycle Only": 0}
        self.accessories_list.append(entry_dict)
        entry_dict: dict = {"Accessory Name": "Spoiler/Airdam, Plastic",                      "Cost": "750",   "Space": "",	    "Weight": "140",   "DP": "",   "Notes": "Must have two for full effect!", "Turret Size":  -2, "Cycle Only": 0}
        self.accessories_list.append(entry_dict)
        entry_dict: dict = {"Accessory Name": "Spoiler/Airdam, Metal",                        "Cost": "750",   "Space": "",	    "Weight": "140",   "DP": "",   "Notes": "Must have two for full effect!", "Turret Size":  -2, "Cycle Only": 0}
        self.accessories_list.append(entry_dict)
        entry_dict: dict = {"Accessory Name": "Targeting Computer",                           "Cost": "1000",  "Space": "",	    "Weight": "",      "DP": "",   "Notes": " +1 To Hit for ONE position", "Turret Size":  -2, "Cycle Only": 0}
        self.accessories_list.append(entry_dict)
        entry_dict: dict = {"Accessory Name": "Turret - Zero-space",                          "Cost": "750",   "Space": "1",	"Weight": "75",    "DP": "",   "Notes": "Uses 1spc For Targeting Laser Only.", "Turret Size":  0, "Cycle Only": 0}
        self.accessories_list.append(entry_dict)
        entry_dict: dict = {"Accessory Name": "Turret - One Space",                           "Cost": "1000",  "Space": "0",	"Weight": "150",   "DP": "",   "Notes": "Uses 1spc GIVES 1 Spc for Weap.Compact +", "Turret Size":  1, "Cycle Only": 0}
        self.accessories_list.append(entry_dict)
        entry_dict: dict = {"Accessory Name": "Turret - Two-space",                           "Cost": "1500",  "Space": "0",	"Weight": "200",   "DP": "",   "Notes": "Uses 2spc GIVES 2 Spc for Weap. Midsize +", "Turret Size":  2, "Cycle Only": 0}
        self.accessories_list.append(entry_dict)
        entry_dict: dict = {"Accessory Name": "Turret - Three-space",                         "Cost": "2500",  "Space": "-1",	"Weight": "300",   "DP": "",   "Notes": "Uses 2spc but GIVES 3 Spc for Weap. Camper +", "Turret Size":  3, "Cycle Only": 0}
        self.accessories_list.append(entry_dict)
        entry_dict: dict = {"Accessory Name": "Wheelguards, Front - Plastic",                 "Cost": "10",    "Space": "", 	"Weight": "4",     "DP": "",   "Notes": "Per point of armor, max wt 40lbs; must match vehicular armor type", "Turret Size":  -2, "Cycle Only": -1}
        self.accessories_list.append(entry_dict)
        entry_dict: dict = {"Accessory Name": "Wheelguards, Front - MET",                     "Cost": "25",    "Space": "",	    "Weight": "20",    "DP": "",   "Notes": "Per point of armor, max wt 40lbs; must match vehicular armor type", "Turret Size":  -2, "Cycle Only": -1}
        self.accessories_list.append(entry_dict)
        entry_dict: dict = {"Accessory Name": "Wheelguards, Rear - Plastic",                  "Cost": "10",    "Space": "",	    "Weight": "4",     "DP": "",   "Notes": "Per point of armor, max wt 40lbs; must match vehicular armor type", "Turret Size":  -2, "Cycle Only": -1}
        self.accessories_list.append(entry_dict)
        entry_dict: dict = {"Accessory Name": "Wheelguards, Rear - MET",                      "Cost": "25",    "Space": "",	    "Weight": "20",    "DP": "",   "Notes": "Per point of armor, max wt 40lbs; must match vehicular armor type", "Turret Size":  -2, "Cycle Only": -1}
        self.accessories_list.append(entry_dict)
        entry_dict: dict = {"Accessory Name": "Wheelhubs - Plastic",                          "Cost": "10",    "Space": "",	    "Weight": "4",     "DP": "",   "Notes": "Per point of armor, max wt 40lbs; must match vehicular armor type", "Turret Size":  -2, "Cycle Only": 0}
        self.accessories_list.append(entry_dict)
        entry_dict: dict = {"Accessory Name": "Wheelhubs - MET",                              "Cost": "25",    "Space": "",	    "Weight": "20",    "DP": "",   "Notes": "Per point of armor, max wt 40lbs; must match vehicular armor type", "Turret Size":  -2, "Cycle Only": 0}
        self.accessories_list.append(entry_dict)
        entry_dict: dict = {"Accessory Name": "---Less Often Used Accessories---",            "Cost": "0",     "Space": "0",    "Weight": "0",     "DP": "",   "Notes": "", "Turret Size": -2, "Cycle Only": 0}
        self.accessories_list.append(entry_dict)
        entry_dict: dict = {"Accessory Name": "EWP Armor - Normal",                           "Cost": "10",    "Space": "",	    "Weight": "4",     "DP": "",   "Notes": "per point; 40 lb per pod max; need not match vehicle armor", "Turret Size":  -2, "Cycle Only": 0}
        self.accessories_list.append(entry_dict)
        entry_dict: dict = {"Accessory Name": "EWP Armor - FP",                               "Cost": "20",    "Space": "",	    "Weight": "4",     "DP": "",   "Notes": "per point; 40 lb per pod max; need not match vehicle armor", "Turret Size":  -2, "Cycle Only": 0}
        self.accessories_list.append(entry_dict)
        entry_dict: dict = {"Accessory Name": "EWP Armor - LR",                               "Cost": "11",    "Space": "",	    "Weight": "4.4",   "DP": "",   "Notes": "per point; 40 lb per pod max; need not match vehicle armor", "Turret Size":  -2, "Cycle Only": 0}
        self.accessories_list.append(entry_dict)
        entry_dict: dict = {"Accessory Name": "EWP Armor - LRFP",                             "Cost": "25",    "Space": "",	    "Weight": "4.4",   "DP": "",   "Notes": "per point; 40 lb per pod max; need not match vehicle armor", "Turret Size":  -2, "Cycle Only": 0}
        self.accessories_list.append(entry_dict)
        entry_dict: dict = {"Accessory Name": "EWP Armor - RP",                               "Cost": "20",    "Space": "",	    "Weight": "4",     "DP": "",   "Notes": "per point; 40 lb per pod max; need not match vehicle armor", "Turret Size":  -2, "Cycle Only": 0}
        self.accessories_list.append(entry_dict)
        entry_dict: dict = {"Accessory Name": "EWP Armor - RPFP",                             "Cost": "40",    "Space": "",	    "Weight": "4",     "DP": "",   "Notes": "per point; 40 lb per pod max; need not match vehicle armor", "Turret Size":  -2, "Cycle Only": 0}
        self.accessories_list.append(entry_dict)
        entry_dict: dict = {"Accessory Name": "EWP Armor - MET",                              "Cost": "25",    "Space": "",	    "Weight": "20",    "DP": "",   "Notes": "per point; 40 lb per pod max; need not match vehicle armor", "Turret Size":  -2, "Cycle Only": 0}
        self.accessories_list.append(entry_dict)
        entry_dict: dict = {"Accessory Name": "EWP Armor - LR MET",                           "Cost": "27.5",  "Space": "",	    "Weight": "20",    "DP": "",   "Notes": "per point; 40 lb per pod max; need not match vehicle armor", "Turret Size":  -2, "Cycle Only": 0}
        self.accessories_list.append(entry_dict)
        entry_dict: dict = {"Accessory Name": "External Weapons Pod - Four-space",            "Cost": "3000",  "Space": "-4",	"Weight": "600",   "DP": "",   "Notes": "Oversized vehicles only", "Turret Size":  4, "Cycle Only": 0}
        self.accessories_list.append(entry_dict)
        entry_dict: dict = {"Accessory Name": "External Weapons Pod - One-space",             "Cost": "500",   "Space": "-1",	"Weight": "150",   "DP": "",   "Notes": "", "Turret Size":  0, "Cycle Only": 0}
        self.accessories_list.append(entry_dict)
        entry_dict: dict = {"Accessory Name": "External Weapons Pod - Three-space",           "Cost": "2000",  "Space": "-3",	"Weight": "400",   "DP": "",   "Notes": "Campers and Vans only", "Turret Size":  3, "Cycle Only": 0}
        self.accessories_list.append(entry_dict)
        entry_dict: dict = {"Accessory Name": "External Weapons Pod - Two-space",             "Cost": "1000",  "Space":  "-2",	"Weight": "250",   "DP": "",   "Notes": "Mid-sized and larger bodies ", "Turret Size": 2, "Cycle Only": 0}
        self.accessories_list.append(entry_dict)
        entry_dict: dict = {"Accessory Name": "External Weapons Pod Ejector",                 "Cost": "250",   "Space": "",	    "Weight": "",      "DP": "",   "Notes": "Per pod", "Turret Size":  -2, "Cycle Only": 0}
        self.accessories_list.append(entry_dict)
        entry_dict: dict = {"Accessory Name": "Improved Super Charger Capacitors",            "Cost": "500",   "Space": "1",	"Weight": "75",    "DP": "1",  "Notes": "", "Turret Size":  -2, "Cycle Only": 0}
        self.accessories_list.append(entry_dict)
        entry_dict: dict = {"Accessory Name": "Infrared Sighting System (IR)",                "Cost": "4000",  "Space": "1",	"Weight": "100",   "DP": "",   "Notes": "", "Turret Size":  -2, "Cycle Only": 0}
        self.accessories_list.append(entry_dict)
        entry_dict: dict = {"Accessory Name": "Heavy-duty Transmission",                      "Cost": "300",   "Space": "2",	"Weight": "300",   "DP": "",   "Notes": "Must select heavy or extra-heavy chassis.  Cars, Pickups, Vans and Campers only.", "Turret Size":  -2, "Cycle Only": 0}
        self.accessories_list.append(entry_dict)
        entry_dict: dict = {"Accessory Name": "Laser Battery",                                "Cost": "500",   "Space": "1",	"Weight": "100",   "DP": "1",  "Notes": "100 PU each; required to use lasers, radar, etc., with gas engines", "Turret Size":  -2, "Cycle Only": 0}
        self.accessories_list.append(entry_dict)
        entry_dict: dict = {"Accessory Name": "Laser Guidance Link Electronics",              "Cost": "500",   "Space": "",	    "Weight": "",      "DP": "",   "Notes": "Required once per laser; (must also buy LGL tuning per round and LGL link to launcher(s))", "Turret Size":  -2, "Cycle Only": 0}
        self.accessories_list.append(entry_dict)
        entry_dict: dict = {"Accessory Name": "Laser Guidance tuning for Rocket",             "Cost": "200",   "Space": "", 	"Weight": "",      "DP": "",   "Notes": "Required for each guided round; (must also buy LGL Electronics and LGL link to launcher(s))", "Turret Size":  -2, "Cycle Only": 0}
        self.accessories_list.append(entry_dict)
        entry_dict: dict = {"Accessory Name": "Laser Guidance Link to Launcher",              "Cost": "50",    "Space": "",	    "Weight": "",      "DP": "",   "Notes": "Required for ea. Launcher; (must also buy LGL tuning per round, and LGL Electronics)", "Turret Size":  -2, "Cycle Only": 0}
        self.accessories_list.append(entry_dict)
        entry_dict: dict = {"Accessory Name": "Laser Reactive Web",                           "Cost": "100",   "Space": "",	    "Weight": "",      "DP": "",   "Notes": "Per armor Location", "Turret Size":  -2, "Cycle Only": 0}
        self.accessories_list.append(entry_dict)
        entry_dict: dict = {"Accessory Name": "Magazine Switch",                              "Cost": "250",   "Space": "",	    "Weight": "",      "DP": "",   "Notes": "", "Turret Size":  -2, "Cycle Only": 0}
        self.accessories_list.append(entry_dict)
        entry_dict: dict = {"Accessory Name": "Nitrous Oxide",                                "Cost": "500",   "Space": "1",	"Weight": "20",    "DP": "",   "Notes": "", "Turret Size":  -2, "Cycle Only": 0}
        self.accessories_list.append(entry_dict)
        entry_dict: dict = {"Accessory Name": "No-Paint Windshield",                          "Cost": "1000",  "Space": "",	    "Weight": "",      "DP": "",   "Notes": "Paint Clouds have no Effect", "Turret Size":  -2, "Cycle Only": 0}
        self.accessories_list.append(entry_dict)
        entry_dict: dict = {"Accessory Name": "Overdrive",                                    "Cost": "600",   "Space": "",	    "Weight": "",      "DP": "",   "Notes": "Increases top speed 20 mph when activated; one perchase per vehicle", "Turret Size":  -2, "Cycle Only": 0}
        self.accessories_list.append(entry_dict)
        entry_dict: dict = {"Accessory Name": "Radio Detonator - receiver",                   "Cost": "50",    "Space": "",	    "Weight": "",      "DP": "",   "Notes": "per munition equipped", "Turret Size":  -2, "Cycle Only": 0}
        self.accessories_list.append(entry_dict)
        entry_dict: dict = {"Accessory Name": "Radio Detonator - sender",                     "Cost": "500",   "Space": "",	    "Weight": "",      "DP": "",   "Notes": "", "Turret Size":  -2, "Cycle Only": 0}
        self.accessories_list.append(entry_dict)
        entry_dict: dict = {"Accessory Name": "Remote Control Guidance System - Reciever",    "Cost": "2000",  "Space": "",	    "Weight": "",      "DP": "",   "Notes": "AADA banned", "Turret Size":  -2, "Cycle Only": 0}
        self.accessories_list.append(entry_dict)
        entry_dict: dict = {"Accessory Name": "Remote Control Guidance System - Transmitter", "Cost": "2000",  "Space": "3",	"Weight": "200",   "DP": "",   "Notes": "AADA banned", "Turret Size":  -2, "Cycle Only": 0}
        self.accessories_list.append(entry_dict)
        entry_dict: dict = {"Accessory Name": "Retractable Wheelguards",                      "Cost": "250",   "Space": "1",	"Weight": "50",    "DP": "",   "Notes": "Per Pair + cost & wt of wheelguard itself", "Turret Size":  -2, "Cycle Only": 0}
        self.accessories_list.append(entry_dict)
        entry_dict: dict = {"Accessory Name": "Rocket Magazine",                              "Cost": "50",    "Space": "0",    "Weight": "15",    "DP": "",   "Notes": "Per spc of capacity (up to 3 per magazine)", "Turret Size":  -2, "Cycle Only": 0}
        self.accessories_list.append(entry_dict)
        entry_dict: dict = {"Accessory Name": "Rocket EWP - One-space",                       "Cost": "250",   "Space": "-1",	"Weight": "75",    "DP": "",   "Notes": "Mounts single-shot rockets only; may not be armored or magazine fed.", "Turret Size":  0, "Cycle Only": 0}
        self.accessories_list.append(entry_dict)
        entry_dict: dict = {"Accessory Name": "Rocket EWP - Two-space",                       "Cost": "500",   "Space": "-2",	"Weight": "125",   "DP": "",   "Notes": "Mounts single-shot rockets only; may not be armored or magazine fed.", "Turret Size":  2, "Cycle Only": 0}
        self.accessories_list.append(entry_dict)
        entry_dict: dict = {"Accessory Name": "Rocket EWP - Three-space",                     "Cost": "1000",  "Space": "-3",	"Weight": "200",   "DP": "",   "Notes": "Mounts single-shot rockets only; may not be armored or magazine fed.", "Turret Size":  3, "Cycle Only": 0}
        self.accessories_list.append(entry_dict)
        entry_dict: dict = {"Accessory Name": "Rocket EWP - Four-space",                      "Cost": "1500",  "Space": "-4",	"Weight": "300",   "DP": "",   "Notes": "Mounts single-shot rockets only; may not be armored or magazine fed.", "Turret Size":  4, "Cycle Only": 0}
        self.accessories_list.append(entry_dict)
        entry_dict: dict = {"Accessory Name": "Rocket Platform - Large",                      "Cost": "150",   "Space": "-3",	"Weight": "200",   "DP": "",   "Notes": "", "Turret Size":  3, "Cycle Only": 0}
        self.accessories_list.append(entry_dict)
        entry_dict: dict = {"Accessory Name": "Rocket Platform - Mini",                       "Cost": "75",    "Space": "-1",	"Weight": "50",    "DP": "",   "Notes": "", "Turret Size":  0, "Cycle Only": 0}
        self.accessories_list.append(entry_dict)
        entry_dict: dict = {"Accessory Name": "Rocket Platform - Small",                      "Cost": "100",   "Space": "-2",	"Weight": "100",   "DP": "",   "Notes": "", "Turret Size":  2, "Cycle Only": 0}
        self.accessories_list.append(entry_dict)
        entry_dict: dict = {"Accessory Name": "Roll Cage",                                    "Cost": "900",   "Space": "1",	"Weight": "420",   "DP": "1",  "Notes": "Must be original equipment", "Turret Size":  -2, "Cycle Only": 0}
        self.accessories_list.append(entry_dict)
        entry_dict: dict = {"Accessory Name": "Rotary Magazine",                              "Cost": "500",   "Space": "",	    "Weight": "10",    "DP": "",   "Notes": "", "Turret Size":  -2, "Cycle Only": 0}
        self.accessories_list.append(entry_dict)
        entry_dict: dict = {"Accessory Name": "Safety Seat",                                  "Cost": "500",   "Space": "",	    "Weight": "25",    "DP": "",   "Notes": "", "Turret Size":  -2, "Cycle Only": 0}
        self.accessories_list.append(entry_dict)
        entry_dict: dict = {"Accessory Name": "Snow Tires",                                   "Cost": "600",   "Space": "",	    "Weight": "",      "DP": "",   "Notes": "Cannot be used with Racing Slicks; one purchase per vehicle", "Turret Size":  -2, "Cycle Only": 0}
        self.accessories_list.append(entry_dict)
        entry_dict: dict = {"Accessory Name": "Snow Tires, Off-Road",                         "Cost": "300",   "Space": "",	    "Weight": "",      "DP": "",   "Notes": "Cannot be used with Racing Slicks; one purchase per vehicle", "Turret Size":  -2, "Cycle Only": 0}
        self.accessories_list.append(entry_dict)
        entry_dict: dict = {"Accessory Name": "Sponson Turret Mount - 1 space",               "Cost": "750",   "Space": "0",	"Weight": "75",    "DP": "",   "Notes": "Uses 1spc GIVES 1 Spc for Weap.Compact +", "Turret Size": 1, "Cycle Only": 0}
        self.accessories_list.append(entry_dict)
        entry_dict: dict = {"Accessory Name": "Sponson Turret Mount - 2 space",               "Cost": "1125",  "Space": "0",	"Weight": "100",   "DP": "",   "Notes": "Uses 2spc GIVES 2 Spc for Weap. Midsize +", "Turret Size": 2, "Cycle Only": 0}
        self.accessories_list.append(entry_dict)
        entry_dict: dict = {"Accessory Name": "Sponson Turret Mount - 3 space",               "Cost": "1875",  "Space": "-1",	"Weight": "150",   "DP": "",   "Notes": "Uses 2spc but GIVES 3 Spc for Weap. Camper +", "Turret Size": 3, "Cycle Only": 0}
        self.accessories_list.append(entry_dict)
        entry_dict: dict = {"Accessory Name": "Sponson Turret Mount - 4 space",               "Cost": "2625",  "Space": "-2",	"Weight": "200",   "DP": "",   "Notes": "Uses 2spc but GIVES 4 Spc for Weap. Oversized Only", "Turret Size":  4, "Cycle Only": 0}
        self.accessories_list.append(entry_dict)
        entry_dict: dict = {"Accessory Name": "Tinted Windows",                               "Cost": "500",   "Space": "",	    "Weight": "",      "DP": "",   "Notes": "", "Turret Size":  -2, "Cycle Only": 0}
        self.accessories_list.append(entry_dict)
        entry_dict: dict = {"Accessory Name": "Tire Chains",                                  "Cost": "150",   "Space": "",	    "Weight": "5",     "DP": "",   "Notes": "One purchase per vehicle", "Turret Size":  -2, "Cycle Only": 0}
        self.accessories_list.append(entry_dict)
        entry_dict: dict = {"Accessory Name": "Turret - Four-space",                          "Cost": "3500",  "Space": "-2",	"Weight": "400",   "DP": "",   "Notes": "Uses 2spc but GIVES 4 Spc for Weap. Oversized ", "Turret Size": 4, "Cycle Only": 0}
        self.accessories_list.append(entry_dict)
        entry_dict: dict = {"Accessory Name": "Turret - Pop-up - Zero-space",                 "Cost": "1750",  "Space": "1",	"Weight": "150",   "DP": "",   "Notes": "Uses 1spc For Targeting Laser Only.", "Turret Size":  0, "Cycle Only": 0}
        self.accessories_list.append(entry_dict)
        entry_dict: dict = {"Accessory Name": "Turret - Pop-up - One-space",                  "Cost": "2000",  "Space": "0",	"Weight": "300",   "DP": "",   "Notes": "Uses 1spc GIVES 1 Spc for Weap. Compact+", "Turret Size":  1, "Cycle Only": 0}
        self.accessories_list.append(entry_dict)
        entry_dict: dict = {"Accessory Name": "Turret - Pop-up - Two-space",                  "Cost": "2500",  "Space": "2",	"Weight": "350",   "DP": "",   "Notes": "Uses 4spc GIVES 2 Spc for Weap. Midsize +", "Turret Size":  2, "Cycle Only": 0}
        self.accessories_list.append(entry_dict)
        entry_dict: dict = {"Accessory Name": "Turret - Pop-up - Three-space",                "Cost": "3500",  "Space": "2",	"Weight": "450",   "DP": "",   "Notes": "Uses 5spc GIVES 3 Spc for Weap. Camper+", "Turret Size":  3, "Cycle Only": 0}
        self.accessories_list.append(entry_dict)
        entry_dict: dict = {"Accessory Name": "Turret - Pop-up - Four-space",                 "Cost": "4500",  "Space": "2",	"Weight": "600",   "DP": "",   "Notes": "Uses 6spc GIVES 4 Spc for Weap. Oversized Only", "Turret Size":  4, "Cycle Only": 0}
        self.accessories_list.append(entry_dict)
        entry_dict: dict = {"Accessory Name": "Universal mod for Turret, Cupola, Platform",   "Cost": "1000",  "Space": "",	    "Weight": "",      "DP": "",   "Notes": "Per mount.  Allows vertical firing above 45 degrees (straight up)", "Turret Size":  -2, "Cycle Only": 0}
        self.accessories_list.append(entry_dict)
        entry_dict: dict = {"Accessory Name": "Universal mount for Cycle Turret Sidecar",     "Cost": "1000",  "Space": "",	    "Weight": "",      "DP": "",   "Notes": "", "Turret Size":  -2, "Cycle Only": 0}
        self.accessories_list.append(entry_dict)
        entry_dict: dict = {"Accessory Name": "Weapon Concealment",                           "Cost": "250",   "Space": "",	    "Weight": "50",    "DP": "",   "Notes": "For 1 and 2 space weapons only.  See end of list for larger weapon concealment.", "Turret Size":  -2, "Cycle Only": 0}
        self.accessories_list.append(entry_dict)
        entry_dict: dict = {"Accessory Name": "Weapon Concealment - 3+ space weapons",        "Cost": "250",   "Space": "",	    "Weight": "50",    "DP": "",   "Notes": "Uses 1 space per weapon", "Turret Size":  -2, "Cycle Only": 0}
        self.accessories_list.append(entry_dict)
        entry_dict: dict = {"Accessory Name": "Weapon Timer",                                 "Cost": "350",   "Space": "",	    "Weight": "",      "DP": "",   "Notes": "", "Turret Size":  -2, "Cycle Only": 0}
        self.accessories_list.append(entry_dict)
        entry_dict: dict = {"Accessory Name": "Airbag Restraints",                            "Cost": "200",   "Space": "",	    "Weight": "10",    "DP": "",   "Notes": "", "Turret Size": -2, "Cycle Only": 0}
        self.accessories_list.append(entry_dict)
        entry_dict: dict = {"Accessory Name": "Amphibious Modifications",                     "Cost": "6000",  "Space": "2",	"Weight": "200",   "DP": "4",  "Notes": "Cars, and trikes only; AADA banned.", "Turret Size": -2, "Cycle Only": 0}
        self.accessories_list.append(entry_dict)
        entry_dict: dict = {"Accessory Name": "Anti-radar Camo Netting",                      "Cost": "105",   "Space": "0.5",	"Weight": "60",    "DP": "",   "Notes": "per 0.5-inch covered; must specify terrain", "Turret Size": -2, "Cycle Only": 0}
        self.accessories_list.append(entry_dict)
        entry_dict: dict = {"Accessory Name": "Anti-theft System",                            "Cost": "1000",  "Space": "",	    "Weight": "",      "DP": "",   "Notes": "Plus cost and weight of linked dischargers.", "Turret Size": -2, "Cycle Only": 0}
        self.accessories_list.append(entry_dict)
        entry_dict: dict = {"Accessory Name": "Armored Beer Refrigerator",                    "Cost": "250",   "Space": "2",	"Weight": "50",    "DP": "20", "Notes": "fireproof; AADA banned", "Turret Size": -2, "Cycle Only": 0}
        self.accessories_list.append(entry_dict)
        entry_dict: dict = {"Accessory Name": "Armored Minifridge",                           "Cost": "100",   "Space": "1",	"Weight": "30",    "DP": "10", "Notes": "fireproof; AADA banned", "Turret Size": -2, "Cycle Only": 0}
        self.accessories_list.append(entry_dict)
        entry_dict: dict = {"Accessory Name": "Armored Searchlight",                          "Cost": "500",   "Space": "1",	"Weight": "75",    "DP": "5",  "Notes": "AADA banned if used as damage sink", "Turret Size":  -2, "Cycle Only": 0}
        self.accessories_list.append(entry_dict)
        entry_dict: dict = {"Accessory Name": "Assault Ramp",                                 "Cost": "1000",  "Space": "1",	"Weight": "10",    "DP": "",   "Notes": "Vans only", "Turret Size":  -2, "Cycle Only": 0}
        self.accessories_list.append(entry_dict)
        entry_dict: dict = {"Accessory Name": "ATAD - Central Logic Unit",                    "Cost": "4000",  "Space": "",	    "Weight": "",      "DP": "",   "Notes": "Buy weapon sensors seperately; AADA banned", "Turret Size":  -2, "Cycle Only": 0}
        self.accessories_list.append(entry_dict)
        entry_dict: dict = {"Accessory Name": "ATAD - Sensor Package",                        "Cost": "1000",  "Space": "",	    "Weight": "",      "DP": "",   "Notes": "Per weapon or set of linked weapons; must buy CLU; AADA banned.", "Turret Size":  -2, "Cycle Only": 0}
        self.accessories_list.append(entry_dict)
        entry_dict: dict = {"Accessory Name": "Autopilot",                                    "Cost": "9000",  "Space": "",	    "Weight": "50",    "DP": "",   "Notes": "AADA banned", "Turret Size":  -2, "Cycle Only": 0}
        self.accessories_list.append(entry_dict)
        entry_dict: dict = {"Accessory Name": "Birdcatcher",                                  "Cost": "1000",  "Space": "",	    "Weight": "",      "DP": "",   "Notes": "Destroyed with Power Plant", "Turret Size":  -2, "Cycle Only": 0}
        self.accessories_list.append(entry_dict)
        entry_dict: dict = {"Accessory Name": "Body Blades",                                  "Cost": "33",    "Space": "",	    "Weight": "15",    "DP": "",   "Notes": "$$/Wt Same as 3 pts armor", "Turret Size":  -2, "Cycle Only": 0}
        self.accessories_list.append(entry_dict)
        entry_dict: dict = {"Accessory Name": "Bollix",                                       "Cost": "5000",  "Space": "2",	"Weight": "200",   "DP": "1",  "Notes": "AADA banned", "Turret Size":  -2, "Cycle Only": 0}
        self.accessories_list.append(entry_dict)
        entry_dict: dict = {"Accessory Name": "Brushcutter",                                  "Cost": "100",   "Space": "",	    "Weight": "20",    "DP": "",   "Notes": "Adds 2 hits to pedestrian damage; no hazard from small trees.", "Turret Size":  -2, "Cycle Only": 0}
        self.accessories_list.append(entry_dict)
        entry_dict: dict = {"Accessory Name": "Brushcutter - Retractable",                    "Cost": "250",   "Space": "1",	"Weight": "30",    "DP": "",   "Notes": "", "Turret Size":  -2, "Cycle Only": 0}
        self.accessories_list.append(entry_dict)
        entry_dict: dict = {"Accessory Name": "Bulk Ammo Boxes",                              "Cost": "50",    "Space": "1",	"Weight": "10",    "DP": "5",  "Notes": "FireProof; AADA banned", "Turret Size":  -2, "Cycle Only": 0}
        self.accessories_list.append(entry_dict)
        entry_dict: dict = {"Accessory Name": "Camouflage Netting",                           "Cost": "35",    "Space": "0.5",	"Weight": "20",    "DP": "",   "Notes": "per 0.5 inch square; specify terrain", "Turret Size":  -2, "Cycle Only": 0}
        self.accessories_list.append(entry_dict)
        entry_dict: dict = {"Accessory Name": "Car Top Carrier - 2 space",                    "Cost": "100",   "Space": "",	    "Weight": "50",    "DP": "",   "Notes": "armor at $5/2 / point", "Turret Size":  -2, "Cycle Only": 0}
        self.accessories_list.append(entry_dict)
        entry_dict: dict = {"Accessory Name": "Car Top Carrier - 4 space",                    "Cost": "200",   "Space": "",	    "Weight": "100",   "DP": "",   "Notes": "armor at $7/3 / point", "Turret Size":  -2, "Cycle Only": 0}
        self.accessories_list.append(entry_dict)
        entry_dict: dict = {"Accessory Name": "Car Top Carrier - 6 space",                    "Cost": "400",   "Space": "",	    "Weight": "150",   "DP": "",   "Notes": "armor at $11/6 / point", "Turret Size":  -2, "Cycle Only": 0}
        self.accessories_list.append(entry_dict)
        entry_dict: dict = {"Accessory Name": "Cargo Safe",                                   "Cost": "22000", "Space": "15",	"Weight": "12000", "DP": "",   "Notes": "AADA banned", "Turret Size":  -2, "Cycle Only": 0}
        self.accessories_list.append(entry_dict)
        entry_dict: dict = {"Accessory Name": "Compact Television (CTV)",                     "Cost": "700",   "Space": "",	    "Weight": "",      "DP": "",   "Notes": "", "Turret Size":  -2, "Cycle Only": 0}
        self.accessories_list.append(entry_dict)
        entry_dict: dict = {"Accessory Name": "Computer Gunner",                              "Cost": "6000",  "Space": "",	    "Weight": "10",    "DP": "",   "Notes": " +1 to Hit; AADA banned", "Turret Size":  -2, "Cycle Only": 0}
        self.accessories_list.append(entry_dict)
        entry_dict: dict = {"Accessory Name": "Computer Gunner/Autopilot Software",           "Cost": "2500",  "Space": "",	    "Weight": "",      "DP": "",   "Notes": " +1 to Hit OR +1 to HC; AADA banned", "Turret Size":  -2, "Cycle Only": 0}
        self.accessories_list.append(entry_dict)
        entry_dict: dict = {"Accessory Name": "Computer Navigator",                           "Cost": "500",   "Space": "",	    "Weight": "",      "DP": "",   "Notes": "AADA banned", "Turret Size":  -2, "Cycle Only": 0}
        self.accessories_list.append(entry_dict)
        entry_dict: dict = {"Accessory Name": "Convertible Hardtop",                          "Cost": "1500",  "Space": "2",	"Weight": "50",    "DP": "",   "Notes": "See UACFH p.68 for restrictions; max 20 pts plastic armor (4 pts. metal)", "Turret Size":  -2, "Cycle Only": 0}
        self.accessories_list.append(entry_dict)
        entry_dict: dict = {"Accessory Name": "Cupola - Three-space",                         "Cost": "3500",  "Space": "-1",	"Weight": "400",   "DP": "",   "Notes": "Uses 2 but gives 3 Weapon Spaces", "Turret Size":  3, "Cycle Only": 0}
        self.accessories_list.append(entry_dict)
        entry_dict: dict = {"Accessory Name": "Cupola - Four-space",                          "Cost": "5500",  "Space": "-2",	"Weight": "500",   "DP": "",   "Notes": "Uses 2 But gives 4 Weapon Spaces", "Turret Size":  4, "Cycle Only": 0}
        self.accessories_list.append(entry_dict)
        entry_dict: dict = {"Accessory Name": "Cuploa - Pop-up - Three-space",                "Cost": "4500",  "Space": "2",	"Weight": "600",   "DP": "",   "Notes": "Uses 5 but gives 3 Weapon Spaces.", "Turret Size":  3, "Cycle Only": 0}
        self.accessories_list.append(entry_dict)
        entry_dict: dict = {"Accessory Name": "Cupola - Pop-up - Four-space",                 "Cost": "6500 ", "Space": "2",	"Weight": "750",   "DP": "",   "Notes": "Uses 6 but gives 4 Weapon Spaces", "Turret Size":  4, "Cycle Only": 0}
        self.accessories_list.append(entry_dict)
        entry_dict: dict = {"Accessory Name": "Cycle Blades",                                 "Cost": "50",    "Space": "",     "Weight": "20",    "DP": "",   "Notes": "Adds 2 hits to pedestrian damage.  Destroyed in a roll.", "Turret Size":  -2, "Cycle Only": 1}
        self.accessories_list.append(entry_dict)
        entry_dict: dict = {"Accessory Name": "Cycle Blades - fake",                          "Cost": "20",    "Space": "",	    "Weight": "",      "DP": "",   "Notes": "", "Turret Size":  -2, "Cycle Only": 1}
        self.accessories_list.append(entry_dict)
        entry_dict: dict = {"Accessory Name": "Cycle Turret Sidecar - 1 space",               "Cost": "1530",  "Space": "-2",	"Weight": "-270",  "DP": "",   "Notes": "Max load 550#; 1 weapon space, 1 magazine space; includes first point of armor for 6 facings", "Turret Size":  -2, "Cycle Only": 1}
        self.accessories_list.append(entry_dict)
        entry_dict: dict = {"Accessory Name": "Cycle Turret Sidecar - 2 space",               "Cost": "2530",  "Space": "-3",	"Weight": "-320",  "DP": "",   "Notes": "Max load 800#; 2 weapon spaces, 1 magazine space; includes first point of armor for 6 facings", "Turret Size":  -2, "Cycle Only": 1}
        self.accessories_list.append(entry_dict)
        entry_dict: dict = {"Accessory Name": "Cycle Turret Sidecar Armor - 1 space",         "Cost": "5",     "Space": "",	    "Weight": "5",     "DP": "",   "Notes": "per point.  First point for all six faces included with sidecar.", "Turret Size":  -2, "Cycle Only": 1}
        self.accessories_list.append(entry_dict)
        entry_dict: dict = {"Accessory Name": "Cycle Turret Sidecar Armor - 2 space",         "Cost": "5",     "Space": "",	    "Weight": "6",     "DP": "",   "Notes": "per point.  First point for all six faces included with sidecar.", "Turret Size":  -2, "Cycle Only": 1}
        self.accessories_list.append(entry_dict)
        entry_dict: dict = {"Accessory Name": "Cycle Wheelhubs/guards - Plastic",             "Cost": "10",    "Space": "",	    "Weight": "2",     "DP": "",   "Notes": "Per point of armor, max wt 20lbs; must match vehicular armor type", "Turret Size":  -2, "Cycle Only": 1}
        self.accessories_list.append(entry_dict)
        entry_dict: dict = {"Accessory Name": "Cycle Wheelhubs/guards - MET",                 "Cost": "25",    "Space": "",	    "Weight": "10",    "DP": "",   "Notes": "Per point of armor, max wt 20lbs; must match vehicular armor type", "Turret Size":  -2, "Cycle Only": 1}
        self.accessories_list.append(entry_dict)
        entry_dict: dict = {"Accessory Name": "Cycle Windshell",                              "Cost": "500",   "Space": "",	    "Weight": "50",    "DP": "2",  "Notes": "Pair with spoiler for full effect!  Cannot be combined with sidecar", "Turret Size":  -2, "Cycle Only": 1}
        self.accessories_list.append(entry_dict)
        entry_dict: dict = {"Accessory Name": "Cycle Windshell Armor - Normal",               "Cost": "10",    "Space": "",	    "Weight": "5",     "DP": "",   "Notes": "per point; max 50 lbs", "Turret Size":  -2, "Cycle Only": 1}
        self.accessories_list.append(entry_dict)
        entry_dict: dict = {"Accessory Name": "Cycle Windshell Armor - MET",                  "Cost": "25",    "Space": "",	    "Weight": "25",    "DP": "",   "Notes": "per point; max 50 lbs", "Turret Size":  -2, "Cycle Only": 1}
        self.accessories_list.append(entry_dict)
        entry_dict: dict = {"Accessory Name": "Deadman Sensor",                               "Cost": "100",   "Space": "",	    "Weight": "",      "DP": "",   "Notes": "AADA banned", "Turret Size":  -2, "Cycle Only": 0}
        self.accessories_list.append(entry_dict)
        entry_dict: dict = {"Accessory Name": "Deadman Switch",                               "Cost": "100",   "Space": "",	    "Weight": "",      "DP": "",   "Notes": "AADA banned", "Turret Size":  -2, "Cycle Only": 0}
        self.accessories_list.append(entry_dict)
        entry_dict: dict = {"Accessory Name": "Deluxe Galley",                                "Cost": "2000",  "Space": "8",	"Weight": "500",   "DP": "",   "Notes": "", "Turret Size":  -2, "Cycle Only": 0}
        self.accessories_list.append(entry_dict)
        entry_dict: dict = {"Accessory Name": "Drag Chute - Normal",                          "Cost": "300",   "Space": "1",	"Weight": "20",    "DP": "1",  "Notes": "", "Turret Size":  -2, "Cycle Only": 0}
        self.accessories_list.append(entry_dict)
        entry_dict: dict = {"Accessory Name": "Drag Chute - FP",                              "Cost": "450",   "Space": "1",	"Weight": "20",    "DP": "1",  "Notes": "", "Turret Size":  -2, "Cycle Only": 0}
        self.accessories_list.append(entry_dict)
        entry_dict: dict = {"Accessory Name": "Ejection Seat",                                "Cost": "500",   "Space": "",	    "Weight": "100",   "DP": "",   "Notes": "", "Turret Size":  -2, "Cycle Only": 0}
        self.accessories_list.append(entry_dict)
        entry_dict: dict = {"Accessory Name": "Ejection Seat - no chute or glider",           "Cost": "400",   "Space": "",	    "Weight": "100",   "DP": "",   "Notes": "User takes 3d+3 damage upon landing, preventable only by impact armor", "Turret Size":  -2, "Cycle Only": 0}
        self.accessories_list.append(entry_dict)
        entry_dict: dict = {"Accessory Name": "ERIS Receiver",                                "Cost": "100",   "Space": "",	    "Weight": "",      "DP": "",   "Notes": "", "Turret Size":  -2, "Cycle Only": 0}
        self.accessories_list.append(entry_dict)
        entry_dict: dict = {"Accessory Name": "Extra Driver Controls",                        "Cost": "1000",  "Space": "",	    "Weight": "50",    "DP": "",   "Notes": "", "Turret Size":  -2, "Cycle Only": 0}
        self.accessories_list.append(entry_dict)
        entry_dict: dict = {"Accessory Name": "Fake Blades",                                  "Cost": "20",    "Space": "",	    "Weight": "",      "DP": "",   "Notes": "", "Turret Size":  -2, "Cycle Only": 0}
        self.accessories_list.append(entry_dict)
        entry_dict: dict = {"Accessory Name": "Fake Passengers",                              "Cost": "50",    "Space": "1",	"Weight": "25",    "DP": "1",  "Notes": "AADA banned", "Turret Size":  -2, "Cycle Only": 0}
        self.accessories_list.append(entry_dict)
        entry_dict: dict = {"Accessory Name": "Fake Ramplate",                                "Cost": "150",   "Space": "",	    "Weight": "70",    "DP": "",   "Notes": "", "Turret Size":  -2, "Cycle Only": 0}
        self.accessories_list.append(entry_dict)
        entry_dict: dict = {"Accessory Name": "Fake Turret",                                  "Cost": "250",   "Space": "",	    "Weight": "50",    "DP": "",   "Notes": "", "Turret Size":  -2, "Cycle Only": 0}
        self.accessories_list.append(entry_dict)
        entry_dict: dict = {"Accessory Name": "Fake Weapons",                                 "Cost": "100",   "Space": "",	    "Weight": "20",    "DP": "",   "Notes": "", "Turret Size":  -2, "Cycle Only": 0}
        self.accessories_list.append(entry_dict)
        entry_dict: dict = {"Accessory Name": "Fake Wheelguards and Armored Hubs",            "Cost": "2",     "Space": "",	    "Weight": "1",     "DP": "",   "Notes": "", "Turret Size":  -2, "Cycle Only": 0}
        self.accessories_list.append(entry_dict)
        entry_dict: dict = {"Accessory Name": "Galley",                                       "Cost": "750",   "Space": "2",	"Weight": "150",   "DP": "",   "Notes": "", "Turret Size":  -2, "Cycle Only": 0}
        self.accessories_list.append(entry_dict)
        entry_dict: dict = {"Accessory Name": "Jettison Joinings",                            "Cost": "300",   "Space": "",	    "Weight": "",      "DP": "",   "Notes": "", "Turret Size":  -2, "Cycle Only": 0}
        self.accessories_list.append(entry_dict)
        entry_dict: dict = {"Accessory Name": "Hang Gliders",                                 "Cost": "500",   "Space": "1",	"Weight": "60",    "DP": "",   "Notes": " 1 GE when carried", "Turret Size": -2, "Cycle Only": 0}
        self.accessories_list.append(entry_dict)
        entry_dict: dict = {"Accessory Name": "Hazard Detector",                              "Cost": "500",   "Space": "",	    "Weight": "",      "DP": "",   "Notes": "", "Turret Size":  -2, "Cycle Only": 0}
        self.accessories_list.append(entry_dict)
        entry_dict: dict = {"Accessory Name": "Identification Friend or Foe (IFF)",           "Cost": "200",   "Space": "",	    "Weight": "",      "DP": "",   "Notes": "AADA banned", "Turret Size":  -2, "Cycle Only": 0}
        self.accessories_list.append(entry_dict)
        entry_dict: dict = {"Accessory Name": "Kamibombs",                                    "Cost": "100",   "Space": "1",	"Weight": "100",   "DP": "2",  "Notes": "AADA banned; multiple spaces may be combined into one bomb.", "Turret Size":  -2, "Cycle Only": 0}
        self.accessories_list.append(entry_dict)
        entry_dict: dict = {"Accessory Name": "Laser Comm Array - Comm Laser",                "Cost": "1750",  "Space": "0",	"Weight": "125",   "DP": "",   "Notes": "put on weapons list; to hit 6, no damage, can be used as targeting laser", "Turret Size":  -2, "Cycle Only": 0}
        self.accessories_list.append(entry_dict)
        entry_dict: dict = {"Accessory Name": "Laser Comm Array - Comm Target Round",         "Cost": "200",   "Space": "",	    "Weight": "",      "DP": "",   "Notes": "per side equippped", "Turret Size":  -2, "Cycle Only": 0}
        self.accessories_list.append(entry_dict)
        entry_dict: dict = {"Accessory Name": "Laser Comm Array - Computer",                  "Cost": "3000",  "Space": "",	    "Weight": "",      "DP": "",   "Notes": "Required to send or receive", "Turret Size":  -2, "Cycle Only": 0}
        self.accessories_list.append(entry_dict)
        entry_dict: dict = {"Accessory Name": "Life Raft",                                    "Cost": "500",   "Space": "",	    "Weight": "25",    "DP": "",   "Notes": "", "Turret Size":  -2, "Cycle Only": 0}
        self.accessories_list.append(entry_dict)
        entry_dict: dict = {"Accessory Name": "Long-Distance Radio",                          "Cost": "600",   "Space": "",	    "Weight": "",      "DP": "",   "Notes": "", "Turret Size":  -2, "Cycle Only": 0}
        self.accessories_list.append(entry_dict)
        entry_dict: dict = {"Accessory Name": "Long-Range Radar",                             "Cost": "10000", "Space": "1",	"Weight": "100",   "DP": "",   "Notes": "", "Turret Size":  -2, "Cycle Only": 0}
        self.accessories_list.append(entry_dict)
        entry_dict: dict = {"Accessory Name": "Mini-Safe - Large",                            "Cost": "700",   "Space": "4",	"Weight": "150",   "DP": "",   "Notes": "AADA banned", "Turret Size":  -2, "Cycle Only": 0}
        self.accessories_list.append(entry_dict)
        entry_dict: dict = {"Accessory Name": "Mini-Safe - Small",                            "Cost": "150",   "Space": "1",	"Weight": "20",    "DP": "",   "Notes": "AADA banned", "Turret Size":  -2, "Cycle Only": 0}
        self.accessories_list.append(entry_dict)
        entry_dict: dict = {"Accessory Name": "Motion Compensator",                           "Cost": "0",     "Space": "",	    "Weight": "",      "DP": "",   "Notes": "$5*loaded wt. of weapon, 10% of weapon's unloaded wt.  Use Misc fields.", "Turret Size":  -2, "Cycle Only": 0}
        self.accessories_list.append(entry_dict)
        entry_dict: dict = {"Accessory Name": "Nuclear/Biological/Chemical Shielding (NBC)",  "Cost": "60000", "Space": "1",	"Weight": "50",    "DP": "2",  "Notes": "", "Turret Size":  -2, "Cycle Only": 0}
        self.accessories_list.append(entry_dict)
        entry_dict: dict = {"Accessory Name": "Oversized Vehicle Airfoils",                   "Cost": "1500",  "Space": "",	    "Weight": "150",   "DP": "4",  "Notes": "Per Pair", "Turret Size":  -2, "Cycle Only": 0}
        self.accessories_list.append(entry_dict)
        entry_dict: dict = {"Accessory Name": "Passenger Accomodations",                      "Cost": "500",   "Space": "2",	"Weight": "100",   "DP": "",   "Notes": "Per Passenger", "Turret Size":  -2, "Cycle Only": 0}
        self.accessories_list.append(entry_dict)
        entry_dict: dict = {"Accessory Name": "Personal Parachute",                           "Cost": "200",   "Space": "",	    "Weight": "20",    "DP": "4",  "Notes": "2 GE", "Turret Size":  -2, "Cycle Only": 0}
        self.accessories_list.append(entry_dict)
        entry_dict: dict = {"Accessory Name": "Pickup Racks",                                 "Cost": "150",   "Space": "",	    "Weight": "25",    "DP": "3",  "Notes": "Adds 8 cargo spaces; pickups only; AADA banned", "Turret Size":  -2, "Cycle Only": 0}
        self.accessories_list.append(entry_dict)
        entry_dict: dict = {"Accessory Name": "Pintle Mount, 1-space",                        "Cost": "150",   "Space": "",	    "Weight": "20",    "DP": "",   "Notes": "Mounts any one 1-space weapon", "Turret Size":  -2, "Cycle Only": 0}
        self.accessories_list.append(entry_dict)
        entry_dict: dict = {"Accessory Name": "Pintle Mount, 2-space",                        "Cost": "300",   "Space": "",	    "Weight": "40",    "DP": "",   "Notes": "Mounts any one 2-space weapon", "Turret Size":  -2, "Cycle Only": 0}
        self.accessories_list.append(entry_dict)
        entry_dict: dict = {"Accessory Name": "Portable Camera",                              "Cost": "400",   "Space": "",	    "Weight": "",      "DP": "",   "Notes": "1 GE", "Turret Size":  -2, "Cycle Only": 0}
        self.accessories_list.append(entry_dict)
        entry_dict: dict = {"Accessory Name": "Portable Earth Station",                       "Cost": "700",   "Space": "2",	"Weight": "150",   "DP": "1",  "Notes": "", "Turret Size":  -2, "Cycle Only": 0}
        self.accessories_list.append(entry_dict)
        entry_dict: dict = {"Accessory Name": "Portable Shop",                                "Cost": "4000",  "Space": "4",	"Weight": "300",   "DP": "8",  "Notes": "Four separate cases.", "Turret Size":  -2, "Cycle Only": 0}
        self.accessories_list.append(entry_dict)
        entry_dict: dict = {"Accessory Name": "Radar",                                        "Cost": "2500",  "Space": "",	    "Weight": "",      "DP": "",   "Notes": "", "Turret Size":  -2, "Cycle Only": 0}
        self.accessories_list.append(entry_dict)
        entry_dict: dict = {"Accessory Name": "Radar Detector",                               "Cost": "300",   "Space": "",	    "Weight": "",      "DP": "",   "Notes": "", "Turret Size":  -2, "Cycle Only": 0}
        self.accessories_list.append(entry_dict)
        entry_dict: dict = {"Accessory Name": "Radar Jammer",                                 "Cost": "3000",  "Space": "",	    "Weight": "",      "DP": "",   "Notes": "", "Turret Size":  -2, "Cycle Only": 0}
        self.accessories_list.append(entry_dict)
        entry_dict: dict = {"Accessory Name": "Searchlight",                                  "Cost": "200",   "Space": "1",	"Weight": "50",    "DP": "1",  "Notes": "", "Turret Size":  -2, "Cycle Only": 0}
        self.accessories_list.append(entry_dict)
        entry_dict: dict = {"Accessory Name": "Semi-Trailer Emergency Plate",                 "Cost": "1500",  "Space": "2",	"Weight": "800",   "DP": "8",  "Notes": "", "Turret Size":  -2, "Cycle Only": 0}
        self.accessories_list.append(entry_dict)
        entry_dict: dict = {"Accessory Name": "Skid Stretchers",                              "Cost": "300",   "Space": "",	    "Weight": "25",    "DP": "2",  "Notes": "", "Turret Size":  -2, "Cycle Only": 0}
        self.accessories_list.append(entry_dict)
        entry_dict: dict = {"Accessory Name": "Sonar",                                        "Cost": "4000",  "Space": "1",	"Weight": "100",   "DP": "",   "Notes": "", "Turret Size":  -2, "Cycle Only": 0}
        self.accessories_list.append(entry_dict)
        entry_dict: dict = {"Accessory Name": "Sound Enhancement",                            "Cost": "6000",  "Space": "1",	"Weight": "150",   "DP": "2",  "Notes": "", "Turret Size":  -2, "Cycle Only": 0}
        self.accessories_list.append(entry_dict)
        entry_dict: dict = {"Accessory Name": "Sound System",                                 "Cost": "1000",  "Space": "1",	"Weight": "100",   "DP": "2",  "Notes": "", "Turret Size":  -2, "Cycle Only": 0}
        self.accessories_list.append(entry_dict)
        entry_dict: dict = {"Accessory Name": "Spinal Mounting for Autocannon",               "Cost": "1500",  "Space": "1",	"Weight": "",      "DP": "",   "Notes": "Purchase Autocannon in Weapons Section", "Turret Size":  -2, "Cycle Only": 0}
        self.accessories_list.append(entry_dict)
        entry_dict: dict = {"Accessory Name": "Spinal Mounting for Anti-Tank Gun",            "Cost": "1000",  "Space": "1",	"Weight": "",      "DP": "",   "Notes": "Purchase ATG in Weapons Section", "Turret Size":  -2, "Cycle Only": 0}
        self.accessories_list.append(entry_dict)
        entry_dict: dict = {"Accessory Name": "Spinal Mounting for Blast Canon",              "Cost": "2000",  "Space": "1",	"Weight": "",      "DP": "",   "Notes": "Purchase Blast Cannon in Weapons Section", "Turret Size":  -2, "Cycle Only": 0}
        self.accessories_list.append(entry_dict)
        entry_dict: dict = {"Accessory Name": "Spinal Mounting for Heavy Recoilless Rifle",   "Cost": "2000",  "Space": "1",	"Weight": "",      "DP": "",   "Notes": "Purchase HRR in Weapons Section", "Turret Size":  -2, "Cycle Only": 0}
        self.accessories_list.append(entry_dict)
        entry_dict: dict = {"Accessory Name": "Spinal Mounting for Heavy VMG",                "Cost": "1500",  "Space": "1",	"Weight": "",      "DP": "",   "Notes": "Purchase HVMG in Weapons Section", "Turret Size":  -2, "Cycle Only": 0}
        self.accessories_list.append(entry_dict)
        entry_dict: dict = {"Accessory Name": "Spinal Mounting for Gatling Cannon",           "Cost": "2000",  "Space": "2",	"Weight": "",      "DP": "",   "Notes": "Purchase Gatling Cannon in Weapons Section", "Turret Size":  -2, "Cycle Only": 0}
        self.accessories_list.append(entry_dict)
        entry_dict: dict = {"Accessory Name": "Spinal Mounting for RFTG",                     "Cost": "2500",  "Space": "2",	"Weight": "",      "DP": "",   "Notes": "Purchase RFTG in Weapons Section", "Turret Size":  -2, "Cycle Only": 0}
        self.accessories_list.append(entry_dict)
        entry_dict: dict = {"Accessory Name": "Spinal Mounting for 75mm Tank Gun",            "Cost": "2000",  "Space": "2",	"Weight": "",      "DP": "",   "Notes": "Purchase 75mm Tank Gun in Weapons Section", "Turret Size":  -2, "Cycle Only": 0}
        self.accessories_list.append(entry_dict)
        entry_dict: dict = {"Accessory Name": "Spinal Mounting for Magnetic Cannon",          "Cost": "3000",  "Space": "2",	"Weight": "",      "DP": "",   "Notes": "Purchase Magnetic Cannon in Weapons Section", "Turret Size":  -2, "Cycle Only": 0}
        self.accessories_list.append(entry_dict)
        entry_dict: dict = {"Accessory Name": "Spinal Mounting for HD Flame Thrower",         "Cost": "750",   "Space": "1",	"Weight": "",      "DP": "",   "Notes": "Purchase HD Flame Thrower in Weapons Section", "Turret Size":  -2, "Cycle Only": 0}
        self.accessories_list.append(entry_dict)
        entry_dict: dict = {"Accessory Name": "Spinal Mounting for Military Flame Thrower",   "Cost": "1000",  "Space": "1",	"Weight": "",      "DP": "",   "Notes": "Purchase Military FT in Weapons Section", "Turret Size":  -2, "Cycle Only": 0}
        self.accessories_list.append(entry_dict)
        entry_dict: dict = {"Accessory Name": "Stealth- Cars",                                "Cost": "6000",  "Space": "1",	"Weight": "150",   "DP": "",   "Notes": "", "Turret Size":  -2, "Cycle Only": 0}
        self.accessories_list.append(entry_dict)
        entry_dict: dict = {"Accessory Name": "Stealth - Cycles & Trikes",                    "Cost": "3000",  "Space": "1",	"Weight": "75",    "DP": "",   "Notes": "", "Turret Size":  -2, "Cycle Only": 0}
        self.accessories_list.append(entry_dict)
        entry_dict: dict = {"Accessory Name": "StealthKote Shield",                           "Cost": "110",   "Space": "0",	"Weight": "0",     "DP": "1",  "Notes": "Per armor facing.  StealthKoted shielding destroyed first when face damaged.", "Turret Size":  -2, "Cycle Only": 0}
        self.accessories_list.append(entry_dict)
        entry_dict: dict = {"Accessory Name": "Sunroof",                                      "Cost": "500",   "Space": "",	    "Weight": "25",    "DP": "",   "Notes": "", "Turret Size": 1, "Cycle Only": 0}
        self.accessories_list.append(entry_dict)
        entry_dict: dict = {"Accessory Name": "Surge Protector",                              "Cost": "250",   "Space": "",	    "Weight": "",      "DP": "",   "Notes": "", "Turret Size":  -2, "Cycle Only": 0}
        self.accessories_list.append(entry_dict)
        entry_dict: dict = {"Accessory Name": "Tow Bar",                                      "Cost": "500",   "Space": "",	    "Weight": "25",    "DP": "",   "Notes": "1 spc as cargo", "Turret Size":  -2, "Cycle Only": 0}
        self.accessories_list.append(entry_dict)
        entry_dict: dict = {"Accessory Name": "Truck Turbo",                                  "Cost": "2000",  "Space": "1",	"Weight": "50",    "DP": "",   "Notes": "", "Turret Size":  -2, "Cycle Only": 0}
        self.accessories_list.append(entry_dict)
        entry_dict: dict = {"Accessory Name": "Vehicular Camera",                             "Cost": "1500",  "Space": "0.5",	"Weight": "25",    "DP": "1",  "Notes": "", "Turret Size":  -2, "Cycle Only": 0}
        self.accessories_list.append(entry_dict)
        entry_dict: dict = {"Accessory Name": "Vehicular Computer",                           "Cost": "4000",  "Space": "",	    "Weight": "",      "DP": "",   "Notes": "Same as targeting computer; also runs other applications.", "Turret Size":  -2, "Cycle Only": 0}
        self.accessories_list.append(entry_dict)
        entry_dict: dict = {"Accessory Name": "Vehicular Parachute",                          "Cost": "1500",  "Space": "3",	"Weight": "150",   "DP": "4",  "Notes": "", "Turret Size":  -2, "Cycle Only": 0}
        self.accessories_list.append(entry_dict)
        entry_dict: dict = {"Accessory Name": "Voice Control Software",                       "Cost": "200",   "Space": "",	    "Weight": "",      "DP": "",   "Notes": "Requires Autopilot or Vehicular Computer", "Turret Size":  -2, "Cycle Only": 0}
        self.accessories_list.append(entry_dict)
        entry_dict: dict = {"Accessory Name": "Waterproofed Weapons",                         "Cost": "0",     "Space": "",	    "Weight": "",      "DP": "",   "Notes": " +25% of unloaded weapon cost; use Misc field", "Turret Size":  -2, "Cycle Only": 0}
        self.accessories_list.append(entry_dict)
        entry_dict: dict = {"Accessory Name": "Winch",                                        "Cost": "500",   "Space": "1",	"Weight": "100",   "DP": "1",  "Notes": "", "Turret Size":  -2, "Cycle Only": 0}
        self.accessories_list.append(entry_dict)

    def get_accessories_options(self):
        """Use the existing self.accessories_list and generate a list based on the Accessory Name
           This will allow any dynamic changes to be accurately represented"""
        options: list = []
        for entry in self.accessories_list:
            accessory_name: str = entry.get("Accessory Name")
            options.append(accessory_name)
        return options

    def get_outer_armor_dictionaries(self):
        self.outer_armor_list = []
        entry_dict: dict = {"Outer Armor": "Outer Armor",                "Cost": "0",    "Weight": "0",   "Abbr": "None"}
        self.outer_armor_list.append(entry_dict)
        entry_dict: dict = {"Outer Armor": "Normal Plastic Outer Armor", "Cost": "1",    "Weight": "1",   "Abbr": "Normal"}
        self.outer_armor_list.append(entry_dict)
        entry_dict: dict = {"Outer Armor": "FP Plastic Outer Armor",     "Cost": "2",    "Weight": "1",   "Abbr": "	FP"}
        self.outer_armor_list.append(entry_dict)
        entry_dict: dict = {"Outer Armor": "LR Plastic Outer Armor",     "Cost": "1.1",  "Weight": "1.1", "Abbr": "LR"}
        self.outer_armor_list.append(entry_dict)
        entry_dict: dict = {"Outer Armor": "LRFP Plastic Outer Armor",   "Cost": "2.5",  "Weight": "1.1", "Abbr": "LRFP"}
        self.outer_armor_list.append(entry_dict)
        entry_dict: dict = {"Outer Armor": "RP Plastic Outer Armor",     "Cost": "2",    "Weight": "1",   "Abbr": "RP"}
        self.outer_armor_list.append(entry_dict)
        entry_dict: dict = {"Outer Armor": "RPFP Plastic Outer Armor",   "Cost": "4",    "Weight": "1",   "Abbr": "RPFP"}
        self.outer_armor_list.append(entry_dict)
        entry_dict: dict = {"Outer Armor": "MET Outer Armor",            "Cost": "2.5",  "Weight": "5",   "Abbr": "MET"}
        self.outer_armor_list.append(entry_dict)
        entry_dict: dict = {"Outer Armor": "LR MET Outer Armor",         "Cost": "2.75", "Weight": "5",   "Abbr": "LR MET"}
        self.outer_armor_list.append(entry_dict)

    def get_inner_armor_dictionaries(self):
        self.inner_armor_list = []
        entry_dict: dict = {"Inner Armor": "Inner Armor",                "Cost": "0",    "Weight": "0",   "Abbr": "None"}
        self.inner_armor_list.append(entry_dict)
        entry_dict: dict = {"Inner Armor": "Normal Plastic Inner Armor", "Cost": "1",    "Weight": "1",   "Abbr": "Normal"}
        self.inner_armor_list.append(entry_dict)
        entry_dict: dict = {"Inner Armor": "FP Plastic Inner Armor",     "Cost": "2",    "Weight": "1",   "Abbr": "	FP"}
        self.inner_armor_list.append(entry_dict)
        entry_dict: dict = {"Inner Armor": "LR Plastic Inner Armor",     "Cost": "1.1",  "Weight": "1.1", "Abbr": "LR"}
        self.inner_armor_list.append(entry_dict)
        entry_dict: dict = {"Inner Armor": "LRFP Plastic Inner Armor",   "Cost": "2.5",  "Weight": "1.1", "Abbr": "LRFP"}
        self.inner_armor_list.append(entry_dict)
        entry_dict: dict = {"Inner Armor": "RP Plastic Inner Armor",     "Cost": "2",    "Weight": "1",   "Abbr": "RP"}
        self.inner_armor_list.append(entry_dict)
        entry_dict: dict = {"Inner Armor": "RPFP Plastic Inner Armor",   "Cost": "4",    "Weight": "1",   "Abbr": "RPFP"}
        self.inner_armor_list.append(entry_dict)
        entry_dict: dict = {"Inner Armor": "MET Inner Armor",            "Cost": "2.5",  "Weight": "5",   "Abbr": "MET"}
        self.inner_armor_list.append(entry_dict)
        entry_dict: dict = {"Inner Armor": "LR MET Inner Armor",         "Cost": "2.75", "Weight": "5",   "Abbr": "LR MET"}
        self.inner_armor_list.append(entry_dict)

    def get_outer_armor_options(self):
        options: list = []
        for entry in self.outer_armor_list:
            outer_armor_name: str = entry.get("Outer Armor")
            options.append(outer_armor_name)
        return options

    def get_inner_armor_options(self):
        options: list = []
        for entry in self.inner_armor_list:
            inner_armor_name: str = entry.get("Inner Armor")
            options.append(inner_armor_name)
        return options

    def launch_it(self):
        self.root.mainloop()

    def get_weapon_options_alt(self) -> list:
        """ This will be a comma delimited list of every single selectable weapon in the weapons list.
            This won't be pretty."""
        options = ["Weapon",
                   "SMALL BORE WEAPONS",
                   "LARGE BORE WEAPONS",
                   "GRENADE LAUNCHERS",
                   "GRENADE AMMO",
                   "ROCKETS",
                   "ENERGY WEAPONS",
                   "FLAMETHROWERS",
                   "DROPPED GASSES",
                   "DROPPED LIQUIDS",
                   "DROPPED SOLIDS",
                   "MINEDROPPERS",
                   "DISCHARGERS"]
        return options
    
    def on_select_sub_weapon_unified(self, row_number: int, *args):
        """
        Runs automatically whenever a sub-weapon item is picked.
        Calculates cost, weight, and spaces for this row and updates the screen labels.
        """
        if getattr(self, 'is_loading', False):
            return


        # 1. Safely retrieve the selected sub-weapon name string
        # We look it up from the array we built earlier
        if row_number <= len(self.sub_weapon_dropdown_string_vars):
            selected_weapon = self.sub_weapon_dropdown_string_vars[row_number - 1].get()
        else:
            return

        # Get the category type to obtain the sub weapon data dictionary, from there once we know the selected weapon, get the weapon stats
        try: category_name = self.weapon_dropdown_string_vars[row_number -1].get() 
        except (IndexError, ValueError, tk.TclError): return #This is a systemic failure

        weapon_sub_list = self.get_weapon_sub_list(category=category_name)

        # 2. Grab current quantities from the tracking string variables
        try: qty = int(self.weapon_qty_string_vars[row_number - 1].get())
        except (IndexError, ValueError, tk.TclError): qty = 0
    
        try: ammo_qty = int(self.weapon_ammo_qty_string_vars[row_number - 1].get())
        except (IndexError, ValueError, tk.TclError): ammo_qty = 0
    
        try: extra_mags = int(self.weapon_extra_mag_qty_string_vars[row_number - 1].get())
        except (IndexError, ValueError, tk.TclError): extra_mags = 0
    
        # 3. FETCH WEAPON BASE STATS FROM YOUR DATABASE
        # (Replace 'self.get_weapon_base_stats' with your actual dictionary/database lookup function)

        weapon_stats = next((entry for entry in weapon_sub_list if entry["Drop-Down Name"] == selected_weapon), None)

        #entry_dict: dict = {
        # 'Weapon Name': 'Light Machine Gun',                 
        # 'Drop-Down Name': 'Light Machine Gun - Reg.',                          
        # 'Ammo Type': 'Reg',                         
        # 'Abbv': 'LMG',                         
        # 'Effect': 'Area',                
        # 'To-Hit': '7',      
        # 'Dam': '1D-1',               
        # 'DP': '2',  
        # 'Cost': '850',    
        # 'Weight': '100',  
        # 'Space': '1 ',           
        # 'Shots': '20', 
        # 'Shot Cost': '20',    
        # 'Shot Weight': '2.5'   ,
        # 'Loaded Cost': '1250',   
        # 'Loaded Weight': '150',  
        # 'Mag Cost': '450',   
        # 'Mag Weight': '65'}

        if not weapon_stats:
            # Fallback to zero if the item name isn't found
            weapon_stats = {"base_cost": 0, "base_weight": 0, "base_space": 0.0, "ammo_cost_per": 0, "ammo_weight_per": 0}
    
        # 4. MATH ENGINE CALCULATIONS
        # Cost = (Base Weapon Cost * Qty) + (Ammo Cost * Ammo Qty) + (Extra Mag Costs, etc.)
        #total_cost = (weapon_stats["Cost"] * qty) + (weapon_stats["Shot Cost"] * ammo_qty)
        total_cost = int(res) if (res := (float(weapon_stats["Cost"]) * qty) + (float(weapon_stats["Shot Cost"]) * ammo_qty) + 50 * extra_mags).is_integer() else round(res, 2)

        #total_weight = (weapon_stats["Weight"] * qty) + (weapon_stats["Shot Weight"] * ammo_qty)
        total_weight = int(w_res) if (w_res := (float(weapon_stats["Weight"]) * qty) + (float(weapon_stats["Shot Weight"]) * ammo_qty) + 15 * extra_mags).is_integer() else round(w_res, 2)

        #total_space = weapon_stats["Space"] * qty
        total_space = int(s_res) if (s_res := float(weapon_stats["Space"]) * qty + extra_mags).is_integer() else round(s_res, 2)

        dp_str = weapon_stats["DP"]
        to_hit_str = weapon_stats["To-Hit"]
        damage_str = weapon_stats["Dam"]
    
        # 5. REWRITE THE ROW LABELS ON SCREEN (Breaking the $0 loop!)
        if row_number <= len(self.weapon_cost_label_objects):
            cost_lbl = self.weapon_cost_label_objects[row_number - 1]
            cost_lbl.config(text=f"{total_cost}")

        if row_number <= len(self.weapon_weight_label_objects):
            weight_lbl = self.weapon_weight_label_objects[row_number - 1]
            weight_lbl.config(text=f"{total_weight}")

        if row_number <= len(self.weapon_spaces_label_objects):
            space_lbl = self.weapon_spaces_label_objects[row_number - 1]
            space_lbl.config(text=f"{total_space}")

        if row_number <= len(self.weapon_dp_label_objects):
            dp_lbl = self.weapon_dp_label_objects[row_number - 1]
            dp_lbl.config(text=f"{dp_str}")

        if row_number <= len(self.weapon_to_hit_label_objects):
            to_hit_lbl = self.weapon_to_hit_label_objects[row_number - 1]
            to_hit_lbl.config(text=f"{to_hit_str}")

        if row_number <= len(self.weapon_damage_label_objects):
            dam_lbl = self.weapon_damage_label_objects[row_number - 1]
            dam_lbl.config(text=f"{damage_str}")

        # 6. TRIGGER THE GLOBAL RECALCULATE ENGINE FOR VEHICLE TOTALS
        if hasattr(self, 'recalculate'):
            self.recalculate()

    def add_to_sub_weapon_row_unified(self, row_number: int, entry: dict):
        """
        A single, unified function that dynamically populates hidden recovery labels, 
        visible screen display values, and calculates multiplier weights/costs for all 10 rows.
        """
        drop_down_name       = entry.get("Drop-Down Name", "")
        weapon_name          = entry.get("Weapon Name", "")
        weapon_ammo_type     = entry.get("Ammo Type", "")
        weapon_abbv          = entry.get("Abbv", "")
        weapon_effect        = entry.get("Effect", "")
        weapon_to_hit        = entry.get("To-Hit", entry.get("To-HIt", entry.get("To- Hit", "7")))
        weapon_damage        = entry.get("Dam", "")
        weapon_dp            = entry.get("DP", "0")
        weapon_cost          = entry.get("Cost", "0")
        weapon_weight        = entry.get("Weight", "0")
        weapon_space         = entry.get("Space", "0")
        weapon_shots         = entry.get("Shots", "0")
        weapon_shot_cost     = entry.get("Shot Cost", "0")
        weapon_shot_weight   = entry.get("Shot Weight", "0")
        weapon_loaded_cost   = entry.get("Loaded Cost", "0")
        weapon_loaded_weight = entry.get("Loaded Weight", "0")
        weapon_mag_cost      = entry.get("Mag Cost", "0")
        weapon_mag_weight    = entry.get("Mag Weight", "0")

        # 1. FIXED EXHAUSTIVE HIDDEN MAPPINGS:
        # Maps keys exactly to what your legacy background calculations look for
        hidden_mappings = [
            ("name", weapon_name),
            ("drop_down_name", drop_down_name),
            ("ammo_type", weapon_ammo_type),
            ("abbv", weapon_abbv),
            ("effect", weapon_effect),
            ("to_hit", weapon_to_hit),
            ("damage", weapon_damage),
            ("dp", weapon_dp),
            ("cost", weapon_cost),
            ("weight", weapon_weight),
            ("space", weapon_space),
            ("shots", weapon_shots),
            ("ammo_cost", weapon_shot_cost),
            ("ammo_weight", weapon_shot_weight),
            ("loaded_cost", weapon_loaded_cost),
            ("loaded_weight", weapon_loaded_weight),
            ("mag_cost", weapon_mag_cost),
            ("mag_weight", weapon_mag_weight)
        ]

        for suffix, value in hidden_mappings:
            lbl_attr = f"label_hidden_sub_weapon_{row_number}_{suffix}"
            if hasattr(self, lbl_attr):
                getattr(self, lbl_attr).configure(text=str(value))

        # 2. Handle Quantity Multipliers for Ammunition
        # 2. Handle Quantity Multipliers for Ammunition with Robust Tkinter Guards
        # 2. SEPARATE WEAPON QTY FROM AMMO QTY
        qty_var_name = f"var_sub_weapon_{row_number}_qty"
        ammo_var_name = f"var_sub_weapon_ammo_{row_number}_qty"
        mags_var_name = f"var_sub_weapon_extra_mags_{row_number}_qty"
        
        current_qty = 1
        current_ammo_qty = 0 # Independent tracking variable
        current_mags_qty = 0 # Independent Extra Magazines Tracking Variable

        # Safe extraction for Weapon Count
        if hasattr(self, qty_var_name) and getattr(self, qty_var_name) is not None:
            try:
                raw_qty_val = getattr(self, qty_var_name).get()
                current_qty = int(raw_qty_val) if str(raw_qty_val).strip() != "" else 0
            except (ValueError, tk.TclError):
                current_qty = 0

        # Safe extraction for actual Ammunition Count
        if hasattr(self, ammo_var_name) and getattr(self, ammo_var_name) is not None:
            try:
                raw_ammo_val = getattr(self, ammo_var_name).get()
                current_ammo_qty = int(raw_ammo_val) if str(raw_ammo_val).strip() != "" else 0
            except (ValueError, tk.TclError):
                current_ammo_qty = 0

        # Safe extraction for Extra Magazines Count
        if hasattr(self, mags_var_name) and getattr(self, mags_var_name) is not None:
            try:
                raw_mags_val = getattr(self, mags_var_name).get()
                current_mags_qty = int(raw_mags_val) if str(raw_mags_val).strip() != "" else 0
            except (ValueError, tk.TclError): current_mags_qty = 0

        try:
            numeric_shot_cost = float(weapon_shot_cost)
            numeric_shot_weight = float(weapon_shot_weight)
            numeric_cost = float(weapon_cost)
            numeric_weight = float(weapon_weight)
            numeric_space = float(weapon_space)
        except ValueError:
            numeric_shot_cost = 0.0
            numeric_shot_weight = 0.0
            numeric_cost = 0.0
            numeric_weight = 0.0
            numeric_space = 0.0

        # 🎯 THE STATIC EXTRA MAGS FIX: Compute flat $50 and 15 lbs per magazine
        calculated_mag_cost = 50.0 * current_mags_qty
        calculated_mag_weight = 15.0 * current_mags_qty

        # 🎯 THE CRITICAL FIX: Multiply ammo metrics against current_ammo_qty, NOT current_qty!
        calculated_ammo_cost = numeric_shot_cost * current_ammo_qty + calculated_mag_cost
        calculated_ammo_weight = numeric_shot_weight * current_ammo_qty + calculated_mag_weight
        
        # Calculate weapon totals separately
        total_row_cost = numeric_cost * current_qty
        total_row_weight = numeric_weight * current_qty
        total_row_space = numeric_space * current_qty + current_mags_qty

        #qty_var_name = f"var_sub_weapon_{row_number}_qty"
        #current_qty = 1
        
        #if hasattr(self, qty_var_name) and getattr(self, qty_var_name) is not None:
        #    try:
        #        # Safely pull the string first to evaluate blank states
        #        raw_qty_val = getattr(self, qty_var_name).get()
        #        current_qty = int(raw_qty_val) if str(raw_qty_val).strip() != "" else 0
        #    except (ValueError, tk.TclError):
        #        # Safely defaults to 0 if the entry field is wiped blank or has non-numeric text
        #        current_qty = 0

        #try:
        #    numeric_shot_cost = float(weapon_shot_cost)
        #    numeric_shot_weight = float(weapon_shot_weight)
        #    numeric_cost = float(weapon_cost)
        #    numeric_weight = float(weapon_weight)
        #    numeric_space = float(weapon_space)
        #except ValueError:
        #    numeric_shot_cost = 0.0
        #    numeric_shot_weight = 0.0
        #    numeric_cost = 0.0
        #    numeric_weight = 0.0
        #    numeric_space = 0.0

        #calculated_ammo_cost = numeric_shot_cost * current_qty
        #calculated_ammo_weight = numeric_shot_weight * current_qty
        
        # Calculate row totals based on active weapon count
        #total_row_cost = numeric_cost * current_qty
        #total_row_weight = numeric_weight * current_qty
        #total_row_space = numeric_space * current_qty

        # 3. FIXED EXPLICIT VISIBLE SCREEN UPDATES:
        # Directly updates the text of your active screen layout grid elements
        visible_mappings = [
            ("cost", total_row_cost),
            ("weight", total_row_weight),
            ("space", total_row_space),
            ("dp", weapon_dp),
            ("shots", weapon_shots),
            ("ammo_cost", calculated_ammo_cost),
            ("ammo_weight", calculated_ammo_weight),
            ("tohit", weapon_to_hit),
            ("damage", weapon_damage)
        ]

        for suffix, value in visible_mappings:
            lbl_attr = f"label_sub_weapon_{row_number}_{suffix}"
            if hasattr(self, lbl_attr):
                getattr(self, lbl_attr).configure(text=str(value))

        # 4. Trigger downstream updates
        update_method_name = f"on_update_sub_weapon_{row_number}_qty"
        if hasattr(self, update_method_name):
            getattr(self, update_method_name)()

    def add_labels_buttons_weapon_row_unified(self, canvas_type, row_number):
        """
        Weapon Row Layout Builder.
        Standardizes drop-down elements to matching themed ttk.OptionMenu components.
        Fixes sub-dropdown list extraction to show only the weapon's text name.
        """
        up_arrow = "\u2191"
        down_arrow = "\u2193"        

        # 1. Instantiate the row-isolated data tracking variables
        category_var  = tk.StringVar(canvas_type, value="Weapon")
        weapon_var    = tk.StringVar(canvas_type, value="Select Item...")
        qty_var       = tk.StringVar(canvas_type, value="0")
        ammo_var      = tk.StringVar(canvas_type, value="0")
        mag_var       = tk.StringVar(canvas_type, value="0")
        
        # Write to tracking lists for backend engine calculation integrity
        self.weapon_dropdown_string_vars.append(weapon_var)
        self.weapon_qty_string_vars.append(qty_var)
        self.weapon_ammo_qty_string_vars.append(ammo_var)
        self.weapon_extra_mag_qty_string_vars.append(mag_var)

        # -------------------------------------------------------------------------
        # COL 0: Dual-Tier Dropdowns (Styled strictly as ttk.OptionMenu elements)
        # -------------------------------------------------------------------------
        dropdown_cluster = tk.Frame(canvas_type)
        dropdown_cluster.grid(row=row_number, column=self.grid_col_item, sticky="w")

        # Fetch Category strings dynamically from your engine layout code
        weapon_options_list = self.get_weapon_options_alt()
        if not weapon_options_list:
            weapon_options_list = ["No items available"]

        # 1a. Primary Dropdown Menu (Themed via ttk)
        category_dropdown = ttk.OptionMenu(
            dropdown_cluster, 
            category_var, 
            "Weapon",
            *weapon_options_list,
            command=lambda chosen_cat, r=row_number, c=dropdown_cluster, wv=weapon_var: self.on_weapon_category_changed(chosen_cat, r, c, wv)
        )
        category_dropdown.pack(side="top", fill="x", anchor="w")

        # Fetch raw weapon sub-lists from database tracking dict
        raw_sub_weapons = self.get_weapon_sub_list(category_var.get())
        
        # CRUCIAL FIX: Parse dictionary list down to text name strings safely [1]
        if raw_sub_weapons and isinstance(raw_sub_weapons[0], dict):
            sub_weapons_list = [item.get("Drop-Down Name", "Unknown Weapon") for item in raw_sub_weapons]
        else:
            sub_weapons_list = ["Select Item..."]

        # 1b. Secondary Sub-Dropdown Menu (Themed via ttk, formed inline)
        sub_weapon_dropdown = ttk.OptionMenu(
            dropdown_cluster, 
            weapon_var, 
            "Select Item...",
            *sub_weapons_list
        )
        sub_weapon_dropdown.pack(side="top", fill="x", anchor="w", pady=(4, 0))
        self.weapon_dropdown_objects.append(sub_weapon_dropdown)

        # =========================================================================
        # CRUCIAL LAYOUT CORRECTION: Shifting numerical control widgets
        # downward exactly 2 full rows using the row=(row_number + 2) track.
        # =========================================================================
        target_control_row = row_number + 2

        # -------------------------------------------------------------------------
        # COL 1 - 3: Main Weapon Qty Track
        # -------------------------------------------------------------------------
        weapon_qty_entry = tk.Entry(canvas_type, width=3, textvariable=qty_var, command=lambda r=row_number: self.on_select_sub_weapon_unified(row_number=r))
        weapon_qty_entry.grid(row=target_control_row, column=self.grid_col_qty)
        self.weapon_qty_entry_objects.append(weapon_qty_entry)

        weapon_qty_up_btn = tk.Button(canvas_type, text=up_arrow, command=lambda r=row_number: self.on_button_sub_weapon_qty_unified(r, direction="up"))
        weapon_qty_up_btn.grid(row=target_control_row, column=self.grid_left_up_button)
        self.weapon_qty_up_button_objects.append(weapon_qty_up_btn)

        weapon_qty_down_btn = tk.Button(canvas_type, text=down_arrow, command=lambda r=row_number: self.on_button_sub_weapon_qty_unified(r, direction="down"))
        weapon_qty_down_btn.grid(row=target_control_row, column=self.grid_left_down_button)
        self.weapon_qty_down_button_objects.append(weapon_qty_down_btn)

        # -------------------------------------------------------------------------
        # COL 4 - 6: Ammo Track
        # -------------------------------------------------------------------------
        ammo_qty_entry = tk.Entry(canvas_type, width=3, textvariable=ammo_var, command=lambda r=row_number: self.on_select_sub_weapon_unified(row_number=r))
        ammo_qty_entry.grid(row=target_control_row, column=self.grid_right_qty)
        self.weapon_ammo_qty_entry_objects.append(ammo_qty_entry)

        ammo_qty_up_btn = tk.Button(canvas_type, text=up_arrow, command=lambda r=row_number: self.on_button_ammo_qty_unified(r, direction="up"))
        ammo_qty_up_btn.grid(row=target_control_row, column=self.grid_right_up_button)
        self.weapon_ammo_qty_up_button_objects.append(ammo_qty_up_btn)

        ammo_qty_down_btn = tk.Button(canvas_type, text=down_arrow, command=lambda r=row_number: self.on_button_ammo_qty_unified(r, direction="down"))
        ammo_qty_down_btn.grid(row=target_control_row, column=self.grid_left_down_button)
        self.weapon_ammo_qty_down_button_objects.append(ammo_qty_down_btn)

        # -------------------------------------------------------------------------
        # COL 7 - 9: Extra Mags Track
        # -------------------------------------------------------------------------
        extra_mag_entry = tk.Entry(canvas_type, width=3, textvariable=mag_var, command=lambda r=row_number: self.on_select_sub_weapon_unified(row_number=r))
        extra_mag_entry.grid(row=target_control_row, column=self.grid_col_weapon_ammo_entry)
        self.weapon_extra_mag_qty_entry_objects.append(extra_mag_entry)

        extra_mag_up_btn = tk.Button(canvas_type, text=up_arrow, command=lambda r=row_number: self.on_button_extra_mags_unified(r, direction="up"))
        extra_mag_up_btn.grid(row=target_control_row, column=self.grid_col_weapon_ammo_qty_up)
        self.weapon_extra_mag_qty_up_button_objects.append(extra_mag_up_btn)

        extra_mag_down_btn = tk.Button(canvas_type, text=down_arrow, command=lambda r=row_number: self.on_button_extra_mags_unified(r, direction="down"))
        extra_mag_down_btn.grid(row=target_control_row, column=self.grid_col_weapon_ammo_qty_down)
        self.weapon_extra_mag_qty_down_button_objects.append(extra_mag_down_btn)

        # -------------------------------------------------------------------------
        # COL 13 - 17: Read-Only Calculated Output Data Cells
        # -------------------------------------------------------------------------
        weapon_cost_label = tk.Label(canvas_type, text="$0", width=6, anchor="e")
        weapon_cost_label.grid(row=target_control_row, column=self.grid_col_cost, sticky="e")
        self.weapon_cost_label_objects.append(weapon_cost_label)

        weapon_weight_label = tk.Label(canvas_type, text="0", width=6, anchor="e")
        weapon_weight_label.grid(row=target_control_row, column=self.grid_col_weight, sticky="e")
        self.weapon_weight_label_objects.append(weapon_weight_label)

        weapon_space_label = tk.Label(canvas_type, text="0", width=4, anchor="center")
        weapon_space_label.grid(row=target_control_row, column=self.grid_col_spaces, sticky="c")
        self.weapon_spaces_label_objects.append(weapon_space_label)

        weapon_dp_label = tk.Label(canvas_type, text="0", width=4, anchor="center")
        weapon_dp_label.grid(row=target_control_row, column=self.grid_col_dp, sticky="c")
        self.weapon_dp_label_objects.append(weapon_dp_label)

        # -------------------------------------------------------------------------
        # COL 18+: Row Management Action Column
        # -------------------------------------------------------------------------
        delete_weapon_row_btn = tk.Button(canvas_type, text="✕", fg="red", command=lambda r=row_number: self.remove_weapon_row(r))
        delete_weapon_row_btn.grid(row=target_control_row, column=self.grid_col_power_factors, padx=5)
        self.weapon_delete_button_objects.append(delete_weapon_row_btn)

    def on_weapon_category_changed(self, selected_category, row_number, cluster_frame):
        """
        Triggers when the first tier dropdown updates.
        Clears the old sub-weapon options and dynamically repopulates the new subset
        directly beneath the Category selector without touching the Category menu.
        """
        # 1. Fetch filtered weapons array passing selection context
        filtered_weapons = self.get_weapon_sub_list(selected_category)
        if not filtered_weapons:
            filtered_weapons = [{"Drop-Down Name": "No items available"}]
    
        weapon_name_list = []
        for entry in filtered_weapons:
            weapon_name_list.append(entry.get("Drop-Down Name"))
    
        # 2. Calculate the row coordinates matching your tactical row setup
        row_top = 2 + ((row_number - 1) * 2)
        row_bottom = row_top + 1
    
        # 3. Setup the text tracking variable for the sub-selection
        default_val = weapon_name_list[0] if weapon_name_list else "Select Weapon"
        sub_weapon_var = tk.StringVar(value=default_val)
        
        # 4. Clean up old sub-dropdown widgets tracking your weapon objects safely
        # FIX: Check self.sub_weapon_dropdown_objects to leave the category menu alone!
        if row_number <= len(self.sub_weapon_dropdown_objects):
            old_widget = self.sub_weapon_dropdown_objects[row_number - 1]
            if old_widget is not None:
                try:
                    old_widget.grid_forget()
                    old_widget.destroy()
                except Exception:
                    pass
    
        # Track or replace the sub-weapon string tracking variable cleanly by index slot
        if row_number <= len(self.sub_weapon_dropdown_string_vars):
            self.sub_weapon_dropdown_string_vars[row_number - 1] = sub_weapon_var
        else:
            self.sub_weapon_dropdown_string_vars.append(sub_weapon_var)
            
        # 5. Generate the new sub-options selector menu 
        new_dropdown = ttk.OptionMenu(cluster_frame, sub_weapon_var, default_val, *weapon_name_list)
        new_dropdown.grid(row=row_bottom, column=self.grid_col_item, sticky="w")
    
        # FIX: Store or replace the widget reference in the dedicated sub-weapon array
        if row_number <= len(self.sub_weapon_dropdown_objects):
            self.sub_weapon_dropdown_objects[row_number - 1] = new_dropdown
        else:
            self.sub_weapon_dropdown_objects.append(new_dropdown)
    
        # 6. Securely trace variable tracking updates
        sub_weapon_var.trace_add(
            "write", 
            lambda *args, r=row_number: (
                self.on_select_sub_weapon_unified(r)
                if (getattr(self, 'is_loading', False) is False) else None
            )
        )

    def add_dropdown_weapon_alt_unified(self, row_number: int, canvas_type):
        """
        A single, unified layout method that dynamically instantiates, grids,
        and binds trace triggers for any of the 10 core weapon category dropdown menus.
        """
        # 1. Instantiate the row's String tracking variable and set its default text
        var_name = f"selected_weapon_alt_{row_number}"
        var_obj = tk.StringVar(value="Weapon")
        setattr(self, var_name, var_obj)
        
        # 2. Query your central rules database to fetch available equipment categories
        options = self.get_weapon_options_alt()
        
        # 3. Dynamically fetch the correct grid row tracking attribute index
        row_attr_name = f"grid_row_weapon_alt_{row_number}"
        if not hasattr(self, row_attr_name):
            return
        target_grid_row = getattr(self, row_attr_name)
        
        # 4. Create and grid the ttk.OptionMenu dropdown control widget
        dropdown_name = f"weapon_alt_{row_number}_dropdown"
        dropdown_obj = ttk.OptionMenu(canvas_type, var_obj, "Weapon", *options)
        setattr(self, dropdown_name, dropdown_obj)
        dropdown_obj.grid(column=self.grid_col_item, row=target_grid_row, sticky="w")
        
        # 5. REFACTORED VIA LAMBDA: Intercepts the trace write and cleanly routes it to your
        # new single centralized choice tracking function, preserving the row and container frame.
        var_obj.trace_add(
            "write", 
            lambda *args, rn=row_number, c=canvas_type: self.on_select_weapon_alt_unified_canvas(rn, c, *args)
        )

    def add_dropdown_sub_weapon_unified(self, row_number: int, canvas_type, dropdown_list: list = None):
        """
        A single, unified layout method that dynamically clears out legacy widgets 
        and builds the secondary sub-weapon dropdown selection menu for any row 1-10.
        """
        # Define dynamic attribute string handles for this specific row index
        selected_var_attr = f"selected_sub_weapon_{row_number}_canvas"
        dropdown_widget_attr = f"sub_weapon_dropdown_{row_number}_canvas"
        
        # 1. CLEANUP PASS: Safely remove and erase pre-existing instances of widgets or variables
        if hasattr(self, selected_var_attr) and getattr(self, selected_var_attr) is not None:
            setattr(self, selected_var_attr, None)
            
        if hasattr(self, dropdown_widget_attr):
            old_dropdown = getattr(self, dropdown_widget_attr)
            if old_dropdown is not None:
                old_dropdown.grid_forget() # Erase it cleanly from the visual workspace screen
                setattr(self, dropdown_widget_attr, None)

        # 2. BLANK/RESET TRIGGER: If no dynamic data pool array list is provided, force reset statistics to zero
        if dropdown_list is None:
            qty_mappings = [
                (f"var_sub_weapon_{row_number}_qty", 0),
                (f"var_sub_weapon_ammo_{row_number}_qty", 0),
                (f"var_sub_weapon_extra_mags_{row_number}_qty", 0)
            ]
            for attr_name, default_val in qty_mappings:
                if hasattr(self, attr_name) and getattr(self, attr_name) is not None:
                    getattr(self, attr_name).set(default_val)
                    
        facing_attr = f"weapon_armor_facing_{row_number}" #this doesn't exist yet

        # 3. INITIALIZATION PASS: Instantiate a safe, row-isolated text tracking variable
        new_str_var = tk.StringVar(value="Weapon")
        setattr(self, selected_var_attr, new_str_var)
        
        # 4. DATA COMPILATION: Query your master rules listings to gather matching sub-weapons
        options = self.get_weapon_options_sub_list(input_list=dropdown_list)
        
        # 5. GRID PLACEMENT: Calculate row index coordinates and instantiate the new OptionMenu widget
        row_grid_attr = f"grid_row_sub_weapon_alt_{row_number}"
        target_grid_row = getattr(self, row_grid_attr) if hasattr(self, row_grid_attr) else row_number
        
        new_dropdown = ttk.OptionMenu(canvas_type, new_str_var, "Weapon", *options)
        setattr(self, dropdown_widget_attr, new_dropdown)
        new_dropdown.grid(column=self.grid_col_item, row=target_grid_row, sticky="w")
        option_list = [dropdown_entry["Drop-Down Name"] for dropdown_entry in dropdown_list]
        
        # 6. EVENT INTERCEPTION: Capture trace writes with isolated variable states
        new_str_var.trace_add(
            "write", 
            lambda *trace_args, r=row_number, d=dropdown_list: (
                self.on_select_sub_weapon_unified(row_number=r)
            )
        )

    def on_select_weapon_alt_unified_canvas(self, row_number, canvas_type=None, *args):
        """
        A single, centralized handler that processes top-level weapon category changes (1-10),
        compiles matching rulesets based on the 12 precise categories, and builds secondary weapon menus.
        """
        # 1. RIGID SAFETY GUARD: Terminate immediately if a file record is actively loading
        if getattr(self, "is_loading", False):
            return

        # 2. TKINTER BIND COMPATIBILITY LAYER: Handle implicit event object routing
        if not isinstance(row_number, int):
            # If bound via .bind(), the first argument passed to the function is the Event object
            event = row_number
            try:
                # Fallback: recover the canvas container from the widget parent context
                if canvas_type is None or not isinstance(canvas_type, (tk.Frame, tk.Canvas)):
                    canvas_type = event.widget.master
                
                # Recover the specific integer row number from a custom property or the widget name
                # (Adjust the following line to match how you track row identities in your UI code)
                row_number = int(re.search(r'\d+', str(event.widget)).group())
            except (AttributeError, ValueError, IndexError):
                return # Terminate execution safely if context cannot be reliably determined

        # 3. If canvas_type wasn't supplied or passed correctly, fall back to second_frame
        if canvas_type is None:
            canvas_type = getattr(self, "second_frame", None)

        # 4. Dynamically fetch the selected top-level category text string
        var_name = f"selected_weapon_alt_{row_number}"
        if not hasattr(self, var_name):
            return
        raw_category = getattr(self, var_name).get()
        
        selected_category = str(raw_category).strip().upper()

        # 5. Execute secure external data matrix lookup
        try:
            compiled_list = self.get_weapon_sub_list(category=selected_category)
        except Exception:
            compiled_list = [] # Fallback container if database lookup keys disconnect

        # 6. Hand off execution cleanly to your unified sub-weapon dropdown builder function
        self.add_dropdown_sub_weapon_unified(
            row_number    = row_number,
            canvas_type   = canvas_type,
            dropdown_list = compiled_list
        )

    def update_weapon_row_statistics_forced(self, row_number: int):
        """
        Forces a weapon lookup and label update for a single row during file loads,
        bypassing background execution flags and canvas rebuild loops.
        """
        var_name = f"selected_weapon_alt_{row_number}"
        if not hasattr(self, var_name):
            return
            
        selected_category = str(getattr(self, var_name).get()).strip().upper()
        
        # 1. Fetch data arrays directly 
        try:
            compiled_list = self.get_weapon_sub_list(category=selected_category)
        except Exception:
            compiled_list = []

        # 2. Directly trigger your database mapping logic or row refresh routine
        selected_category: str = getattr(self, f"selected_weapon_alt_{row_number}").get()
        dropdown_list = self.get_weapon_sub_list(category=selected_category)
        var_name = f"selected_sub_weapon_{row_number}_canvas"
        if not hasattr(self, var_name):
            return
        selected_value = getattr(self, var_name).get()

        for entry in dropdown_list:
            if selected_value == entry.get("Drop-Down Name"):
                # Forcefully inject statistics into both hidden and visible fields
                self.add_to_sub_weapon_row_unified(row_number, entry)
                break

            self.add_to_sub_weapon_row_unified(row_number, entry=entry)

    def add_dropdown_sub_weapon_unified(self, row_number: int, canvas_type, dropdown_list: list = None):
        """
        A single, unified layout method that dynamically clears out legacy widgets 
        and builds the secondary sub-weapon dropdown selection menu for any row 1-10.
        """
        selected_var_attr = f"selected_sub_weapon_{row_number}_canvas"
        dropdown_widget_attr = f"sub_weapon_dropdown_{row_number}_canvas"
        
        # 1. CLEANUP PASS: Safely remove and erase pre-existing instances of widgets or variables
        if hasattr(self, selected_var_attr) and getattr(self, selected_var_attr) is not None:
            setattr(self, selected_var_attr, None)
            
        if hasattr(self, dropdown_widget_attr):
            old_dropdown = getattr(self, dropdown_widget_attr)
            if old_dropdown is not None:
                try: old_dropdown.grid_forget()
                except Exception: pass
                setattr(self, dropdown_widget_attr, None)

        # 2. BLANK/RESET TRIGGER: If no dynamic list is provided, force reset statistics to zero
        if dropdown_list is None:
            qty_mappings = [
                (f"var_sub_weapon_{row_number}_qty", 0),
                (f"var_sub_weapon_ammo_{row_number}_qty", 0),
                (f"var_sub_weapon_extra_mags_{row_number}_qty", 0)
            ]
            for attr_name, default_val in qty_mappings:
                if hasattr(self, attr_name) and getattr(self, attr_name) is not None:
                    getattr(self, attr_name).set(default_val)
                    
        # 3. INITIALIZATION PASS: Instantiate a safe, row-isolated text tracking variable
        new_str_var = tk.StringVar(value="Weapon")
        setattr(self, selected_var_attr, new_str_var)
        
        # Create a new StringVar instance dynamically for each row
        string_var = tk.StringVar()
        string_var.set("Weapon")
            
        # Assign the StringVar object to the dynamically constructed attribute name
        setattr(self, f"selected_sub_weapon_{row_number}_canvas", string_var)        
        #self.selected_sub_weapon_1_canvas = tk.StringVar()
        #self.selected_sub_weapon_1_canvas.set("Weapon")
        # Create the dropdown widget

        option_list = [dropdown_entry["Drop-Down Name"] for dropdown_entry in dropdown_list]

        # Capture the current index in a default argument for the lambda function
        dropdown = ttk.OptionMenu(canvas_type, getattr(self, f"selected_sub_weapon_{row_number}_canvas"), 
                "Weapon", *option_list, command=lambda selected_value, idx=row_number: self.on_select_sub_weapon_unified(idx))
            
        # Store the dropdown widget object dynamically
        setattr(self, f"selected_sub_weapon_dropdown_{row_number}", dropdown)
            
        # Grid the newly created dropdown widget using the row tracker positional offset
        dropdown.grid(column=self.grid_col_item, row=getattr(self, f"grid_row_sub_weapon_alt_{row_number}"), sticky="w")

    def on_button_sub_weapon_qty_unified(self, row_number: int, direction: str):
        """
        Handles up/down arrow button clicks for weapon quantities across all rows.
        """
        var_name = self.weapon_qty_string_vars[row_number-1]
            
        try:
            var_value_str = var_name.get()
            current_val = int(var_value_str)
        except (ValueError, tk.TclError):
            current_val = 0

        new_val = current_val + 1 if direction == "up" else max(0, current_val - 1)
        var_name.set(str(new_val))
        if hasattr(self, "on_select_sub_weapon_unified"): 
            self.on_select_sub_weapon_unified(row_number=row_number)        

    def on_button_ammo_qty_unified(self, row_number: int, direction: str):
        """
        Handles up/down arrow button clicks for weapon quantities across all rows.
        """
        var_name = self.weapon_ammo_qty_string_vars[row_number - 1]
            
        try:
            var_value_str = var_name.get()
            current_val = int(var_value_str)
        except (ValueError, tk.TclError):
            current_val = 0

        new_val = current_val + 1 if direction == "up" else max(0, current_val - 1)
        var_name.set(str(new_val))
        if hasattr(self, "on_select_sub_weapon_unified"): 
            self.on_select_sub_weapon_unified(row_number=row_number)        

    def on_button_extra_mags_unified(self, row_number: int, direction: str):
        """
        Handles up/down arrow button clicks for extra magazine counts across all rows.
        """
        var_name = self.weapon_extra_mag_qty_string_vars[row_number - 1]
        try:
            var_value_str = var_name.get()
            current_val = int(var_value_str)
        except (ValueError, tk.TclError):
            current_val = 0

        new_val = current_val + 1 if direction == "up" else max(0, current_val - 1)
        var_name.set(str(new_val))
        if hasattr(self, "on_select_sub_weapon_unified"): 
            self.on_select_sub_weapon_unified(row_number=row_number)        
      
    def on_button_ammo_qty_unified(self, row_number: int, direction: str):
        """
        Handles up/down arrow button clicks for ammunition quantities across all rows.
        Forces instant math recalculations for costs and weights.
        """
        var_name = self.weapon_ammo_qty_string_vars[row_number-1]
            
        try:
            var_value_str = var_name.get()
            current_val = int(var_value_str)
        except (ValueError, tk.TclError):
            current_val = 0

        new_val = current_val + 1 if direction == "up" else max(0, current_val - 1)
        var_name.set(str(new_val))
        if hasattr(self, "on_select_sub_weapon_unified"): 
            self.on_select_sub_weapon_unified(row_number=row_number)        

    def on_update_extra_mags_qty_unified(self, row_number: int):
        """
        Passes extra magazine trace writes straight through to our main calculation method.
        """
        self.on_select_sub_weapon_unified(row_number)

    def get_weapon_sub_list(self, category: str) -> list:
        output_list: list = []
        if category == "SMALL BORE WEAPONS":
            output_list = getattr(self, "weapons_small_bore_list", None)
        elif category == "LARGE BORE WEAPONS":
            output_list = getattr(self, "weapons_large_bore_list", None)
        elif category == "GRENADE LAUNCHERS":
            output_list = getattr(self, "weapons_grenade_launchers_list", None)
        elif category == "GRENADE AMMO":
            output_list = getattr(self, "weapons_grenade_ammo_list", None)
        elif category == "ROCKETS":
            output_list = getattr(self, "weapons_rockets_list", None)
        elif category == "ENERGY WEAPONS":
            output_list = getattr(self, "weapons_energy_list", None)
        elif category == "FLAMETHROWERS":
            output_list = getattr(self, "weapons_flamethrower_list", None)
        elif category == "DROPPED GASSES":
            output_list = getattr(self, "weapons_dropped_gas_list", None)
        elif category == "DROPPED LIQUIDS":
            output_list = getattr(self, "weapons_dropped_liquid_list", None)
        elif category == "DROPPED SOLIDS":
            output_list = getattr(self, "weapons_dropped_solid_list", None)
        elif category == "MINEDROPPERS":
            output_list = getattr(self, "weapons_minedroppers_list", None)
        elif category == "DISCHARGERS":
            output_list = getattr(self, "weapons_dischargers_list", None)
        return output_list

    def get_weapon_options_sub_list(self, input_list: list):
        if input_list is None:
            return None
        options: list = []
        for entry in input_list:
            weapon_name: str = entry.get("Drop-Down Name")
            options.append(weapon_name)
        return options

    def get_weapon_dictionaries_alt(self):
        """ This will be a comma delimited list of every single selectable weapon in the weapons list.
            This won't be even prettier."""
        self.weapons_small_bore_list = []
        self.weapons_large_bore_list = []
        self.weapons_grenade_launchers_list = []
        self.weapons_grenade_ammo_list = []
        self.weapons_rockets_list = []
        self.weapons_missiles_list = []
        self.weapons_energy_list = []
        self.weapons_flamethrower_list = []
        self.weapons_dropped_gas_list = []
        self.weapons_dropped_liquid_list = []
        self.weapons_dropped_solid_list = []
        self.weapons_minedroppers_list = []
        self.weapons_dischargers_list = []
        #entry_dict: dict = {'Weapon Name': '',                                  'Drop-Down Name': 'Weapon',                                            'Ammo Type': '',                            'Abbv': '',                            'Effect': '',                    'To-Hit': '0',      'Dam': '',                   'DP': '0',  'Cost': '0',      'Weight': '0',    'Space': '0 ',           'Shots': '0',  'Shot Cost': '0',     'Shot Weight': '0'     ,'Loaded Cost': '0',      'Loaded Weight': '0',    'Mag Cost': '0',     'Mag Weight': '0'}
        #self.weapons_list.append(entry_dict)
        entry_dict: dict = {'Weapon Name': '',                                  'Drop-Down Name': 'SMALL BORE WEAPONS',                                'Ammo Type': '',                            'Abbv': '',                            'Effect': '',                    'To-Hit': '',       'Dam': '',                   'DP': '',   'Cost': '0',      'Weight': '0',     'Space': '0',             'Shots': '',   'Shot Cost': '',      'Shot Weight': ''      ,'Loaded Cost': '',       'Loaded Weight': '',     'Mag Cost': '',      'Mag Weight': ''}
        self.weapons_small_bore_list.append(entry_dict)
        entry_dict: dict = {'Weapon Name': 'Light Machine Gun',                 'Drop-Down Name': 'Light Machine Gun - Reg.',                          'Ammo Type': 'Reg',                         'Abbv': 'LMG',                         'Effect': 'Area',                'To-Hit': '7',      'Dam': '1D-1',               'DP': '2',  'Cost': '850',    'Weight': '100',  'Space': '1 ',           'Shots': '20', 'Shot Cost': '20',    'Shot Weight': '2.5'   ,'Loaded Cost': '1250',   'Loaded Weight': '150',  'Mag Cost': '450',   'Mag Weight': '65'}
        self.weapons_small_bore_list.append(entry_dict)
        entry_dict: dict = {'Weapon Name': 'Light Machine Gun',                 'Drop-Down Name': 'Light Machine Gun - HD Ammo',                       'Ammo Type': 'HD Ammo',                     'Abbv': 'LGM w/HD',                    'Effect': 'Area',                'To-Hit': '7',      'Dam': '1D',                 'DP': '2',  'Cost': '850',    'Weight': '100',  'Space': '1 ',           'Shots': '20', 'Shot Cost': '40',    'Shot Weight': '5'     ,'Loaded Cost': '1650',   'Loaded Weight': '200',  'Mag Cost': '850',   'Mag Weight': '115'}
        self.weapons_small_bore_list.append(entry_dict)
        entry_dict: dict = {'Weapon Name': 'Light Machine Gun',                 'Drop-Down Name': 'Light Machine Gun - Incendiary',                    'Ammo Type': 'Incedenary',                  'Abbv': 'LGM w/inc',                   'Effect': 'Area',                'To-Hit': '7',      'Dam': '1D-1* (2/1)',        'DP': '2',  'Cost': '850',    'Weight': '100',  'Space': '1 ',           'Shots': '20', 'Shot Cost': '30',    'Shot Weight': '2.5'   ,'Loaded Cost': '1450',   'Loaded Weight': '150',  'Mag Cost': '650',   'Mag Weight': '65'}
        self.weapons_small_bore_list.append(entry_dict)
        entry_dict: dict = {'Weapon Name': 'Light Machine Gun',                 'Drop-Down Name': 'Light Machine Gun - Anti-Pers.',                    'Ammo Type': 'Anti-Personnel',              'Abbv': 'LGM w/Anti',                  'Effect': 'Area',                'To-Hit': '7',      'Dam': '1D-1*',              'DP': '2',  'Cost': '850',    'Weight': '100',  'Space': '1 ',           'Shots': '20', 'Shot Cost': '100',   'Shot Weight': '2.5'   ,'Loaded Cost': '2850',   'Loaded Weight': '150',  'Mag Cost': '2050',  'Mag Weight': '65'}
        self.weapons_small_bore_list.append(entry_dict)
        entry_dict: dict = {'Weapon Name': 'Light Machine Gun',                 'Drop-Down Name': 'Light Machine Gun - Explosive',                     'Ammo Type': 'Explosive',                   'Abbv': 'LGM w/Exp',                   'Effect': '1/2 inch Radius',     'To-Hit': '7',      'Dam': '1D-1',               'DP': '2',  'Cost': '850',    'Weight': '100',  'Space': '1 ',           'Shots': '20', 'Shot Cost': '40',    'Shot Weight': '5'     ,'Loaded Cost': '1650',   'Loaded Weight': '200',  'Mag Cost': '850',   'Mag Weight': '115'}
        self.weapons_small_bore_list.append(entry_dict)
        entry_dict: dict = {'Weapon Name': 'Machine Gun',                       'Drop-Down Name': 'Machine Gun - Reg',                                 'Ammo Type': 'Reg',                         'Abbv': 'MG',                          'Effect': 'Area',                'To-Hit': '7',      'Dam': '1D',                 'DP': '3',  'Cost': '1000',   'Weight': '150',  'Space': '1',            'Shots': '20', 'Shot Cost': '25',    'Shot Weight': '2.5'   ,'Loaded Cost': '1500',   'Loaded Weight': '200',  'Mag Cost': '550',   'Mag Weight': '65'}
        self.weapons_small_bore_list.append(entry_dict)
        entry_dict: dict = {'Weapon Name': 'Machine Gun',                       'Drop-Down Name': 'Machine Gun - HD Ammo',                             'Ammo Type': 'HD Ammo',                     'Abbv': 'MG W/HD',                     'Effect': 'Area',                'To-Hit': '7',      'Dam': '1D+1',               'DP': '3',  'Cost': '1000',   'Weight': '150',  'Space': '1',            'Shots': '20', 'Shot Cost': '50',    'Shot Weight': '5'     ,'Loaded Cost': '2000',   'Loaded Weight': '250',  'Mag Cost': '1050',  'Mag Weight': '115'}
        self.weapons_small_bore_list.append(entry_dict)
        entry_dict: dict = {'Weapon Name': 'Machine Gun',                       'Drop-Down Name': 'Machine Gun - Incendiary',                          'Ammo Type': 'Incedenary',                  'Abbv': 'MG w/INC',                    'Effect': 'Area',                'To-Hit': '7',      'Dam': '1D (2/1)',           'DP': '3',  'Cost': '1000',   'Weight': '150',  'Space': '1',            'Shots': '20', 'Shot Cost': '38',    'Shot Weight': '2.5'   ,'Loaded Cost': '1750',   'Loaded Weight': '200',  'Mag Cost': '800',   'Mag Weight': '65'}
        self.weapons_small_bore_list.append(entry_dict)
        entry_dict: dict = {'Weapon Name': 'Machine Gun',                       'Drop-Down Name': 'Machine Gun - Anti-Personnel',                      'Ammo Type': 'Anti-Personnel',              'Abbv': 'MG w/AP',                     'Effect': 'Area',                'To-Hit': '7',      'Dam': '1D',                 'DP': '3',  'Cost': '1000',   'Weight': '150',  'Space': '1',            'Shots': '20', 'Shot Cost': '125',   'Shot Weight': '2.5'   ,'Loaded Cost': '3500',   'Loaded Weight': '200',  'Mag Cost': '2550',  'Mag Weight': '65'}
        self.weapons_small_bore_list.append(entry_dict)
        entry_dict: dict = {'Weapon Name': 'Machine Gun',                       'Drop-Down Name': 'Machine Gun - Explosive',                           'Ammo Type': 'Explosive',                   'Abbv': 'MG w/Exp',                    'Effect': '1/2 inch Radius',     'To-Hit': '7',      'Dam': '1D',                 'DP': '3',  'Cost': '1000',   'Weight': '150',  'Space': '1',            'Shots': '20', 'Shot Cost': '50',    'Shot Weight': '5'     ,'Loaded Cost': '2000',   'Loaded Weight': '250',  'Mag Cost': '1050',  'Mag Weight': '115'}
        self.weapons_small_bore_list.append(entry_dict)
        entry_dict: dict = {'Weapon Name': 'Heavy Machine Gun',                 'Drop-Down Name': 'Heavy Machine Gun - Reg',                           'Ammo Type': 'Reg',                         'Abbv': 'HMG',                         'Effect': 'Area',                'To-Hit': '7',      'Dam': '2D-2',               'DP': '4',  'Cost': '1500',   'Weight': '250',  'Space': '1',            'Shots': '20', 'Shot Cost': '50',    'Shot Weight': '5'     ,'Loaded Cost': '2500',   'Loaded Weight': '350',  'Mag Cost': '1050',  'Mag Weight': '115'}
        self.weapons_small_bore_list.append(entry_dict)
        entry_dict: dict = {'Weapon Name': 'Heavy Machine Gun',                 'Drop-Down Name': 'Heavy Machine Gun - HD Ammo',                       'Ammo Type': 'HD Ammo',                     'Abbv': 'HMG w/HD',                    'Effect': 'Area',                'To-Hit': '7',      'Dam': '2D',                 'DP': '4',  'Cost': '1500',   'Weight': '250',  'Space': '1',            'Shots': '20', 'Shot Cost': '100',   'Shot Weight': '10'    ,'Loaded Cost': '3500',   'Loaded Weight': '400',  'Mag Cost': '2050',  'Mag Weight': '215'}
        self.weapons_small_bore_list.append(entry_dict)
        entry_dict: dict = {'Weapon Name': 'Heavy Machine Gun',                 'Drop-Down Name': 'Heavy Machine Gun - Incendiary',                    'Ammo Type': 'Incendiary',                  'Abbv': 'HMG w/Inc',                   'Effect': 'Area',                'To-Hit': '7',      'Dam': '2D-2* (2/1)',        'DP': '4',  'Cost': '1500',   'Weight': '250',  'Space': '1',            'Shots': '20', 'Shot Cost': '75',    'Shot Weight': '5'     ,'Loaded Cost': '3000',   'Loaded Weight': '300',  'Mag Cost': '1550',  'Mag Weight': '115'}
        self.weapons_small_bore_list.append(entry_dict)
        entry_dict: dict = {'Weapon Name': 'Heavy Machine Gun',                 'Drop-Down Name': 'Heavy Machine Gun - Anti-Personnel',                'Ammo Type': 'Anti-Personnel',              'Abbv': 'HMG w/AP',                    'Effect': 'Area',                'To-Hit': '7',      'Dam': '2D-2*',              'DP': '4',  'Cost': '1500',   'Weight': '250',  'Space': '1',            'Shots': '20', 'Shot Cost': '250',   'Shot Weight': '5'     ,'Loaded Cost': '6500',   'Loaded Weight': '300',  'Mag Cost': '5050',  'Mag Weight': '115'}
        self.weapons_small_bore_list.append(entry_dict)
        entry_dict: dict = {'Weapon Name': 'Heavy Machine Gun',                 'Drop-Down Name': 'Heavy Machine Gun - Explosive',                     'Ammo Type': 'Explosive',                   'Abbv': 'HMG w/EXP',                   'Effect': '1/2 inch Radius',     'To-Hit': '7',      'Dam': '2D-2',               'DP': '4',  'Cost': '1500',   'Weight': '250',  'Space': '1',            'Shots': '20', 'Shot Cost': '100',   'Shot Weight': '10'    ,'Loaded Cost': '3500',   'Loaded Weight': '400',  'Mag Cost': '2050',  'Mag Weight': '215'}
        self.weapons_small_bore_list.append(entry_dict)
        entry_dict: dict = {'Weapon Name': 'Vulcan MG',                         'Drop-Down Name': 'Vulcan MG - Reg',                                   'Ammo Type': 'Reg',                         'Abbv': 'VMG',                         'Effect': 'Area',                'To-Hit': '6',      'Dam': '2D',                 'DP': '3',  'Cost': '2000',   'Weight': '350',  'Space': '2',            'Shots': '20', 'Shot Cost': '35',    'Shot Weight': '5'     ,'Loaded Cost': '2700',   'Loaded Weight': '450',  'Mag Cost': '750',   'Mag Weight': '115'}
        self.weapons_small_bore_list.append(entry_dict)
        entry_dict: dict = {'Weapon Name': 'Vulcan MG',                         'Drop-Down Name': 'Vulcan MG - HD',                                    'Ammo Type': 'HD',                          'Abbv': 'VMG w/HD',                    'Effect': 'Area',                'To-Hit': '6',      'Dam': '2D+2',               'DP': '3',  'Cost': '2000',   'Weight': '350',  'Space': '2',            'Shots': '20', 'Shot Cost': '70',    'Shot Weight': '10'    ,'Loaded Cost': '3400',   'Loaded Weight': '550',  'Mag Cost': '1450',  'Mag Weight': '215'}
        self.weapons_small_bore_list.append(entry_dict)
        entry_dict: dict = {'Weapon Name': 'Vulcan MG',                         'Drop-Down Name': 'Vulcan MG - Incendiary',                            'Ammo Type': 'Incendiary',                  'Abbv': 'VMG w/INC',                   'Effect': 'Area',                'To-Hit': '6',      'Dam': '2D (2/1)',           'DP': '3',  'Cost': '2000',   'Weight': '350',  'Space': '2',            'Shots': '20', 'Shot Cost': '53',    'Shot Weight': '5'     ,'Loaded Cost': '3050',   'Loaded Weight': '450',  'Mag Cost': '1100',  'Mag Weight': '115'}
        self.weapons_small_bore_list.append(entry_dict)
        entry_dict: dict = {'Weapon Name': 'Vulcan MG',                         'Drop-Down Name': 'Vulcan MG - Antipersonnel',                         'Ammo Type': 'Antipersonnel',               'Abbv': 'VMG w/AP',                    'Effect': 'Area',                'To-Hit': '6',      'Dam': '2D',                 'DP': '3',  'Cost': '2000',   'Weight': '350',  'Space': '2',            'Shots': '20', 'Shot Cost': '175',   'Shot Weight': '5'     ,'Loaded Cost': '5500',   'Loaded Weight': '450',  'Mag Cost': '3550',  'Mag Weight': '115'}
        self.weapons_small_bore_list.append(entry_dict)
        entry_dict: dict = {'Weapon Name': 'Vulcan MG',                         'Drop-Down Name': 'Vulcan MG - Explosive',                             'Ammo Type': 'Explosive',                   'Abbv': 'VMG w/EXP',                   'Effect': '1/4" Radius',         'To-Hit': '6',      'Dam': '2D',                 'DP': '3',  'Cost': '2000',   'Weight': '350',  'Space': '2',            'Shots': '20', 'Shot Cost': '70',    'Shot Weight': '10'    ,'Loaded Cost': '3400',   'Loaded Weight': '550',  'Mag Cost': '1450',  'Mag Weight': '215'}
        self.weapons_small_bore_list.append(entry_dict)
        entry_dict: dict = {'Weapon Name': 'Heavy Vulcan Machine Gun',          'Drop-Down Name': 'Heavy Vulcan Machine Gun - Reg',                    'Ammo Type': 'Reg',                         'Abbv': 'HVMG',                        'Effect': 'Area',                'To-Hit': '6',      'Dam': '4D',                 'DP': '5',  'Cost': '7000',   'Weight': '650',  'Space': '3',            'Shots': '10', 'Shot Cost': '75',    'Shot Weight': '15'    ,'Loaded Cost': '7750',   'Loaded Weight': '800',  'Mag Cost': '800',   'Mag Weight': '165'}
        self.weapons_small_bore_list.append(entry_dict)
        entry_dict: dict = {'Weapon Name': 'Heavy Vulcan Machine Gun',          'Drop-Down Name': 'Heavy Vulcan Machine Gun - HD Ammo',                'Ammo Type': 'HD',                          'Abbv': 'HVMG w/HD',                   'Effect': 'Area',                'To-Hit': '6',      'Dam': '4D+4',               'DP': '5',  'Cost': '7000',   'Weight': '650',  'Space': '3',            'Shots': '10', 'Shot Cost': '150',   'Shot Weight': '30'    ,'Loaded Cost': '8500',   'Loaded Weight': '950',  'Mag Cost': '1550',  'Mag Weight': '315'}
        self.weapons_small_bore_list.append(entry_dict)
        entry_dict: dict = {'Weapon Name': 'Heavy Vulcan Machine Gun',          'Drop-Down Name': 'Heavy Vulcan Machine Gun - Incendiary',             'Ammo Type': 'Incendiary',                  'Abbv': 'HVMG w/INC',                  'Effect': 'Area',                'To-Hit': '6',      'Dam': '4D* (2/1)',          'DP': '5',  'Cost': '7000',   'Weight': '650',  'Space': '3',            'Shots': '10', 'Shot Cost': '113',   'Shot Weight': '15'    ,'Loaded Cost': '8125',   'Loaded Weight': '800',  'Mag Cost': '1175',  'Mag Weight': '165'}
        self.weapons_small_bore_list.append(entry_dict)
        entry_dict: dict = {'Weapon Name': 'Heavy Vulcan Machine Gun',          'Drop-Down Name': 'Heavy Vulcan Machine Gun - Anti-Personnel',         'Ammo Type': 'Antipersonnel',               'Abbv': 'HVMG w/AP',                   'Effect': 'Area',                'To-Hit': '6',      'Dam': '4D*',                'DP': '5',  'Cost': '7000',   'Weight': '650',  'Space': '3',            'Shots': '10', 'Shot Cost': '375',   'Shot Weight': '15'    ,'Loaded Cost': '8125',   'Loaded Weight': '800',  'Mag Cost': '1175',  'Mag Weight': '165'}
        self.weapons_small_bore_list.append(entry_dict)
        entry_dict: dict = {'Weapon Name': 'Heavy Vulcan Machine Gun',          'Drop-Down Name': 'Heavy Vulcan Machine Gun - Explosive',              'Ammo Type': 'Explosive',                   'Abbv': 'HVMG w/EXP',                  'Effect': '1/2 inch Radius',     'To-Hit': '6',      'Dam': '4D',                 'DP': '5',  'Cost': '7000',   'Weight': '650',  'Space': '3',            'Shots': '10', 'Shot Cost': '150',   'Shot Weight': '30'    ,'Loaded Cost': '8500',   'Loaded Weight': '950',  'Mag Cost': '1550',  'Mag Weight': '315'}
        self.weapons_small_bore_list.append(entry_dict)
        entry_dict: dict = {'Weapon Name': 'Flechette Gun',                     'Drop-Down Name': 'Flechette Gun',                                     'Ammo Type': 'Normal',                      'Abbv': 'FG',                          'Effect': 'Area',                'To-Hit': '6',      'Dam': '1D+1',               'DP': '2',  'Cost': '700',    'Weight': '100',  'Space': '1',            'Shots': '20', 'Shot Cost': '10',    'Shot Weight': '2.5'   ,'Loaded Cost': '900',    'Loaded Weight': '150',  'Mag Cost': '250',   'Mag Weight': '65'}
        self.weapons_small_bore_list.append(entry_dict)
        entry_dict: dict = {'Weapon Name': 'Vehicular Shotgun',                 'Drop-Down Name': 'Vehicular Shotgun',                                 'Ammo Type': 'Normal',                      'Abbv': 'VS',                          'Effect': 'Area',                'To-Hit': '6',      'Dam': '2 Hits',             'DP': '2',  'Cost': '950',    'Weight': '90',   'Space': '1',            'Shots': '10', 'Shot Cost': '5',     'Shot Weight': '1'     ,'Loaded Cost': '1000',   'Loaded Weight': '100',  'Mag Cost': '100',   'Mag Weight': '25'}
        self.weapons_small_bore_list.append(entry_dict)
        entry_dict: dict = {'Weapon Name': 'Gauss Gun',                         'Drop-Down Name': 'Gauss Gun',                                         'Ammo Type': 'Normal',                      'Abbv': 'GG',                          'Effect': 'Area',                'To-Hit': '6',      'Dam': '3D',                 'DP': '3',  'Cost': '10000',  'Weight': '300',  'Space': '2',            'Shots': '10', 'Shot Cost': '50',    'Shot Weight': '10'    ,'Loaded Cost': '10500',  'Loaded Weight': '400',  'Mag Cost': '550',   'Mag Weight': '115'}
        self.weapons_small_bore_list.append(entry_dict)
        entry_dict: dict = {'Weapon Name': 'Recoiless Rifle',                   'Drop-Down Name': 'Recoiless Rifle',                                   'Ammo Type': 'Normal',                      'Abbv': 'RR',                          'Effect': '2 inch Radius',       'To-Hit': '7',      'Dam': '2D',                 'DP': '4',  'Cost': '1500',   'Weight': '300',  'Space': '2',            'Shots': '10', 'Shot Cost': '35',    'Shot Weight': '5'     ,'Loaded Cost': '1850',   'Loaded Weight': '350',  'Mag Cost': '400',   'Mag Weight': '65'}
        self.weapons_small_bore_list.append(entry_dict)
        entry_dict: dict = {'Weapon Name': 'Recoiless Rifle',                   'Drop-Down Name': 'Recoiless Rifle - HEAT',                            'Ammo Type': 'HEAT',                        'Abbv': 'RR w/HEAT',                   'Effect': '2 inch Radius',       'To-Hit': '7',      'Dam': '2D+2',               'DP': '4',  'Cost': '1500',   'Weight': '300',  'Space': '2',            'Shots': '10', 'Shot Cost': '53',    'Shot Weight': '5'     ,'Loaded Cost': '2025',   'Loaded Weight': '350',  'Mag Cost': '575',   'Mag Weight': '65'}
        self.weapons_small_bore_list.append(entry_dict)
        entry_dict: dict = {'Weapon Name': 'Recoiless Rifle',                   'Drop-Down Name': 'Recoiless Rifle - HESH',                            'Ammo Type': 'HESH',                        'Abbv': 'RR w/HESH',                   'Effect': '2 inch Radius',       'To-Hit': '7',      'Dam': '2D',                 'DP': '4',  'Cost': '1500',   'Weight': '300',  'Space': '2',            'Shots': '10', 'Shot Cost': '53',    'Shot Weight': '5'     ,'Loaded Cost': '2025',   'Loaded Weight': '350',  'Mag Cost': '575',   'Mag Weight': '65'}
        self.weapons_small_bore_list.append(entry_dict)
        entry_dict: dict = {'Weapon Name': 'AutoCannon',                        'Drop-Down Name': 'AutoCannon',                                        'Ammo Type': 'Normal',                      'Abbv': 'AC',                          'Effect': '2 inch Radius',       'To-Hit': '6',      'Dam': '3D',                 'DP': '4',  'Cost': '6500',   'Weight': '500',  'Space': '3',            'Shots': '10', 'Shot Cost': '75',    'Shot Weight': '10'    ,'Loaded Cost': '7250',   'Loaded Weight': '600',  'Mag Cost': '800',   'Mag Weight': '115'}
        self.weapons_small_bore_list.append(entry_dict)
        entry_dict: dict = {'Weapon Name': 'AutoCannon',                        'Drop-Down Name': 'AutoCannon - HD Ammo',                              'Ammo Type': 'HD Ammo',                     'Abbv': 'AC w/HD',                     'Effect': '2 inch Radius',       'To-Hit': '6',      'Dam': '3D+3',               'DP': '4',  'Cost': '6500',   'Weight': '500',  'Space': '3',            'Shots': '10', 'Shot Cost': '150',   'Shot Weight': '20'    ,'Loaded Cost': '8000',   'Loaded Weight': '700',  'Mag Cost': '1550',  'Mag Weight': '215'}
        self.weapons_small_bore_list.append(entry_dict)
        entry_dict: dict = {'Weapon Name': 'AutoCannon',                        'Drop-Down Name': 'AutoCannon - Incendiary',                           'Ammo Type': 'Incendiary',                  'Abbv': 'Ac w/INC',                    'Effect': '2 inch Radius',       'To-Hit': '6',      'Dam': '3D* (2/1)',          'DP': '4',  'Cost': '6500',   'Weight': '500',  'Space': '3',            'Shots': '10', 'Shot Cost': '113',   'Shot Weight': '10'    ,'Loaded Cost': '7625',   'Loaded Weight': '600',  'Mag Cost': '1175',  'Mag Weight': '115'}
        self.weapons_small_bore_list.append(entry_dict)
        entry_dict: dict = {'Weapon Name': '*AutoCannon',                       'Drop-Down Name': '*AutoCannon - DPU Ammo',                            'Ammo Type': 'DPU Ammo',                    'Abbv': 'AC w/DPU',                    'Effect': '2 inch Radius',       'To-Hit': '6',      'Dam': '18',                 'DP': '4',  'Cost': '6500',   'Weight': '500',  'Space': '3',            'Shots': '10', 'Shot Cost': '750',   'Shot Weight': '30'    ,'Loaded Cost': '14000',  'Loaded Weight': '800',  'Mag Cost': '8300',  'Mag Weight': '315'}
        self.weapons_small_bore_list.append(entry_dict)
        entry_dict: dict = {'Weapon Name': '*Gatling Cannon',                   'Drop-Down Name': '*Gatling Cannon',                                   'Ammo Type': 'Normal',                      'Abbv': 'GC',                          'Effect': '2 inch Radius',       'To-Hit': '6',      'Dam': '5D',                 'DP': '5',  'Cost': '7000',   'Weight': '750',  'Space': '5',            'Shots': '10', 'Shot Cost': '45',    'Shot Weight': '15'    ,'Loaded Cost': '7450',   'Loaded Weight': '900',  'Mag Cost': '500',   'Mag Weight': '165'}
        self.weapons_small_bore_list.append(entry_dict)
        entry_dict: dict = {'Weapon Name': '*Gatling Cannon',                   'Drop-Down Name': '*Gatling Cannon - HD Ammo',                         'Ammo Type': 'HD Ammo',                     'Abbv': 'GC w/HD',                     'Effect': '2 inch Radius',       'To-Hit': '6',      'Dam': '5D+5',               'DP': '5',  'Cost': '7000',   'Weight': '750',  'Space': '5',            'Shots': '10', 'Shot Cost': '90',    'Shot Weight': '30'    ,'Loaded Cost': '7900',   'Loaded Weight': '1050',' Mag Cost': '950',   'Mag Weight': '315'}
        self.weapons_small_bore_list.append(entry_dict)
        entry_dict: dict = {'Weapon Name': '*Gatling Cannon',                   'Drop-Down Name': '*Gatling Cannon - Incendiary',                      'Ammo Type': 'Incendiary',                  'Abbv': 'GC w/INC',                    'Effect': '2 inch Radius',       'To-Hit': '6',      'Dam': '5D* (2/1)',          'DP': '5',  'Cost': '7000',   'Weight': '750',  'Space': '5',            'Shots': '10', 'Shot Cost': '68',    'Shot Weight': '15'    ,'Loaded Cost': '7675',   'Loaded Weight': '900',  'Mag Cost': '725',   'Mag Weight': '165'}
        self.weapons_small_bore_list.append(entry_dict)
        entry_dict: dict = {'Weapon Name': '',                                  'Drop-Down Name': 'LARGE BORE WEAPONS',                                'Ammo Type': '',                            'Abbv': '',                            'Effect': '',                    'To-Hit': '',       'Dam': '',                   'DP': '',   'Cost': '0',      'Weight': '0',     'Space': '0',             'Shots': '',   'Shot Cost': '',      'Shot Weight': ''      ,'Loaded Cost': '',       'Loaded Weight': '',     'Mag Cost': '',      'Mag Weight': ''}
        self.weapons_large_bore_list.append(entry_dict)
        entry_dict: dict = {'Weapon Name': 'Starshell Launcher',                'Drop-Down Name': 'Starshell Launcher',                                'Ammo Type': 'Normal',                      'Abbv': 'SL',                          'Effect': '0',                   'To-Hit': '0',      'Dam': '0',                  'DP': '2',  'Cost': '500',    'Weight': '100',  'Space': '1',            'Shots': '5',  'Shot Cost': '50',    'Shot Weight': '5'     ,'Loaded Cost': '750',    'Loaded Weight': '125',  'Mag Cost': '300',   'Mag Weight': '40'}
        self.weapons_large_bore_list.append(entry_dict)
        entry_dict: dict = {'Weapon Name': '*Drag Chute Harpoon',               'Drop-Down Name': '*Drag Chute Harpoon',                               'Ammo Type': 'Normal',                      'Abbv': 'DCH',                         'Effect': '0',                   'To-Hit': '9',      'Dam': '1 hit',              'DP': '2',  'Cost': '400',    'Weight': '40',   'Space': '1',            'Shots': '1',  'Shot Cost': '0',     'Shot Weight': '0'     ,'Loaded Cost': '400',    'Loaded Weight': '40',   'Mag Cost': '',      'Mag Weight': ''}
        self.weapons_large_bore_list.append(entry_dict)
        entry_dict: dict = {'Weapon Name': '*Drag Chute Harpoon',               'Drop-Down Name': '*Drag Chute Harpoon - FP',                          'Ammo Type': 'FP',                          'Abbv': 'DCH',                         'Effect': '0',                   'To-Hit': '9',      'Dam': '1 hit',              'DP': '2',  'Cost': '550',    'Weight': '40',   'Space': '1',            'Shots': '1',  'Shot Cost': '0',     'Shot Weight': '0'     ,'Loaded Cost': '400',    'Loaded Weight': '40',   'Mag Cost': '',      'Mag Weight': ''}
        self.weapons_large_bore_list.append(entry_dict)
        entry_dict: dict = {'Weapon Name': 'Mine-Flinger',                      'Drop-Down Name': 'Mine-Flinger',                                      'Ammo Type': 'Normal',                      'Abbv': 'MF',                          'Effect': '1 inch Radius',       'To-Hit': '5 or 9', 'Dam': '2d / 1d',            'DP': '3',  'Cost': '2250',   'Weight': '275',  'Space': '3',            'Shots': '5',  'Shot Cost': '50',    'Shot Weight': '5'     ,'Loaded Cost': '2500',   'Loaded Weight': '300',  'Mag Cost': '300',   'Mag Weight': '40'}
        self.weapons_large_bore_list.append(entry_dict)
        entry_dict: dict = {'Weapon Name': 'Mine-Flinger',                      'Drop-Down Name': 'Mine-Flinger - Anti-Ped',                           'Ammo Type': 'Anti-Ped' ,                   'Abbv': 'MF, Anti-Ped',                'Effect': '1 inch Radius',       'To-Hit': '5 or 9', 'Dam': '2d/1d/0',            'DP': '3',  'Cost': '2250',   'Weight': '275',  'Space': '3',            'Shots': '5',  'Shot Cost': '25',    'Shot Weight': '3'     ,'Loaded Cost': '2375',   'Loaded Weight': '290',  'Mag Cost': '175',   'Mag Weight': '30'}
        self.weapons_large_bore_list.append(entry_dict)
        entry_dict: dict = {'Weapon Name': 'Mine-Flinger',                      'Drop-Down Name': 'Mine-Flinger - Beacon',                             'Ammo Type': 'Beacon' ,                     'Abbv': 'MF, Beacon',                  'Effect': '3 inch Radius',       'To-Hit': '5 or 9', 'Dam': '2d/1d',              'DP': '3',  'Cost': '2250',   'Weight': '275',  'Space': '3',            'Shots': '5',  'Shot Cost': '200',   'Shot Weight': '5'     ,'Loaded Cost': '3250',   'Loaded Weight': '300',  'Mag Cost': '1050',  'Mag Weight': '40'}
        self.weapons_large_bore_list.append(entry_dict)
        entry_dict: dict = {'Weapon Name': 'Mine-Flinger',                      'Drop-Down Name': 'Mine-Flinger - Smoke',                              'Ammo Type': 'Smoke' ,                      'Abbv': 'MF, Smoke',                   'Effect': '1 x 1',               'To-Hit': '5 or 9', 'Dam': '0',                  'DP': '3',  'Cost': '2250',   'Weight': '275',  'Space': '3',            'Shots': '5',  'Shot Cost': '45',    'Shot Weight': '5'     ,'Loaded Cost': '2475',   'Loaded Weight': '300',  'Mag Cost': '275',   'Mag Weight': '40'}
        self.weapons_large_bore_list.append(entry_dict)
        entry_dict: dict = {'Weapon Name': 'Mine-Flinger',                      'Drop-Down Name': 'Mine-Flinger - Hot Smoke',                          'Ammo Type': 'Hot Smoke' ,                  'Abbv': 'MF, Hot Smoke',               'Effect': '1 x 1',               'To-Hit': '5 or 9', 'Dam': '0',                  'DP': '3',  'Cost': '2250',   'Weight': '275',  'Space': '3',            'Shots': '5',  'Shot Cost': '55',    'Shot Weight': '5'     ,'Loaded Cost': '2525',   'Loaded Weight': '300',  'Mag Cost': '325',   'Mag Weight': '40'}
        self.weapons_large_bore_list.append(entry_dict)
        entry_dict: dict = {'Weapon Name': 'Mine-Flinger',                      'Drop-Down Name': 'Mine-Flinger - Paint',                              'Ammo Type': 'Paint' ,                      'Abbv': 'MF, Paint',                   'Effect': '1 x 1',               'To-Hit': '5 or 9', 'Dam': '0',                  'DP': '3',  'Cost': '2250',   'Weight': '275',  'Space': '3',            'Shots': '5',  'Shot Cost': '45',    'Shot Weight': '5'     ,'Loaded Cost': '2475',   'Loaded Weight': '300',  'Mag Cost': '275',   'Mag Weight': '40'}
        self.weapons_large_bore_list.append(entry_dict)
        entry_dict: dict = {'Weapon Name': 'Mine-Flinger',                      'Drop-Down Name': 'Mine-Flinger - Paint, Glow-in-the-dark',            'Ammo Type': 'Paint, Glow-in-the-dark',     'Abbv': 'MF, GLOW',                    'Effect': '1 x 1',               'To-Hit': '5 or 9', 'Dam': '0',                  'DP': '3',  'Cost': '2250',   'Weight': '275',  'Space': '3',            'Shots': '5',  'Shot Cost': '105',   'Shot Weight': '5'     ,'Loaded Cost': '2775',   'Loaded Weight': '300',  'Mag Cost': '575',   'Mag Weight': '40'}
        self.weapons_large_bore_list.append(entry_dict)
        entry_dict: dict = {'Weapon Name': 'Mine-Flinger',                      'Drop-Down Name': 'Mine-Flinger - Flame Cloud',                        'Ammo Type': 'Flame Cloud' ,                'Abbv': 'MF, Flame Cloud',             'Effect': '1 x 1',               'To-Hit': '5 or 9', 'Dam': '1d-1 (3/1)',         'DP': '3',  'Cost': '2250',   'Weight': '275',  'Space': '3',            'Shots': '5',  'Shot Cost': '145',   'Shot Weight': '5'     ,'Loaded Cost': '2975',   'Loaded Weight': '300',  'Mag Cost': '775',   'Mag Weight': '40'}
        self.weapons_large_bore_list.append(entry_dict)
        entry_dict: dict = {'Weapon Name': 'Mine-Flinger',                      'Drop-Down Name': 'Mine-Flinger - Tear Gas',                           'Ammo Type': 'Tear Gas' ,                   'Abbv': 'MF, Tear Gas',                'Effect': '1 x 1',               'To-Hit': '5 or 9', 'Dam': '0',                  'DP': '3',  'Cost': '2250',   'Weight': '275',  'Space': '3',            'Shots': '5',  'Shot Cost': '65',    'Shot Weight': '5'     ,'Loaded Cost': '2575',   'Loaded Weight': '300',  'Mag Cost': '375',   'Mag Weight': '40'}
        self.weapons_large_bore_list.append(entry_dict)
        entry_dict: dict = {'Weapon Name': 'Mine-Flinger',                      'Drop-Down Name': 'Mine-Flinger - Toxin Gas',                          'Ammo Type': 'Toxin Gas',                   'Abbv': 'MF, Toxin Gas',               'Effect': '1 x 1',               'To-Hit': '5 or 9', 'Dam': '0',                  'DP': '3',  'Cost': '2250',   'Weight': '275',  'Space': '3',            'Shots': '5',  'Shot Cost': '4025',  'Shot Weight': '5'     ,'Loaded Cost': '22375',  'Loaded Weight': '300',  'Mag Cost': '20175', 'Mag Weight': '40'}
        self.weapons_large_bore_list.append(entry_dict)
        entry_dict: dict = {'Weapon Name': 'Mine-Flinger',                      'Drop-Down Name': 'Mine-Flinger - Fake Mines',                         'Ammo Type': 'Fake Mines',                  'Abbv': 'MF, Fake Mines',              'Effect': '0',                   'To-Hit': '5 or 9', 'Dam': '0',                  'DP': '3',  'Cost': '2250',   'Weight': '275',  'Space': '3',            'Shots': '5',  'Shot Cost': '10',    'Shot Weight': '5'     ,'Loaded Cost': '2300',   'Loaded Weight': '300',  'Mag Cost': '100',   'Mag Weight': '40'}
        self.weapons_large_bore_list.append(entry_dict)
        entry_dict: dict = {'Weapon Name': 'Mine-Flinger',                      'Drop-Down Name': 'Mine-Flinger - Floating Mines',                     'Ammo Type': 'Floating Mines',              'Abbv': 'MF, Floating',                'Effect': '1 inch Radius',       'To-Hit': '5 or 9', 'Dam': '2d/1d',              'DP': '3',  'Cost': '2250',   'Weight': '275',  'Space': '3',            'Shots': '5',  'Shot Cost': '100',   'Shot Weight': '5'     ,'Loaded Cost': '2750',   'Loaded Weight': '300',  'Mag Cost': '550',   'Mag Weight': '40'}
        self.weapons_large_bore_list.append(entry_dict)
        entry_dict: dict = {'Weapon Name': 'Mine-Flinger',                      'Drop-Down Name': 'Mine-Flinger - Napalm',                             'Ammo Type': 'Napalm',                      'Abbv': 'MF, Napalm',                  'Effect': '1 inch Radius',       'To-Hit': '5 or 9', 'Dam': '1d (4/3)',           'DP': '3',  'Cost': '2250',   'Weight': '275',  'Space': '3',            'Shots': '5',  'Shot Cost': '60',    'Shot Weight': '5'     ,'Loaded Cost': '2550',   'Loaded Weight': '300',  'Mag Cost': '350',   'Mag Weight': '40'}
        self.weapons_large_bore_list.append(entry_dict)
        entry_dict: dict = {'Weapon Name': 'Mine-Flinger',                      'Drop-Down Name': 'Mine-Flinger - StickyFoam Neutralizer',             'Ammo Type': 'StickyFoam Neutralizer',      'Abbv': 'MF, SF Neut',                 'Effect': '1 inch Radius',       'To-Hit': '5 or 9', 'Dam': '*',                  'DP': '3',  'Cost': '2250',   'Weight': '275',  'Space': '3',            'Shots': '5',  'Shot Cost': '250',   'Shot Weight': '5'     ,'Loaded Cost': '3500',   'Loaded Weight': '300',  'Mag Cost': '1300',  'Mag Weight': '40'}
        self.weapons_large_bore_list.append(entry_dict)
        entry_dict: dict = {'Weapon Name': 'Oil/Paint Gun',                     'Drop-Down Name': 'Oil/Paint Gun',                                     'Ammo Type': 'Normal',                      'Abbv': 'OPG',                         'Effect': '1/2 inchx1/2 inch',   'To-Hit': '9',      'Dam': '0',                  'DP': '3',  'Cost': '1000',   'Weight': '250',  'Space': '3',            'Shots': '10', 'Shot Cost': '25',    'Shot Weight': '5'     ,'Loaded Cost': '1250',   'Loaded Weight': '300',  'Mag Cost': '300',   'Mag Weight': '65'}
        self.weapons_large_bore_list.append(entry_dict)
        entry_dict: dict = {'Weapon Name': 'Oil/Paint Gun',                     'Drop-Down Name': 'Oil/Paint Gun - Flaming Oil',                       'Ammo Type': 'Flaming Oil',                 'Abbv': 'OPG/FLAME',                   'Effect': '1/2 inchx1/2 inch',   'To-Hit': '9',      'Dam': '1D-2 (3/2)',         'DP': '3',  'Cost': '1000',   'Weight': '250',  'Space': '3',            'Shots': '10', 'Shot Cost': '90',    'Shot Weight': '5'     ,'Loaded Cost': '1900',   'Loaded Weight': '300',  'Mag Cost': '950',   'Mag Weight': '65'}
        self.weapons_large_bore_list.append(entry_dict)
        entry_dict: dict = {'Weapon Name': 'Oil/Paint Gun',                     'Drop-Down Name': 'Oil/Paint Gun - HT Flaming Oil',                    'Ammo Type': 'HT Flaming Oil',              'Abbv': 'OPG/HT FLAME',                'Effect': '1/2 inchx1/2 inch',   'To-Hit': '9',      'Dam': '1D (4/1)',           'DP': '3',  'Cost': '1000',   'Weight': '250',  'Space': '3',            'Shots': '10', 'Shot Cost': '360',   'Shot Weight': '7.5'   ,'Loaded Cost': '4600',   'Loaded Weight': '325',  'Mag Cost': '3650',  'Mag Weight': '90'}
        self.weapons_large_bore_list.append(entry_dict)
        entry_dict: dict = {'Weapon Name': 'Oil/Paint Gun',                     'Drop-Down Name': 'Oil/Paint Gun - Glow-in-the-dark Paint',            'Ammo Type': 'Glow-in-the-dark Paint',      'Abbv': 'OPG/GLOW',                    'Effect': '1/2 inchx1/2 inch',   'To-Hit': '9',      'Dam': '0',                  'DP': '3',  'Cost': '1000',   'Weight': '250',  'Space': '3',            'Shots': '10', 'Shot Cost': '100',   'Shot Weight': '5'     ,'Loaded Cost': '2000',   'Loaded Weight': '300',  'Mag Cost': '1050',  'Mag Weight': '65'}
        self.weapons_large_bore_list.append(entry_dict)
        entry_dict: dict = {'Weapon Name': 'Oil/Paint Gun',                     'Drop-Down Name': 'Oil/Paint Gun - Ice Ammo',                          'Ammo Type': 'Ice Ammo',                    'Abbv': 'OPG/Ice',                     'Effect': '1/2 inchx1/2 inch',   'To-Hit': '9',      'Dam': '0',                  'DP': '3',  'Cost': '1000',   'Weight': '250',  'Space': '3',            'Shots': '10', 'Shot Cost': '40',    'Shot Weight': '5'     ,'Loaded Cost': '1400',   'Loaded Weight': '300',  'Mag Cost': '450',   'Mag Weight': '65'}
        self.weapons_large_bore_list.append(entry_dict)
        entry_dict: dict = {'Weapon Name': 'Oil/Paint Gun',                     'Drop-Down Name': 'Oil/Paint Gun - Sand Ammo',                         'Ammo Type': 'Sand Ammo',                   'Abbv': 'OPG/Sand',                    'Effect': '1/2 inchx1/2 inch',   'To-Hit': '9',      'Dam': '0',                  'DP': '3',  'Cost': '1000',   'Weight': '250',  'Space': '3',            'Shots': '10', 'Shot Cost': '10',    'Shot Weight': '5'     ,'Loaded Cost': '1100',   'Loaded Weight': '300',  'Mag Cost': '150',   'Mag Weight': '65'}
        self.weapons_large_bore_list.append(entry_dict)
        entry_dict: dict = {'Weapon Name': 'Oil/Paint Gun',                     'Drop-Down Name': 'Oil/Paint Gun - Paint',                             'Ammo Type': 'Paint',                       'Abbv': 'OPG',                         'Effect': '1/2 inchx1/2 inch',   'To-Hit': '9',      'Dam': '0',                  'DP': '3',  'Cost': '1000',   'Weight': '250',  'Space': '3',            'Shots': '10', 'Shot Cost': '25',    'Shot Weight': '5'     ,'Loaded Cost': '1250',   'Loaded Weight': '300',  'Mag Cost': '300',   'Mag Weight': '65'}
        self.weapons_large_bore_list.append(entry_dict)
        entry_dict: dict = {'Weapon Name': 'Oil/Paint Gun',                     'Drop-Down Name': 'Oil/Paint Gun - StickyFoam Neutralizer',            'Ammo Type': 'StickyFoam Neutralizer',      'Abbv': 'OPG/SF Neut',                 'Effect': '1/x1/2 inch',         'To-Hit': '9',      'Dam': '0',                  'DP': '3',  'Cost': '1000',   'Weight': '250',  'Space': '3',            'Shots': '10', 'Shot Cost': '125',   'Shot Weight': '5'     ,'Loaded Cost': '2250',   'Loaded Weight': '300',  'Mag Cost': '1300',  'Mag Weight': '65'}
        self.weapons_large_bore_list.append(entry_dict)
        entry_dict: dict = {'Weapon Name': 'Spike Gun',                         'Drop-Down Name': 'Spike Gun',                                         'Ammo Type': 'Normal',                      'Abbv': 'SG',                          'Effect': '1/2 inchx1/2 inch',   'To-Hit': '7',      'Dam': '1D',                 'DP': '2',  'Cost': '750',    'Weight': '150',  'Space': '2',            'Shots': '10', 'Shot Cost': '40',    'Shot Weight': '10'    ,'Loaded Cost': '1150',   'Loaded Weight': '250',  'Mag Cost': '450',   'Mag Weight': '115'}
        self.weapons_large_bore_list.append(entry_dict)
        entry_dict: dict = {'Weapon Name': '*Rapid Fire Tank Gun',              'Drop-Down Name': '*Rapid Fire Tank Gun',                              'Ammo Type': 'Normal',                      'Abbv': 'RFTG',                        'Effect': '2 inch Radius',       'To-Hit': '6',      'Dam': '6D',                 'DP': '8',  'Cost': '9500',   'Weight': '900',  'Space': '6',            'Shots': '10', 'Shot Cost': '25',    'Shot Weight': '10'    ,'Loaded Cost': '9750',   'Loaded Weight': '1000', 'Mag Cost': '300',   'Mag Weight': '115'}
        self.weapons_large_bore_list.append(entry_dict)
        entry_dict: dict = {'Weapon Name': '*Rapid Fire Tank Gun',              'Drop-Down Name': '*Rapid Fire Tank Gun - HEAT Ammo',                  'Ammo Type': 'HEAT Ammo',                   'Abbv': 'RFTG w/HEAT',                 'Effect': '2 inch Radius',       'To-Hit': '6',      'Dam': '6D+6',               'DP': '8',  'Cost': '9500',   'Weight': '900',  'Space': '6',            'Shots': '10', 'Shot Cost': '38',    'Shot Weight': '10'    ,'Loaded Cost': '9875',   'Loaded Weight': '1000', 'Mag Cost': '440',   'Mag Weight': '115'}
        self.weapons_large_bore_list.append(entry_dict)
        entry_dict: dict = {'Weapon Name': '*Rapid Fire Tank Gun',              'Drop-Down Name': '*Rapid Fire Tank Gun - HESH',                       'Ammo Type': 'HESH',                        'Abbv': 'RFTGw/HESH',                  'Effect': '2 inch Radius',       'To-Hit': '6',      'Dam': '6D*',                'DP': '8',  'Cost': '9500',   'Weight': '900',  'Space': '6',            'Shots': '10', 'Shot Cost': '38',    'Shot Weight': '10'    ,'Loaded Cost': '9875',   'Loaded Weight': '1000', 'Mag Cost': '440',   'Mag Weight': '115'}
        self.weapons_large_bore_list.append(entry_dict)
        entry_dict: dict = {'Weapon Name': '*Rapid Fire Tank Gun',              'Drop-Down Name': '*Rapid Fire Tank Gun - APFSDS',                     'Ammo Type': 'APFSDS',                      'Abbv': 'RFTG w/APFSDS',               'Effect': '2 inch Radius',       'To-Hit': '6',      'Dam': '6D+12',              'DP': '8',  'Cost': '9500',   'Weight': '900',  'Space': '6',            'Shots': '10', 'Shot Cost': '50',    'Shot Weight': '15'    ,'Loaded Cost': '10000',  'Loaded Weight': '1050', 'Mag Cost': '550',   'Mag Weight': '165'}
        self.weapons_large_bore_list.append(entry_dict)
        entry_dict: dict = {'Weapon Name': '*Rapid Fire Tank Gun',              'Drop-Down Name': '*Rapid Fire Tank Gun - DPU Ammo',                   'Ammo Type': 'DPU Ammo',                    'Abbv': 'RFTG w/DPU',                  'Effect': '2 inch Radius',       'To-Hit': '6',      'Dam': '36',                 'DP': '8',  'Cost': '9500',   'Weight': '900',  'Space': '6',            'Shots': '10', 'Shot Cost': '250',   'Shot Weight': '30'    ,'Loaded Cost': '12000',  'Loaded Weight': '1200', 'Mag Cost': '2550',  'Mag Weight': '315'}
        self.weapons_large_bore_list.append(entry_dict)
        entry_dict: dict = {'Weapon Name': 'Blast Cannon',                      'Drop-Down Name': 'Blast Cannon',                                      'Ammo Type': 'Normal',                      'Abbv': 'BC',                          'Effect': '2 inch Radius',       'To-Hit': '7',      'Dam': '4D',                 'DP': '5',  'Cost': '4500',   'Weight': '500',  'Space': '4',            'Shots': '10', 'Shot Cost': '100',   'Shot Weight': '10'    ,'Loaded Cost': '5500',   'Loaded Weight': '600',  'Mag Cost': '1050',  'Mag Weight': '115'}
        self.weapons_large_bore_list.append(entry_dict)
        entry_dict: dict = {'Weapon Name': '*Blast Cannon',                     'Drop-Down Name': '*Blast Cannon - HEAT',                              'Ammo Type': 'HEAT',                        'Abbv': 'BC w/HEAT',                   'Effect': '2 inch Radius',       'To-Hit': '7',      'Dam': '4D+4',               'DP': '5',  'Cost': '4500',   'Weight': '500',  'Space': '4',            'Shots': '10', 'Shot Cost': '150',   'Shot Weight': '10'    ,'Loaded Cost': '6000',   'Loaded Weight': '600',  'Mag Cost': '1550',  'Mag Weight': '115'}
        self.weapons_large_bore_list.append(entry_dict)
        entry_dict: dict = {'Weapon Name': 'Blast Cannon',                      'Drop-Down Name': 'Blast Cannon - HESH',                               'Ammo Type': 'HESH',                        'Abbv': 'BC w/HESH',                   'Effect': '2 inch Radius',       'To-Hit': '7',      'Dam': '4D*',                'DP': '5',  'Cost': '4500',   'Weight': '500',  'Space': '4',            'Shots': '10', 'Shot Cost': '150',   'Shot Weight': '10'    ,'Loaded Cost': '6000',   'Loaded Weight': '600',  'Mag Cost': '1050',  'Mag Weight': '115'}
        self.weapons_large_bore_list.append(entry_dict)
        entry_dict: dict = {'Weapon Name': '*Heavy Recoiless Rifle',            'Drop-Down Name': '*Heavy Recoiless Rifle',                            'Ammo Type': 'Normal',                      'Abbv': 'HRR',                         'Effect': '2 inch Radius',       'To-Hit': '7',      'Dam': '7D',                 'DP': '9',  'Cost': '9000',   'Weight': '1000', 'Space': '8',            'Shots': '10', 'Shot Cost': '150',   'Shot Weight': '15'    ,'Loaded Cost': '10500',  'Loaded Weight': '1150', 'Mag Cost': '1550',  'Mag Weight': '165'}
        self.weapons_large_bore_list.append(entry_dict)
        entry_dict: dict = {'Weapon Name': '*Heavy Recoiless Rifle',            'Drop-Down Name': '*Heavy Recoiless Rifle - HEAT',                     'Ammo Type': 'HEAT',                        'Abbv': 'HRR w/HEAT',                  'Effect': '2 inch Radius',       'To-Hit': '7',      'Dam': '7D+7',               'DP': '9',  'Cost': '9000',   'Weight': '1000', 'Space': '8',            'Shots': '10', 'Shot Cost': '225',   'Shot Weight': '15'    ,'Loaded Cost': '11250',  'Loaded Weight': '1150', 'Mag Cost': '2300',  'Mag Weight': '165'}
        self.weapons_large_bore_list.append(entry_dict)
        entry_dict: dict = {'Weapon Name': '*Heavy Recoiless Rifle',            'Drop-Down Name': '*Heavy Recoiless Rifle - HESH',                     'Ammo Type': 'HESH',                        'Abbv': 'HRR w/HESH',                  'Effect': '2 inch Radius',       'To-Hit': '7',      'Dam': '7D*',                'DP': '9',  'Cost': '9000',   'Weight': '1000', 'Space': '8',            'Shots': '10', 'Shot Cost': '225',   'Shot Weight': '15'    ,'Loaded Cost': '11250',  'Loaded Weight': '1150', 'Mag Cost': '2300',  'Mag Weight': '165'}
        self.weapons_large_bore_list.append(entry_dict)
        entry_dict: dict = {'Weapon Name': '*Magnetic Cannon',                  'Drop-Down Name': '*Magnetic Cannon',                                  'Ammo Type': 'Normal',                      'Abbv': 'MC',                          'Effect': '0',                   'To-Hit': '7',      'Dam': '13D+26',             'DP': '10', 'Cost': '250000', 'Weight': '4000', 'Space': '12',           'Shots': '10', 'Shot Cost': '100',   'Shot Weight': '10'    ,'Loaded Cost': '251000', 'Loaded Weight': '4100', 'Mag Cost': '1050',  'Mag Weight': '115'}
        self.weapons_large_bore_list.append(entry_dict)
        entry_dict: dict = {'Weapon Name': 'Anti-Tank Gun',                     'Drop-Down Name': 'Anti-Tank Gun',                                     'Ammo Type': 'Normal',                      'Abbv': 'ATG',                         'Effect': '2 inch Radius',       'To-Hit': '8',      'Dam': '3D',                 'DP': '5',  'Cost': '2000',   'Weight': '600',  'Space': '3',            'Shots': '10', 'Shot Cost': '50',    'Shot Weight': '10'    ,'Loaded Cost': '2500',   'Loaded Weight': '700',  'Mag Cost': '550',   'Mag Weight': '115'}
        self.weapons_large_bore_list.append(entry_dict)
        entry_dict: dict = {'Weapon Name': 'Anti-Tank Gun',                     'Drop-Down Name': 'Anti-Tank Gun - HEAT',                              'Ammo Type': 'HEAT',                        'Abbv': 'ATG w/HEAT',                  'Effect': '0',                   'To-Hit': '8',      'Dam': '3D+3',               'DP': '5',  'Cost': '2000',   'Weight': '600',  'Space': '3',            'Shots': '10', 'Shot Cost': '75',    'Shot Weight': '10'    ,'Loaded Cost': '2750',   'Loaded Weight': '700',  'Mag Cost': '800',   'Mag Weight': '115'}
        self.weapons_large_bore_list.append(entry_dict)
        entry_dict: dict = {'Weapon Name': 'Anti-Tank Gun',                     'Drop-Down Name': 'Anti-Tank Gun - HESH',                              'Ammo Type': 'HESH',                        'Abbv': 'ATG w/HESH',                  'Effect': '0',                   'To-Hit': '8',      'Dam': '3D',                 'DP': '5',  'Cost': '2000',   'Weight': '600',  'Space': '3',            'Shots': '10', 'Shot Cost': '75',    'Shot Weight': '10'    ,'Loaded Cost': '2750',   'Loaded Weight': '700',  'Mag Cost': '800',   'Mag Weight': '115'}
        self.weapons_large_bore_list.append(entry_dict)
        entry_dict: dict = {'Weapon Name': 'Anti-Tank Gun',                     'Drop-Down Name': 'Anti-Tank Gun - APFSDS',                            'Ammo Type': 'APFSDS',                      'Abbv': 'ATG w/APFSDS',                'Effect': '0',                   'To-Hit': '8',      'Dam': '3D+6',               'DP': '5',  'Cost': '2000',   'Weight': '600',  'Space': '3',            'Shots': '10', 'Shot Cost': '100',   'Shot Weight': '15'    ,'Loaded Cost': '3000',   'Loaded Weight': '750',  'Mag Cost': '1050',  'Mag Weight': '165'}
        self.weapons_large_bore_list.append(entry_dict)
        entry_dict: dict = {'Weapon Name': 'Anti-Tank Gun',                     'Drop-Down Name': 'Anti-Tank Gun - DPU Ammo',                          'Ammo Type': 'DPU Ammo',                    'Abbv': 'ATG w/DPU',                   'Effect': '0',                   'To-Hit': '8',      'Dam': '18',                 'DP': '5',  'Cost': '2000',   'Weight': '600',  'Space': '3',            'Shots': '10', 'Shot Cost': '500',   'Shot Weight': '30'    ,'Loaded Cost': '7000',   'Loaded Weight': '800',  'Mag Cost': '5050',  'Mag Weight': '215'}
        self.weapons_large_bore_list.append(entry_dict)
        entry_dict: dict = {'Weapon Name': '*Tank Gun 75mm',                    'Drop-Down Name': '*Tank Gun 75mm',                                    'Ammo Type': 'Normal',                      'Abbv': 'TG',                          'Effect': '2 inch Radius',       'To-Hit': '7',      'Dam': '8D',                 'DP': '10', 'Cost': '10000',  'Weight': '1200', 'Space': '10',           'Shots': '10', 'Shot Cost': '100',   'Shot Weight': '20'    ,'Loaded Cost': '11000',  'Loaded Weight': '1400', 'Mag Cost': '1050',  'Mag Weight': '215'}
        self.weapons_large_bore_list.append(entry_dict)
        entry_dict: dict = {'Weapon Name': '*Tank Gun 75mm',                    'Drop-Down Name': '*Tank Gun 75mm - HEAT',                             'Ammo Type': 'HEAT',                        'Abbv': 'TG w/HEAT',                   'Effect': '0',                   'To-Hit': '7',      'Dam': '8D+8',               'DP': '10', 'Cost': '10000',  'Weight': '1200', 'Space': '10',           'Shots': '10', 'Shot Cost': '150',   'Shot Weight': '20'    ,'Loaded Cost': '11500',  'Loaded Weight': '1400', 'Mag Cost': '1550',  'Mag Weight': '215'}
        self.weapons_large_bore_list.append(entry_dict)
        entry_dict: dict = {'Weapon Name': '*Tank Gun 75mm',                    'Drop-Down Name': '*Tank Gun 75mm - HESH',                             'Ammo Type': 'HESH',                        'Abbv': 'TG w/HESH',                   'Effect': '0',                   'To-Hit': '7',      'Dam': '8D',                 'DP': '10', 'Cost': '10000',  'Weight': '1200', 'Space': '10',           'Shots': '10', 'Shot Cost': '150',   'Shot Weight': '20'    ,'Loaded Cost': '11500',  'Loaded Weight': '1400', 'Mag Cost': '1550',  'Mag Weight': '215'}
        self.weapons_large_bore_list.append(entry_dict)
        entry_dict: dict = {'Weapon Name': '*Tank Gun 75mm',                    'Drop-Down Name': '*Tank Gun 75mm - APFSDS',                           'Ammo Type': 'APFSDS',                      'Abbv': 'TG w/APFSDS',                 'Effect': '0',                   'To-Hit': '7',      'Dam': '8D+16',              'DP': '10', 'Cost': '10000',  'Weight': '1200', 'Space': '10',           'Shots': '10', 'Shot Cost': '200',   'Shot Weight': '30'    ,'Loaded Cost': '12000',  'Loaded Weight': '1500', 'Mag Cost': '2050',  'Mag Weight': '315'}
        self.weapons_large_bore_list.append(entry_dict)
        entry_dict: dict = {'Weapon Name': '*Tank Gun 75mm',                    'Drop-Down Name': '*Tank Gun 75mm - Beehive',                          'Ammo Type': 'Beehive',                     'Abbv': 'TG w/BEE',                    'Effect': '2" Path',             'To-Hit': '2',      'Dam': '4D',                 'DP': '10', 'Cost': '10000',  'Weight': '1200', 'Space': '10',           'Shots': '10', 'Shot Cost': '300',   'Shot Weight': '20'    ,'Loaded Cost': '12000',  'Loaded Weight': '1400', 'Mag Cost': '2050',  'Mag Weight': '215'}
        self.weapons_large_bore_list.append(entry_dict)
        entry_dict: dict = {'Weapon Name': '*Tank Gun 75mm',                    'Drop-Down Name': '*Tank Gun 75mm - DPU Ammo',                         'Ammo Type': 'DPU Ammo',                    'Abbv': 'TG w/DPU',                    'Effect': '0',                   'To-Hit': '7',      'Dam': '48',                 'DP': '10', 'Cost': '10000',  'Weight': '1200', 'Space': '10',           'Shots': '10', 'Shot Cost': '1000',  'Shot Weight': '60'    ,'Loaded Cost': '20000',  'Loaded Weight': '1800', 'Mag Cost': '10050', 'Mag Weight': '615'}
        self.weapons_large_bore_list.append(entry_dict)
        entry_dict: dict = {'Weapon Name': '',                                  'Drop-Down Name': 'GRENADE LAUNCHERS AND MAGAZINES',                   'Ammo Type': '',                            'Abbv': '',                            'Effect': '',                    'To-Hit': '',       'Dam': '',                   'DP': '',   'Cost': '0',      'Weight': '0',     'Space': '0',             'Shots': '',   'Shot Cost': '',      'Shot Weight': ''      ,'Loaded Cost': '',       'Loaded Weight': '',     'Mag Cost': '',      'Mag Weight': ''}
        self.weapons_grenade_launchers_list.append(entry_dict)
        entry_dict: dict = {'Weapon Name': '',                                  'Drop-Down Name': '----Buy grenades seperately, below----',            'Ammo Type': '',                            'Abbv': '',                            'Effect': '',                    'To-Hit': '',       'Dam': '',                   'DP': '',   'Cost': '0',      'Weight': '0',     'Space': '0',             'Shots': '',   'Shot Cost': '',      'Shot Weight': ''      ,'Loaded Cost': '',       'Loaded Weight': '',     'Mag Cost': '',      'Mag Weight': ''}
        self.weapons_grenade_launchers_list.append(entry_dict)
        entry_dict: dict = {'Weapon Name': 'Grenade Launcher',                  'Drop-Down Name': 'Grenade Launcher - Empty',                          'Ammo Type': 'Empty',                       'Abbv': 'GL',                          'Effect': 'Grenade',             'To-Hit': '7',      'Dam': 'Grenade',            'DP': '2',  'Cost': '1000',   'Weight': '200',  'Space': '2',            'Shots': '10', 'Shot Cost': '0',     'Shot Weight': '0'     ,'Loaded Cost': '1000',   'Loaded Weight': '200',  'Mag Cost': '50',    'Mag Weight': '15'}
        self.weapons_grenade_launchers_list.append(entry_dict)
        entry_dict: dict = {'Weapon Name': '*Auto Grenade Launcher',            'Drop-Down Name': '*Auto Grenade Launcher - Empty',                    'Ammo Type': 'Empty',                       'Abbv': 'AGL',                         'Effect': 'Grenade',             'To-Hit': '7',      'Dam': 'Grenade',            'DP': '3',  'Cost': '5000',   'Weight': '250',  'Space': '2',            'Shots': '20', 'Shot Cost': '0',     'Shot Weight': '0'     ,'Loaded Cost': '5000',   'Loaded Weight': '250',  'Mag Cost': '50',    'Mag Weight': '15'}
        self.weapons_grenade_launchers_list.append(entry_dict)
        entry_dict: dict = {'Weapon Name': '',                                  'Drop-Down Name': 'GRENADE AMMO - buy impact fuses seperately',        'Ammo Type': '',                            'Abbv': '',                            'Effect': '',                    'To-Hit': '',       'Dam': '',                   'DP': '',   'Cost': '0',      'Weight': '0',     'Space': '0',             'Shots': '0',  'Shot Cost': '0',     'Shot Weight': ''      ,'Loaded Cost': '1000',   'Loaded Weight': '50',   'Mag Cost': '',      'Mag Weight': ''}
        self.weapons_grenade_launchers_list.append(entry_dict)
        entry_dict: dict = {'Weapon Name': '',                                  'Drop-Down Name': '--Mix freely, buy extra mags with launchers--',     'Ammo Type': '',                            'Abbv': '',                            'Effect': '',                    'To-Hit': '',       'Dam': '',                   'DP': '',   'Cost': '0',      'Weight': '0',     'Space': '0',             'Shots': '',   'Shot Cost': '',      'Shot Weight': ''      ,'Loaded Cost': '',       'Loaded Weight': '',     'Mag Cost': '',      'Mag Weight': ''}
        self.weapons_grenade_ammo_list.append(entry_dict)
        entry_dict: dict = {'Weapon Name': 'Fuse',                              'Drop-Down Name': 'Impact Fuses, per grenade',                         'Ammo Type': 'Impact Fuse',                 'Abbv': '',                            'Effect': '',                    'To-Hit': '',       'Dam': '',                   'DP': '',   'Cost': '50',     'Weight': '0',    'Space': '0',             'Shots': '',   'Shot Cost': '',      'Shot Weight': ''      ,'Loaded Cost': '',       'Loaded Weight': '',     'Mag Cost': '',      'Mag Weight': ''}
        self.weapons_grenade_ammo_list.append(entry_dict)
        entry_dict: dict = {'Weapon Name': 'Grenade',                           'Drop-Down Name': 'Grenade - Chem-Laser',                              'Ammo Type': 'Chem-Laser',                  'Abbv': '',                            'Effect': '0',                   'To-Hit': '7',      'Dam': '1D+1',               'DP': '',   'Cost': '200',    'Weight': '4',    'Space': '0',             'Shots': '',   'Shot Cost': '',      'Shot Weight': ''      ,'Loaded Cost': '',       'Loaded Weight': '',     'Mag Cost': '',      'Mag Weight': ''}
        self.weapons_grenade_ammo_list.append(entry_dict)
        entry_dict: dict = {'Weapon Name': 'Grenade',                           'Drop-Down Name': 'Grenade - Concussion',                              'Ammo Type': 'Concussion',                  'Abbv': '',                            'Effect': '1 R / 2 R',           'To-Hit': '',       'Dam': '1 point',            'DP': '',   'Cost': '40',     'Weight': '4',    'Space': '0',             'Shots': '',   'Shot Cost': '',      'Shot Weight': ''      ,'Loaded Cost': '',       'Loaded Weight': '',     'Mag Cost': '',      'Mag Weight': ''}
        self.weapons_grenade_ammo_list.append(entry_dict)
        entry_dict: dict = {'Weapon Name': 'Grenade',                           'Drop-Down Name': 'Grenade - Explosive',                               'Ammo Type': 'Explosive',                   'Abbv': '',                            'Effect': '1/2 inch R / 2R',     'To-Hit': '',       'Dam': '1D',                 'DP': '',   'Cost': '25',     'Weight': '4',    'Space': '0',             'Shots': '',   'Shot Cost': '',      'Shot Weight': ''      ,'Loaded Cost': '',       'Loaded Weight': '',     'Mag Cost': '',      'Mag Weight': ''}
        self.weapons_grenade_ammo_list.append(entry_dict)
        entry_dict: dict = {'Weapon Name': 'Grenade',                           'Drop-Down Name': 'Grenade - Fake',                                    'Ammo Type': 'Fake',                        'Abbv': '',                            'Effect': 'fake',                'To-Hit': '',       'Dam': '0',                  'DP': '',   'Cost': '5',      'Weight': '4',    'Space': '0',             'Shots': '',   'Shot Cost': '',      'Shot Weight': ''      ,'Loaded Cost': '',       'Loaded Weight': '',     'Mag Cost': '',      'Mag Weight': ''}
        self.weapons_grenade_ammo_list.append(entry_dict)
        entry_dict: dict = {'Weapon Name': 'Grenade',                           'Drop-Down Name': 'Grenade - Flaming Oil',                             'Ammo Type': 'Flaming Oil',                 'Abbv': '',                            'Effect': '1/2 inch x 1/2 inch', 'To-Hit': '',       'Dam': '1d-2 (3/2)',         'DP': '',   'Cost': '75',     'Weight': '4',    'Space': '0',             'Shots': '',   'Shot Cost': '',      'Shot Weight': ''      ,'Loaded Cost': '',       'Loaded Weight': '',     'Mag Cost': '',      'Mag Weight': ''}
        self.weapons_grenade_ammo_list.append(entry_dict)
        entry_dict: dict = {'Weapon Name': 'Grenade',                           'Drop-Down Name': 'Grenade - Flash',                                   'Ammo Type': 'Flash',                       'Abbv': '',                            'Effect': '2 inch Radius',       'To-Hit': '',       'Dam': '',                   'DP': '',   'Cost': '150',    'Weight': '4',    'Space': '0',             'Shots': '',   'Shot Cost': '',      'Shot Weight': ''      ,'Loaded Cost': '',       'Loaded Weight': '',     'Mag Cost': '',      'Mag Weight': ''}
        self.weapons_grenade_ammo_list.append(entry_dict)
        entry_dict: dict = {'Weapon Name': 'Grenade',                           'Drop-Down Name': 'Grenade - Flechette',                               'Ammo Type': 'Flechette',                   'Abbv': '',                            'Effect': '2 Burst',             'To-Hit': '',       'Dam': '1d (peds)',          'DP': '',   'Cost': '20',     'Weight': '4',    'Space': '0',             'Shots': '',   'Shot Cost': '',      'Shot Weight': ''      ,'Loaded Cost': '',       'Loaded Weight': '',     'Mag Cost': '',      'Mag Weight': ''}
        self.weapons_grenade_ammo_list.append(entry_dict)
        entry_dict: dict = {'Weapon Name': 'Grenade',                           'Drop-Down Name': 'Grenade - Foam',                                    'Ammo Type': 'Foam',                        'Abbv': '',                            'Effect': '1/2 inch Radius',     'To-Hit': '',       'Dam': '',                   'DP': '',   'Cost': '30',     'Weight': '4',    'Space': '0',             'Shots': '',   'Shot Cost': '',      'Shot Weight': ''      ,'Loaded Cost': '',       'Loaded Weight': '',     'Mag Cost': '',      'Mag Weight': ''}
        self.weapons_grenade_ammo_list.append(entry_dict)
        entry_dict: dict = {'Weapon Name': 'Grenade',                           'Drop-Down Name': 'Grenade - HESH',                                    'Ammo Type': 'HESH',                        'Abbv': '',                            'Effect': '0',                   'To-Hit': '',       'Dam': '2D',                 'DP': '',   'Cost': '90',     'Weight': '4',    'Space': '0',             'Shots': '',   'Shot Cost': '',      'Shot Weight': ''      ,'Loaded Cost': '',       'Loaded Weight': '',     'Mag Cost': '',      'Mag Weight': ''}
        self.weapons_grenade_ammo_list.append(entry_dict)
        entry_dict: dict = {'Weapon Name': 'Grenade',                           'Drop-Down Name': 'Grenade - Net',                                     'Ammo Type': 'Net',                         'Abbv': '',                            'Effect': '1/2 inchx1/2 inch',   'To-Hit': '',       'Dam': '0',                  'DP': '',   'Cost': '100',    'Weight': '4',    'Space': '0',             'Shots': '',   'Shot Cost': '',      'Shot Weight': ''      ,'Loaded Cost': '',       'Loaded Weight': '',     'Mag Cost': '',      'Mag Weight': ''}
        self.weapons_grenade_ammo_list.append(entry_dict)
        entry_dict: dict = {'Weapon Name': 'Grenade',                           'Drop-Down Name': 'Grenade - Net, Det-Cord',                           'Ammo Type': 'Net, Det-Cord',               'Abbv': '',                            'Effect': '1/2 inchx1/2 inch',   'To-Hit': '',       'Dam': '1d-5',               'DP': '',   'Cost': '200',    'Weight': '4',    'Space': '0',             'Shots': '',   'Shot Cost': '',      'Shot Weight': ''      ,'Loaded Cost': '',       'Loaded Weight': '',     'Mag Cost': '',      'Mag Weight': ''}
        self.weapons_grenade_ammo_list.append(entry_dict)
        entry_dict: dict = {'Weapon Name': 'Grenade',                           'Drop-Down Name': 'Grenade - Paint',                                   'Ammo Type': 'Paint',                       'Abbv': '',                            'Effect': '1 x 1',               'To-Hit': '',       'Dam': '',                   'DP': '',   'Cost': '20',     'Weight': '4',    'Space': '0',             'Shots': '',   'Shot Cost': '',      'Shot Weight': ''      ,'Loaded Cost': '',       'Loaded Weight': '',     'Mag Cost': '',      'Mag Weight': ''}
        self.weapons_grenade_ammo_list.append(entry_dict)
        entry_dict: dict = {'Weapon Name': 'Grenade',                           'Drop-Down Name': 'Grenade - Smoke',                                   'Ammo Type': 'Smoke',                       'Abbv': '',                            'Effect': '1 x 1',               'To-Hit': '',       'Dam': '',                   'DP': '',   'Cost': '20',     'Weight': '4',    'Space': '0',             'Shots': '',   'Shot Cost': '',      'Shot Weight': ''      ,'Loaded Cost': '',       'Loaded Weight': '',     'Mag Cost': '',      'Mag Weight': ''}
        self.weapons_grenade_ammo_list.append(entry_dict)
        entry_dict: dict = {'Weapon Name': 'Grenade',                           'Drop-Down Name': 'Grenade - StickyFoam Neutralizer',                  'Ammo Type': 'StickyFoam Neutralizer',      'Abbv': '',                            'Effect': '1 x 1',               'To-Hit': '',       'Dam': '*',                  'DP': '',   'Cost': '125',    'Weight': '4',    'Space': '0',             'Shots': '',   'Shot Cost': '',      'Shot Weight': ''      ,'Loaded Cost': '',       'Loaded Weight': '',     'Mag Cost': '',      'Mag Weight': ''}
        self.weapons_grenade_ammo_list.append(entry_dict)
        entry_dict: dict = {'Weapon Name': 'Grenade',                           'Drop-Down Name': 'Grenade - Tear Gas',                                'Ammo Type': 'Tear Gas',                    'Abbv': '',                            'Effect': '1 x 1',               'To-Hit': '',       'Dam': '',                   'DP': '',   'Cost': '30',     'Weight': '4',    'Space': '0',             'Shots': '',   'Shot Cost': '',      'Shot Weight': ''      ,'Loaded Cost': '',       'Loaded Weight': '',     'Mag Cost': '',      'Mag Weight': ''}
        self.weapons_grenade_ammo_list.append(entry_dict)
        entry_dict: dict = {'Weapon Name': 'Grenade',                           'Drop-Down Name': 'Grenade - Thermite',                                'Ammo Type': 'Thermite',                    'Abbv': '',                            'Effect': '1/2 inch Radius',     'To-Hit': '',       'Dam': '1D',                 'DP': '',   'Cost': '100',    'Weight': '4',    'Space': '0',             'Shots': '',   'Shot Cost': '',      'Shot Weight': ''      ,'Loaded Cost': '',       'Loaded Weight': '',     'Mag Cost': '',      'Mag Weight': ''}
        self.weapons_grenade_ammo_list.append(entry_dict)
        entry_dict: dict = {'Weapon Name': 'Grenade',                           'Drop-Down Name': 'Grenade - White Phosphorus',                        'Ammo Type': 'White Phosphorus',            'Abbv': '',                            'Effect': '1/2 inch Radius',     'To-Hit': '',       'Dam': '1D',                 'DP': '',   'Cost': '75',     'Weight': '4',    'Space': '0',             'Shots': '',   'Shot Cost': '',      'Shot Weight': ''      ,'Loaded Cost': '',       'Loaded Weight': '',     'Mag Cost': '',      'Mag Weight': ''}
        self.weapons_grenade_ammo_list.append(entry_dict)
        entry_dict: dict = {'Weapon Name': '*Grenade',                          'Drop-Down Name': '*Grenade - Concussion, AGL',                        'Ammo Type': 'Concussion, AGL',             'Abbv': '',                            'Effect': '1 inch R / 2 inch R', 'To-Hit': '',       'Dam': '1 point',            'DP': '',   'Cost': '60',     'Weight': '5',    'Space': '0',             'Shots': '',   'Shot Cost': '',      'Shot Weight': ''      ,'Loaded Cost': '',       'Loaded Weight': '',     'Mag Cost': '',      'Mag Weight': ''}
        self.weapons_grenade_ammo_list.append(entry_dict)
        entry_dict: dict = {'Weapon Name': '*Grenade',                          'Drop-Down Name': '*Grenade - Explosive, AGL',                         'Ammo Type': 'Explosive, AGL',              'Abbv': '',                            'Effect': '1/2 inch R / 2R',     'To-Hit': '',       'Dam': '1D',                 'DP': '',   'Cost': '45',     'Weight': '5',    'Space': '0',             'Shots': '',   'Shot Cost': '',      'Shot Weight': ''      ,'Loaded Cost': '',       'Loaded Weight': '',     'Mag Cost': '',      'Mag Weight': ''}
        self.weapons_grenade_ammo_list.append(entry_dict)
        entry_dict: dict = {'Weapon Name': '*Grenade',                          'Drop-Down Name': '*Grenade - Fake, AGL',                              'Ammo Type': 'Fake, AGL',                   'Abbv': '',                            'Effect': 'fake',                'To-Hit': '',       'Dam': '0',                  'DP': '',   'Cost': '25',     'Weight': '5',    'Space': '0',             'Shots': '',   'Shot Cost': '',      'Shot Weight': ''      ,'Loaded Cost': '',       'Loaded Weight': '',     'Mag Cost': '',      'Mag Weight': ''}
        self.weapons_grenade_ammo_list.append(entry_dict)
        entry_dict: dict = {'Weapon Name': '*Grenade',                          'Drop-Down Name': '*Grenade - Flaming Oil, AGL',                       'Ammo Type': 'Flaming Oil, AGL',            'Abbv': '',                            'Effect': '1/2 inch x 1/2 inch', 'To-Hit': '',       'Dam': '1d-2 (3/2)',         'DP': '',   'Cost': '95',     'Weight': '5',    'Space': '0',             'Shots': '',   'Shot Cost': '',      'Shot Weight': ''      ,'Loaded Cost': '',       'Loaded Weight': '',     'Mag Cost': '',      'Mag Weight': ''}
        self.weapons_grenade_ammo_list.append(entry_dict)
        entry_dict: dict = {'Weapon Name': '*Grenade',                          'Drop-Down Name': '*Grenade - Flash, AGL',                             'Ammo Type': 'Flash, AGL',                  'Abbv': '',                            'Effect': '2 inch Radius',       'To-Hit': '',       'Dam': '',                   'DP': '',   'Cost': '170',    'Weight': '5',    'Space': '0',             'Shots': '',   'Shot Cost': '',      'Shot Weight': ''      ,'Loaded Cost': '',       'Loaded Weight': '',     'Mag Cost': '',      'Mag Weight': ''}
        self.weapons_grenade_ammo_list.append(entry_dict)
        entry_dict: dict = {'Weapon Name': '*Grenade',                          'Drop-Down Name': '*Grenade - Flechette, AGL',                         'Ammo Type': 'Flechette, AGL',              'Abbv': '',                            'Effect': '2 inch Burst',        'To-Hit': '',       'Dam': '1d (peds)',          'DP': '',   'Cost': '40',     'Weight': '5',    'Space': '0',             'Shots': '',   'Shot Cost': '',      'Shot Weight': ''      ,'Loaded Cost': '',       'Loaded Weight': '',     'Mag Cost': '',      'Mag Weight': ''}
        self.weapons_grenade_ammo_list.append(entry_dict)
        entry_dict: dict = {'Weapon Name': '*Grenade',                          'Drop-Down Name': '*Grenade - Foam, AGL',                              'Ammo Type': 'Foam, AGL',                   'Abbv': '',                            'Effect': '1/2 inch Radius',     'To-Hit': '',       'Dam': '',                   'DP': '',   'Cost': '50',     'Weight': '5',    'Space': '0',             'Shots': '',   'Shot Cost': '',      'Shot Weight': ''      ,'Loaded Cost': '',       'Loaded Weight': '',     'Mag Cost': '',      'Mag Weight': ''}
        self.weapons_grenade_ammo_list.append(entry_dict)
        entry_dict: dict = {'Weapon Name': '*Grenade',                          'Drop-Down Name': '*Grenade - HESH, AGL',                              'Ammo Type': 'HESH, AGL',                   'Abbv': '',                            'Effect': '0',                   'To-Hit': '',       'Dam': '2D',                 'DP': '',   'Cost': '110',    'Weight': '5',    'Space': '0',             'Shots': '',   'Shot Cost': '',      'Shot Weight': ''      ,'Loaded Cost': '',       'Loaded Weight': '',     'Mag Cost': '',      'Mag Weight': ''}
        self.weapons_grenade_ammo_list.append(entry_dict)
        entry_dict: dict = {'Weapon Name': '*Grenade',                          'Drop-Down Name': '*Grenade - Paint, AGL',                             'Ammo Type': 'Paint, AGL',                  'Abbv': '',                            'Effect': '1 x 1',               'To-Hit': '',       'Dam': '',                   'DP': '',   'Cost': '40',     'Weight': '5',    'Space': '0',             'Shots': '',   'Shot Cost': '',      'Shot Weight': ''      ,'Loaded Cost': '',       'Loaded Weight': '',     'Mag Cost': '',      'Mag Weight': ''}
        self.weapons_grenade_ammo_list.append(entry_dict)
        entry_dict: dict = {'Weapon Name': '*Grenade',                          'Drop-Down Name': '*Grenade - Smoke, AGL',                             'Ammo Type': 'Smoke, AGL',                  'Abbv': '',                            'Effect': '1 x 1',               'To-Hit': '',       'Dam': '',                   'DP': '',   'Cost': '40',     'Weight': '5',    'Space': '0',             'Shots': '',   'Shot Cost': '',      'Shot Weight': ''      ,'Loaded Cost': '',       'Loaded Weight': '',     'Mag Cost': '',      'Mag Weight': ''}
        self.weapons_grenade_ammo_list.append(entry_dict)
        entry_dict: dict = {'Weapon Name': '*Grenade',                          'Drop-Down Name': '*Grenade - StickyFoam Neutralizer, AGL',            'Ammo Type': 'StickyFoam Neutralizer, AGL', 'Abbv': '',                            'Effect': '1 x 1',               'To-Hit': '',       'Dam': '',                   'DP': '',   'Cost': '225',    'Weight': '5',    'Space': '0',             'Shots': '',   'Shot Cost': '',      'Shot Weight': ''      ,'Loaded Cost': '',       'Loaded Weight': '',     'Mag Cost': '',      'Mag Weight': ''}
        self.weapons_grenade_ammo_list.append(entry_dict)
        entry_dict: dict = {'Weapon Name': '*Grenade',                          'Drop-Down Name': '*Grenade - Tear Gas, AGL',                          'Ammo Type': 'Tear Gas, AGL',               'Abbv': '',                            'Effect': '1 x 1',               'To-Hit': '',       'Dam': '',                   'DP': '',   'Cost': '50',     'Weight': '5',    'Space': '0',             'Shots': '',   'Shot Cost': '',      'Shot Weight': ''      ,'Loaded Cost': '',       'Loaded Weight': '',     'Mag Cost': '',      'Mag Weight': ''}
        self.weapons_grenade_ammo_list.append(entry_dict)
        entry_dict: dict = {'Weapon Name': '*Grenade',                          'Drop-Down Name': '*Grenade - Thermite, AGL',                          'Ammo Type': 'Thermite, AGL',               'Abbv': '',                            'Effect': '1/2 inch Radius',     'To-Hit': '',       'Dam': '1D',                 'DP': '',   'Cost': '120',    'Weight': '5',    'Space': '0',             'Shots': '',   'Shot Cost': '',      'Shot Weight': ''      ,'Loaded Cost': '',       'Loaded Weight': '',     'Mag Cost': '',      'Mag Weight': ''}
        self.weapons_grenade_ammo_list.append(entry_dict)
        entry_dict: dict = {'Weapon Name': '*Grenade',                          'Drop-Down Name': '*Grenade - White Phosphorus, AGL',                  'Ammo Type': 'White Phosphorus, AGL',       'Abbv': '',                            'Effect': '1/2 inch Radius',     'To-Hit': '',       'Dam': '1D',                 'DP': '',   'Cost': '95',     'Weight': '5',    'Space': '0',             'Shots': '',   'Shot Cost': '',      'Shot Weight': ''      ,'Loaded Cost': '',       'Loaded Weight': '',     'Mag Cost': '',      'Mag Weight': ''}
        self.weapons_grenade_ammo_list.append(entry_dict)
        entry_dict: dict = {'Weapon Name': '*Grenade',                          'Drop-Down Name': '*Grenade - Concussion, HV AGL',                     'Ammo Type': 'Concussion, HV AGL',          'Abbv': '',                            'Effect': '1 R / 2 R',           'To-Hit': '',       'Dam': '1 point',            'DP': '',   'Cost': '90',     'Weight': '8',    'Space': '0',             'Shots': '',   'Shot Cost': '',      'Shot Weight': ''      ,'Loaded Cost': '',       'Loaded Weight': '',     'Mag Cost': '',      'Mag Weight': ''}
        self.weapons_grenade_ammo_list.append(entry_dict)
        entry_dict: dict = {'Weapon Name': '*Grenade',                          'Drop-Down Name': '*Grenade - Explosive, HV AGL',                      'Ammo Type': 'Explosive, HV AGL',           'Abbv': '',                            'Effect': '1/2 inch R / 2R',     'To-Hit': '',       'Dam': '1D',                 'DP': '',   'Cost': '75',     'Weight': '8',    'Space': '0',             'Shots': '',   'Shot Cost': '',      'Shot Weight': ''      ,'Loaded Cost': '',       'Loaded Weight': '',     'Mag Cost': '',      'Mag Weight': ''}
        self.weapons_grenade_ammo_list.append(entry_dict)
        entry_dict: dict = {'Weapon Name': '*Grenade',                          'Drop-Down Name': '*Grenade - Fake, HV AGL',                           'Ammo Type': 'Fake, HV AGL',                'Abbv': '',                            'Effect': 'fake',                'To-Hit': '',       'Dam': '0',                  'DP': '',   'Cost': '55',     'Weight': '8',    'Space': '0',             'Shots': '',   'Shot Cost': '',      'Shot Weight': ''      ,'Loaded Cost': '',       'Loaded Weight': '',     'Mag Cost': '',      'Mag Weight': ''}
        self.weapons_grenade_ammo_list.append(entry_dict)
        entry_dict: dict = {'Weapon Name': '*Grenade',                          'Drop-Down Name': '*Grenade - Flaming Oil, HV AGL',                    'Ammo Type': 'Flaming Oil, HV AGL',         'Abbv': '',                            'Effect': '1/2 inch x 1/2 inch', 'To-Hit': '',       'Dam': '1d-2 (3/2)',         'DP': '',   'Cost': '125',    'Weight': '8',    'Space': '0',             'Shots': '',   'Shot Cost': '',      'Shot Weight': ''      ,'Loaded Cost': '',       'Loaded Weight': '',     'Mag Cost': '',      'Mag Weight': ''}
        self.weapons_grenade_ammo_list.append(entry_dict)
        entry_dict: dict = {'Weapon Name': '*Grenade',                          'Drop-Down Name': '*Grenade - Flash, HV AGL',                          'Ammo Type': 'Flash, HV AGL',               'Abbv': '',                            'Effect': '2 inch Radius',       'To-Hit': '',       'Dam': '',                   'DP': '',   'Cost': '200',    'Weight': '8',    'Space': '0',             'Shots': '',   'Shot Cost': '',      'Shot Weight': ''      ,'Loaded Cost': '',       'Loaded Weight': '',     'Mag Cost': '',      'Mag Weight': ''}
        self.weapons_grenade_ammo_list.append(entry_dict)
        entry_dict: dict = {'Weapon Name': '*Grenade',                          'Drop-Down Name': '*Grenade - Flechette, HV AGL',                      'Ammo Type': 'Flechette, HV AGL',           'Abbv': '',                            'Effect': '2 inch Burst',        'To-Hit': '',       'Dam': '1d (peds)',          'DP': '',   'Cost': '70',     'Weight': '8',    'Space': '0',             'Shots': '',   'Shot Cost': '',      'Shot Weight': ''      ,'Loaded Cost': '',       'Loaded Weight': '',     'Mag Cost': '',      'Mag Weight': ''}
        self.weapons_grenade_ammo_list.append(entry_dict)
        entry_dict: dict = {'Weapon Name': '*Grenade',                          'Drop-Down Name': '*Grenade - Foam, HV AGL',                           'Ammo Type': 'Foam, HV AGL',                'Abbv': '',                            'Effect': '1/2 inch Radius',     'To-Hit': '',       'Dam': '',                   'DP': '',   'Cost': '80',     'Weight': '8',    'Space': '0',             'Shots': '',   'Shot Cost': '',      'Shot Weight': ''      ,'Loaded Cost': '',       'Loaded Weight': '',     'Mag Cost': '',      'Mag Weight': ''}
        self.weapons_grenade_ammo_list.append(entry_dict)
        entry_dict: dict = {'Weapon Name': '*Grenade',                          'Drop-Down Name': '*Grenade - Paint, HV AGL',                          'Ammo Type': 'Paint, HV AGL',               'Abbv': '',                            'Effect': '1 x 1',               'To-Hit': '',       'Dam': '',                   'DP': '',   'Cost': '70',     'Weight': '8',    'Space': '0',             'Shots': '',   'Shot Cost': '',      'Shot Weight': ''      ,'Loaded Cost': '',       'Loaded Weight': '',     'Mag Cost': '',      'Mag Weight': ''}
        self.weapons_grenade_ammo_list.append(entry_dict)
        entry_dict: dict = {'Weapon Name': '*Grenade',                          'Drop-Down Name': '*Grenade - Smoke, HV AGL',                          'Ammo Type': 'Smoke, HV AGL',               'Abbv': '',                            'Effect': '1 x 1',               'To-Hit': '',       'Dam': '',                   'DP': '',   'Cost': '70',     'Weight': '8',    'Space': '0',             'Shots': '',   'Shot Cost': '',      'Shot Weight': ''      ,'Loaded Cost': '',       'Loaded Weight': '',     'Mag Cost': '',      'Mag Weight': ''}
        self.weapons_grenade_ammo_list.append(entry_dict)
        entry_dict: dict = {'Weapon Name': '*Grenade',                          'Drop-Down Name': '*Grenade - Tear Gas, HV AGL',                       'Ammo Type': 'Tear Gas, HV AGL',            'Abbv': '',                            'Effect': '1 x 1',               'To-Hit': '',       'Dam': '',                   'DP': '',   'Cost': '80',     'Weight': '8',    'Space': '0',             'Shots': '',   'Shot Cost': '',      'Shot Weight': ''      ,'Loaded Cost': '',       'Loaded Weight': '',     'Mag Cost': '',      'Mag Weight': ''}
        self.weapons_grenade_ammo_list.append(entry_dict)
        entry_dict: dict = {'Weapon Name': '*Grenade',                          'Drop-Down Name': '*Grenade - Thermite, HV AGL',                       'Ammo Type': 'Thermite, HV AGL',            'Abbv': '',                            'Effect': '1/2 inch Radius',     'To-Hit': '',       'Dam': '1D',                 'DP': '',   'Cost': '150',    'Weight': '8',    'Space': '0',             'Shots': '',   'Shot Cost': '',      'Shot Weight': ''      ,'Loaded Cost': '',       'Loaded Weight': '',     'Mag Cost': '',      'Mag Weight': ''}
        self.weapons_grenade_ammo_list.append(entry_dict)
        entry_dict: dict = {'Weapon Name': '*Grenade',                          'Drop-Down Name': '*Grenade - White Phosphorus, HV AGL',               'Ammo Type': 'White Phosphorus, HV AGL',    'Abbv': '',                            'Effect': '1/2 inch Radius',     'To-Hit': '',       'Dam': '1D',                 'DP': '',   'Cost': '125',    'Weight': '8',    'Space': '0',             'Shots': '',   'Shot Cost': '',      'Shot Weight': ''      ,'Loaded Cost': '',       'Loaded Weight': '',     'Mag Cost': '',      'Mag Weight': ''}
        self.weapons_grenade_ammo_list.append(entry_dict)
        entry_dict: dict = {'Weapon Name': '',                                  'Drop-Down Name': 'ROCKETS',                                           'Ammo Type': '',                            'Abbv': '',                            'Effect': '',                    'To-Hit': '',       'Dam': '',                   'DP': '',   'Cost': '0',      'Weight': '0',     'Space': '0',             'Shots': '',   'Shot Cost': '',      'Shot Weight': ''      ,'Loaded Cost': '',       'Loaded Weight': '',     'Mag Cost': '',      'Mag Weight': ''}
        self.weapons_rockets_list.append(entry_dict)
        entry_dict: dict = {'Weapon Name': 'Mini Rocket',                       'Drop-Down Name': 'Mini Rocket',                                       'Ammo Type': 'Normal',                      'Abbv': 'MNR',                         'Effect': '1/2 inch Radius',     'To-Hit': '9',      'Dam': '1D-1',               'DP': '1',  'Cost': '50',     'Weight': '20',   'Space': '0.3333333333', 'Shots': '1',  'Shot Cost': '0',     'Shot Weight': '0'     ,'Loaded Cost': '50',     'Loaded Weight': '20',   'Mag Cost': '0',     'Mag Weight': '0'}
        self.weapons_rockets_list.append(entry_dict)
        entry_dict: dict = {'Weapon Name': 'Mini Rocket',                       'Drop-Down Name': 'Mini Rocket - Armor Piercing',                      'Ammo Type': 'Armor Piercing',              'Abbv': 'MNR- AP',                     'Effect': '',                    'To-Hit': '9',      'Dam': '1D',                 'DP': '1',  'Cost': '75',     'Weight': '20',   'Space': '0.3333333333', 'Shots': '1',  'Shot Cost': '0',     'Shot Weight': '0'     ,'Loaded Cost': '75',     'Loaded Weight': '20',   'Mag Cost': '0',     'Mag Weight': '0'}
        self.weapons_rockets_list.append(entry_dict)
        entry_dict: dict = {'Weapon Name': 'Mini Rocket',                       'Drop-Down Name': 'Mini Rocket - Incendiary',                          'Ammo Type': 'Incendiary',                  'Abbv': 'MNR-Incendiary',              'Effect': '1/2 inch Radius',     'To-Hit': '9',      'Dam': '1D* (1/0)',          'DP': '1',  'Cost': '100',    'Weight': '30',   'Space': '0.3333333333', 'Shots': '1',  'Shot Cost': '0',     'Shot Weight': '0'     ,'Loaded Cost': '100',    'Loaded Weight': '30',   'Mag Cost': '0',     'Mag Weight': '0'}
        self.weapons_rockets_list.append(entry_dict)
        entry_dict: dict = {'Weapon Name': 'Mini Rocket',                       'Drop-Down Name': 'Mini Rocket - Chaff',                               'Ammo Type': 'Chaff',                       'Abbv': 'MNR-Chaff',                   'Effect': '1/2 inch x 1',        'To-Hit': '9',      'Dam': '',                   'DP': '1',  'Cost': '45',     'Weight': '20',   'Space': '0.3333333333', 'Shots': '1',  'Shot Cost': '0',     'Shot Weight': '0'     ,'Loaded Cost': '45',     'Loaded Weight': '20',   'Mag Cost': '0',     'Mag Weight': '0'}
        self.weapons_rockets_list.append(entry_dict)
        entry_dict: dict = {'Weapon Name': 'Mini Rocket',                       'Drop-Down Name': 'Mini Rocket - Foam',                                'Ammo Type': 'Foam',                        'Abbv': 'MNR-Foam',                    'Effect': '1/2 inch x 1/2 inch', 'To-Hit': '9',      'Dam': '',                   'DP': '1',  'Cost': '25',     'Weight': '20',   'Space': '0.3333333333', 'Shots': '1',  'Shot Cost': '0',     'Shot Weight': '0'     ,'Loaded Cost': '25',     'Loaded Weight': '20',   'Mag Cost': '0',     'Mag Weight': '0'}
        self.weapons_rockets_list.append(entry_dict)
        entry_dict: dict = {'Weapon Name': 'Mini Rocket',                       'Drop-Down Name': 'Mini Rocket - Smoke',                               'Ammo Type': 'Smoke',                       'Abbv': 'MNR-Smoke',                   'Effect': '1/2 inch x 2',        'To-Hit': '9',      'Dam': '',                   'DP': '1',  'Cost': '50',     'Weight': '20',   'Space': '0.3333333333', 'Shots': '1',  'Shot Cost': '0',     'Shot Weight': '0'     ,'Loaded Cost': '50',     'Loaded Weight': '20',   'Mag Cost': '0',     'Mag Weight': '0'}
        self.weapons_rockets_list.append(entry_dict)
        entry_dict: dict = {'Weapon Name': 'Mini Rocket',                       'Drop-Down Name': 'Mini Rocket - Hot Smoke',                           'Ammo Type': 'Hot Smoke',                   'Abbv': 'MNR-Hot Smoke',               'Effect': '1/2 inch x 2',        'To-Hit': '9',      'Dam': '',                   'DP': '1',  'Cost': '50',     'Weight': '20',   'Space': '0.3333333333', 'Shots': '1',  'Shot Cost': '0',     'Shot Weight': '0'     ,'Loaded Cost': '50',     'Loaded Weight': '20',   'Mag Cost': '0',     'Mag Weight': '0'}
        self.weapons_rockets_list.append(entry_dict)
        entry_dict: dict = {'Weapon Name': 'Mini Rocket',                       'Drop-Down Name': 'Mini Rocket - Tear Gas',                            'Ammo Type': 'Tear Gas',                    'Abbv': 'MNR-Tear Gas',                'Effect': '1/2 inch x 2',        'To-Hit': '9',      'Dam': '',                   'DP': '1',  'Cost': '100',    'Weight': '20',   'Space': '0.3333333333', 'Shots': '1',  'Shot Cost': '0',     'Shot Weight': '0'     ,'Loaded Cost': '100',    'Loaded Weight': '20',   'Mag Cost': '0',     'Mag Weight': '0'}
        self.weapons_rockets_list.append(entry_dict)
        entry_dict: dict = {'Weapon Name': 'Light Rocket',                      'Drop-Down Name': 'Light Rocket',                                      'Ammo Type': 'Normal',                      'Abbv': 'LR',                          'Effect': '1 inch Radius',       'To-Hit': '9',      'Dam': '1D',                 'DP': '1',  'Cost': '75',     'Weight': '25',   'Space': '0.5',          'Shots': '1',  'Shot Cost': '0',     'Shot Weight': '0'     ,'Loaded Cost': '75',     'Loaded Weight': '25',   'Mag Cost': '0',     'Mag Weight': '0'}
        self.weapons_rockets_list.append(entry_dict)
        entry_dict: dict = {'Weapon Name': 'Light Rocket',                      'Drop-Down Name': 'Light Rocket - Armor Piercing',                     'Ammo Type': 'Armor Piercing',              'Abbv': 'LR-AP',                       'Effect': '',                    'To-Hit': '9',      'Dam': '1D+1',               'DP': '1',  'Cost': '112.5',  'Weight': '25',   'Space': '0.5',          'Shots': '1',  'Shot Cost': '0',     'Shot Weight': '0'     ,'Loaded Cost': '112.5',  'Loaded Weight': '25',   'Mag Cost': '0',     'Mag Weight': '0'}
        self.weapons_rockets_list.append(entry_dict)
        entry_dict: dict = {'Weapon Name': 'Light Rocket',                      'Drop-Down Name': 'Light Rocket - Incendiary',                         'Ammo Type': 'Incendiary',                  'Abbv': 'LR-Incendiary',               'Effect': '1 inch Radius',       'To-Hit': '9',      'Dam': '1D+1* (2/1)',        'DP': '1',  'Cost': '150',    'Weight': '37.5', 'Space': '0.5',          'Shots': '1',  'Shot Cost': '0',     'Shot Weight': '0'     ,'Loaded Cost': '150',    'Loaded Weight': '37.5', 'Mag Cost': '0',     'Mag Weight': '0'}
        self.weapons_rockets_list.append(entry_dict)
        entry_dict: dict = {'Weapon Name': 'Light Rocket',                      'Drop-Down Name': 'Light Rocket - Chaff',                              'Ammo Type': 'Chaff',                       'Abbv': 'LR-Chaff',                    'Effect': '1/2 inch x 1',        'To-Hit': '9',      'Dam': '',                   'DP': '1',  'Cost': '70',     'Weight': '25',   'Space': '0.5',          'Shots': '1',  'Shot Cost': '0',     'Shot Weight': '0'     ,'Loaded Cost': '70',     'Loaded Weight': '25',   'Mag Cost': '0',     'Mag Weight': '0'}
        self.weapons_rockets_list.append(entry_dict)
        entry_dict: dict = {'Weapon Name': 'Light Rocket',                      'Drop-Down Name': 'Light Rocket - Foam',                               'Ammo Type': 'Foam',                        'Abbv': 'LR-Foam',                     'Effect': '1/2 inch x 1/2 inch', 'To-Hit': '9',      'Dam': '',                   'DP': '1',  'Cost': '37.5',   'Weight': '25',   'Space': '0.5',          'Shots': '1',  'Shot Cost': '0',     'Shot Weight': '0'     ,'Loaded Cost': '37.5',   'Loaded Weight': '25',   'Mag Cost': '0',     'Mag Weight': '0'}
        self.weapons_rockets_list.append(entry_dict)
        entry_dict: dict = {'Weapon Name': 'Light Rocket',                      'Drop-Down Name': 'Light Rocket - Smoke',                              'Ammo Type': 'Smoke',                       'Abbv': 'LR-Smoke',                    'Effect': '1/2 inch x 2',        'To-Hit': '9',      'Dam': '',                   'DP': '1',  'Cost': '75',     'Weight': '25',   'Space': '0.5',          'Shots': '1',  'Shot Cost': '0',     'Shot Weight': '0'     ,'Loaded Cost': '75',     'Loaded Weight': '25',   'Mag Cost': '0',     'Mag Weight': '0'}
        self.weapons_rockets_list.append(entry_dict)
        entry_dict: dict = {'Weapon Name': 'Light Rocket',                      'Drop-Down Name': 'Light Rocket - Hot Smoke',                          'Ammo Type': 'Hot Smoke',                   'Abbv': 'LR-Hot Smoke',                'Effect': '1/2 inch x 2',        'To-Hit': '9',      'Dam': '',                   'DP': '1',  'Cost': '75',     'Weight': '25',   'Space': '0.5',          'Shots': '1',  'Shot Cost': '0',     'Shot Weight': '0'     ,'Loaded Cost': '75',     'Loaded Weight': '25',   'Mag Cost': '0',     'Mag Weight': '0'}
        self.weapons_rockets_list.append(entry_dict)
        entry_dict: dict = {'Weapon Name': 'Light Rocket',                      'Drop-Down Name': 'Light Rocket - Tear Gas',                           'Ammo Type': 'Tear Gas',                    'Abbv': 'LR-Tear Gas',                 'Effect': '1/2 inch x 2',        'To-Hit': '9',      'Dam': '',                   'DP': '1',  'Cost': '150',    'Weight': '25',   'Space': '0.5',          'Shots': '1',  'Shot Cost': '0',     'Shot Weight': '0'     ,'Loaded Cost': '150',    'Loaded Weight': '25',   'Mag Cost': '0',     'Mag Weight': '0'}
        self.weapons_rockets_list.append(entry_dict)
        entry_dict: dict = {'Weapon Name': 'Medium Rocket',                     'Drop-Down Name': 'Medium Rocket',                                     'Ammo Type': 'Normal',                      'Abbv': 'MR',                          'Effect': '1 inch Radius',       'To-Hit': '9',      'Dam': '2D',                 'DP': '2',  'Cost': '140',    'Weight': '50',   'Space': '1',            'Shots': '1',  'Shot Cost': '0',     'Shot Weight': '0'     ,'Loaded Cost': '140',    'Loaded Weight': '50',   'Mag Cost': '0',     'Mag Weight': '0'}
        self.weapons_rockets_list.append(entry_dict)
        entry_dict: dict = {'Weapon Name': 'Medium Rocket',                     'Drop-Down Name': 'Medium Rocket - Armor Piercing',                    'Ammo Type': 'Armor Piercing',              'Abbv': 'MR-AP',                       'Effect': '',                    'To-Hit': '9',      'Dam': '2D+2',               'DP': '2',  'Cost': '210',    'Weight': '50',   'Space': '1',            'Shots': '1',  'Shot Cost': '0',     'Shot Weight': '0'     ,'Loaded Cost': '210',    'Loaded Weight': '50',   'Mag Cost': '0',     'Mag Weight': '0'}
        self.weapons_rockets_list.append(entry_dict)
        entry_dict: dict = {'Weapon Name': 'Medium Rocket',                     'Drop-Down Name': 'Medium Rocket - Incendiary',                        'Ammo Type': 'Incendiary',                  'Abbv': 'MR-Incendiary',               'Effect': '1 inch Radius',       'To-Hit': '9',      'Dam': '2D+2* (3/2)',        'DP': '2',  'Cost': '280',    'Weight': '75',   'Space': '1',            'Shots': '1',  'Shot Cost': '0',     'Shot Weight': '0'     ,'Loaded Cost': '280',    'Loaded Weight': '75',   'Mag Cost': '0',     'Mag Weight': '0'}
        self.weapons_rockets_list.append(entry_dict)
        entry_dict: dict = {'Weapon Name': 'Medium Rocket',                     'Drop-Down Name': 'Medium Rocket - Chaff',                             'Ammo Type': 'Chaff',                       'Abbv': 'MR-Chaff',                    'Effect': '1 x 1',               'To-Hit': '9',      'Dam': '',                   'DP': '2',  'Cost': '135',    'Weight': '50',   'Space': '1',            'Shots': '1',  'Shot Cost': '0',     'Shot Weight': '0'     ,'Loaded Cost': '135',    'Loaded Weight': '50',   'Mag Cost': '0',     'Mag Weight': '0'}
        self.weapons_rockets_list.append(entry_dict)
        entry_dict: dict = {'Weapon Name': 'Medium Rocket',                     'Drop-Down Name': 'Medium Rocket - Foam',                              'Ammo Type': 'Foam',                        'Abbv': 'MR-Foam',                     'Effect': '1 x 1',               'To-Hit': '9',      'Dam': '',                   'DP': '2',  'Cost': '70',     'Weight': '50',   'Space': '1',            'Shots': '1',  'Shot Cost': '0',     'Shot Weight': '0'     ,'Loaded Cost': '70',     'Loaded Weight': '50',   'Mag Cost': '0',     'Mag Weight': '0'}
        self.weapons_rockets_list.append(entry_dict)
        entry_dict: dict = {'Weapon Name': 'Medium Rocket',                     'Drop-Down Name': 'Medium Rocket - Smoke',                             'Ammo Type': 'Smoke',                       'Abbv': 'MR-Smoke',                    'Effect': '1/2 inch x 4',        'To-Hit': '9',      'Dam': '',                   'DP': '2',  'Cost': '140',    'Weight': '50',   'Space': '1',            'Shots': '1',  'Shot Cost': '0',     'Shot Weight': '0'     ,'Loaded Cost': '140',    'Loaded Weight': '50',   'Mag Cost': '0',     'Mag Weight': '0'}
        self.weapons_rockets_list.append(entry_dict)
        entry_dict: dict = {'Weapon Name': 'Medium Rocket',                     'Drop-Down Name': 'Medium Rocket - Hot Smoke',                         'Ammo Type': 'Hot Smoke',                   'Abbv': 'MR-Hot Smoke',                'Effect': '1/2 inch x 4',        'To-Hit': '9',      'Dam': '',                   'DP': '2',  'Cost': '140',    'Weight': '50',   'Space': '1',            'Shots': '1',  'Shot Cost': '0',     'Shot Weight': '0'     ,'Loaded Cost': '140',    'Loaded Weight': '50',   'Mag Cost': '0',     'Mag Weight': '0'}
        self.weapons_rockets_list.append(entry_dict)
        entry_dict: dict = {'Weapon Name': 'Medium Rocket',                     'Drop-Down Name': 'Medium Rocket - Tear Gas',                          'Ammo Type': 'Tear Gas',                    'Abbv': 'MR-Tear Gas',                 'Effect': '1/2 inch x 4',        'To-Hit': '9',      'Dam': '',                   'DP': '2',  'Cost': '280',    'Weight': '50',   'Space': '1',            'Shots': '1',  'Shot Cost': '0',     'Shot Weight': '0'     ,'Loaded Cost': '280',    'Loaded Weight': '50',   'Mag Cost': '0',     'Mag Weight': '0'}
        self.weapons_rockets_list.append(entry_dict)
        entry_dict: dict = {'Weapon Name': 'Heavy Rocket',                      'Drop-Down Name': 'Heavy Rocket',                                      'Ammo Type': 'Normal',                      'Abbv': 'HR',                          'Effect': '2 inch Radius',       'To-Hit': '9',      'Dam': '3D',                 'DP': '2',  'Cost': '200',    'Weight': '100',  'Space': '1',            'Shots': '1',  'Shot Cost': '0',     'Shot Weight': '0'     ,'Loaded Cost': '200',    'Loaded Weight': '100',  'Mag Cost': '0',     'Mag Weight': '0'}
        self.weapons_rockets_list.append(entry_dict)
        entry_dict: dict = {'Weapon Name': 'Heavy Rocket',                      'Drop-Down Name': 'Heavy Rocket - Armor Piercing',                     'Ammo Type': 'Armor Piercing',              'Abbv': 'HR-AP',                       'Effect': '',                    'To-Hit': '9',      'Dam': '3D+3',               'DP': '2',  'Cost': '300',    'Weight': '100',  'Space': '1',            'Shots': '1',  'Shot Cost': '0',     'Shot Weight': '0'     ,'Loaded Cost': '300',    'Loaded Weight': '100',  'Mag Cost': '0',     'Mag Weight': '0'}
        self.weapons_rockets_list.append(entry_dict)
        entry_dict: dict = {'Weapon Name': 'Heavy Rocket',                      'Drop-Down Name': 'Heavy Rocket - Incendiary',                         'Ammo Type': 'Incendiary',                  'Abbv': 'HR-Incendiary',               'Effect': '2 inch Radius',       'To-Hit': '9',      'Dam': '3D+3* (4/3)',        'DP': '2',  'Cost': '400',    'Weight': '150',  'Space': '1',            'Shots': '1',  'Shot Cost': '0',     'Shot Weight': '0'     ,'Loaded Cost': '400',    'Loaded Weight': '150',  'Mag Cost': '0',     'Mag Weight': '0'}
        self.weapons_rockets_list.append(entry_dict)
        entry_dict: dict = {'Weapon Name': 'Heavy Rocket',                      'Drop-Down Name': 'Heavy Rocket - Chaff',                              'Ammo Type': 'Chaff',                       'Abbv': 'HR-Chaff',                    'Effect': '1 x 2',               'To-Hit': '9',      'Dam': '',                   'DP': '2',  'Cost': '175',    'Weight': '100',  'Space': '1',            'Shots': '1',  'Shot Cost': '0',     'Shot Weight': '0'     ,'Loaded Cost': '175',    'Loaded Weight': '100',  'Mag Cost': '0',     'Mag Weight': '0'}
        self.weapons_rockets_list.append(entry_dict)
        entry_dict: dict = {'Weapon Name': 'Heavy Rocket',                      'Drop-Down Name': 'Heavy Rocket - Foam',                               'Ammo Type': 'Foam',                        'Abbv': 'HR-Foam',                     'Effect': '1 x 2',               'To-Hit': '9',      'Dam': '',                   'DP': '2',  'Cost': '100',    'Weight': '100',  'Space': '1',            'Shots': '1',  'Shot Cost': '0',     'Shot Weight': '0'     ,'Loaded Cost': '100',    'Loaded Weight': '100',  'Mag Cost': '0',     'Mag Weight': '0'}
        self.weapons_rockets_list.append(entry_dict)
        entry_dict: dict = {'Weapon Name': 'Heavy Rocket',                      'Drop-Down Name': 'Heavy Rocket - Smoke',                              'Ammo Type': 'Smoke',                       'Abbv': 'HR-Smoke',                    'Effect': '1/2 inch x 6',        'To-Hit': '9',      'Dam': '',                   'DP': '2',  'Cost': '200',    'Weight': '100',  'Space': '1',            'Shots': '1',  'Shot Cost': '0',     'Shot Weight': '0'     ,'Loaded Cost': '200',    'Loaded Weight': '100',  'Mag Cost': '0',     'Mag Weight': '0'}
        self.weapons_rockets_list.append(entry_dict)
        entry_dict: dict = {'Weapon Name': 'Heavy Rocket',                      'Drop-Down Name': 'Heavy Rocket - Hot Smoke',                          'Ammo Type': 'Hot Smoke',                   'Abbv': 'HR-Hot Smoke',                'Effect': '1/2 inch x 6',        'To-Hit': '9',      'Dam': '',                   'DP': '2',  'Cost': '200',    'Weight': '100',  'Space': '1',            'Shots': '1',  'Shot Cost': '0',     'Shot Weight': '0'     ,'Loaded Cost': '200',    'Loaded Weight': '100',  'Mag Cost': '0',     'Mag Weight': '0'}
        self.weapons_rockets_list.append(entry_dict)
        entry_dict: dict = {'Weapon Name': 'Heavy Rocket',                      'Drop-Down Name': 'Heavy Rocket - Tear Gas',                           'Ammo Type': 'Tear Gas',                    'Abbv': 'HR-Tear Gas',                 'Effect': '1/2 inch x 6',        'To-Hit': '9',      'Dam': '',                   'DP': '2',  'Cost': '400',    'Weight': '100',  'Space': '1',            'Shots': '1',  'Shot Cost': '0',     'Shot Weight': '0'     ,'Loaded Cost': '400',    'Loaded Weight': '100',  'Mag Cost': '0',     'Mag Weight': '0'}
        self.weapons_rockets_list.append(entry_dict)
        entry_dict: dict = {'Weapon Name': '*Super Rocket',                     'Drop-Down Name': '*Super Rocket',                                     'Ammo Type': 'Normal',                      'Abbv': 'SR',                          'Effect': '2 inch Radius',       'To-Hit': '9',      'Dam': '9D',                 'DP': '2',  'Cost': '15000',  'Weight': '150',  'Space': '1',            'Shots': '1',  'Shot Cost': '0',     'Shot Weight': '0'     ,'Loaded Cost': '15000',  'Loaded Weight': '150',  'Mag Cost': '0',     'Mag Weight': '0'}
        self.weapons_rockets_list.append(entry_dict)
        entry_dict: dict = {'Weapon Name': '*Super Rocket',                     'Drop-Down Name': '*Super Rocket - Armor Piercing',                    'Ammo Type': 'Armor Piercing',              'Abbv': 'SR-AP',                       'Effect': '',                    'To-Hit': '9',      'Dam': '9D+9',               'DP': '2',  'Cost': '22500',  'Weight': '150',  'Space': '1',            'Shots': '1',  'Shot Cost': '0',     'Shot Weight': '0'     ,'Loaded Cost': '22500',  'Loaded Weight': '150',  'Mag Cost': '0',     'Mag Weight': '0'}
        self.weapons_rockets_list.append(entry_dict)
        entry_dict: dict = {'Weapon Name': '*Super Rocket',                     'Drop-Down Name': '*Super Rocket - Incendiary',                        'Ammo Type': 'Incendiary',                  'Abbv': 'SR-Incendiary',               'Effect': '2 inch Radius',       'To-Hit': '9',      'Dam': '9D+9* (4/3)',        'DP': '2',  'Cost': '30000',  'Weight': '225',  'Space': '1',            'Shots': '1',  'Shot Cost': '0',     'Shot Weight': '0'     ,'Loaded Cost': '30000',  'Loaded Weight': '225',  'Mag Cost': '0',     'Mag Weight': '0'}
        self.weapons_rockets_list.append(entry_dict)
        entry_dict: dict = {'Weapon Name': '*Super Rocket',                     'Drop-Down Name': '*Super Rocket - Chaff',                             'Ammo Type': 'Chaff',                       'Abbv': 'SR-Chaff',                    'Effect': '2 x 2',               'To-Hit': '9',      'Dam': '',                   'DP': '2',  'Cost': '7500',   'Weight': '150',  'Space': '1',            'Shots': '1',  'Shot Cost': '0',     'Shot Weight': '0'     ,'Loaded Cost': '7500',   'Loaded Weight': '150',  'Mag Cost': '0',     'Mag Weight': '0'}
        self.weapons_rockets_list.append(entry_dict)
        entry_dict: dict = {'Weapon Name': '*Super Rocket',                     'Drop-Down Name': '*Super Rocket - Foam',                              'Ammo Type': 'Foam',                        'Abbv': 'SR-Foam',                     'Effect': '1 x 2',               'To-Hit': '9',      'Dam': '',                   'DP': '2',  'Cost': '7500',   'Weight': '150',  'Space': '1',            'Shots': '1',  'Shot Cost': '0',     'Shot Weight': '0'     ,'Loaded Cost': '7500',   'Loaded Weight': '150',  'Mag Cost': '0',     'Mag Weight': '0'}
        self.weapons_rockets_list.append(entry_dict)
        entry_dict: dict = {'Weapon Name': '*Super Rocket',                     'Drop-Down Name': '*Super Rocket - Smoke',                             'Ammo Type': 'Smoke',                       'Abbv': 'SR-Smoke',                    'Effect': '1/2 inch x 18',       'To-Hit': '9',      'Dam': '',                   'DP': '2',  'Cost': '15000',  'Weight': '150',  'Space': '1',            'Shots': '1',  'Shot Cost': '0',     'Shot Weight': '0'     ,'Loaded Cost': '15000',  'Loaded Weight': '150',  'Mag Cost': '0',     'Mag Weight': '0'}
        self.weapons_rockets_list.append(entry_dict)
        entry_dict: dict = {'Weapon Name': '*Super Rocket',                     'Drop-Down Name': '*Super Rocket - Hot Smoke',                         'Ammo Type': 'Hot Smoke',                   'Abbv': 'SR-Hot Smoke',                'Effect': '1/2 inch x 18',       'To-Hit': '9',      'Dam': '',                   'DP': '2',  'Cost': '15000',  'Weight': '150',  'Space': '1',            'Shots': '1',  'Shot Cost': '0',     'Shot Weight': '0'     ,'Loaded Cost': '15000',  'Loaded Weight': '150',  'Mag Cost': '0',     'Mag Weight': '0'}
        self.weapons_rockets_list.append(entry_dict)
        entry_dict: dict = {'Weapon Name': '*Super Rocket',                     'Drop-Down Name': '*Super Rocket - Tear Gas',                          'Ammo Type': 'Tear Gas',                    'Abbv': 'SR-Tear Gas',                 'Effect': '1/2 inch x 18',       'To-Hit': '9',      'Dam': '',                   'DP': '2',  'Cost': '30000',  'Weight': '150',  'Space': '1',            'Shots': '1',  'Shot Cost': '0',     'Shot Weight': '0'     ,'Loaded Cost': '30000',  'Loaded Weight': '150',  'Mag Cost': '0',     'Mag Weight': '0'}
        self.weapons_rockets_list.append(entry_dict)
        entry_dict: dict = {'Weapon Name': 'Anti-Power Plant Rocket',           'Drop-Down Name': 'Anti-Power Plant Rocket',                           'Ammo Type': 'Normal',                      'Abbv': 'APPR',                        'Effect': '1 inch Radius',       'To-Hit': '9',      'Dam': '1D-1*',              'DP': '1',  'Cost': '500',    'Weight': '40',   'Space': '1',            'Shots': '1',  'Shot Cost': '0',     'Shot Weight': '0'     ,'Loaded Cost': '500',    'Loaded Weight': '40',   'Mag Cost': '0',     'Mag Weight': '0'}
        self.weapons_rockets_list.append(entry_dict)
        entry_dict: dict = {'Weapon Name': 'Micromissile Launcher',             'Drop-Down Name': 'Micromissile Launcher',                             'Ammo Type': 'Normal',                      'Abbv': 'MML',                         'Effect': '1 inch Radius',       'To-Hit': '8',      'Dam': '1D',                 'DP': '2',  'Cost': '750',    'Weight': '100',  'Space': '1',            'Shots': '10', 'Shot Cost': '20',    'Shot Weight': '2.5'   ,'Loaded Cost': '950',    'Loaded Weight': '125',  'Mag Cost': '250',   'Mag Weight': '40'}
        self.weapons_rockets_list.append(entry_dict)
        entry_dict: dict = {'Weapon Name': 'Micromissile Launcher',             'Drop-Down Name': 'Micromissile Launcher - Armor Piercing',            'Ammo Type': 'Armor Piercing',              'Abbv': 'MML-AP',                      'Effect': '',                    'To-Hit': '8',      'Dam': '1D+1',               'DP': '2',  'Cost': '750',    'Weight': '100',  'Space': '1',            'Shots': '10', 'Shot Cost': '30',    'Shot Weight': '2.5'   ,'Loaded Cost': '1050',   'Loaded Weight': '125',  'Mag Cost': '350',   'Mag Weight': '40'}
        self.weapons_rockets_list.append(entry_dict)
        entry_dict: dict = {'Weapon Name': 'Micromissile Launcher',             'Drop-Down Name': 'Micromissile Launcher - Incendiary',                'Ammo Type': 'Incendiary',                  'Abbv': 'MML-Incendiary',              'Effect': '1 inch Radius',       'To-Hit': '8',      'Dam': '1D+1* (2/1)',        'DP': '2',  'Cost': '750',    'Weight': '100',  'Space': '1',            'Shots': '10', 'Shot Cost': '35',    'Shot Weight': '6'     ,'Loaded Cost': '1100',   'Loaded Weight': '160',  'Mag Cost': '400',   'Mag Weight': '75'}
        self.weapons_rockets_list.append(entry_dict)
        entry_dict: dict = {'Weapon Name': 'Micromissile Launcher',             'Drop-Down Name': 'Micromissile Launcher - Chaff',                     'Ammo Type': 'Chaff',                       'Abbv': 'MML-Chaff',                   'Effect': '1/2 inch x 1',        'To-Hit': '8',      'Dam': '',                   'DP': '2',  'Cost': '750',    'Weight': '100',  'Space': '1',            'Shots': '10', 'Shot Cost': '15',    'Shot Weight': '2.5'   ,'Loaded Cost': '900',    'Loaded Weight': '125',  'Mag Cost': '200',   'Mag Weight': '40'}
        self.weapons_rockets_list.append(entry_dict)
        entry_dict: dict = {'Weapon Name': 'Micromissile Launcher',             'Drop-Down Name': 'Micromissile Launcher - Foam',                      'Ammo Type': 'Foam',                        'Abbv': 'MML-Foam',                    'Effect': '1/2 inch x 1/2 inch', 'To-Hit': '8',      'Dam': '',                   'DP': '2',  'Cost': '750',    'Weight': '100',  'Space': '1',            'Shots': '10', 'Shot Cost': '10',    'Shot Weight': '2.5'   ,'Loaded Cost': '850',    'Loaded Weight': '125',  'Mag Cost': '150',   'Mag Weight': '40'}
        self.weapons_rockets_list.append(entry_dict)
        entry_dict: dict = {'Weapon Name': 'Micromissile Launcher',             'Drop-Down Name': 'Micromissile Launcher - Smoke',                     'Ammo Type': 'Smoke',                       'Abbv': 'MML-Smoke',                   'Effect': '1/2 inch x 2',        'To-Hit': '8',      'Dam': '',                   'DP': '2',  'Cost': '750',    'Weight': '100',  'Space': '1',            'Shots': '10', 'Shot Cost': '20',    'Shot Weight': '2.5'   ,'Loaded Cost': '950',    'Loaded Weight': '125',  'Mag Cost': '250',   'Mag Weight': '40'}
        self.weapons_rockets_list.append(entry_dict)
        entry_dict: dict = {'Weapon Name': 'Micromissile Launcher',             'Drop-Down Name': 'Micromissile Launcher - Hot Smoke',                 'Ammo Type': 'Hot Smoke',                   'Abbv': 'MML-Hot Smoke',               'Effect': '1/2 inch x 2',        'To-Hit': '8',      'Dam': '',                   'DP': '2',  'Cost': '750',    'Weight': '100',  'Space': '1',            'Shots': '10', 'Shot Cost': '20',    'Shot Weight': '2.5'   ,'Loaded Cost': '950',    'Loaded Weight': '125',  'Mag Cost': '250',   'Mag Weight': '40'}
        self.weapons_rockets_list.append(entry_dict)
        entry_dict: dict = {'Weapon Name': 'Micromissile Launcher',             'Drop-Down Name': 'Micromissile Launcher - Tear Gas',                  'Ammo Type': 'Tear Gas',                    'Abbv': 'MML-Tear Gas',                'Effect': '1/2 inch x 2',        'To-Hit': '8',      'Dam': '',                   'DP': '2',  'Cost': '1500',   'Weight': '100',  'Space': '1',            'Shots': '10', 'Shot Cost': '40',    'Shot Weight': '2.5'   ,'Loaded Cost': '1900',   'Loaded Weight': '125',  'Mag Cost': '450',   'Mag Weight': '40'}
        self.weapons_rockets_list.append(entry_dict)
        entry_dict: dict = {'Weapon Name': 'Rocket Launcher',                   'Drop-Down Name': 'Rocket Launcher',                                   'Ammo Type': 'Normal',                      'Abbv': 'RL',                          'Effect': '2 inch Radius',       'To-Hit': '8',      'Dam': '2D',                 'DP': '2',  'Cost': '1000',   'Weight': '200',  'Space': '2',            'Shots': '10', 'Shot Cost': '35',    'Shot Weight': '5'     ,'Loaded Cost': '1350',   'Loaded Weight': '250',  'Mag Cost': '400',   'Mag Weight': '65'}
        self.weapons_rockets_list.append(entry_dict)
        entry_dict: dict = {'Weapon Name': 'Rocket Launcher',                   'Drop-Down Name': 'Rocket Launcher - Armor Piercing',                  'Ammo Type': 'Armor Piercing',              'Abbv': 'RL-AP',                       'Effect': '',                    'To-Hit': '8',      'Dam': '2D+2',               'DP': '2',  'Cost': '1000',   'Weight': '200',  'Space': '2',            'Shots': '10', 'Shot Cost': '53',    'Shot Weight': '5'     ,'Loaded Cost': '1525',   'Loaded Weight': '250',  'Mag Cost': '575',   'Mag Weight': '65'}
        self.weapons_rockets_list.append(entry_dict)
        entry_dict: dict = {'Weapon Name': 'Rocket Launcher',                   'Drop-Down Name': 'Rocket Launcher - Incendiary',                      'Ammo Type': 'Incendiary',                  'Abbv': 'RL-Incendiary',               'Effect': '2 inch Radius',       'To-Hit': '8',      'Dam': '2D+2* (3/2)',        'DP': '2',  'Cost': '1000',   'Weight': '200',  'Space': '2',            'Shots': '10', 'Shot Cost': '60',    'Shot Weight': '11'    ,'Loaded Cost': '1600',   'Loaded Weight': '310',  'Mag Cost': '650',   'Mag Weight': '125'}
        self.weapons_rockets_list.append(entry_dict)
        entry_dict: dict = {'Weapon Name': 'Rocket Launcher',                   'Drop-Down Name': 'Rocket Launcher - Chaff',                           'Ammo Type': 'Chaff',                       'Abbv': 'RL-Chaff',                    'Effect': '1 x 1',               'To-Hit': '8',      'Dam': '',                   'DP': '2',  'Cost': '1000',   'Weight': '200',  'Space': '2',            'Shots': '10', 'Shot Cost': '30',    'Shot Weight': '5'     ,'Loaded Cost': '1300',   'Loaded Weight': '250',  'Mag Cost': '350',   'Mag Weight': '65'}
        self.weapons_rockets_list.append(entry_dict)
        entry_dict: dict = {'Weapon Name': 'Rocket Launcher',                   'Drop-Down Name': 'Rocket Launcher - Foam',                            'Ammo Type': 'Foam',                        'Abbv': 'RL-Foam',                     'Effect': '1 x 1',               'To-Hit': '8',      'Dam': '',                   'DP': '2',  'Cost': '1000',   'Weight': '200',  'Space': '2',            'Shots': '10', 'Shot Cost': '18',    'Shot Weight': '5'     ,'Loaded Cost': '1175',   'Loaded Weight': '250',  'Mag Cost': '225',   'Mag Weight': '65'}
        self.weapons_rockets_list.append(entry_dict)
        entry_dict: dict = {'Weapon Name': 'Rocket Launcher',                   'Drop-Down Name': 'Rocket Launcher - Smoke',                           'Ammo Type': 'Smoke',                       'Abbv': 'RL-Smoke',                    'Effect': '1/2 inch x 4',        'To-Hit': '8',      'Dam': '',                   'DP': '2',  'Cost': '1000',   'Weight': '200',  'Space': '2',            'Shots': '10', 'Shot Cost': '35',    'Shot Weight': '5'     ,'Loaded Cost': '1350',   'Loaded Weight': '250',  'Mag Cost': '400',   'Mag Weight': '65'}
        self.weapons_rockets_list.append(entry_dict)
        entry_dict: dict = {'Weapon Name': 'Rocket Launcher',                   'Drop-Down Name': 'Rocket Launcher - Hot Smoke',                       'Ammo Type': 'Hot Smoke',                   'Abbv': 'RL-Hot Smoke',                'Effect': '1/2 inch x 4',        'To-Hit': '8',      'Dam': '',                   'DP': '2',  'Cost': '1000',   'Weight': '200',  'Space': '2',            'Shots': '10', 'Shot Cost': '35',    'Shot Weight': '5'     ,'Loaded Cost': '1350',   'Loaded Weight': '250',  'Mag Cost': '400',   'Mag Weight': '65'}
        self.weapons_rockets_list.append(entry_dict)
        entry_dict: dict = {'Weapon Name': 'Rocket Launcher',                   'Drop-Down Name': 'Rocket Launcher - Tear Gas',                        'Ammo Type': 'Tear Gas',                    'Abbv': 'RL-Tear Gas',                 'Effect': '1/2 inch x 4',        'To-Hit': '8',      'Dam': '',                   'DP': '2',  'Cost': '1000',   'Weight': '200',  'Space': '2',            'Shots': '10', 'Shot Cost': '70',    'Shot Weight': '5'     ,'Loaded Cost': '1700',   'Loaded Weight': '250',  'Mag Cost': '750',   'Mag Weight': '65'}
        self.weapons_rockets_list.append(entry_dict)
        entry_dict: dict = {'Weapon Name': 'Rocket Launcher',                   'Drop-Down Name': 'Rocket Launcher - Flare Round',                     'Ammo Type': 'Flare Round',                 'Abbv': 'RL w/Flare',                  'Effect': '0',                   'To-Hit': '10',     'Dam': '1D-2',               'DP': '2',  'Cost': '1000',   'Weight': '200',  'Space': '2',            'Shots': '10', 'Shot Cost': '20',    'Shot Weight': '5'     ,'Loaded Cost': '1200',   'Loaded Weight': '250',  'Mag Cost': '250',   'Mag Weight': '65'}
        self.weapons_rockets_list.append(entry_dict)
        entry_dict: dict = {'Weapon Name': 'Multi-Fire Rocket Pod',             'Drop-Down Name': 'Multi-Fire Rocket Pod',                             'Ammo Type': 'Normal',                      'Abbv': 'MFR',                         'Effect': '2 inch Radius',       'To-Hit': '9',      'Dam': '1D/rocket (6)',      'DP': '3',  'Cost': '450',    'Weight': '150',  'Space': '2',            'Shots': '1',  'Shot Cost': '0',     'Shot Weight': '0'     ,'Loaded Cost': '450',    'Loaded Weight': '150',  'Mag Cost': '0',     'Mag Weight': '0'}
        self.weapons_rockets_list.append(entry_dict)
        entry_dict: dict = {'Weapon Name': 'Multi-Fire Rocket Pod',             'Drop-Down Name': 'Multi-Fire Rocket Pod - Armor Piercing',            'Ammo Type': 'Armor Piercing',              'Abbv': 'MFR-AP',                      'Effect': '',                    'To-Hit': '9',      'Dam': '1D+1/rocket (6D+6)', 'DP': '3',  'Cost': '675',    'Weight': '150',  'Space': '2',            'Shots': '1',  'Shot Cost': '0',     'Shot Weight': '0'     ,'Loaded Cost': '675',    'Loaded Weight': '150',  'Mag Cost': '0',     'Mag Weight': '0'}
        self.weapons_rockets_list.append(entry_dict)
        entry_dict: dict = {'Weapon Name': 'Multi-Fire Rocket Pod',             'Drop-Down Name': 'Multi-Fire Rocket Pod - Foam',                      'Ammo Type': 'Foam',                        'Abbv': 'MFR-Foam',                    'Effect': '1/2 inch x 1/2 inch', 'To-Hit': '9',      'Dam': '',                   'DP': '3',  'Cost': '225',    'Weight': '150',  'Space': '2',            'Shots': '1',  'Shot Cost': '0',     'Shot Weight': '0'     ,'Loaded Cost': '225',    'Loaded Weight': '150',  'Mag Cost': '0',     'Mag Weight': '0'}
        self.weapons_rockets_list.append(entry_dict)
        entry_dict: dict = {'Weapon Name': 'Multi-Fire Rocket Pod',             'Drop-Down Name': 'Multi-Fire Rocket Pod - Smoke',                     'Ammo Type': 'Smoke',                       'Abbv': 'MFR-Smoke',                   'Effect': '1/2 inch x 2',        'To-Hit': '9',      'Dam': '',                   'DP': '3',  'Cost': '450',    'Weight': '150',  'Space': '2',            'Shots': '1',  'Shot Cost': '0',     'Shot Weight': '0'     ,'Loaded Cost': '450',    'Loaded Weight': '150',  'Mag Cost': '0',     'Mag Weight': '0'}
        self.weapons_rockets_list.append(entry_dict)
        entry_dict: dict = {'Weapon Name': 'Multi-Fire Rocket Pod',             'Drop-Down Name': 'Multi-Fire Rocket Pod - Hot Smoke',                 'Ammo Type': 'Hot Smoke',                   'Abbv': 'MFR-Hot Smoke',               'Effect': '1/2 inch x 2',        'To-Hit': '9',      'Dam': '',                   'DP': '3',  'Cost': '450',    'Weight': '150',  'Space': '2',            'Shots': '1',  'Shot Cost': '0',     'Shot Weight': '0'     ,'Loaded Cost': '450',    'Loaded Weight': '150',  'Mag Cost': '0',     'Mag Weight': '0'}
        self.weapons_rockets_list.append(entry_dict)
        entry_dict: dict = {'Weapon Name': 'Multi-Fire Rocket Pod',             'Drop-Down Name': 'Multi-Fire Rocket Pod - Tear Gas',                  'Ammo Type': 'Tear Gas',                    'Abbv': 'MFR-Tear Gas',                'Effect': '1/2 inch x 2',        'To-Hit': '9',      'Dam': '',                   'DP': '3',  'Cost': '900',    'Weight': '150',  'Space': '2',            'Shots': '1',  'Shot Cost': '0',     'Shot Weight': '0'     ,'Loaded Cost': '900',    'Loaded Weight': '150',  'Mag Cost': '0',     'Mag Weight': '0'}
        self.weapons_rockets_list.append(entry_dict)
        entry_dict: dict = {'Weapon Name': 'Variable-Fire Rocket Pod',          'Drop-Down Name': 'Variable-Fire Rocket Pod',                          'Ammo Type': 'Normal',                      'Abbv': 'VFRP',                        'Effect': '2 inch Radius',       'To-Hit': '9',      'Dam': '1D per rocket',      'DP': '5',  'Cost': '2000',   'Weight': '200',  'Space': '3',            'Shots': '30', 'Shot Cost': '35',    'Shot Weight': '7.5'   ,'Loaded Cost': '3050',   'Loaded Weight': '425',  'Mag Cost': '1100',  'Mag Weight': '240'}
        self.weapons_rockets_list.append(entry_dict)
        entry_dict: dict = {'Weapon Name': 'Variable-Fire Rocket Pod',          'Drop-Down Name': 'Variable-Fire Rocket Pod - Armor Piercing',         'Ammo Type': 'Armor Piercing',              'Abbv': 'VFRP-AP',                     'Effect': '',                    'To-Hit': '9',      'Dam': '1D+1 per rocket',    'DP': '5',  'Cost': '2000',   'Weight': '200',  'Space': '3',            'Shots': '30', 'Shot Cost': '53',    'Shot Weight': '7.5'   ,'Loaded Cost': '3575',   'Loaded Weight': '425',  'Mag Cost': '1625',  'Mag Weight': '240'}
        self.weapons_rockets_list.append(entry_dict)
        entry_dict: dict = {'Weapon Name': 'Variable-Fire Rocket Pod',          'Drop-Down Name': 'Variable-Fire Rocket Pod - Chaff',                  'Ammo Type': 'Chaff',                       'Abbv': 'VFRP-Chaff',                  'Effect': '1/2 inch x 1',        'To-Hit': '9',      'Dam': '',                   'DP': '5',  'Cost': '2000',   'Weight': '200',  'Space': '3',            'Shots': '30', 'Shot Cost': '30',    'Shot Weight': '7.5'   ,'Loaded Cost': '2900',   'Loaded Weight': '425',  'Mag Cost': '950',   'Mag Weight': '240'}
        self.weapons_rockets_list.append(entry_dict)
        entry_dict: dict = {'Weapon Name': 'Variable-Fire Rocket Pod',          'Drop-Down Name': 'Variable-Fire Rocket Pod - Foam',                   'Ammo Type': 'Foam',                        'Abbv': 'VFRP-Foam',                   'Effect': '1/2 inch x 1/2 inch', 'To-Hit': '9',      'Dam': '',                   'DP': '5',  'Cost': '2000',   'Weight': '200',  'Space': '3',            'Shots': '30', 'Shot Cost': '18',    'Shot Weight': '7.5'   ,'Loaded Cost': '2525',   'Loaded Weight': '425',  'Mag Cost': '575',   'Mag Weight': '240'}
        self.weapons_rockets_list.append(entry_dict)
        entry_dict: dict = {'Weapon Name': 'Variable-Fire Rocket Pod',          'Drop-Down Name': 'Variable-Fire Rocket Pod - Smoke',                  'Ammo Type': 'Smoke',                       'Abbv': 'VFRP-Smoke',                  'Effect': '1/2 inch x 2',        'To-Hit': '9',      'Dam': '',                   'DP': '5',  'Cost': '2000',   'Weight': '200',  'Space': '3',            'Shots': '30', 'Shot Cost': '35',    'Shot Weight': '7.5'   ,'Loaded Cost': '3050',   'Loaded Weight': '425',  'Mag Cost': '1100',  'Mag Weight': '240'}
        self.weapons_rockets_list.append(entry_dict)
        entry_dict: dict = {'Weapon Name': 'Variable-Fire Rocket Pod',          'Drop-Down Name': 'Variable-Fire Rocket Pod - Hot Smoke',              'Ammo Type': 'Hot Smoke',                   'Abbv': 'VFRP-Hot Smoke',              'Effect': '1/2 inch x 2',        'To-Hit': '9',      'Dam': '',                   'DP': '5',  'Cost': '2000',   'Weight': '200',  'Space': '3',            'Shots': '30', 'Shot Cost': '35',    'Shot Weight': '7.5'   ,'Loaded Cost': '3050',   'Loaded Weight': '425',  'Mag Cost': '1100',  'Mag Weight': '240'}
        self.weapons_rockets_list.append(entry_dict)
        entry_dict: dict = {'Weapon Name': 'Variable-Fire Rocket Pod',          'Drop-Down Name': 'Variable-Fire Rocket Pod - Tear Gas',               'Ammo Type': 'Tear Gas',                    'Abbv': 'VFRP-Tear Gas',               'Effect': '1/2 inch x 2',        'To-Hit': '9',      'Dam': '',                   'DP': '5',  'Cost': '2000',   'Weight': '200',  'Space': '3',            'Shots': '30', 'Shot Cost': '70',    'Shot Weight': '7.5'   ,'Loaded Cost': '4100',   'Loaded Weight': '425',  'Mag Cost': '2150',  'Mag Weight': '240'}
        self.weapons_rockets_list.append(entry_dict)
        entry_dict: dict = {'Weapon Name': '',                                  'Drop-Down Name': 'MISSILES',                                          'Ammo Type': '',                            'Abbv': '',                            'Effect': '',                    'To-Hit': '',       'Dam': '',                   'DP': '',   'Cost': '0',      'Weight': '0',     'Space': '0',             'Shots': '',   'Shot Cost': '',      'Shot Weight': ''      ,'Loaded Cost': '',       'Loaded Weight': '',     'Mag Cost': '',      'Mag Weight': ''}
        self.weapons_missiles_list.append(entry_dict)
        entry_dict: dict = {'Weapon Name': 'Surface-to-Air Missile',            'Drop-Down Name': 'Surface-to-Air Missile',                            'Ammo Type': 'Normal',                      'Abbv': 'SAM',                         'Effect': '2 inch Radius',       'To-Hit': '6/11',   'Dam': '4D',                 'DP': '3',  'Cost': '500',    'Weight': '150',  'Space': '1',            'Shots': '1',  'Shot Cost': '0',     'Shot Weight': '0'     ,'Loaded Cost': '500',    'Loaded Weight': '150',  'Mag Cost': '0',     'Mag Weight': '0'}
        self.weapons_missiles_list.append(entry_dict)
        entry_dict: dict = {'Weapon Name': 'Surface-to-Air Missile',            'Drop-Down Name': 'Surface-to-Air Missile - Armor Piercing',           'Ammo Type': 'Armor Piercing',              'Abbv': 'SAM-AP',                      'Effect': '2 inch Radius',       'To-Hit': '6/11',   'Dam': '4D+4',               'DP': '3',  'Cost': '750',    'Weight': '150',  'Space': '1',            'Shots': '1',  'Shot Cost': '0',     'Shot Weight': '0'     ,'Loaded Cost': '750',    'Loaded Weight': '150',  'Mag Cost': '0',     'Mag Weight': '0'}
        self.weapons_missiles_list.append(entry_dict)
        entry_dict: dict = {'Weapon Name': 'Surface-to-Air Missile',            'Drop-Down Name': 'Surface-to-Air Missile - HARM',                     'Ammo Type': 'HARM',                        'Abbv': 'SAM-HARM',                    'Effect': '2 inch Radius',       'To-Hit': '6/11',   'Dam': '4D',                 'DP': '3',  'Cost': '600',    'Weight': '150',  'Space': '1',            'Shots': '1',  'Shot Cost': '0',     'Shot Weight': '0'     ,'Loaded Cost': '600',    'Loaded Weight': '150',  'Mag Cost': '0',     'Mag Weight': '0'}
        self.weapons_missiles_list.append(entry_dict)
        entry_dict: dict = {'Weapon Name': 'Surface-to-Air Missile',            'Drop-Down Name': 'Surface-to-Air Missile - AP HARM',                  'Ammo Type': 'AP HARM',                     'Abbv': 'SAM-AP HARM',                 'Effect': '2 inch Radius',       'To-Hit': '6/11',   'Dam': '4D+4',               'DP': '3',  'Cost': '850',    'Weight': '150',  'Space': '1',            'Shots': '1',  'Shot Cost': '0',     'Shot Weight': '0'     ,'Loaded Cost': '850',    'Loaded Weight': '150',  'Mag Cost': '0',     'Mag Weight': '0'}
        self.weapons_missiles_list.append(entry_dict)
        entry_dict: dict = {'Weapon Name': 'Surface-to-Air Missile',            'Drop-Down Name': 'Surface-to-Air Missile - Stealth',                  'Ammo Type': 'Stealth',                     'Abbv': 'SAM Stealth',                 'Effect': '2 inch Radius',       'To-Hit': '6/11',   'Dam': '4D',                 'DP': '3',  'Cost': '500',    'Weight': '150',  'Space': '1',            'Shots': '1',  'Shot Cost': '0',     'Shot Weight': '0'     ,'Loaded Cost': '500',    'Loaded Weight': '150',  'Mag Cost': '0',     'Mag Weight': '0'}
        self.weapons_missiles_list.append(entry_dict)
        entry_dict: dict = {'Weapon Name': 'Surface-to-Air Missile',            'Drop-Down Name': 'Surface-to-Air Missile - AP Stealth',               'Ammo Type': 'AP Stealth',                  'Abbv': 'SAM-AP Stealth',              'Effect': '2 inch Radius',       'To-Hit': '6/11',   'Dam': '4D+4',               'DP': '3',  'Cost': '750',    'Weight': '150',  'Space': '1',            'Shots': '1',  'Shot Cost': '0',     'Shot Weight': '0'     ,'Loaded Cost': '750',    'Loaded Weight': '150',  'Mag Cost': '0',     'Mag Weight': '0'}
        self.weapons_missiles_list.append(entry_dict)
        entry_dict: dict = {'Weapon Name': 'Surface-to-Air Missile',            'Drop-Down Name': 'Surface-to-Air Missile - HARM Stealth',             'Ammo Type': 'HARM Stealth',                'Abbv': 'SAM-HARM Stealth',            'Effect': '2 inch Radius',       'To-Hit': '6/11',   'Dam': '4D',                 'DP': '3',  'Cost': '600',    'Weight': '150',  'Space': '1',            'Shots': '1',  'Shot Cost': '0',     'Shot Weight': '0'     ,'Loaded Cost': '600',    'Loaded Weight': '150',  'Mag Cost': '0',     'Mag Weight': '0'}
        self.weapons_missiles_list.append(entry_dict)
        entry_dict: dict = {'Weapon Name': 'Surface-to-Air Missile',            'Drop-Down Name': 'Surface-to-Air Missile - AP HARM Stealth',          'Ammo Type': 'AP HARM Stealth',             'Abbv': 'SAM-AP HARM Stealth',         'Effect': '2 inch Radius',       'To-Hit': '6/11',   'Dam': '4D+4',               'DP': '3',  'Cost': '850',    'Weight': '150',  'Space': '1',            'Shots': '1',  'Shot Cost': '0',     'Shot Weight': '0'     ,'Loaded Cost': '850',    'Loaded Weight': '150',  'Mag Cost': '0',     'Mag Weight': '0'}
        self.weapons_missiles_list.append(entry_dict)
        entry_dict: dict = {'Weapon Name': 'Wire-Guided Missile',               'Drop-Down Name': 'Wire-Guided Missile',                               'Ammo Type': 'Normal',                      'Abbv': 'WGM',                         'Effect': '2 inch Radius',       'To-Hit': '6',      'Dam': '3D',                 'DP': '2',  'Cost': '2000',   'Weight': '100',  'Space': '1',            'Shots': '1',  'Shot Cost': '0',     'Shot Weight': '0'     ,'Loaded Cost': '2000',   'Loaded Weight': '100',  'Mag Cost': '0',     'Mag Weight': '0'}
        self.weapons_missiles_list.append(entry_dict)
        entry_dict: dict = {'Weapon Name': 'Wire-Guided Missile',               'Drop-Down Name': 'Wire-Guided Missile - Armor Piercing',              'Ammo Type': 'Armor Piercing',              'Abbv': 'WGM-AP',                      'Effect': '',                    'To-Hit': '6',      'Dam': '3D+3',               'DP': '2',  'Cost': '3000',   'Weight': '100',  'Space': '1',            'Shots': '1',  'Shot Cost': '0',     'Shot Weight': '0'     ,'Loaded Cost': '3000',   'Loaded Weight': '100',  'Mag Cost': '0',     'Mag Weight': '0'}
        self.weapons_missiles_list.append(entry_dict)
        entry_dict: dict = {'Weapon Name': 'Wire-Guided Missile',               'Drop-Down Name': 'Wire-Guided Missile - HARM',                        'Ammo Type': 'HARM',                        'Abbv': 'WGM-HARM',                    'Effect': '2 inch Radius',       'To-Hit': '6',      'Dam': '3D',                 'DP': '2',  'Cost': '2100',   'Weight': '100',  'Space': '1',            'Shots': '1',  'Shot Cost': '0',     'Shot Weight': '0'     ,'Loaded Cost': '2100',   'Loaded Weight': '100',  'Mag Cost': '0',     'Mag Weight': '0'}
        self.weapons_missiles_list.append(entry_dict)
        entry_dict: dict = {'Weapon Name': 'Wire-Guided Missile',               'Drop-Down Name': 'Wire-Guided Missile - Long Range',                  'Ammo Type': 'Long Range',                  'Abbv': 'WGM-LR',                      'Effect': '2 inch Radius',       'To-Hit': '6',      'Dam': '3D',                 'DP': '2',  'Cost': '4000',   'Weight': '200',  'Space': '1',            'Shots': '1',  'Shot Cost': '0',     'Shot Weight': '0'     ,'Loaded Cost': '4000',   'Loaded Weight': '200',  'Mag Cost': '0',     'Mag Weight': '0'}
        self.weapons_missiles_list.append(entry_dict)
        entry_dict: dict = {'Weapon Name': 'Wire-Guided Missile',               'Drop-Down Name': 'Wire-Guided Missile - Long Range High Speed',       'Ammo Type': 'Long Range High Speed',       'Abbv': 'WGM-LRHS',                    'Effect': '2 inch Radius',       'To-Hit': '6',      'Dam': '3D',                 'DP': '2',  'Cost': '8000',   'Weight': '200',  'Space': '1',            'Shots': '1',  'Shot Cost': '0',     'Shot Weight': '0'     ,'Loaded Cost': '8000',   'Loaded Weight': '200',  'Mag Cost': '0',     'Mag Weight': '0'}
        self.weapons_missiles_list.append(entry_dict)
        entry_dict: dict = {'Weapon Name': 'Wire-Guided Missile',               'Drop-Down Name': 'Wire-Guided Missile - AP HARM',                     'Ammo Type': 'AP HARM',                     'Abbv': 'WGM-AP HARM',                 'Effect': '',                    'To-Hit': '6',      'Dam': '3D+3',               'DP': '2',  'Cost': '3100',   'Weight': '100',  'Space': '1',            'Shots': '1',  'Shot Cost': '0',     'Shot Weight': '0'     ,'Loaded Cost': '3100',   'Loaded Weight': '100',  'Mag Cost': '0',     'Mag Weight': '0'}
        self.weapons_missiles_list.append(entry_dict)
        entry_dict: dict = {'Weapon Name': 'Wire-Guided Missile',               'Drop-Down Name': 'Wire-Guided Missile - AP LR',                       'Ammo Type': 'AP LR',                       'Abbv': 'WGM-AP LR',                   'Effect': '',                    'To-Hit': '6',      'Dam': '3D+3',               'DP': '2',  'Cost': '6000',   'Weight': '200',  'Space': '1',            'Shots': '1',  'Shot Cost': '0',     'Shot Weight': '0'     ,'Loaded Cost': '6000',   'Loaded Weight': '200',  'Mag Cost': '0',     'Mag Weight': '0'}
        self.weapons_missiles_list.append(entry_dict)
        entry_dict: dict = {'Weapon Name': 'Wire-Guided Missile',               'Drop-Down Name': 'Wire-Guided Missile - AP LRHS',                     'Ammo Type': 'AP LRHS',                     'Abbv': 'WGM-AP LRHS',                 'Effect': '',                    'To-Hit': '6',      'Dam': '3D+3',               'DP': '2',  'Cost': '12000',  'Weight': '200',  'Space': '1',            'Shots': '1',  'Shot Cost': '0',     'Shot Weight': '0'     ,'Loaded Cost': '12000',  'Loaded Weight': '2000', 'Mag Cost': '0',     'Mag Weight': '0'}
        self.weapons_missiles_list.append(entry_dict)
        entry_dict: dict = {'Weapon Name': 'Wire-Guided Missile',               'Drop-Down Name': 'Wire-Guided Missile - AP HARM LR',                  'Ammo Type': 'AP HARM LR',                  'Abbv': 'WGM-AP HARM LR',              'Effect': '',                    'To-Hit': '6',      'Dam': '3D+3',               'DP': '2',  'Cost': '6100',   'Weight': '200',  'Space': '1',            'Shots': '1',  'Shot Cost': '0',     'Shot Weight': '0'     ,'Loaded Cost': '6100',   'Loaded Weight': '200',  'Mag Cost': '0',     'Mag Weight': '0'}
        self.weapons_missiles_list.append(entry_dict)
        entry_dict: dict = {'Weapon Name': 'Wire-Guided Missile',               'Drop-Down Name': 'Wire-Guided Missile - AP HARM LRHS',                'Ammo Type': 'AP HARM LRHS',                'Abbv': 'WGM-AP HARM LRHS',            'Effect': '',                    'To-Hit': '6',      'Dam': '3D+3',               'DP': '2',  'Cost': '12100',  'Weight': '200',  'Space': '1',            'Shots': '1',  'Shot Cost': '0',     'Shot Weight': '0'     ,'Loaded Cost': '12100',  'Loaded Weight': '2000', 'Mag Cost': '0',     'Mag Weight': '0'}
        self.weapons_missiles_list.append(entry_dict)
        entry_dict: dict = {'Weapon Name': 'Wire-Guided Missile',               'Drop-Down Name': 'Wire-Guided Missile - Stealth',                     'Ammo Type': 'Stealth',                     'Abbv': 'WGM-Stealth',                 'Effect': '2 inch Radius',       'To-Hit': '6',      'Dam': '3D',                 'DP': '2',  'Cost': '5000',   'Weight': '100',  'Space': '1',            'Shots': '1',  'Shot Cost': '0',     'Shot Weight': '0'     ,'Loaded Cost': '5000',   'Loaded Weight': '100',  'Mag Cost': '0',     'Mag Weight': '0'}
        self.weapons_missiles_list.append(entry_dict)
        entry_dict: dict = {'Weapon Name': 'Wire-Guided Missile',               'Drop-Down Name': 'Wire-Guided Missile - Stealth AP',                  'Ammo Type': 'Stealth AP',                  'Abbv': 'WGM-Stealth AP',              'Effect': '',                    'To-Hit': '6',      'Dam': '3D+3',               'DP': '2',  'Cost': '7500',   'Weight': '100',  'Space': '1',            'Shots': '1',  'Shot Cost': '0',     'Shot Weight': '0'     ,'Loaded Cost': '7500',   'Loaded Weight': '100',  'Mag Cost': '0',     'Mag Weight': '0'}
        self.weapons_missiles_list.append(entry_dict)
        entry_dict: dict = {'Weapon Name': 'Wire-Guided Missile',               'Drop-Down Name': 'Wire-Guided Missile - Stealth HARM',                'Ammo Type': 'Stealth HARM',                'Abbv': 'WGM-Stealth HARM',            'Effect': '2 inch Radius',       'To-Hit': '6',      'Dam': '3D',                 'DP': '2',  'Cost': '5100',   'Weight': '100',  'Space': '1',            'Shots': '1',  'Shot Cost': '0',     'Shot Weight': '0'     ,'Loaded Cost': '5100',   'Loaded Weight': '100',  'Mag Cost': '0',     'Mag Weight': '0'}
        self.weapons_missiles_list.append(entry_dict)
        entry_dict: dict = {'Weapon Name': 'Wire-Guided Missile',               'Drop-Down Name': 'Wire-Guided Missile - Stealth LR',                  'Ammo Type': 'Stealth LR',                  'Abbv': 'WGM-Stealth LR',              'Effect': '2 inch Radius',       'To-Hit': '6',      'Dam': '3D',                 'DP': '2',  'Cost': '10000',  'Weight': '200',  'Space': '1',            'Shots': '1',  'Shot Cost': '0',     'Shot Weight': '0'     ,'Loaded Cost': '10000',  'Loaded Weight': '200',  'Mag Cost': '0',     'Mag Weight': '0'}
        self.weapons_missiles_list.append(entry_dict)
        entry_dict: dict = {'Weapon Name': 'Wire-Guided Missile',               'Drop-Down Name': 'Wire-Guided Missile - Stealth LRHS',                'Ammo Type': 'Stealth LRHS',                'Abbv': 'WGM-Stealth LRHS',            'Effect': '2 inch Radius',       'To-Hit': '6',      'Dam': '3D',                 'DP': '2',  'Cost': '20000',  'Weight': '200',  'Space': '1',            'Shots': '1',  'Shot Cost': '0',     'Shot Weight': '0'     ,'Loaded Cost': '20000',  'Loaded Weight': '200',  'Mag Cost': '0',     'Mag Weight': '0'}
        self.weapons_missiles_list.append(entry_dict)
        entry_dict: dict = {'Weapon Name': 'Wire-Guided Missile',               'Drop-Down Name': 'Wire-Guided Missile - Stealth AP HARM',             'Ammo Type': 'Stealth AP HARM',             'Abbv': 'WGM-Stealth AP HARM',         'Effect': '',                    'To-Hit': '6',      'Dam': '3D+3',               'DP': '2',  'Cost': '7600',   'Weight': '100',  'Space': '1',            'Shots': '1',  'Shot Cost': '0',     'Shot Weight': '0'     ,'Loaded Cost': '7600',   'Loaded Weight': '100',  'Mag Cost': '0',     'Mag Weight': '0'}
        self.weapons_missiles_list.append(entry_dict)
        entry_dict: dict = {'Weapon Name': 'Wire-Guided Missile',               'Drop-Down Name': 'Wire-Guided Missile - Stealth AP LR',               'Ammo Type': 'Stealth AP LR',               'Abbv': 'WGM-Stealth AP LR',           'Effect': '',                    'To-Hit': '6',      'Dam': '3D+3',               'DP': '2',  'Cost': '15000',  'Weight': '200',  'Space': '1',            'Shots': '1',  'Shot Cost': '0',     'Shot Weight': '0'     ,'Loaded Cost': '15000',  'Loaded Weight': '200',  'Mag Cost': '0',     'Mag Weight': '0'}
        self.weapons_missiles_list.append(entry_dict)
        entry_dict: dict = {'Weapon Name': 'Wire-Guided Missile',               'Drop-Down Name': 'Wire-Guided Missile - Stealth AP LRHS',             'Ammo Type': 'Stealth AP LRHS',             'Abbv': 'WGM-Stealth AP LRHS',         'Effect': '',                    'To-Hit': '6',      'Dam': '3D+3',               'DP': '2',  'Cost': '30000',  'Weight': '200',  'Space': '1',            'Shots': '1',  'Shot Cost': '0',     'Shot Weight': '0'     ,'Loaded Cost': '30000',  'Loaded Weight': '2000', 'Mag Cost': '0',     'Mag Weight': '0'}
        self.weapons_missiles_list.append(entry_dict)
        entry_dict: dict = {'Weapon Name': 'Wire-Guided Missile',               'Drop-Down Name': 'Wire-Guided Missile - Stealth AP HARM LR',          'Ammo Type': 'Stealth AP HARM LR',          'Abbv': 'WGM-Stealth AP HARM LR',      'Effect': '',                    'To-Hit': '6',      'Dam': '3D+3',               'DP': '2',  'Cost': '15100',  'Weight': '200',  'Space': '1',            'Shots': '1',  'Shot Cost': '0',     'Shot Weight': '0'     ,'Loaded Cost': '15100',  'Loaded Weight': '200',  'Mag Cost': '0',     'Mag Weight': '0'}
        self.weapons_missiles_list.append(entry_dict)
        entry_dict: dict = {'Weapon Name': 'Wire-Guided Missile',               'Drop-Down Name': 'Wire-Guided Missile - Stealth AP HARM LRHS',        'Ammo Type': 'Stealth AP HARM LRHS',        'Abbv': 'WGM-Stealth AP HARM LRHS',    'Effect': '',                    'To-Hit': '6',      'Dam': '3D+3',               'DP': '2',  'Cost': '30100',  'Weight': '200',  'Space': '1',            'Shots': '1',  'Shot Cost': '0',     'Shot Weight': '0'     ,'Loaded Cost': '30100',  'Loaded Weight': '2000', 'Mag Cost': '0',     'Mag Weight': '0'}
        self.weapons_missiles_list.append(entry_dict)
        entry_dict: dict = {'Weapon Name': '',                                  'Drop-Down Name': 'ENERGY WEAPONS',                                    'Ammo Type': '',                            'Abbv': '',                            'Effect': '',                    'To-Hit': '',       'Dam': '',                   'DP': '',   'Cost': '0',      'Weight': '0',     'Space': '0',             'Shots': '',   'Shot Cost': '',      'Shot Weight': ''      ,'Loaded Cost': '',       'Loaded Weight': '',     'Mag Cost': '',      'Mag Weight': ''}
        self.weapons_energy_list.append(entry_dict)
        entry_dict: dict = {'Weapon Name': 'Targeting Laser',                   'Drop-Down Name': 'Targeting Laser',                                   'Ammo Type': 'Normal',                      'Abbv': 'TL',                          'Effect': '0',                   'To-Hit': '6',      'Dam': '0',                  'DP': '1',  'Cost': '1000',   'Weight': '50',   'Space': '0',            'Shots': '0',  'Shot Cost': '0',     'Shot Weight': '0'     ,'Loaded Cost': '1000',   'Loaded Weight': '50',   'Mag Cost': '0',     'Mag Weight': '0'}
        self.weapons_energy_list.append(entry_dict)
        entry_dict: dict = {'Weapon Name': 'Targeting Laser',                   'Drop-Down Name': 'Targeting Laser - Infared',                         'Ammo Type': 'Infared',                     'Abbv': 'IR-TL',                       'Effect': '0',                   'To-Hit': '6',      'Dam': '0',                  'DP': '1',  'Cost': '2000',   'Weight': '50',   'Space': '0',            'Shots': '0',  'Shot Cost': '0',     'Shot Weight': '0'     ,'Loaded Cost': '2000',   'Loaded Weight': '50',   'Mag Cost': '0',     'Mag Weight': '0'}
        self.weapons_energy_list.append(entry_dict)
        entry_dict: dict = {'Weapon Name': 'Targeting Laser',                   'Drop-Down Name': 'Targeting Laser - Blue-Green',                      'Ammo Type': 'Blue-Green',                  'Abbv': 'BG-TL',                       'Effect': '0',                   'To-Hit': '6',      'Dam': '0',                  'DP': '1',  'Cost': '1250',   'Weight': '50',   'Space': '0',            'Shots': '0',  'Shot Cost': '0',     'Shot Weight': '0'     ,'Loaded Cost': '1250',   'Loaded Weight': '50',   'Mag Cost': '0',     'Mag Weight': '0'}
        self.weapons_energy_list.append(entry_dict)
        entry_dict: dict = {'Weapon Name': 'Targeting Laser',                   'Drop-Down Name': 'Targeting Laser - Pulse',                           'Ammo Type': 'Pulse',                       'Abbv': 'Pulse-TL',                    'Effect': '0',                   'To-Hit': '6',      'Dam': '0',                  'DP': '1',  'Cost': '1500',   'Weight': '50',   'Space': '0',            'Shots': '0',  'Shot Cost': '0',     'Shot Weight': '0'     ,'Loaded Cost': '1500',   'Loaded Weight': '50',   'Mag Cost': '0',     'Mag Weight': '0'}
        self.weapons_energy_list.append(entry_dict)
        entry_dict: dict = {'Weapon Name': '*Military Targeting Laser',         'Drop-Down Name': '*Military Targeting Laser',                         'Ammo Type': 'Normal',                      'Abbv': 'MTL',                         'Effect': '0',                   'To-Hit': '6',      'Dam': '0',                  'DP': '1',  'Cost': '15000',  'Weight': '50',   'Space': '0',            'Shots': '0',  'Shot Cost': '0',     'Shot Weight': '0'     ,'Loaded Cost': '15000',  'Loaded Weight': '50',   'Mag Cost': '0',     'Mag Weight': '0'}
        self.weapons_energy_list.append(entry_dict)
        entry_dict: dict = {'Weapon Name': '*Military Targeting Laser',         'Drop-Down Name': '*Military Targeting Laser - Infared',               'Ammo Type': 'Infared',                     'Abbv': 'IR-MTL',                      'Effect': '0',                   'To-Hit': '6',      'Dam': '0',                  'DP': '1',  'Cost': '30000',  'Weight': '50',   'Space': '0',            'Shots': '0',  'Shot Cost': '0',     'Shot Weight': '0'     ,'Loaded Cost': '30000',  'Loaded Weight': '50',   'Mag Cost': '0',     'Mag Weight': '0'}
        self.weapons_energy_list.append(entry_dict)
        entry_dict: dict = {'Weapon Name': '*Military Targeting Laser',         'Drop-Down Name': '*Military Targeting Laser - Blue-Green',            'Ammo Type': 'Blue-Green',                  'Abbv': 'BG-MTL',                      'Effect': '0',                   'To-Hit': '6',      'Dam': '0',                  'DP': '1',  'Cost': '18750',  'Weight': '50',   'Space': '0',            'Shots': '0',  'Shot Cost': '0',     'Shot Weight': '0'     ,'Loaded Cost': '18750',  'Loaded Weight': '50',   'Mag Cost': '0',     'Mag Weight': '0'}
        self.weapons_energy_list.append(entry_dict)
        entry_dict: dict = {'Weapon Name': '*Military Targeting Laser',         'Drop-Down Name': '*Military Targeting Laser - Pulse',                 'Ammo Type': 'Pulse',                       'Abbv': 'Pulse-MTL',                   'Effect': '0',                   'To-Hit': '6',      'Dam': '0',                  'DP': '1',  'Cost': '22500',  'Weight': '50',   'Space': '0',            'Shots': '0',  'Shot Cost': '0',     'Shot Weight': '0'     ,'Loaded Cost': '22500',  'Loaded Weight': '50',   'Mag Cost': '0',     'Mag Weight': '0'}
        self.weapons_energy_list.append(entry_dict)
        entry_dict: dict = {'Weapon Name': 'Light Laser',                       'Drop-Down Name': 'Light Laser',                                       'Ammo Type': 'Normal',                      'Abbv': 'LL',                          'Effect': 'Area',                'To-Hit': '6',      'Dam': '1D (0/0)',           'DP': '2',  'Cost': '3000',   'Weight': '200',  'Space': '1',            'Shots': '0',  'Shot Cost': '0',     'Shot Weight': '0'     ,'Loaded Cost': '3000',   'Loaded Weight': '200',  'Mag Cost': '0',     'Mag Weight': '0'}
        self.weapons_energy_list.append(entry_dict)
        entry_dict: dict = {'Weapon Name': 'Light Laser',                       'Drop-Down Name': 'Light Laser - Infared',                             'Ammo Type': 'Infared',                     'Abbv': 'IR-LL',                       'Effect': 'Area',                'To-Hit': '6',      'Dam': '1D* (0/0)',          'DP': '2',  'Cost': '6000',   'Weight': '200',  'Space': '1',            'Shots': '0',  'Shot Cost': '0',     'Shot Weight': '0'     ,'Loaded Cost': '6000',   'Loaded Weight': '200',  'Mag Cost': '0',     'Mag Weight': '0'}
        self.weapons_energy_list.append(entry_dict)
        entry_dict: dict = {'Weapon Name': 'Light Laser',                       'Drop-Down Name': 'Light Laser - Blue-Green',                          'Ammo Type': 'Blue-Green',                  'Abbv': 'BG-LL',                       'Effect': 'Area',                'To-Hit': '6',      'Dam': '1D (0/0)',           'DP': '2',  'Cost': '3750',   'Weight': '200',  'Space': '1',            'Shots': '0',  'Shot Cost': '0',     'Shot Weight': '0'     ,'Loaded Cost': '3750',   'Loaded Weight': '200',  'Mag Cost': '0',     'Mag Weight': '0'}
        self.weapons_energy_list.append(entry_dict)
        entry_dict: dict = {'Weapon Name': 'Light Laser',                       'Drop-Down Name': 'Light Laser - Pulse',                               'Ammo Type': 'Pulse',                       'Abbv': 'Pulse-LL',                    'Effect': 'Area',                'To-Hit': '6',      'Dam': '1D+1 (0/0)',         'DP': '2',  'Cost': '4500',   'Weight': '200',  'Space': '1',            'Shots': '0',  'Shot Cost': '0',     'Shot Weight': '0'     ,'Loaded Cost': '4500',   'Loaded Weight': '200',  'Mag Cost': '0',     'Mag Weight': '0'}
        self.weapons_energy_list.append(entry_dict)
        entry_dict: dict = {'Weapon Name': 'Medium Laser',                      'Drop-Down Name': 'Medium Laser',                                      'Ammo Type': 'Normal',                      'Abbv': 'ML',                          'Effect': 'Area',                'To-Hit': '6',      'Dam': '2D (1/0)',           'DP': '2',  'Cost': '5500',   'Weight': '350',  'Space': '2',            'Shots': '0',  'Shot Cost': '0',     'Shot Weight': '0'     ,'Loaded Cost': '5500',   'Loaded Weight': '350',  'Mag Cost': '0',     'Mag Weight': '0'}
        self.weapons_energy_list.append(entry_dict)
        entry_dict: dict = {'Weapon Name': 'Medium Laser',                      'Drop-Down Name': 'Medium Laser - Infared',                            'Ammo Type': 'Infared',                     'Abbv': 'IR-ML',                       'Effect': 'Area',                'To-Hit': '6',      'Dam': '2D* (1/0)',          'DP': '2',  'Cost': '11000',  'Weight': '350',  'Space': '2',            'Shots': '0',  'Shot Cost': '0',     'Shot Weight': '0'     ,'Loaded Cost': '11000',  'Loaded Weight': '350',  'Mag Cost': '0',     'Mag Weight': '0'}
        self.weapons_energy_list.append(entry_dict)
        entry_dict: dict = {'Weapon Name': 'Medium Laser',                      'Drop-Down Name': 'Medium Laser - Blue-Green',                         'Ammo Type': 'Blue-Green',                  'Abbv': 'BG-ML',                       'Effect': 'Area',                'To-Hit': '6',      'Dam': '2D (1/0)',           'DP': '2',  'Cost': '6875',   'Weight': '350',  'Space': '2',            'Shots': '0',  'Shot Cost': '0',     'Shot Weight': '0'     ,'Loaded Cost': '6875',   'Loaded Weight': '350',  'Mag Cost': '0',     'Mag Weight': '0'}
        self.weapons_energy_list.append(entry_dict)
        entry_dict: dict = {'Weapon Name': 'Medium Laser',                      'Drop-Down Name': 'Medium Laser - Pulse',                              'Ammo Type': 'Pulse',                       'Abbv': 'Pulse-ML',                    'Effect': 'Area',                'To-Hit': '6',      'Dam': '2D+2 (1/0)',         'DP': '2',  'Cost': '8250',   'Weight': '350',  'Space': '2',            'Shots': '0',  'Shot Cost': '0',     'Shot Weight': '0'     ,'Loaded Cost': '8250',   'Loaded Weight': '350',  'Mag Cost': '0',     'Mag Weight': '0'}
        self.weapons_energy_list.append(entry_dict)
        entry_dict: dict = {'Weapon Name': 'Laser',                             'Drop-Down Name': 'Laser',                                             'Ammo Type': 'Normal',                      'Abbv': 'L',                           'Effect': 'Area',                'To-Hit': '6',      'Dam': '3D (1/0)',           'DP': '2',  'Cost': '8000',   'Weight': '500',  'Space': '2',            'Shots': '0',  'Shot Cost': '0',     'Shot Weight': '0'     ,'Loaded Cost': '8000',   'Loaded Weight': '500',  'Mag Cost': '0',     'Mag Weight': '0'}
        self.weapons_energy_list.append(entry_dict)
        entry_dict: dict = {'Weapon Name': 'Laser',                             'Drop-Down Name': 'Laser - Infared',                                   'Ammo Type': 'Infared',                     'Abbv': 'IR-L',                        'Effect': 'Area',                'To-Hit': '6',      'Dam': '3D* (1/0)',          'DP': '2',  'Cost': '16000',  'Weight': '500',  'Space': '2',            'Shots': '0',  'Shot Cost': '0',     'Shot Weight': '0'     ,'Loaded Cost': '16000',  'Loaded Weight': '500',  'Mag Cost': '0',     'Mag Weight': '0'}
        self.weapons_energy_list.append(entry_dict)
        entry_dict: dict = {'Weapon Name': 'Laser',                             'Drop-Down Name': 'Laser - Blue-Green',                                'Ammo Type': 'Blue-Green',                  'Abbv': 'BG-L',                        'Effect': 'Area',                'To-Hit': '6',      'Dam': '3D (1/0)',           'DP': '2',  'Cost': '10000',  'Weight': '500',  'Space': '2',            'Shots': '0',  'Shot Cost': '0',     'Shot Weight': '0'     ,'Loaded Cost': '10000',  'Loaded Weight': '500',  'Mag Cost': '0',     'Mag Weight': '0'}
        self.weapons_energy_list.append(entry_dict)
        entry_dict: dict = {'Weapon Name': 'Laser',                             'Drop-Down Name': 'Laser - Pulse',                                     'Ammo Type': 'Pulse',                       'Abbv': 'Pulse-L',                     'Effect': 'Area',                'To-Hit': '6',      'Dam': '3D+3 (1/0)',         'DP': '2',  'Cost': '12000',  'Weight': '500',  'Space': '2',            'Shots': '0',  'Shot Cost': '0',     'Shot Weight': '0'     ,'Loaded Cost': '12000',  'Loaded Weight': '500',  'Mag Cost': '0',     'Mag Weight': '0'}
        self.weapons_energy_list.append(entry_dict)
        entry_dict: dict = {'Weapon Name': 'Twin Laser',                        'Drop-Down Name': 'Twin Laser',                                        'Ammo Type': 'Normal',                      'Abbv': 'TwL',                         'Effect': 'Area',                'To-Hit': '6',      'Dam': '2D+6 (1/0)',         'DP': '3',  'Cost': '10000',  'Weight': '750',  'Space': '2',            'Shots': '0',  'Shot Cost': '0',     'Shot Weight': '0'     ,'Loaded Cost': '10000',  'Loaded Weight': '750',  'Mag Cost': '0',     'Mag Weight': '0'}
        self.weapons_energy_list.append(entry_dict)
        entry_dict: dict = {'Weapon Name': 'Twin Laser',                        'Drop-Down Name': 'Twin Laser - Infared',                              'Ammo Type': 'Infared',                     'Abbv': 'IR-TwL',                      'Effect': 'Area',                'To-Hit': '6',      'Dam': '2D+6* (1/0)',        'DP': '3',  'Cost': '20000',  'Weight': '750',  'Space': '2',            'Shots': '0',  'Shot Cost': '0',     'Shot Weight': '0'     ,'Loaded Cost': '20000',  'Loaded Weight': '750',  'Mag Cost': '0',     'Mag Weight': '0'}
        self.weapons_energy_list.append(entry_dict)
        entry_dict: dict = {'Weapon Name': 'Twin Laser',                        'Drop-Down Name': 'Twin Laser - Blue-Green',                           'Ammo Type': 'Blue-Green',                  'Abbv': 'BG-TwL',                      'Effect': 'Area',                'To-Hit': '6',      'Dam': '2D+6 (1/0)',         'DP': '3',  'Cost': '12500',  'Weight': '750',  'Space': '2',            'Shots': '0',  'Shot Cost': '0',     'Shot Weight': '0'     ,'Loaded Cost': '12500',  'Loaded Weight': '750',  'Mag Cost': '0',     'Mag Weight': '0'}
        self.weapons_energy_list.append(entry_dict)
        entry_dict: dict = {'Weapon Name': 'Twin Laser',                        'Drop-Down Name': 'Twin Laser - Pulse',                                'Ammo Type': 'Pulse',                       'Abbv': 'Pulse-TwL',                   'Effect': 'Area',                'To-Hit': '6',      'Dam': '2D+8 (1/0)',         'DP': '3',  'Cost': '15000',  'Weight': '750',  'Space': '2',            'Shots': '0',  'Shot Cost': '0',     'Shot Weight': '0'     ,'Loaded Cost': '15000',  'Loaded Weight': '750',  'Mag Cost': '0',     'Mag Weight': '0'}
        self.weapons_energy_list.append(entry_dict)
        entry_dict: dict = {'Weapon Name': 'Heavy Laser',                       'Drop-Down Name': 'Heavy Laser',                                       'Ammo Type': 'Normal',                      'Abbv': 'HL',                          'Effect': 'Area',                'To-Hit': '6',      'Dam': '4D (2/0)',           'DP': '2',  'Cost': '12000',  'Weight': '1000', 'Space': '3',            'Shots': '0',  'Shot Cost': '0',     'Shot Weight': '0'     ,'Loaded Cost': '12000',  'Loaded Weight': '1000', 'Mag Cost': '0',     'Mag Weight': '0'}
        self.weapons_energy_list.append(entry_dict)
        entry_dict: dict = {'Weapon Name': 'Heavy Laser',                       'Drop-Down Name': 'Heavy Laser - Infared',                             'Ammo Type': 'Infared',                     'Abbv': 'IR-HL',                       'Effect': 'Area',                'To-Hit': '6',      'Dam': '4D* (2/0)',          'DP': '2',  'Cost': '24000',  'Weight': '1000', 'Space': '3',            'Shots': '0',  'Shot Cost': '0',     'Shot Weight': '0'     ,'Loaded Cost': '24000',  'Loaded Weight': '1000', 'Mag Cost': '0',     'Mag Weight': '0'}
        self.weapons_energy_list.append(entry_dict)
        entry_dict: dict = {'Weapon Name': 'Heavy Laser',                       'Drop-Down Name': 'Heavy Laser - Blue-Green',                          'Ammo Type': 'Blue-Green',                  'Abbv': 'BG-HL',                       'Effect': 'Area',                'To-Hit': '6',      'Dam': '4D* (2/0)',          'DP': '2',  'Cost': '15000',  'Weight': '1000', 'Space': '3',            'Shots': '0',  'Shot Cost': '0',     'Shot Weight': '0'     ,'Loaded Cost': '15000',  'Loaded Weight': '1000', 'Mag Cost': '0',     'Mag Weight': '0'}
        self.weapons_energy_list.append(entry_dict)
        entry_dict: dict = {'Weapon Name': 'Heavy Laser',                       'Drop-Down Name': 'Heavy Laser - Pulse',                               'Ammo Type': 'Pulse',                       'Abbv': 'Pulse-HL',                    'Effect': 'Area',                'To-Hit': '6',      'Dam': '4D+4 (2/0)',         'DP': '2',  'Cost': '18000',  'Weight': '1000', 'Space': '3',            'Shots': '0',  'Shot Cost': '0',     'Shot Weight': '0'     ,'Loaded Cost': '18000',  'Loaded Weight': '1000', 'Mag Cost': '0',     'Mag Weight': '0'}
        self.weapons_energy_list.append(entry_dict)
        entry_dict: dict = {'Weapon Name': 'X-Ray Laser',                       'Drop-Down Name': 'X-Ray Laser',                                       'Ammo Type': 'Normal',                      'Abbv': 'XL',                          'Effect': 'Area',                'To-Hit': '7',      'Dam': '4D',                 'DP': '3',  'Cost': '15000',  'Weight': '750',  'Space': '3',            'Shots': '0',  'Shot Cost': '0',     'Shot Weight': '0'     ,'Loaded Cost': '15000',  'Loaded Weight': '750',  'Mag Cost': '0',     'Mag Weight': '0'}
        self.weapons_energy_list.append(entry_dict)
        entry_dict: dict = {'Weapon Name': 'X-Ray Laser',                       'Drop-Down Name': 'X-Ray Laser - Pulse',                               'Ammo Type': 'Pulse',                       'Abbv': 'Pulse-XL',                    'Effect': 'Area',                'To-Hit': '7',      'Dam': '4D+4',               'DP': '3',  'Cost': '22500',  'Weight': '750',  'Space': '3',            'Shots': '0',  'Shot Cost': '0',     'Shot Weight': '0'     ,'Loaded Cost': '22500',  'Loaded Weight': '750',  'Mag Cost': '0',     'Mag Weight': '0'}
        self.weapons_energy_list.append(entry_dict)
        entry_dict: dict = {'Weapon Name': 'Heavy X-Ray Laser',                 'Drop-Down Name': 'Heavy X-Ray Laser',                                 'Ammo Type': 'Normal',                      'Abbv': 'HXL',                         'Effect': 'Area',                'To-Hit': '7',      'Dam': '5D',                 'DP': '3',  'Cost': '20000',  'Weight': '1500', 'Space': '5',            'Shots': '0',  'Shot Cost': '0',     'Shot Weight': '0'     ,'Loaded Cost': '20000',  'Loaded Weight': '1500', 'Mag Cost': '0',     'Mag Weight': '0'}
        self.weapons_energy_list.append(entry_dict)
        entry_dict: dict = {'Weapon Name': 'Heavy X-Ray Laser',                 'Drop-Down Name': 'Heavy X-Ray Laser - Pulse',                         'Ammo Type': 'Pulse',                       'Abbv': 'Pulse-HXL',                   'Effect': 'Area',                'To-Hit': '7',      'Dam': '5D+5',               'DP': '3',  'Cost': '30000',  'Weight': '1500', 'Space': '5',            'Shots': '0',  'Shot Cost': '0',     'Shot Weight': '0'     ,'Loaded Cost': '30000',  'Loaded Weight': '1500', 'Mag Cost': '0',     'Mag Weight': '0'}
        self.weapons_energy_list.append(entry_dict)
        entry_dict: dict = {'Weapon Name': 'Sonic Cannon',                      'Drop-Down Name': 'Sonic Cannon - Light',                              'Ammo Type': 'Light',                       'Abbv': 'LSC',                         'Effect': 'Area',                'To-Hit': '6',      'Dam': '1D',                 'DP': '2',  'Cost': '3500',   'Weight': '450',  'Space': '1',            'Shots': '0',  'Shot Cost': '0',     'Shot Weight': '0'     ,'Loaded Cost': '3500',   'Loaded Weight': '450',  'Mag Cost': '0',     'Mag Weight': '0'}
        self.weapons_energy_list.append(entry_dict)
        entry_dict: dict = {'Weapon Name': 'Sonic Cannon',                      'Drop-Down Name': 'Sonic Cannon',                                      'Ammo Type': 'Normal',                      'Abbv': 'SC',                          'Effect': 'Area',                'To-Hit': '6',      'Dam': '2D',                 'DP': '3',  'Cost': '6100',   'Weight': '800',  'Space': '3',            'Shots': '0',  'Shot Cost': '0',     'Shot Weight': '0'     ,'Loaded Cost': '6100',   'Loaded Weight': '800',  'Mag Cost': '0',     'Mag Weight': '0'}
        self.weapons_energy_list.append(entry_dict)
        entry_dict: dict = {'Weapon Name': 'Sonic Cannon',                      'Drop-Down Name': 'Sonic Cannon - Heavy',                              'Ammo Type': 'Heavy',                       'Abbv': 'HSC',                         'Effect': 'Area',                'To-Hit': '6',      'Dam': '3D',                 'DP': '4',  'Cost': '9600',   'Weight': '1100', 'Space': '5',            'Shots': '0',  'Shot Cost': '0',     'Shot Weight': '0'     ,'Loaded Cost': '9600',   'Loaded Weight': '1100', 'Mag Cost': '0',     'Mag Weight': '0'}
        self.weapons_energy_list.append(entry_dict)
        entry_dict: dict = {'Weapon Name': '*Sonic Cannon',                     'Drop-Down Name': '*Sonic Cannon - Military',                          'Ammo Type': 'Military',                    'Abbv': 'MSC',                         'Effect': 'Area',                'To-Hit': '6',      'Dam': '6D',                 'DP': '6',  'Cost': '22000',  'Weight': '2000', 'Space': '8',            'Shots': '0',  'Shot Cost': '0',     'Shot Weight': '0'     ,'Loaded Cost': '22000',  'Loaded Weight': '2000', 'Mag Cost': '0',     'Mag Weight': '0'}
        self.weapons_energy_list.append(entry_dict)
        entry_dict: dict = {'Weapon Name': 'Tight Beam Sonic Cannon',           'Drop-Down Name': 'Tight Beam Sonic Cannon - Light',                   'Ammo Type': 'Light',                       'Abbv': 'TBMLSC',                      'Effect': 'Area',                'To-Hit': '6',      'Dam': '1D',                 'DP': '2',  'Cost': '7000',   'Weight': '450',  'Space': '1',            'Shots': '0',  'Shot Cost': '0',     'Shot Weight': '0'     ,'Loaded Cost': '3500',   'Loaded Weight': '450',  'Mag Cost': '0',     'Mag Weight': '0'}
        self.weapons_energy_list.append(entry_dict)
        entry_dict: dict = {'Weapon Name': 'Tight Beam Sonic Cannon',           'Drop-Down Name': 'Tight Beam Sonic Cannon',                           'Ammo Type': 'Normal',                      'Abbv': 'TBMSC',                       'Effect': 'Area',                'To-Hit': '6',      'Dam': '2D',                 'DP': '3',  'Cost': '12200',  'Weight': '800',  'Space': '3',            'Shots': '0',  'Shot Cost': '0',     'Shot Weight': '0'     ,'Loaded Cost': '6100',   'Loaded Weight': '800',  'Mag Cost': '0',     'Mag Weight': '0'}
        self.weapons_energy_list.append(entry_dict)
        entry_dict: dict = {'Weapon Name': 'Tight Beam Sonic Cannon',           'Drop-Down Name': 'Tight Beam Sonic Cannon - Heavy',                   'Ammo Type': 'Heavy',                       'Abbv': 'TBMHSC',                      'Effect': 'Area',                'To-Hit': '6',      'Dam': '3D',                 'DP': '4',  'Cost': '19200',  'Weight': '1100', 'Space': '5',            'Shots': '0',  'Shot Cost': '0',     'Shot Weight': '0'     ,'Loaded Cost': '9600',   'Loaded Weight': '1100', 'Mag Cost': '0',     'Mag Weight': '0'}
        self.weapons_energy_list.append(entry_dict)
        entry_dict: dict = {'Weapon Name': '*Tight Beam Sonic Cannon',          'Drop-Down Name': '*Tight Beam Sonic Cannon - Military',               'Ammo Type': 'Military',                    'Abbv': 'TBMMSC',                      'Effect': 'Area',                'To-Hit': '6',      'Dam': '6D',                 'DP': '6',  'Cost': '44000',  'Weight': '2000', 'Space': '8',            'Shots': '0',  'Shot Cost': '0',     'Shot Weight': '0'     ,'Loaded Cost': '22000',  'Loaded Weight': '2000', 'Mag Cost': '0',     'Mag Weight': '0'}
        self.weapons_energy_list.append(entry_dict)
        entry_dict: dict = {'Weapon Name': '',                                  'Drop-Down Name': 'FLAMETHROWERS',                                     'Ammo Type': '',                            'Abbv': '',                            'Effect': '',                    'To-Hit': '',       'Dam': '',                   'DP': '',   'Cost': '0',      'Weight': '0',     'Space': '0',             'Shots': '',   'Shot Cost': '',      'Shot Weight': ''      ,'Loaded Cost': '',       'Loaded Weight': '',     'Mag Cost': '',      'Mag Weight': ''}
        self.weapons_flamethrower_list.append(entry_dict)
        entry_dict: dict = {'Weapon Name': 'Light Flamethrower',                'Drop-Down Name': 'Light Flamethrower',                                'Ammo Type': 'Normal',                      'Abbv': 'LFT',                         'Effect': 'Area;Max 5',          'To-Hit': '6',      'Dam': '1D-2 (2/3)',         'DP': '1',  'Cost': '350',    'Weight': '250',  'Space': '1',            'Shots': '10', 'Shot Cost': '15',    'Shot Weight': '3'     ,'Loaded Cost': '500',    'Loaded Weight': '280',  'Mag Cost': '200',   'Mag Weight': '45'}
        self.weapons_flamethrower_list.append(entry_dict)
        entry_dict: dict = {'Weapon Name': 'Light Flamethrower',                'Drop-Down Name': 'Light Flamethrower - High-Temp',                    'Ammo Type': 'High-Temp',                   'Abbv': 'LFT w/Hi-Temp',               'Effect': 'Area;Max 5',          'To-Hit': '6',      'Dam': '1D (3/1)',           'DP': '1',  'Cost': '350',    'Weight': '250',  'Space': '1',            'Shots': '10', 'Shot Cost': '60',    'Shot Weight': '4.5'   ,'Loaded Cost': '950',    'Loaded Weight': '295',  'Mag Cost': '500',   'Mag Weight': '60'}
        self.weapons_flamethrower_list.append(entry_dict)
        entry_dict: dict = {'Weapon Name': 'Flamethrower',                      'Drop-Down Name': 'Flamethrower',                                      'Ammo Type': 'Normal',                      'Abbv': 'FT',                          'Effect': 'Area;Max 10',         'To-Hit': '6',      'Dam': '1D (4/3)',           'DP': '2',  'Cost': '500',    'Weight': '450',  'Space': '2',            'Shots': '10', 'Shot Cost': '25',    'Shot Weight': '5'     ,'Loaded Cost': '750',    'Loaded Weight': '500',  'Mag Cost': '300',   'Mag Weight': '65'}
        self.weapons_flamethrower_list.append(entry_dict)
        entry_dict: dict = {'Weapon Name': 'Flamethrower',                      'Drop-Down Name': 'Flamethrower - High-Temp',                          'Ammo Type': 'High-Temp',                   'Abbv': 'FT w/Hi-Temp',                'Effect': 'Area;Max 10',         'To-Hit': '6',      'Dam': '1D+2 (5/1)',         'DP': '2',  'Cost': '500',    'Weight': '450',  'Space': '2',            'Shots': '10', 'Shot Cost': '100',   'Shot Weight': '7.5'   ,'Loaded Cost': '1500',   'Loaded Weight': '525',  'Mag Cost': '550',   'Mag Weight': '90'}
        self.weapons_flamethrower_list.append(entry_dict)
        entry_dict: dict = {'Weapon Name': 'HD Flamethrower',                   'Drop-Down Name': 'HD Flamethrower',                                   'Ammo Type': 'Normal',                      'Abbv': 'HDFT',                        'Effect': 'Area;Mac 15',         'To-Hit': '6',      'Dam': '2D (5/3)',           'DP': '3',  'Cost': '1250',   'Weight': '650',  'Space': '3',            'Shots': '10', 'Shot Cost': '50',    'Shot Weight': '10'    ,'Loaded Cost': '1750',   'Loaded Weight': '750',  'Mag Cost': '550',   'Mag Weight': '115'}
        self.weapons_flamethrower_list.append(entry_dict)
        entry_dict: dict = {'Weapon Name': 'HD Flamethrower',                   'Drop-Down Name': 'HD Flamethrower - High-Temp',                       'Ammo Type': 'High-Temp',                   'Abbv': 'HDFT w/Hi-Temp',              'Effect': 'Area;Mac 15',         'To-Hit': '6',      'Dam': '2D+4 (6/1)',         'DP': '3',  'Cost': '1250',   'Weight': '650',  'Space': '3',            'Shots': '10', 'Shot Cost': '200',   'Shot Weight': '15'    ,'Loaded Cost': '3250',   'Loaded Weight': '800',  'Mag Cost': '2050',  'Mag Weight': '165'}
        self.weapons_flamethrower_list.append(entry_dict)
        entry_dict: dict = {'Weapon Name': '*Military Flamethrower',            'Drop-Down Name': '*Military Flamethrower',                            'Ammo Type': 'Normal',                      'Abbv': 'MFT',                         'Effect': 'Area;Mac 30',         'To-Hit': '6',      'Dam': '3D',                 'DP': '5',  'Cost': '2000',   'Weight': '1000', 'Space': '5',            'Shots': '10', 'Shot Cost': '100',   'Shot Weight': '15'    ,'Loaded Cost': '3000',   'Loaded Weight': '1150', 'Mag Cost': '1050',  'Mag Weight': '165'}
        self.weapons_flamethrower_list.append(entry_dict)
        entry_dict: dict = {'Weapon Name': '*Military Flamethrower',            'Drop-Down Name': '*Military Flamethrower - High-Temp',                'Ammo Type': 'High-Temp',                   'Abbv': 'MFT w/Hi-Temp',               'Effect': 'Area;Mac 30',         'To-Hit': '6',      'Dam': '3D+6',               'DP': '5',  'Cost': '2000',   'Weight': '1000', 'Space': '5',            'Shots': '10', 'Shot Cost': '400',   'Shot Weight': '22.5'  ,'Loaded Cost': '6000',   'Loaded Weight': '1225', 'Mag Cost': '4050',  'Mag Weight': '240'}
        self.weapons_flamethrower_list.append(entry_dict)
        entry_dict: dict = {'Weapon Name': '',                                  'Drop-Down Name': 'DROPPED GASSES',                                    'Ammo Type': '',                            'Abbv': '',                            'Effect': '',                    'To-Hit': '',       'Dam': '',                   'DP': '',   'Cost': '0',      'Weight': '0',     'Space': '0',             'Shots': '',   'Shot Cost': '',      'Shot Weight': ''      ,'Loaded Cost': '',       'Loaded Weight': '',     'Mag Cost': '',      'Mag Weight': ''}
        self.weapons_dropped_gas_list.append(entry_dict)
        entry_dict: dict = {'Weapon Name': 'SmokeScreen',                       'Drop-Down Name': 'SmokeScreen',                                       'Ammo Type': 'Normal',                      'Abbv': 'SS',                          'Effect': '1/2 inchx1',          'To-Hit': '0',      'Dam': '0',                  'DP': '4',  'Cost': '250',    'Weight': '25',   'Space': '1',            'Shots': '10', 'Shot Cost': '10',    'Shot Weight': '5'     ,'Loaded Cost': '350',    'Loaded Weight': '75',   'Mag Cost': '150',   'Mag Weight': '65'}
        self.weapons_dropped_gas_list.append(entry_dict)
        entry_dict: dict = {'Weapon Name': 'SmokeScreen',                       'Drop-Down Name': 'SmokeScreen - HotSmoke',                            'Ammo Type': 'HotSmoke',                    'Abbv': 'SSw/HotSmoke',                'Effect': '1/2 inchx1',          'To-Hit': '0',      'Dam': '0',                  'DP': '4',  'Cost': '250',    'Weight': '25',   'Space': '1',            'Shots': '10', 'Shot Cost': '15',    'Shot Weight': '5'     ,'Loaded Cost': '400',    'Loaded Weight': '75',   'Mag Cost': '200',   'Mag Weight': '65'}
        self.weapons_dropped_gas_list.append(entry_dict)
        entry_dict: dict = {'Weapon Name': 'SmokeScreen',                       'Drop-Down Name': 'SmokeScreen - Tear Gas',                            'Ammo Type': 'Tear Gas',                    'Abbv': 'SS w/Tear Gas',               'Effect': '1/2 inchx1',          'To-Hit': '0',      'Dam': '*',                  'DP': '4',  'Cost': '250',    'Weight': '25',   'Space': '1',            'Shots': '10', 'Shot Cost': '20',    'Shot Weight': '5'     ,'Loaded Cost': '450',    'Loaded Weight': '75',   'Mag Cost': '250',   'Mag Weight': '65'}
        self.weapons_dropped_gas_list.append(entry_dict)
        entry_dict: dict = {'Weapon Name': 'Paint Spray',                       'Drop-Down Name': 'Paint Spray',                                       'Ammo Type': 'Normal',                      'Abbv': 'PS',                          'Effect': '1/2 inchx1',          'To-Hit': '0',      'Dam': '0',                  'DP': '2',  'Cost': '400',    'Weight': '25',   'Space': '1',            'Shots': '25', 'Shot Cost': '10',    'Shot Weight': '2'     ,'Loaded Cost': '650',    'Loaded Weight': '75',   'Mag Cost': '300',   'Mag Weight': '65'}
        self.weapons_dropped_gas_list.append(entry_dict)
        entry_dict: dict = {'Weapon Name': 'Paint Spray',                       'Drop-Down Name': 'Paint Spray - StickyFoam Neutralizer',              'Ammo Type': 'StickyFoam Neutralizer',      'Abbv': 'PS, SF Neut.',                'Effect': '1/2 inchx1',          'To-Hit': '0',      'Dam': '0',                  'DP': '2',  'Cost': '400',    'Weight': '25',   'Space': '1',            'Shots': '25', 'Shot Cost': '50',    'Shot Weight': '2'     ,'Loaded Cost': '1650',   'Loaded Weight': '75',   'Mag Cost': '1250',  'Mag Weight': '65'}
        self.weapons_dropped_gas_list.append(entry_dict)
        entry_dict: dict = {'Weapon Name': 'Gas Streamer',                      'Drop-Down Name': 'Gas Streamer - Smoke',                              'Ammo Type': 'Smoke',                       'Abbv': 'GS W/Smoke',                  'Effect': '1/2 inchx5',          'To-Hit': '0',      'Dam': '0',                  'DP': '1',  'Cost': '100',    'Weight': '50',   'Space': '1',            'Shots': '2',  'Shot Cost': '50',    'Shot Weight': '25'    ,'Loaded Cost': '200',    'Loaded Weight': '100',  'Mag Cost': '150',   'Mag Weight': '65'}
        self.weapons_dropped_gas_list.append(entry_dict)
        entry_dict: dict = {'Weapon Name': 'Gas Streamer',                      'Drop-Down Name': 'Gas Streamer - Hot Smoke',                          'Ammo Type': 'Hot Smoke',                   'Abbv': 'GS W/Hot Smoke',              'Effect': '1/2 inchx5',          'To-Hit': '0',      'Dam': '0',                  'DP': '1',  'Cost': '100',    'Weight': '50',   'Space': '1',            'Shots': '2',  'Shot Cost': '75',    'Shot Weight': '25'    ,'Loaded Cost': '250',    'Loaded Weight': '100',  'Mag Cost': '200',   'Mag Weight': '65'}
        self.weapons_dropped_gas_list.append(entry_dict)
        entry_dict: dict = {'Weapon Name': 'Gas Streamer',                      'Drop-Down Name': 'Gas Streamer - Paint',                              'Ammo Type': 'Paint',                       'Abbv': 'GS w/Paint',                  'Effect': '1/2 inchx5',          'To-Hit': '0',      'Dam': '0',                  'DP': '1',  'Cost': '100',    'Weight': '50',   'Space': '1',            'Shots': '2',  'Shot Cost': '50',    'Shot Weight': '10'    ,'Loaded Cost': '200',    'Loaded Weight': '70',   'Mag Cost': '150',   'Mag Weight': '35'}
        self.weapons_dropped_gas_list.append(entry_dict)
        entry_dict: dict = {'Weapon Name': 'Gas Streamer',                      'Drop-Down Name': 'Gas Streamer - StickyFoam Neutralizer',             'Ammo Type': 'StickyFoam Neutralizer',      'Abbv': 'GS w/SF Neut.',               'Effect': '1/2 inchx5',          'To-Hit': '0',      'Dam': '0',                  'DP': '1',  'Cost': '100',    'Weight': '50',   'Space': '1',            'Shots': '2',  'Shot Cost': '250',   'Shot Weight': '10'    ,'Loaded Cost': '600',    'Loaded Weight': '70',   'Mag Cost': '650',   'Mag Weight': '35'}
        self.weapons_dropped_gas_list.append(entry_dict)
        entry_dict: dict = {'Weapon Name': 'Gas Streamer',                      'Drop-Down Name': 'Gas Streamer - Tear Gas',                           'Ammo Type': 'Tear Gas',                    'Abbv': 'GS w/Tear Gas',               'Effect': '1/2 inchx5',          'To-Hit': '0',      'Dam': '*',                  'DP': '1',  'Cost': '100',    'Weight': '50',   'Space': '1',            'Shots': '2',  'Shot Cost': '100',   'Shot Weight': '25'    ,'Loaded Cost': '300',    'Loaded Weight': '100',  'Mag Cost': '250',   'Mag Weight': '65'}
        self.weapons_dropped_gas_list.append(entry_dict)
        entry_dict: dict = {'Weapon Name': '*Gas Streamer',                     'Drop-Down Name': '*Gas Streamer - Toxin Gas',                         'Ammo Type': 'Toxin Gas',                   'Abbv': 'GS w/Toxin Gas',              'Effect': '1/2 inchx5',          'To-Hit': '0',      'Dam': '*',                  'DP': '1',  'Cost': '100',    'Weight': '50',   'Space': '1',            'Shots': '2',  'Shot Cost': '10000', 'Shot Weight': '25'    ,'Loaded Cost': '20100',  'Loaded Weight': '100',  'Mag Cost': '20050', 'Mag Weight': '65'}
        self.weapons_dropped_gas_list.append(entry_dict)
        entry_dict: dict = {'Weapon Name': 'Flame Cloud Ejector',               'Drop-Down Name': 'Flame Cloud Ejector',                               'Ammo Type': 'Normal',                      'Abbv': 'FCE',                         'Effect': '1/2 inchx1',          'To-Hit': '0',      'Dam': '1D-1 (3/1)',         'DP': '1',  'Cost': '500',    'Weight': '50',   'Space': '2',            'Shots': '10', 'Shot Cost': '60',    'Shot Weight': '5'     ,'Loaded Cost': '1100',   'Loaded Weight': '100',  'Mag Cost': '650',   'Mag Weight': '65'}
        self.weapons_dropped_gas_list.append(entry_dict)
        entry_dict: dict = {'Weapon Name': 'Flame Cloud Streamer',              'Drop-Down Name': 'Flame Cloud Streamer',                              'Ammo Type': 'Normal',                      'Abbv': 'FCGS',                        'Effect': '1/2 inchx5',          'To-Hit': '0',      'Dam': '1D-1 (3/1)',         'DP': '1',  'Cost': '200',    'Weight': '100',  'Space': '2',            'Shots': '2',  'Shot Cost': '300',   'Shot Weight': '25'    ,'Loaded Cost': '800',    'Loaded Weight': '150',  'Mag Cost': '650',   'Mag Weight': '65'}
        self.weapons_dropped_gas_list.append(entry_dict)
        entry_dict: dict = {'Weapon Name': 'Cloud Bomb',                        'Drop-Down Name': 'Cloud Bomb',                                        'Ammo Type': 'Normal',                      'Abbv': 'CBSS',                        'Effect': '2 inch Radius',       'To-Hit': '6',      'Dam': '*',                  'DP': '1',  'Cost': '1000',   'Weight': '100',  'Space': '1',            'Shots': '1',  'Shot Cost': '0',     'Shot Weight': '0'     ,'Loaded Cost': '1000',   'Loaded Weight': '100',  'Mag Cost': '0',     'Mag Weight': '0'}
        self.weapons_dropped_gas_list.append(entry_dict)
        entry_dict: dict = {'Weapon Name': '*Toxin Gas',                        'Drop-Down Name': '*Toxin Gas',                                        'Ammo Type': 'Normal',                      'Abbv': 'TXG',                         'Effect': '1/2 inchx1',          'To-Hit': '0',      'Dam': '*',                  'DP': '3',  'Cost': '500',    'Weight': '25',   'Space': '1',            'Shots': '10', 'Shot Cost': '2000',  'Shot Weight': '5'     ,'Loaded Cost': '20500',  'Loaded Weight': '75',   'Mag Cost': '20050', 'Mag Weight': '65'}
        self.weapons_dropped_gas_list.append(entry_dict)
        entry_dict: dict = {'Weapon Name': '*Toxic Gas',                        'Drop-Down Name': '*Toxic Gas - Super Acid',                           'Ammo Type': 'Super Acid',                  'Abbv': 'TXG',                         'Effect': '1/2 inchx1',          'To-Hit': '0',      'Dam': '*',                  'DP': '3',  'Cost': '500',    'Weight': '25',   'Space': '1',            'Shots': '10', 'Shot Cost': '2000',  'Shot Weight': '5'     ,'Loaded Cost': '20500',  'Loaded Weight': '75',   'Mag Cost': '20500', 'Mag Weight': '65'}
        self.weapons_dropped_gas_list.append(entry_dict)
        entry_dict: dict = {'Weapon Name': 'HD Smokescreen',                    'Drop-Down Name': 'HD Smokescreen',                                    'Ammo Type': 'Normal',                      'Abbv': 'HDSS',                        'Effect': '1x2',                 'To-Hit': '0',      'Dam': '0',                  'DP': '4',  'Cost': '500',    'Weight': '50',   'Space': '2',            'Shots': '10', 'Shot Cost': '40',    'Shot Weight': '20'    ,'Loaded Cost': '900',    'Loaded Weight': '250',  'Mag Cost': '450',   'Mag Weight': '215'}
        self.weapons_dropped_gas_list.append(entry_dict)
        entry_dict: dict = {'Weapon Name': 'HD Smokescreen',                    'Drop-Down Name': 'HD Smokescreen - Hot Smoke',                        'Ammo Type': 'Hot Smoke',                   'Abbv': 'HDSS w/ Hot',                 'Effect': '1x2',                 'To-Hit': '0',      'Dam': '0',                  'DP': '4',  'Cost': '500',    'Weight': '50',   'Space': '2',            'Shots': '10', 'Shot Cost': '60',    'Shot Weight': '20'    ,'Loaded Cost': '1100',   'Loaded Weight': '250',  'Mag Cost': '650',   'Mag Weight': '215'}
        self.weapons_dropped_gas_list.append(entry_dict)
        entry_dict: dict = {'Weapon Name': 'HD Smokescreen',                    'Drop-Down Name': 'HD Smokescreen - Tear Gas',                         'Ammo Type': 'Tear Gas',                    'Abbv': 'HDSS w/Tear Gas',             'Effect': '1x2',                 'To-Hit': '0',      'Dam': '*',                  'DP': '4',  'Cost': '500',    'Weight': '50',   'Space': '2',            'Shots': '10', 'Shot Cost': '80',    'Shot Weight': '20'    ,'Loaded Cost': '1300',   'Loaded Weight': '250',  'Mag Cost': '850',   'Mag Weight': '215'}
        self.weapons_dropped_gas_list.append(entry_dict)
        entry_dict: dict = {'Weapon Name': 'HD Paint Spray',                    'Drop-Down Name': 'HD Paint Spray',                                    'Ammo Type': 'Normal',                      'Abbv': 'HDPS',                        'Effect': '1x2',                 'To-Hit': '0',      'Dam': '0',                  'DP': '3',  'Cost': '800',    'Weight': '50',   'Space': '2',            'Shots': '10', 'Shot Cost': '40',    'Shot Weight': '8'     ,'Loaded Cost': '1200',   'Loaded Weight': '130',  'Mag Cost': '450',   'Mag Weight': '95'}
        self.weapons_dropped_gas_list.append(entry_dict)
        entry_dict: dict = {'Weapon Name': 'HD Paint Spray',                    'Drop-Down Name': 'HD Paint Spray - StickyFoam Neutralizer',           'Ammo Type': 'StickyFoam Neutralizer',      'Abbv': 'HDPS w/SF Neut',              'Effect': '1x2',                 'To-Hit': '0',      'Dam': '0',                  'DP': '3',  'Cost': '800',    'Weight': '50',   'Space': '2',            'Shots': '10', 'Shot Cost': '200',   'Shot Weight': '8'     ,'Loaded Cost': '2800',   'Loaded Weight': '130',  'Mag Cost': '2050',  'Mag Weight': '95'}
        self.weapons_dropped_gas_list.append(entry_dict)
        entry_dict: dict = {'Weapon Name': 'HD Flame Cloud Ejector',            'Drop-Down Name': 'HD Flame Cloud Ejector',                            'Ammo Type': 'Normal',                      'Abbv': 'HDFCE',                       'Effect': '1x2',                 'To-Hit': '0',      'Dam': '1D-1 (3/1)',         'DP': '2',  'Cost': '1000',   'Weight': '100',  'Space': '3',            'Shots': '10', 'Shot Cost': '240',   'Shot Weight': '20'    ,'Loaded Cost': '3400',   'Loaded Weight': '300',  'Mag Cost': '2450',  'Mag Weight': '215'}
        self.weapons_dropped_gas_list.append(entry_dict)
        entry_dict: dict = {'Weapon Name': '*HD Toxin Gas Ejector',             'Drop-Down Name': '*HD Toxin Gas Ejector',                             'Ammo Type': 'Normal',                      'Abbv': 'HDTXG',                       'Effect': '1x2',                 'To-Hit': '0',      'Dam': '*',                  'DP': '3',  'Cost': '1000',   'Weight': '50',   'Space': '2',            'Shots': '10', 'Shot Cost': '8000',  'Shot Weight': '20'    ,'Loaded Cost': '81000',  'Loaded Weight': '250',  'Mag Cost': '80050', 'Mag Weight': '215'}
        self.weapons_dropped_gas_list.append(entry_dict)
        entry_dict: dict = {'Weapon Name': '*HD Toxin Gas Ejector',             'Drop-Down Name': '*HD Toxin Gas Ejector - Super Acid',                'Ammo Type': 'Super Acid',                  'Abbv': 'HDTXG',                       'Effect': '1x2',                 'To-Hit': '0',      'Dam': '*',                  'DP': '3',  'Cost': '1000',   'Weight': '50',   'Space': '2',            'Shots': '10', 'Shot Cost': '8000',  'Shot Weight': '20'    ,'Loaded Cost': '81000',  'Loaded Weight': '250',  'Mag Cost': '80050', 'Mag Weight': '215'}
        self.weapons_dropped_gas_list.append(entry_dict)
        entry_dict: dict = {'Weapon Name': '',                                  'Drop-Down Name': 'DROPPED LIQUIDS',                                   'Ammo Type': '',                            'Abbv': '',                            'Effect': '',                    'To-Hit': '',       'Dam': '',                   'DP': '',   'Cost': '0',      'Weight': '0',     'Space': '0',             'Shots': '',   'Shot Cost': '',      'Shot Weight': ''      ,'Loaded Cost': '',       'Loaded Weight': '',     'Mag Cost': '',      'Mag Weight': ''}
        self.weapons_dropped_liquid_list.append(entry_dict)
        entry_dict: dict = {'Weapon Name': 'StickyFoam Sprayer',                'Drop-Down Name': 'StickyFoam Sprayer',                                'Ammo Type': 'Normal',                      'Abbv': 'SfS',                         'Effect': '1x1/2 inch',          'To-Hit': '0',      'Dam': '*',                  'DP': '3',  'Cost': '750',    'Weight': '25',   'Space': '2',            'Shots': '25', 'Shot Cost': '30',    'Shot Weight': '2'     ,'Loaded Cost': '1500',   'Loaded Weight': '75',   'Mag Cost': '350',   'Mag Weight': '65'}
        self.weapons_dropped_liquid_list.append(entry_dict)
        entry_dict: dict = {'Weapon Name': 'Oil Jet',                           'Drop-Down Name': 'Oil Jet',                                           'Ammo Type': 'Normal',                      'Abbv': 'OJ',                          'Effect': '1/2 inchx1',          'To-Hit': '0',      'Dam': '0',                  'DP': '3',  'Cost': '250',    'Weight': '25',   'Space': '2',            'Shots': '25', 'Shot Cost': '10',    'Shot Weight': '2'     ,'Loaded Cost': '500',    'Loaded Weight': '75',   'Mag Cost': '300',   'Mag Weight': '65'}
        self.weapons_dropped_liquid_list.append(entry_dict)
        entry_dict: dict = {'Weapon Name': 'Oil Jet',                           'Drop-Down Name': 'Oil Jet - Pyrophoric',                              'Ammo Type': 'Pyrophoric',                  'Abbv': 'POJ',                         'Effect': '1/2 inchx1',          'To-Hit': '0',      'Dam': '1D-2 (3/2)',         'DP': '3',  'Cost': '250',    'Weight': '25',   'Space': '2',            'Shots': '25', 'Shot Cost': '50',    'Shot Weight': '2'     ,'Loaded Cost': '1500',   'Loaded Weight': '75',   'Mag Cost': '1300',  'Mag Weight': '65'}
        self.weapons_dropped_liquid_list.append(entry_dict)
        entry_dict: dict = {'Weapon Name': 'HD Oil Jet',                        'Drop-Down Name': 'HD Oil Jet',                                        'Ammo Type': 'Normal',                      'Abbv': 'HDOJ',                        'Effect': '1x2',                 'To-Hit': '0',      'Dam': '0',                  'DP': '4',  'Cost': '500',    'Weight': '50',   'Space': '3',            'Shots': '10', 'Shot Cost': '40',    'Shot Weight': '8'     ,'Loaded Cost': '900',    'Loaded Weight': '130',  'Mag Cost': '450',   'Mag Weight': '95'}
        self.weapons_dropped_liquid_list.append(entry_dict)
        entry_dict: dict = {'Weapon Name': 'HD Oil Jet',                        'Drop-Down Name': 'HD Oil Jet - Pyrophoric',                           'Ammo Type': 'Pyrophoric',                  'Abbv': 'HDPOJ',                       'Effect': '1x2',                 'To-Hit': '0',      'Dam': '1D-2 (3/2)',         'DP': '4',  'Cost': '500',    'Weight': '50',   'Space': '3',            'Shots': '10', 'Shot Cost': '200',   'Shot Weight': '8'     ,'Loaded Cost': '2500',   'Loaded Weight': '130',  'Mag Cost': '2050',  'Mag Weight': '95'}
        self.weapons_dropped_liquid_list.append(entry_dict)
        entry_dict: dict = {'Weapon Name': 'Flaming Oil Jet',                   'Drop-Down Name': 'Flaming Oil Jet',                                   'Ammo Type': 'Normal',                      'Abbv': 'FOJ',                         'Effect': '1/2 inchx1',          'To-Hit': '0',      'Dam': '1D-2 (3/2)',         'DP': '3',  'Cost': '300',    'Weight': '30',   'Space': '2',            'Shots': '25', 'Shot Cost': '35',    'Shot Weight': '2'     ,'Loaded Cost': '1175',   'Loaded Weight': '80',   'Mag Cost': '925',   'Mag Weight': '65'}
        self.weapons_dropped_liquid_list.append(entry_dict)
        entry_dict: dict = {'Weapon Name': 'Flaming Oil Jet',                   'Drop-Down Name': 'Flaming Oil Jet - High-Temp Fuel',                  'Ammo Type': 'High-Temp Fuel',              'Abbv': 'FOJ-HT',                      'Effect': '1/2 inchx1',          'To-Hit': '0',      'Dam': '1d (4/1)',           'DP': '3',  'Cost': '300',    'Weight': '30',   'Space': '2',            'Shots': '25', 'Shot Cost': '140',   'Shot Weight': '3'     ,'Loaded Cost': '3800',   'Loaded Weight': '105',  'Mag Cost': '3550',  'Mag Weight': '90'}
        self.weapons_dropped_liquid_list.append(entry_dict)
        entry_dict: dict = {'Weapon Name': 'HD Flaming Oil Jet',                'Drop-Down Name': 'HD Flaming Oil Jet',                                'Ammo Type': 'Normal',                      'Abbv': 'HDFOJ',                       'Effect': '1x2',                 'To-Hit': '0',      'Dam': '1D-2 (3/2)',         'DP': '4',  'Cost': '550',    'Weight': '60',   'Space': '3',            'Shots': '10', 'Shot Cost': '140',   'Shot Weight': '8'     ,'Loaded Cost': '1950',   'Loaded Weight': '140',  'Mag Cost': '1450',  'Mag Weight': '95'}
        self.weapons_dropped_liquid_list.append(entry_dict)
        entry_dict: dict = {'Weapon Name': 'HD Flaming Oil Jet',                'Drop-Down Name': 'HD Flaming Oil Jet - High-Temp Fuel',               'Ammo Type': 'High-Temp Fuel',              'Abbv': 'HDFOJ-HT',                    'Effect': '1x2',                 'To-Hit': '0',      'Dam': '1D (4/1)',           'DP': '4',  'Cost': '550',    'Weight': '60',   'Space': '3',            'Shots': '10', 'Shot Cost': '560',   'Shot Weight': '12'    ,'Loaded Cost': '6150',   'Loaded Weight': '180',  'Mag Cost': '5650',  'Mag Weight': '135'}
        self.weapons_dropped_liquid_list.append(entry_dict)
        entry_dict: dict = {'Weapon Name': 'Ice Dropper',                       'Drop-Down Name': 'Ice Dropper',                                       'Ammo Type': 'Normal',                      'Abbv': 'ID',                          'Effect': '1/2 inchx1',          'To-Hit': '0',      'Dam': '0',                  'DP': '3',  'Cost': '750',    'Weight': '50',   'Space': '2',            'Shots': '25', 'Shot Cost': '20',    'Shot Weight': '2'     ,'Loaded Cost': '1250',   'Loaded Weight': '100',  'Mag Cost': '550',   'Mag Weight': '65'}
        self.weapons_dropped_liquid_list.append(entry_dict)
        entry_dict: dict = {'Weapon Name': 'Heavy Duty Ice Dropper',            'Drop-Down Name': 'Heavy Duty Ice Dropper',                            'Ammo Type': 'Normal',                      'Abbv': 'HDID',                        'Effect': '1x2',                 'To-Hit': '0',      'Dam': '0',                  'DP': '4',  'Cost': '1000',   'Weight': '100',  'Space': '3',            'Shots': '10', 'Shot Cost': '100',   'Shot Weight': '10'    ,'Loaded Cost': '2000',   'Loaded Weight': '200',  'Mag Cost': '1050',  'Mag Weight': '115'}
        self.weapons_dropped_liquid_list.append(entry_dict)
        entry_dict: dict = {'Weapon Name': '',                                  'Drop-Down Name': 'DROPPED SOLIDS',                                    'Ammo Type': '',                            'Abbv': '',                            'Effect': '',                    'To-Hit': '',       'Dam': '',                   'DP': '',   'Cost': '0',      'Weight': '0',     'Space': '0',             'Shots': '',   'Shot Cost': '',      'Shot Weight': ''      ,'Loaded Cost': '',       'Loaded Weight': '',     'Mag Cost': '',      'Mag Weight': ''}
        self.weapons_dropped_solid_list.append(entry_dict)
        entry_dict: dict = {'Weapon Name': 'Chaff Dispenser',                   'Drop-Down Name': 'Chaff Dispenser',                                   'Ammo Type': 'Normal',                      'Abbv': 'CD',                          'Effect': '1/2 inchx1',          'To-Hit': '0',      'Dam': '0',                  'DP': '2',  'Cost': '300',    'Weight': '25',   'Space': '1',            'Shots': '10', 'Shot Cost': '10',    'Shot Weight': '2'     ,'Loaded Cost': '400',    'Loaded Weight': '45',   'Mag Cost': '150',   'Mag Weight': '35'}
        self.weapons_dropped_solid_list.append(entry_dict)
        entry_dict: dict = {'Weapon Name': 'HD Chaff Dispenser',                'Drop-Down Name': 'HD Chaff Dispenser',                                'Ammo Type': 'Normal',                      'Abbv': 'HDCD',                        'Effect': '1x2',                 'To-Hit': '0',      'Dam': '0',                  'DP': '2',  'Cost': '600',    'Weight': '50',   'Space': '2',            'Shots': '10', 'Shot Cost': '40',    'Shot Weight': '8'     ,'Loaded Cost': '1000',   'Loaded Weight': '130',  'Mag Cost': '450',   'Mag Weight': '95'}
        self.weapons_dropped_solid_list.append(entry_dict)
        entry_dict: dict = {'Weapon Name': 'Depth Charge',                      'Drop-Down Name': 'Depth Charge',                                      'Ammo Type': 'Normal',                      'Abbv': 'DC',                          'Effect': '*',                   'To-Hit': '0',      'Dam': '1D+3*',              'DP': '5',  'Cost': '250',    'Weight': '100',  'Space': '1',            'Shots': '1',  'Shot Cost': '0',     'Shot Weight': '0'     ,'Loaded Cost': '250',    'Loaded Weight': '100',  'Mag Cost': '0',     'Mag Weight': '0'}
        self.weapons_dropped_solid_list.append(entry_dict)
        entry_dict: dict = {'Weapon Name': 'Large Depth Charge',                'Drop-Down Name': 'Large Depth Charge',                                'Ammo Type': 'Normal',                      'Abbv': 'LDC',                         'Effect': '*',                   'To-Hit': '0',      'Dam': '10D*',               'DP': '8',  'Cost': '500',    'Weight': '250',  'Space': '2',            'Shots': '1',  'Shot Cost': '0',     'Shot Weight': '0'     ,'Loaded Cost': '500',    'Loaded Weight': '250',  'Mag Cost': '0',     'Mag Weight': '0'}
        self.weapons_dropped_solid_list.append(entry_dict)
        entry_dict: dict = {'Weapon Name': 'Spike Dropper',                     'Drop-Down Name': 'Spike Dropper',                                     'Ammo Type': 'Normal',                      'Abbv': 'SD',                          'Effect': '1/2 inchx1/2 inch',   'To-Hit': '0',      'Dam': '1D',                 'DP': '4',  'Cost': '100',    'Weight': '25',   'Space': '1',            'Shots': '10', 'Shot Cost': '20',    'Shot Weight': '5'     ,'Loaded Cost': '300',    'Loaded Weight': '75',   'Mag Cost': '250',   'Mag Weight': '65'}
        self.weapons_dropped_solid_list.append(entry_dict)
        entry_dict: dict = {'Weapon Name': 'Spike Dropper',                     'Drop-Down Name': 'Spike Dropper - Catalytic Spikes',                  'Ammo Type': 'Catalytic Spikes',            'Abbv': 'SD',                          'Effect': '1/2 inchx1/2 inch',   'To-Hit': '0',      'Dam': '1d*',                'DP': '4',  'Cost': '100',    'Weight': '25',   'Space': '1',            'Shots': '10', 'Shot Cost': '60',    'Shot Weight': '5'     ,'Loaded Cost': '700',    'Loaded Weight': '75',   'Mag Cost': '650',   'Mag Weight': '65'}
        self.weapons_dropped_solid_list.append(entry_dict)
        entry_dict: dict = {'Weapon Name': 'Spike Dropper',                     'Drop-Down Name': 'Spike Dropper - Crystal Spikes',                    'Ammo Type': 'Crystal Spikes',              'Abbv': 'SD',                          'Effect': '1/2 inchx1/2 inch',   'To-Hit': '0',      'Dam': '1D',                 'DP': '4',  'Cost': '100',    'Weight': '25',   'Space': '1',            'Shots': '10', 'Shot Cost': '30',    'Shot Weight': '4'     ,'Loaded Cost': '400',    'Loaded Weight': '65',   'Mag Cost': '350',   'Mag Weight': '45'}
        self.weapons_dropped_solid_list.append(entry_dict)
        entry_dict: dict = {'Weapon Name': 'Spike Dropper',                     'Drop-Down Name': 'Spike Dropper - Explosive Spikes',                  'Ammo Type': 'Explosive Spikes',            'Abbv': 'SD,EXP',                      'Effect': '1/2 inchx1/2 inch',   'To-Hit': '0',      'Dam': '1d+1(1d-1)',         'DP': '4',  'Cost': '100',    'Weight': '25',   'Space': '1',            'Shots': '10', 'Shot Cost': '50',    'Shot Weight': '5'     ,'Loaded Cost': '600',    'Loaded Weight': '75',   'Mag Cost': '550',   'Mag Weight': '65'}
        self.weapons_dropped_solid_list.append(entry_dict)
        entry_dict: dict = {'Weapon Name': 'Spike Dropper',                     'Drop-Down Name': 'Spike Dropper - Incendiary Spikes',                 'Ammo Type': 'Incendiary Spikes',           'Abbv': 'SD,INC',                      'Effect': '1/2 inchx1/2 inch',   'To-Hit': '0',      'Dam': '1d-1* (2/2)',        'DP': '4',  'Cost': '100',    'Weight': '25',   'Space': '1',            'Shots': '10', 'Shot Cost': '50',    'Shot Weight': '5'     ,'Loaded Cost': '600',    'Loaded Weight': '75',   'Mag Cost': '550',   'Mag Weight': '65'}
        self.weapons_dropped_solid_list.append(entry_dict)
        entry_dict: dict = {'Weapon Name': 'Drop-Spike Plate',                  'Drop-Down Name': 'Drop-Spike Plate',                                  'Ammo Type': 'Normal',                      'Abbv': 'DSP',                         'Effect': '1/2 inchx1/2 inch',   'To-Hit': '0',      'Dam': '2d(1d)',             'DP': '4',  'Cost': '200',    'Weight': '50',   'Space': '1',            'Shots': '1',  'Shot Cost': '0',     'Shot Weight': '0'     ,'Loaded Cost': '200',    'Loaded Weight': '50',   'Mag Cost': '0',     'Mag Weight': '0'}
        self.weapons_dropped_solid_list.append(entry_dict)
        entry_dict: dict = {'Weapon Name': 'Drop-Spike Plate',                  'Drop-Down Name': 'Drop-Spike Plate - Radio',                          'Ammo Type': 'Radio',                       'Abbv': 'RDSP',                        'Effect': '1/2 inchx1/2 inch',   'To-Hit': '0',      'Dam': '2d(1d)',             'DP': '4',  'Cost': '400',    'Weight': '50',   'Space': '1',            'Shots': '1',  'Shot Cost': '0',     'Shot Weight': '0'     ,'Loaded Cost': '200',    'Loaded Weight': '50',   'Mag Cost': '0',     'Mag Weight': '0'}
        self.weapons_dropped_solid_list.append(entry_dict)
        entry_dict: dict = {'Weapon Name': 'Large Drop-Spike Plate',            'Drop-Down Name': 'Large Drop-Spike Plate',                            'Ammo Type': 'Normal',                      'Abbv': 'LDSP',                        'Effect': '1/2 inchx1',          'To-Hit': '0',      'Dam': '2d(1d)',             'DP': '6',  'Cost': '350',    'Weight': '100',  'Space': '1',            'Shots': '1',  'Shot Cost': '0',     'Shot Weight': '0'     ,'Loaded Cost': '350',    'Loaded Weight': '100',  'Mag Cost': '0',     'Mag Weight': '0'}
        self.weapons_dropped_solid_list.append(entry_dict)
        entry_dict: dict = {'Weapon Name': 'Large Drop-Spike Plate',            'Drop-Down Name': 'Large Drop-Spike Plate - Radio',                    'Ammo Type': 'Radio',                       'Abbv': 'RLDSP',                       'Effect': '1/2 inchx1',          'To-Hit': '0',      'Dam': '2d(1d)',             'DP': '6',  'Cost': '700',    'Weight': '100',  'Space': '1',            'Shots': '1',  'Shot Cost': '0',     'Shot Weight': '0'     ,'Loaded Cost': '350',    'Loaded Weight': '100',  'Mag Cost': '0',     'Mag Weight': '0'}
        self.weapons_dropped_solid_list.append(entry_dict)
        entry_dict: dict = {'Weapon Name': 'Fake Drop Spike Plate',             'Drop-Down Name': 'Fake Drop Spike Plate',                             'Ammo Type': 'Normal',                      'Abbv': 'FDSP',                        'Effect': '1/2 inchx1/2 inch',   'To-Hit': '0',      'Dam': '0',                  'DP': '1',  'Cost': '50',     'Weight': '10',   'Space': '1',            'Shots': '1',  'Shot Cost': '0',     'Shot Weight': '0'     ,'Loaded Cost': '50',     'Loaded Weight': '10',   'Mag Cost': '0',     'Mag Weight': '0'}
        self.weapons_dropped_solid_list.append(entry_dict)
        entry_dict: dict = {'Weapon Name': 'Fake Drop Spike Plate',             'Drop-Down Name': 'Fake Drop Spike Plate - Large',                     'Ammo Type': 'Large',                       'Abbv': 'FLDSP',                       'Effect': '1/2 inchx1',          'To-Hit': '0',      'Dam': '0',                  'DP': '1',  'Cost': '75',     'Weight': '10',   'Space': '1',            'Shots': '1',  'Shot Cost': '0',     'Shot Weight': '0'     ,'Loaded Cost': '75',     'Loaded Weight': '10',   'Mag Cost': '0',     'Mag Weight': '0'}
        self.weapons_dropped_solid_list.append(entry_dict)
        entry_dict: dict = {'Weapon Name': 'Junk Dropper',                      'Drop-Down Name': 'Junk Dropper',                                      'Ammo Type': 'Normal',                      'Abbv': 'JD',                          'Effect': '1/2 inchx1/2 inch',   'To-Hit': '0',      'Dam': '1d-3',               'DP': '4',  'Cost': '50',     'Weight': '25',   'Space': '1',            'Shots': '10', 'Shot Cost': '0',     'Shot Weight': '10'    ,'Loaded Cost': '50',     'Loaded Weight': '125',  'Mag Cost': '50',    'Mag Weight': '115'}
        self.weapons_dropped_solid_list.append(entry_dict)
        entry_dict: dict = {'Weapon Name': 'Junk Dropper',                      'Drop-Down Name': 'Junk Dropper - Sand Ammo',                          'Ammo Type': 'Sand Ammo',                   'Abbv': 'JD-S',                        'Effect': '1/2 inchx1',          'To-Hit': '0',      'Dam': '',                   'DP': '4',  'Cost': '50',     'Weight': '25',   'Space': '1',            'Shots': '10', 'Shot Cost': '0',     'Shot Weight': '10'    ,'Loaded Cost': '50',     'Loaded Weight': '125',  'Mag Cost': '50',    'Mag Weight': '115'}
        self.weapons_dropped_solid_list.append(entry_dict)
        entry_dict: dict = {'Weapon Name': '',                                  'Drop-Down Name': 'MINEDROPPERS',                                      'Ammo Type': '',                            'Abbv': '',                            'Effect': '',                    'To-Hit': '',       'Dam': '',                   'DP': '',   'Cost': '0',      'Weight': '0',     'Space': '0',             'Shots': '',   'Shot Cost': '',      'Shot Weight': ''      ,'Loaded Cost': '',       'Loaded Weight': '',     'Mag Cost': '',      'Mag Weight': ''}
        self.weapons_minedroppers_list.append(entry_dict)
        entry_dict: dict = {'Weapon Name': 'Minedropper',                       'Drop-Down Name': 'Minedropper',                                       'Ammo Type': 'Normal',                      'Abbv': 'MD',                          'Effect': '1/2 inchx1/2 inch',   'To-Hit': '0',      'Dam': '1d/2d',              'DP': '2',  'Cost': '500',    'Weight': '150',  'Space': '2',            'Shots': '10', 'Shot Cost': '50',    'Shot Weight': '5'     ,'Loaded Cost': '1000',   'Loaded Weight': '200',  'Mag Cost': '550',   'Mag Weight': '65'}
        self.weapons_minedroppers_list.append(entry_dict)
        entry_dict: dict = {'Weapon Name': 'Minedropper',                       'Drop-Down Name': 'Minedropper - Anti-Ped',                            'Ammo Type': 'Anti-Ped',                    'Abbv': 'MD, Anti-Ped',                'Effect': '1 inch Radius',       'To-Hit': '0',      'Dam': '2d/1d/0',            'DP': '2',  'Cost': '500',    'Weight': '150',  'Space': '2',            'Shots': '10', 'Shot Cost': '25',    'Shot Weight': '3'     ,'Loaded Cost': '750',    'Loaded Weight': '180',  'Mag Cost': '300',   'Mag Weight': '45'}
        self.weapons_minedroppers_list.append(entry_dict)
        entry_dict: dict = {'Weapon Name': 'Minedropper',                       'Drop-Down Name': 'Minedropper - Beacon',                              'Ammo Type': 'Beacon',                      'Abbv': 'MD, Beacon',                  'Effect': '1 x 1',               'To-Hit': '0',      'Dam': '0',                  'DP': '2',  'Cost': '500',    'Weight': '150',  'Space': '2',            'Shots': '10', 'Shot Cost': '200',   'Shot Weight': '5'     ,'Loaded Cost': '2500',   'Loaded Weight': '200',  'Mag Cost': '2050',  'Mag Weight': '65'}
        self.weapons_minedroppers_list.append(entry_dict)
        entry_dict: dict = {'Weapon Name': 'Minedropper',                       'Drop-Down Name': 'Minedropper - Smoke',                               'Ammo Type': 'Smoke',                       'Abbv': 'MD, Smoke',                   'Effect': '1 x 1',               'To-Hit': '0',      'Dam': '0',                  'DP': '2',  'Cost': '500',    'Weight': '150',  'Space': '2',            'Shots': '10', 'Shot Cost': '45',    'Shot Weight': '5'     ,'Loaded Cost': '950',    'Loaded Weight': '200',  'Mag Cost': '500',   'Mag Weight': '65'}
        self.weapons_minedroppers_list.append(entry_dict)
        entry_dict: dict = {'Weapon Name': 'Minedropper',                       'Drop-Down Name': 'Minedropper - Hot Smoke',                           'Ammo Type': 'Hot Smoke',                   'Abbv': 'MD, Hot Smoke',               'Effect': '1 x 1',               'To-Hit': '0',      'Dam': '0',                  'DP': '2',  'Cost': '500',    'Weight': '150',  'Space': '2',            'Shots': '10', 'Shot Cost': '55',    'Shot Weight': '5'     ,'Loaded Cost': '1050',   'Loaded Weight': '200',  'Mag Cost': '600',   'Mag Weight': '65'}
        self.weapons_minedroppers_list.append(entry_dict)
        entry_dict: dict = {'Weapon Name': 'Minedropper',                       'Drop-Down Name': 'Minedropper - Paint',                               'Ammo Type': 'Paint',                       'Abbv': 'MD, Paint',                   'Effect': '1 x 1',               'To-Hit': '0',      'Dam': '0',                  'DP': '2',  'Cost': '500',    'Weight': '150',  'Space': '2',            'Shots': '10', 'Shot Cost': '45',    'Shot Weight': '5'     ,'Loaded Cost': '950',    'Loaded Weight': '200',  'Mag Cost': '500',   'Mag Weight': '65'}
        self.weapons_minedroppers_list.append(entry_dict)
        entry_dict: dict = {'Weapon Name': 'Minedropper',                       'Drop-Down Name': 'Minedropper - Paint, Glow-in-the-dark',             'Ammo Type': 'Paint, Glow-in-the-dark',     'Abbv': 'MD, Paint, Glow-in-the-dark', 'Effect': '1 x 1',               'To-Hit': '0',      'Dam': '0',                  'DP': '2',  'Cost': '500',    'Weight': '150',  'Space': '2',            'Shots': '10', 'Shot Cost': '105',   'Shot Weight': '5'     ,'Loaded Cost': '1550',   'Loaded Weight': '200',  'Mag Cost': '1100',  'Mag Weight': '65'}
        self.weapons_minedroppers_list.append(entry_dict)
        entry_dict: dict = {'Weapon Name': 'Minedropper',                       'Drop-Down Name': 'Minedropper - Flame Cloud',                         'Ammo Type': 'Flame Cloud',                 'Abbv': 'MD, Flame Cloud',             'Effect': '1 x 1',               'To-Hit': '0',      'Dam': '1d-1 (3/1)',         'DP': '2',  'Cost': '500',    'Weight': '150',  'Space': '2',            'Shots': '10', 'Shot Cost': '145',   'Shot Weight': '5'     ,'Loaded Cost': '1950',   'Loaded Weight': '200',  'Mag Cost': '1500',  'Mag Weight': '65'}
        self.weapons_minedroppers_list.append(entry_dict)
        entry_dict: dict = {'Weapon Name': 'Minedropper',                       'Drop-Down Name': 'Minedropper - StickyFoam Neutralizer',              'Ammo Type': 'StickyFoam Neutralizer',      'Abbv': 'MD, SF Neut.',                'Effect': '1 x 1',               'To-Hit': '0',      'Dam': '*',                  'DP': '2',  'Cost': '500',    'Weight': '150',  'Space': '2',            'Shots': '10', 'Shot Cost': '250',   'Shot Weight': '5'     ,'Loaded Cost': '3000',   'Loaded Weight': '200',  'Mag Cost': '2550',  'Mag Weight': '65'}
        self.weapons_minedroppers_list.append(entry_dict)
        entry_dict: dict = {'Weapon Name': 'Minedropper',                       'Drop-Down Name': 'Minedropper - Tear Gas',                            'Ammo Type': 'Tear Gas',                    'Abbv': 'MD, Tear Gas',                'Effect': '1 x 1',               'To-Hit': '0',      'Dam': '0',                  'DP': '2',  'Cost': '500',    'Weight': '150',  'Space': '2',            'Shots': '10', 'Shot Cost': '65',    'Shot Weight': '5'     ,'Loaded Cost': '1150',   'Loaded Weight': '200',  'Mag Cost': '700',   'Mag Weight': '65'}
        self.weapons_minedroppers_list.append(entry_dict)
        entry_dict: dict = {'Weapon Name': '*Minedropper',                      'Drop-Down Name': '*Minedropper - Toxin Gas',                          'Ammo Type': 'Toxin Gas',                   'Abbv': 'MD, Toxin Gas',               'Effect': '1 x 1',               'To-Hit': '0',      'Dam': '0',                  'DP': '2',  'Cost': '500',    'Weight': '150',  'Space': '2',            'Shots': '10', 'Shot Cost': '4025',  'Shot Weight': '5'     ,'Loaded Cost': '40750',  'Loaded Weight': '200',  'Mag Cost': '40300', 'Mag Weight': '65'}
        self.weapons_minedroppers_list.append(entry_dict)
        entry_dict: dict = {'Weapon Name': 'Minedropper',                       'Drop-Down Name': 'Minedropper - Fake Mines',                          'Ammo Type': 'Fake Mines',                  'Abbv': 'MD, Fake Mines',              'Effect': '0',                   'To-Hit': '0',      'Dam': '0',                  'DP': '2',  'Cost': '500',    'Weight': '150',  'Space': '2',            'Shots': '10', 'Shot Cost': '10',    'Shot Weight': '5'     ,'Loaded Cost': '600',    'Loaded Weight': '200',  'Mag Cost': '150',   'Mag Weight': '65'}
        self.weapons_minedroppers_list.append(entry_dict)
        entry_dict: dict = {'Weapon Name': 'Minedropper',                       'Drop-Down Name': 'Minedropper - Floating',                            'Ammo Type': 'Floating',                    'Abbv': 'MD, Floating',                'Effect': '1/2 inchx1/2 inch',   'To-Hit': '0',      'Dam': '1d*',                'DP': '2',  'Cost': '500',    'Weight': '150',  'Space': '2',            'Shots': '10', 'Shot Cost': '120',   'Shot Weight': '5'     ,'Loaded Cost': '1700',   'Loaded Weight': '200',  'Mag Cost': '1750',  'Mag Weight': '215'}
        self.weapons_minedroppers_list.append(entry_dict)
        entry_dict: dict = {'Weapon Name': 'Minedropper',                       'Drop-Down Name': 'Minedropper - Napalm',                              'Ammo Type': 'Napalm',                      'Abbv': 'MD, Napalm',                  'Effect': '1/2 inchx1/2 inch',   'To-Hit': '0',      'Dam': '1d* (4/3)',          'DP': '2',  'Cost': '500',    'Weight': '150',  'Space': '2',            'Shots': '10', 'Shot Cost': '60',    'Shot Weight': '5'     ,'Loaded Cost': '1100',   'Loaded Weight': '200',  'Mag Cost': '1150',  'Mag Weight': '215'}
        self.weapons_minedroppers_list.append(entry_dict)
        entry_dict: dict = {'Weapon Name': 'Spear 1000 MD',                     'Drop-Down Name': 'Spear 1000 MD',                                     'Ammo Type': 'Normal',                      'Abbv': 'SMD',                         'Effect': '1/2 inchx1/2 inch',   'To-Hit': '0',      'Dam': '1d-3/2d+3',          'DP': '2',  'Cost': '750',    'Weight': '150',  'Space': '2',            'Shots': '5',  'Shot Cost': '100',   'Shot Weight': '10'    ,'Loaded Cost': '1250',   'Loaded Weight': '200',  'Mag Cost': '550',   'Mag Weight': '65'}
        self.weapons_minedroppers_list.append(entry_dict)
        entry_dict: dict = {'Weapon Name': 'Spear 1000 MD',                     'Drop-Down Name': 'Spear 1000 MD - TDX',                               'Ammo Type': 'TDX',                         'Abbv': 'SMD, TDX',                    'Effect': '1/2 inchx1/2 inch',   'To-Hit': '0',      'Dam': '1d+3/1d-2',          'DP': '2',  'Cost': '750',    'Weight': '150',  'Space': '2',            'Shots': '5',  'Shot Cost': '100',   'Shot Weight': '10'    ,'Loaded Cost': '1250',   'Loaded Weight': '200',  'Mag Cost': '550',   'Mag Weight': '65'}
        self.weapons_minedroppers_list.append(entry_dict)
        entry_dict: dict = {'Weapon Name': 'Spear 1000 MD',                     'Drop-Down Name': 'Spear 1000 MD - Napalm',                            'Ammo Type': 'Napalm',                      'Abbv': 'SMD, Napalm',                 'Effect': '1/2 inchx1/2 inch',   'To-Hit': '0',      'Dam': '1d/2d*',             'DP': '2',  'Cost': '750',    'Weight': '150',  'Space': '2',            'Shots': '5',  'Shot Cost': '150',   'Shot Weight': '10'    ,'Loaded Cost': '1500',   'Loaded Weight': '200',  'Mag Cost': '800',   'Mag Weight': '65'}
        self.weapons_minedroppers_list.append(entry_dict)
        entry_dict: dict = {'Weapon Name': 'Spear 1000 MD',                     'Drop-Down Name': 'Spear 1000 MD - Spider Mine',                       'Ammo Type': 'Spider Mine',                 'Abbv': 'SMD,Spider',                  'Effect': '1/2 inchx1/2 inch',   'To-Hit': '0',      'Dam': '1d/2d',              'DP': '2',  'Cost': '750',    'Weight': '150',  'Space': '2',            'Shots': '5',  'Shot Cost': '150',   'Shot Weight': '10'    ,'Loaded Cost': '1500',   'Loaded Weight': '200',  'Mag Cost': '800',   'Mag Weight': '65'}
        self.weapons_minedroppers_list.append(entry_dict)
        entry_dict: dict = {'Weapon Name': '*Heavy Mine Dropper',               'Drop-Down Name': '*Heavy Mine Dropper',                               'Ammo Type': 'Normal',                      'Abbv': 'HMD',                         'Effect': '1',                   'To-Hit': '0',      'Dam': '3D/2D',              'DP': '3',  'Cost': '1500',   'Weight': '250',  'Space': '4',            'Shots': '10', 'Shot Cost': '200',   'Shot Weight': '20'    ,'Loaded Cost': '3500',   'Loaded Weight': '450',  'Mag Cost': '2050',  'Mag Weight': '215'}
        self.weapons_minedroppers_list.append(entry_dict)
        entry_dict: dict = {'Weapon Name': '*Heavy Mine Dropper',               'Drop-Down Name': '*Heavy Mine Dropper - Spider Mine',                 'Ammo Type': 'Spider Mine',                 'Abbv': 'HMD, Spider',                 'Effect': '1',                   'To-Hit': '0',      'Dam': '2d+1/1d+1',          'DP': '3',  'Cost': '1500',   'Weight': '250',  'Space': '4',            'Shots': '10', 'Shot Cost': '300',   'Shot Weight': '20'    ,'Loaded Cost': '4500',   'Loaded Weight': '450',  'Mag Cost': '3050',  'Mag Weight': '215'}
        self.weapons_minedroppers_list.append(entry_dict)
        entry_dict: dict = {'Weapon Name': '',                                  'Drop-Down Name': 'DISCHARGERS',                                       'Ammo Type': '',                            'Abbv': '',                            'Effect': '',                    'To-Hit': '',       'Dam': '',                   'DP': '',   'Cost': '0',      'Weight': '0',     'Space': '0',             'Shots': '',   'Shot Cost': '',      'Shot Weight': ''      ,'Loaded Cost': '',       'Loaded Weight': '',     'Mag Cost': '',      'Mag Weight': ''}
        self.weapons_dischargers_list.append(entry_dict)
        entry_dict: dict = {'Weapon Name': 'Chaff Discharger',                  'Drop-Down Name': 'Chaff Discharger',                                  'Ammo Type': 'Normal',                      'Abbv': 'ChD',                         'Effect': '1/2 inchx1',          'To-Hit': '0',      'Dam': '0',                  'DP': '0',  'Cost': '50',     'Weight': '5',    'Space': '0',            'Shots': '0',  'Shot Cost': '0',     'Shot Weight': '0'     ,'Loaded Cost': '0',      'Loaded Weight': '0',    'Mag Cost': '0',     'Mag Weight': '0'}
        self.weapons_dischargers_list.append(entry_dict)
        entry_dict: dict = {'Weapon Name': 'Fake Discharger',                   'Drop-Down Name': 'Fake Discharger',                                   'Ammo Type': 'Normal',                      'Abbv': 'FkD',                         'Effect': '0',                   'To-Hit': '0',      'Dam': '0',                  'DP': '0',  'Cost': '5',      'Weight': '5',    'Space': '0',            'Shots': '0',  'Shot Cost': '0',     'Shot Weight': '0'     ,'Loaded Cost': '0',      'Loaded Weight': '0',    'Mag Cost': '0',     'Mag Weight': '0'}
        self.weapons_dischargers_list.append(entry_dict)
        entry_dict: dict = {'Weapon Name': 'Flame Cloud Discharger',            'Drop-Down Name': 'Flame Cloud Discharger',                            'Ammo Type': 'Normal',                      'Abbv': 'FCD',                         'Effect': '1/2 inchx1',          'To-Hit': '0',      'Dam': '1d-1 (3/1)',         'DP': '0',  'Cost': '150',    'Weight': '5',    'Space': '0',            'Shots': '0',  'Shot Cost': '0',     'Shot Weight': '0'     ,'Loaded Cost': '0',      'Loaded Weight': '0',    'Mag Cost': '0',     'Mag Weight': '0'}
        self.weapons_dischargers_list.append(entry_dict)
        entry_dict: dict = {'Weapon Name': 'Flaming Oil Discharger',            'Drop-Down Name': 'Flaming Oil Discharger',                            'Ammo Type': 'Normal',                      'Abbv': 'FOD',                         'Effect': '1/2 inchx1',          'To-Hit': '0',      'Dam': '1d-2 (3/2)',         'DP': '0',  'Cost': '100',    'Weight': '5',    'Space': '0',            'Shots': '0',  'Shot Cost': '0',     'Shot Weight': '0'     ,'Loaded Cost': '0',      'Loaded Weight': '0',    'Mag Cost': '0',     'Mag Weight': '0'}
        self.weapons_dischargers_list.append(entry_dict)
        entry_dict: dict = {'Weapon Name': 'Flechette Discharger',              'Drop-Down Name': 'Flechette Discharger',                              'Ammo Type': 'Normal',                      'Abbv': 'FD',                          'Effect': '1/2 inchx1',          'To-Hit': '0',      'Dam': '0 (1d)',             'DP': '0',  'Cost': '50',     'Weight': '5',    'Space': '0',            'Shots': '0',  'Shot Cost': '0',     'Shot Weight': '0'     ,'Loaded Cost': '0',      'Loaded Weight': '0',    'Mag Cost': '0',     'Mag Weight': '0'}
        self.weapons_dischargers_list.append(entry_dict)
        entry_dict: dict = {'Weapon Name': 'Foam Discharger',                   'Drop-Down Name': 'Foam Discharger',                                   'Ammo Type': 'Normal',                      'Abbv': 'FmD',                         'Effect': '1/2 inchx1/2 inch',   'To-Hit': '0',      'Dam': '*',                  'DP': '0',  'Cost': '25',     'Weight': '5',    'Space': '0',            'Shots': '0',  'Shot Cost': '0',     'Shot Weight': '0'     ,'Loaded Cost': '0',      'Loaded Weight': '0',    'Mag Cost': '0',     'Mag Weight': '0'}
        self.weapons_dischargers_list.append(entry_dict)
        entry_dict: dict = {'Weapon Name': 'Hot Smoke Discharger',              'Drop-Down Name': 'Hot Smoke Discharger',                              'Ammo Type': 'Normal',                      'Abbv': 'HsD',                         'Effect': '1/2 inchx1',          'To-Hit': '0',      'Dam': '0',                  'DP': '0',  'Cost': '65',     'Weight': '5',    'Space': '0',            'Shots': '0',  'Shot Cost': '0',     'Shot Weight': '0'     ,'Loaded Cost': '0',      'Loaded Weight': '0',    'Mag Cost': '0',     'Mag Weight': '0'}
        self.weapons_dischargers_list.append(entry_dict)
        entry_dict: dict = {'Weapon Name': 'Ice Discharger',                    'Drop-Down Name': 'Ice Discharger',                                    'Ammo Type': 'Normal',                      'Abbv': 'IcD',                         'Effect': '1/2 inchx1',          'To-Hit': '0',      'Dam': '',                   'DP': '0',  'Cost': '75',     'Weight': '5',    'Space': '0',            'Shots': '0',  'Shot Cost': '0',     'Shot Weight': '0'     ,'Loaded Cost': '0',      'Loaded Weight': '0',    'Mag Cost': '0',     'Mag Weight': '0'}
        self.weapons_dischargers_list.append(entry_dict)
        entry_dict: dict = {'Weapon Name': 'Oil Dscharger',                     'Drop-Down Name': 'Oil Dscharger',                                     'Ammo Type': 'Normal',                      'Abbv': 'OD',                          'Effect': '1/2 inchx1',          'To-Hit': '0',      'Dam': '',                   'DP': '0',  'Cost': '50',     'Weight': '5',    'Space': '0',            'Shots': '0',  'Shot Cost': '0',     'Shot Weight': '0'     ,'Loaded Cost': '0',      'Loaded Weight': '0',    'Mag Cost': '0',     'Mag Weight': '0'}
        self.weapons_dischargers_list.append(entry_dict)
        entry_dict: dict = {'Weapon Name': 'Paint Discharger',                  'Drop-Down Name': 'Paint Discharger',                                  'Ammo Type': 'Normal',                      'Abbv': 'PD',                          'Effect': '1/2 inchx1',          'To-Hit': '0',      'Dam': '',                   'DP': '0',  'Cost': '40',     'Weight': '5',    'Space': '0',            'Shots': '0',  'Shot Cost': '0',     'Shot Weight': '0'     ,'Loaded Cost': '0',      'Loaded Weight': '0',    'Mag Cost': '0',     'Mag Weight': '0'}
        self.weapons_dischargers_list.append(entry_dict)
        entry_dict: dict = {'Weapon Name': 'Paint Discharger',                  'Drop-Down Name': 'Paint Discharger - Glow-in-the-dark',               'Ammo Type': 'Glow-in-the-dark',            'Abbv': 'PD/glow',                     'Effect': '1/2 inchx1',          'To-Hit': '0',      'Dam': '',                   'DP': '0',  'Cost': '160',    'Weight': '5',    'Space': '0',            'Shots': '0',  'Shot Cost': '0',     'Shot Weight': '0'     ,'Loaded Cost': '0',      'Loaded Weight': '0',    'Mag Cost': '0',     'Mag Weight': '0'}
        self.weapons_dischargers_list.append(entry_dict)
        entry_dict: dict = {'Weapon Name': 'Point-Defense Discharger',          'Drop-Down Name': 'Point-Defense Discharger',                 'Ammo Type': 'Normal',                      'Abbv': 'PDG',                         'Effect': '1 inch Radius',       'To-Hit': '0',      'Dam': '1/2 inch (1d)',      'DP': '0',  'Cost': '100',    'Weight': '5',    'Space': '0',            'Shots': '0',  'Shot Cost': '0',     'Shot Weight': '0'     ,'Loaded Cost': '0',      'Loaded Weight': '0',    'Mag Cost': '0',     'Mag Weight': '0'}
        self.weapons_dischargers_list.append(entry_dict)
        entry_dict: dict = {'Weapon Name': 'Pyrophoric Oil Discharger',         'Drop-Down Name': 'Pyrophoric Oil Discharger',                'Ammo Type': 'Normal',                      'Abbv': 'POD',                         'Effect': '1/2 inchx1',          'To-Hit': '0',      'Dam': '1D-2 (3/2)',         'DP': '0',  'Cost': '250',    'Weight': '5',    'Space': '0',            'Shots': '0',  'Shot Cost': '0',     'Shot Weight': '0'     ,'Loaded Cost': '0',      'Loaded Weight': '0',    'Mag Cost': '0',     'Mag Weight': '0'}
        self.weapons_dischargers_list.append(entry_dict)
        entry_dict: dict = {'Weapon Name': 'Sand Discharger',                   'Drop-Down Name': 'Sand Discharger',                                   'Ammo Type': 'Normal',                      'Abbv': 'SaD',                         'Effect': '1/2 inchx1',          'To-Hit': '0',      'Dam': '0',                  'DP': '0',  'Cost': '25',     'Weight': '5',    'Space': '0',            'Shots': '0',  'Shot Cost': '0',     'Shot Weight': '0'     ,'Loaded Cost': '0',      'Loaded Weight': '0',    'Mag Cost': '0',     'Mag Weight': '0'}
        self.weapons_dischargers_list.append(entry_dict)
        entry_dict: dict = {'Weapon Name': 'Smoke Discharger',                  'Drop-Down Name': 'Smoke Discharger',                                  'Ammo Type': 'Normal',                      'Abbv': 'SkD',                         'Effect': '1/2 inchx1',          'To-Hit': '0',      'Dam': '0',                  'DP': '0',  'Cost': '50',     'Weight': '5',    'Space': '0',            'Shots': '0',  'Shot Cost': '0',     'Shot Weight': '0'     ,'Loaded Cost': '0',      'Loaded Weight': '0',    'Mag Cost': '0',     'Mag Weight': '0'}
        self.weapons_dischargers_list.append(entry_dict)
        entry_dict: dict = {'Weapon Name': 'StickyFoam Discharger',             'Drop-Down Name': 'StickyFoam Discharger',                             'Ammo Type': 'Normal',                      'Abbv': 'SfD',                         'Effect': '1/2 inchx1',          'To-Hit': '0',      'Dam': '0',                  'DP': '0',  'Cost': '75',     'Weight': '5',    'Space': '0',            'Shots': '0',  'Shot Cost': '0',     'Shot Weight': '0'     ,'Loaded Cost': '0',      'Loaded Weight': '0',    'Mag Cost': '0',     'Mag Weight': '0'}
        self.weapons_dischargers_list.append(entry_dict)
        entry_dict: dict = {'Weapon Name': 'StickyFoam Neutralizer Discharger', 'Drop-Down Name': 'StickyFoam Neutralizer Discharger',                 'Ammo Type': 'Normal',                      'Abbv': 'SfND',                        'Effect': '1/2 inchx1',          'To-Hit': '0',      'Dam': '0',                  'DP': '0',  'Cost': '200',    'Weight': '5',    'Space': '0',            'Shots': '0',  'Shot Cost': '0',     'Shot Weight': '0'     ,'Loaded Cost': '0',      'Loaded Weight': '0',    'Mag Cost': '0',     'Mag Weight': '0'}
        self.weapons_dischargers_list.append(entry_dict)
        entry_dict: dict = {'Weapon Name': 'Tear Gas Discharger',               'Drop-Down Name': 'Tear Gas Discharger',                               'Ammo Type': 'Normal',                      'Abbv': 'TGD',                         'Effect': '1/2 inchx1',          'To-Hit': '0',      'Dam': '',                   'DP': '0',  'Cost': '75',     'Weight': '5',    'Space': '0',            'Shots': '0',  'Shot Cost': '0',     'Shot Weight': '0'     ,'Loaded Cost': '0',      'Loaded Weight': '0',    'Mag Cost': '0',     'Mag Weight': '0'}
        self.weapons_dischargers_list.append(entry_dict)

    ######################################################################
    # Weapon Row 1 processing here                                       #
    ######################################################################

    def add_dropdown_weapons(self, canvas_type):
        """
        Master initializer method that automatically builds and grids the category 
        and facing direction dropdown menus for all 10 weapon rows using tight loops.
        """
        # 1. Loop-initialize all 10 primary weapon category dropdown slots
        for row_idx in range(1, self.weapon_rows_count + 1):
            self.add_dropdown_weapon_alt_unified(row_idx, canvas_type=canvas_type)

        # 2. Loop-initialize all 10 armor facing direction dropdown slots
        for row_idx in range(1, self.weapon_rows_count + 1):
            # Dynamically fetch the correct grid row tracking coordinate for this slot
            row_attr_name = f"grid_row_sub_weapon_alt_{row_idx}"
            target_grid_row = getattr(self, row_attr_name) if hasattr(self, row_attr_name) else row_idx
            
            # Dynamically execute your existing add_weapon_facing_dropdown function
            facing_var, facing_dropdown = self.add_weapon_facing_dropdown(
                canvas_type=canvas_type,
                column_val=self.grid_col_test_track,
                row_val=target_grid_row
            )
            
            # Dynamically assign the returning UI handles back to your standard instance namespaces
            setattr(self, f"weapon_armor_facing_{row_idx}", facing_var)
            setattr(self, f"weapon_armor_facing_{row_idx}_dropdown", facing_dropdown)

    def add_weapon_facing_dropdown(self, canvas_type, column_val, row_val):
        """ Generic function to create facings for weapon rows"""
        facing = tk.StringVar()
        facing.set("Facing")
        options = ["Facing", "Front", "Back", "Left", "Right", "Top", "Underbody"]
        # Create the dropdown widget
        dropdown = ttk.OptionMenu(canvas_type, facing, "Facing", *options) #filled elsewhere
        dropdown.grid(column=column_val, row=row_val, sticky="w")
        facing.trace_add("write", lambda *trace_args, r=row_val: (self.recalculate()))
        return facing, "dropdown"

    ######################################################################
    # Links Row 1 Processing here                                        #
    ######################################################################
    def add_labels_buttons_link_rows(self, canvas_type):
        """Generates 10 rows of link controls featuring multi-select entry bars."""
        start_row = self.grid_row_links_header 
    
        tk.Label(canvas_type, text="Links").grid(row=start_row, column=self.grid_col_item, sticky="w", pady=(10, 5))

        current_row = start_row + 1
        for i in range(self.link_rows_count):
            tk.Label(canvas_type, text=f"Link #{i+1}:").grid(row=current_row, column=self.grid_col_item, sticky="w")
        
            # Read-only Entry field that behaves like a clickable button
            entry = tk.Entry(canvas_type, textvariable=self.link_entry_vars[i], width=50, state="readonly", cursor="hand2")
            entry.grid(row=current_row, column=self.grid_col_qty, columnspan=15, sticky="ew", padx=5, pady=2)
        
            # Bind left-mouse-click to open our popup window
            entry.bind("<Button-1>", lambda event, idx=i: self.open_link_selector(event, idx))
            self.link_entry_fields[i] = entry
        
            # Link cost display
            #tk.Label(canvas_type, text="$50").grid(row=current_row, column=self.grid_col_spaces, sticky="w")
        
            current_row += 1

    def add_labels_buttons_bumper_trigger_rows(self, canvas_type):
        """Generates 10 rows of Bumper Trigger controls with facing drop-downs, 
        safely isolated to protect grid column proportions."""
    
        # Call the header index variable assigned via set_columns
        start_row = self.grid_row_bumper_trigger_header
    
        # 1. Create the master sandbox frame using your tested columnspan bridge
        bt_master_frame = tk.Frame(canvas_type)
        bt_master_frame.grid(row=start_row, column=self.grid_col_item, columnspan=15, sticky="w", pady=(15, 5))
    
        # 2. Section Header
        tk.Label(bt_master_frame, text="Bumper Triggers").grid(row=0, column=0, columnspan=4, sticky="w", pady=(0, 5))
    
        # 3. Standard Facing Directions
        facings = ["Facing", "Front", "Back", "Left", "Right", "Top", "Underbody"]
    
        # 4. Build the rows
        for i in range(self.bt_rows_count):
            current_frame_row = i + 1
        
            # Identification Title
            lbl = tk.Label(bt_master_frame, text=f"Trigger #{i+1}:", width=9, anchor="w")
            lbl.grid(row=current_frame_row, column=0, sticky="w", pady=2)
        
            # Clickable multi-select entry line
            entry = tk.Entry(bt_master_frame, textvariable=self.bt_entry_vars[i], width=45, state="readonly", cursor="hand2")
            entry.grid(row=current_frame_row, column=2, sticky="w", padx=(0, 15), pady=2)
        
            # Bind left click to open the selector window
            entry.bind("<Button-1>", lambda event, idx=i: self.open_bt_selector(event, idx))
            self.bt_entry_fields[i] = entry

            # Facing selection drop-down menu
            facing_menu = ttk.OptionMenu(bt_master_frame, self.selected_bt_facing[i], "Facing", *facings)
            facing_menu.grid(row=current_frame_row, column=1, sticky="w", padx=(0, 10))
        
    ######################################################################
    # Accessories Row 1 processing here                                  #
    ######################################################################
    def add_labels_buttons_accessories_1_canvas(self, canvas_type):
        self.label_hidden_accessories_1_name = tk.Label(canvas_type, text="0", anchor="w")
        self.label_hidden_accessories_1_cost = tk.Label(canvas_type, text="0", anchor="w")
        self.label_hidden_accessories_1_weight = tk.Label(canvas_type, text="0", anchor="w")
        self.label_hidden_accessories_1_space = tk.Label(canvas_type, text="0", anchor="w")
        self.label_hidden_accessories_1_dp = tk.Label(canvas_type, text="0", anchor="w")
        self.label_hidden_accessories_1_notes = tk.Label(canvas_type, text="", anchor="w")
        self.label_hidden_accessories_1_turret_size = tk.Label(canvas_type, text="0", anchor="w")

        self.label_accessories_1_cost = tk.Label(canvas_type, text="0", anchor="w")
        self.label_accessories_1_cost.grid(column=self.grid_col_cost,row=self.grid_row_accessories_1, sticky="w")
        self.label_accessories_1_weight = tk.Label(canvas_type, text="0", anchor="w")
        self.label_accessories_1_weight.grid(column=self.grid_col_weight ,row=self.grid_row_accessories_1, sticky="w")
        self.label_accessories_1_space = tk.Label(canvas_type, text="0", anchor="w")
        self.label_accessories_1_space.grid(column=self.grid_col_spaces,row=self.grid_row_accessories_1, sticky="w")
        self.label_accessories_1_dp = tk.Label(canvas_type, text="0", anchor="w")
        self.label_accessories_1_dp.grid(column=self.grid_col_dp,row=self.grid_row_accessories_1, sticky="w")
        self.label_accessories_1_notes = tk.Label(canvas_type, text="", anchor="w")
        self.label_accessories_1_notes.grid(column=self.grid_col_max_weight,row=self.grid_row_accessories_1, sticky="w", columnspan=4)

        self.var_accessories_1_qty = tk.IntVar(value=0)
        self.entry_accessories_1_qty = ttk.Entry(canvas_type, textvariable=self.var_accessories_1_qty, width=3)
        self.entry_accessories_1_qty.grid(column=self.grid_col_qty, row=self.grid_row_accessories_1, sticky="w")
        self.var_accessories_1_qty.trace_add("write", self.accessories_qty_1_update)

    def add_dropdown_accessories_1_canvas(self, canvas_type):
        self.selected_accessories_1 = tk.StringVar()
        self.selected_accessories_1.set("Accessories")
        options = self.get_accessories_options()
        # Create the dropdown widget
        self.accessories_1_dropdown = ttk.OptionMenu(canvas_type, self.selected_accessories_1, "Accessory", *options) #filled elsewhere
        self.accessories_1_dropdown.grid(column=self.grid_col_item, row=self.grid_row_accessories_1, sticky="w")
        self.selected_accessories_1.trace_add("write", self.on_select_accessories_1)

    def on_select_accessories_1(self, *args):
        selected_value = self.selected_accessories_1.get()
        for entry in self.accessories_list: #use the same self.accessories_list for every accessories dropdown
            accessories_name: str = entry.get("Accessory Name")
            if selected_value == accessories_name:
                accessories_cost:          str = entry.get("Cost")
                accessories_weight:        str = entry.get("Weight")
                accessories_space:         str = entry.get("Space")
                accessories_dp:            str = entry.get("DP")
                accessories_notes:         str = entry.get("Notes")
                accessories_turret_size:   str = entry.get("Turret Size")

                if accessories_cost == "":
                    accessories_cost = "0"
                if accessories_weight == "":
                    accessories_weight = "0"
                if accessories_space == "":
                    accessories_space = "0"

                self.label_hidden_accessories_1_name.configure(text=str(accessories_name))
                self.label_hidden_accessories_1_cost.configure(text=self.float_to_str(accessories_cost))
                self.label_hidden_accessories_1_weight.configure(text=self.float_to_str(accessories_weight))
                self.label_hidden_accessories_1_space.configure(text=self.float_to_str(accessories_space))
                self.label_hidden_accessories_1_dp.configure(text=str(accessories_dp))
                self.label_hidden_accessories_1_notes.configure(text=str(accessories_notes))
                self.label_hidden_accessories_1_turret_size.configure(text=str(accessories_turret_size))
                self.accessories_qty_1_update()
                self.recalculate()

    def on_button_accessories_1_qty_up(self, *args):
        accessories_1_qty = self.var_accessories_1_qty.get()
        accessories_1_qty = accessories_1_qty + 1
        self.var_accessories_1_qty.set(value=accessories_1_qty)
        accessories_1_cost   = int(self.label_hidden_accessories_1_cost.cget("text"))
        accessories_1_weight = int(self.label_hidden_accessories_1_weight.cget("text"))
        accessories_1_space: str  = self.label_hidden_accessories_1_space.cget("text")
        accessories_1_dp:    str  = self.label_hidden_accessories_1_dp.cget("text")
        accessories_1_notes: str  = self.label_hidden_accessories_1_notes.cget("text")

        if accessories_1_space == "":
            accessories_1_space = 0.0
        else:
            accessories_1_space = float(accessories_1_space)

        self.label_accessories_1_cost.configure(text=self.float_to_str(accessories_1_cost * accessories_1_qty))
        self.label_accessories_1_weight.configure(text=self.float_to_str(accessories_1_weight * accessories_1_qty))
        self.label_accessories_1_space.configure(text=self.float_to_str(accessories_1_space * accessories_1_qty))
        self.label_accessories_1_dp.configure(text=str(accessories_1_dp))
        self.label_accessories_1_notes.configure(text=str(accessories_1_notes))
        self.accessories_special_processing()
        self.recalculate()

    def on_button_accessories_1_qty_down(self, *args):
        accessories_1_qty = self.var_accessories_1_qty.get()
        accessories_1_qty = max(accessories_1_qty - 1, 0)
        self.var_accessories_1_qty.set(value=accessories_1_qty)
        accessories_1_cost   = int(self.label_hidden_accessories_1_cost.cget("text"))
        accessories_1_weight = int(self.label_hidden_accessories_1_weight.cget("text"))
        accessories_1_space  = float(self.label_hidden_accessories_1_space.cget("text"))
        accessories_1_dp     = self.label_hidden_accessories_1_dp.cget("text")
        accessories_1_notes  = self.label_hidden_accessories_1_notes.cget("text")
        self.label_accessories_1_cost.configure(text=self.float_to_str(accessories_1_cost * accessories_1_qty))
        self.label_accessories_1_weight.configure(text=self.float_to_str(accessories_1_weight * accessories_1_qty))
        self.label_accessories_1_space.configure(text=self.float_to_str(accessories_1_space * accessories_1_qty))
        self.label_accessories_1_dp.configure(text=str(accessories_1_dp))
        if accessories_1_qty > 0:
            self.label_accessories_1_notes.configure(text=str(accessories_1_notes))
        else:
            self.label_accessories_1_notes.configure(text=str(""))
        self.accessories_special_processing()
        self.recalculate()

    def accessories_qty_1_update(self, *args):
        accessories_1_qty = self.var_accessories_1_qty.get()
        accessories_1_cost   = int(self.label_hidden_accessories_1_cost.cget("text"))
        accessories_1_weight = int(self.label_hidden_accessories_1_weight.cget("text"))
        accessories_1_space  = float(self.label_hidden_accessories_1_space.cget("text"))
        accessories_1_dp     = self.label_hidden_accessories_1_dp.cget("text")
        accessories_1_notes  = self.label_hidden_accessories_1_notes.cget("text")
        self.label_accessories_1_cost.configure(text=self.float_to_str(accessories_1_cost * accessories_1_qty))
        self.label_accessories_1_weight.configure(text=self.float_to_str(accessories_1_weight * accessories_1_qty))
        self.label_accessories_1_space.configure(text=self.float_to_str(accessories_1_space * accessories_1_qty))
        self.label_accessories_1_dp.configure(text=str(accessories_1_dp))
        if accessories_1_qty > 0:
            self.label_accessories_1_notes.configure(text=str(accessories_1_notes))
        else:
            self.label_accessories_1_notes.configure(text=str(""))
        self.accessories_special_processing()
        self.recalculate()

    def load_accessories_processing_list(self):
        self.accessories_processing_list: list = []
        entry_dict: dict = {0: self.selected_accessories_1, 1: self.label_accessories_1_cost, 2: self.label_accessories_1_weight, 3: self.var_accessories_1_qty, 4: self.label_hidden_accessories_hc_1}
        self.accessories_processing_list.append(entry_dict)
        entry_dict: dict = {0: self.selected_accessories_2, 1: self.label_accessories_2_cost, 2: self.label_accessories_2_weight, 3: self.var_accessories_2_qty, 4: self.label_hidden_accessories_hc_2}
        self.accessories_processing_list.append(entry_dict)
        entry_dict: dict = {0: self.selected_accessories_3, 1: self.label_accessories_3_cost, 2: self.label_accessories_3_weight, 3: self.var_accessories_3_qty, 4: self.label_hidden_accessories_hc_3}
        self.accessories_processing_list.append(entry_dict)
        entry_dict: dict = {0: self.selected_accessories_4, 1: self.label_accessories_4_cost, 2: self.label_accessories_4_weight, 3: self.var_accessories_4_qty, 4: self.label_hidden_accessories_hc_4}
        self.accessories_processing_list.append(entry_dict)
        entry_dict: dict = {0: self.selected_accessories_5, 1: self.label_accessories_5_cost, 2: self.label_accessories_5_weight, 3: self.var_accessories_5_qty, 4: self.label_hidden_accessories_hc_5}
        self.accessories_processing_list.append(entry_dict)
        entry_dict: dict = {0: self.selected_accessories_6, 1: self.label_accessories_6_cost, 2: self.label_accessories_6_weight, 3: self.var_accessories_6_qty, 4: self.label_hidden_accessories_hc_6}
        self.accessories_processing_list.append(entry_dict)
        entry_dict: dict = {0: self.selected_accessories_7, 1: self.label_accessories_7_cost, 2: self.label_accessories_7_weight, 3: self.var_accessories_7_qty, 4: self.label_hidden_accessories_hc_7}
        self.accessories_processing_list.append(entry_dict)
        entry_dict: dict = {0: self.selected_accessories_8, 1: self.label_accessories_8_cost, 2: self.label_accessories_8_weight, 3: self.var_accessories_8_qty, 4: self.label_hidden_accessories_hc_8}
        self.accessories_processing_list.append(entry_dict)
        entry_dict: dict = {0: self.selected_accessories_9, 1: self.label_accessories_9_cost, 2: self.label_accessories_9_weight, 3: self.var_accessories_9_qty, 4: self.label_hidden_accessories_hc_9}
        self.accessories_processing_list.append(entry_dict)
        entry_dict: dict = {0: self.selected_accessories_10, 1: self.label_accessories_10_cost, 2: self.label_accessories_10_weight, 3: self.var_accessories_10_qty, 4: self.label_hidden_accessories_hc_10}
        self.accessories_processing_list.append(entry_dict)
        entry_dict: dict = {0: self.selected_accessories_11, 1: self.label_accessories_11_cost, 2: self.label_accessories_11_weight, 3: self.var_accessories_11_qty, 4: self.label_hidden_accessories_hc_11}
        self.accessories_processing_list.append(entry_dict)
        entry_dict: dict = {0: self.selected_accessories_12, 1: self.label_accessories_12_cost, 2: self.label_accessories_12_weight, 3: self.var_accessories_12_qty, 4: self.label_hidden_accessories_hc_12}
        self.accessories_processing_list.append(entry_dict)
        entry_dict: dict = {0: self.selected_accessories_13, 1: self.label_accessories_13_cost, 2: self.label_accessories_13_weight, 3: self.var_accessories_13_qty, 4: self.label_hidden_accessories_hc_13}
        self.accessories_processing_list.append(entry_dict)
        entry_dict: dict = {0: self.selected_accessories_14, 1: self.label_accessories_14_cost, 2: self.label_accessories_14_weight, 3: self.var_accessories_14_qty, 4: self.label_hidden_accessories_hc_14}
        self.accessories_processing_list.append(entry_dict)
        entry_dict: dict = {0: self.selected_accessories_15, 1: self.label_accessories_15_cost, 2: self.label_accessories_15_weight, 3: self.var_accessories_15_qty, 4: self.label_hidden_accessories_hc_15}
        self.accessories_processing_list.append(entry_dict)
        entry_dict: dict = {0: self.selected_accessories_16, 1: self.label_accessories_16_cost, 2: self.label_accessories_16_weight, 3: self.var_accessories_16_qty, 4: self.label_hidden_accessories_hc_16}
        self.accessories_processing_list.append(entry_dict)
        entry_dict: dict = {0: self.selected_accessories_17, 1: self.label_accessories_17_cost, 2: self.label_accessories_17_weight, 3: self.var_accessories_17_qty, 4: self.label_hidden_accessories_hc_17}
        self.accessories_processing_list.append(entry_dict)
        entry_dict: dict = {0: self.selected_accessories_18, 1: self.label_accessories_18_cost, 2: self.label_accessories_18_weight, 3: self.var_accessories_18_qty, 4: self.label_hidden_accessories_hc_18}
        self.accessories_processing_list.append(entry_dict)
        entry_dict: dict = {0: self.selected_accessories_19, 1: self.label_accessories_19_cost, 2: self.label_accessories_19_weight, 3: self.var_accessories_19_qty, 4: self.label_hidden_accessories_hc_19}
        self.accessories_processing_list.append(entry_dict)
        entry_dict: dict = {0: self.selected_accessories_20, 1: self.label_accessories_20_cost, 2: self.label_accessories_20_weight, 3: self.var_accessories_20_qty, 4: self.label_hidden_accessories_hc_20}
        self.accessories_processing_list.append(entry_dict)
        entry_dict: dict = {0: self.selected_accessories_21, 1: self.label_accessories_21_cost, 2: self.label_accessories_21_weight, 3: self.var_accessories_21_qty, 4: self.label_hidden_accessories_hc_21}
        self.accessories_processing_list.append(entry_dict)
        entry_dict: dict = {0: self.selected_accessories_22, 1: self.label_accessories_22_cost, 2: self.label_accessories_22_weight, 3: self.var_accessories_22_qty, 4: self.label_hidden_accessories_hc_22}
        self.accessories_processing_list.append(entry_dict)
        entry_dict: dict = {0: self.selected_accessories_23, 1: self.label_accessories_23_cost, 2: self.label_accessories_23_weight, 3: self.var_accessories_23_qty, 4: self.label_hidden_accessories_hc_23}
        self.accessories_processing_list.append(entry_dict)
        entry_dict: dict = {0: self.selected_accessories_24, 1: self.label_accessories_24_cost, 2: self.label_accessories_24_weight, 3: self.var_accessories_24_qty, 4: self.label_hidden_accessories_hc_24}
        self.accessories_processing_list.append(entry_dict)
        entry_dict: dict = {0: self.selected_accessories_25, 1: self.label_accessories_25_cost, 2: self.label_accessories_25_weight, 3: self.var_accessories_25_qty, 4: self.label_hidden_accessories_hc_25}
        self.accessories_processing_list.append(entry_dict)
        entry_dict: dict = {0: self.selected_accessories_26, 1: self.label_accessories_26_cost, 2: self.label_accessories_26_weight, 3: self.var_accessories_26_qty, 4: self.label_hidden_accessories_hc_26}
        self.accessories_processing_list.append(entry_dict)
        entry_dict: dict = {0: self.selected_accessories_27, 1: self.label_accessories_27_cost, 2: self.label_accessories_27_weight, 3: self.var_accessories_27_qty, 4: self.label_hidden_accessories_hc_27}
        self.accessories_processing_list.append(entry_dict)
        entry_dict: dict = {0: self.selected_accessories_28, 1: self.label_accessories_28_cost, 2: self.label_accessories_28_weight, 3: self.var_accessories_28_qty, 4: self.label_hidden_accessories_hc_28}
        self.accessories_processing_list.append(entry_dict)
        entry_dict: dict = {0: self.selected_accessories_29, 1: self.label_accessories_29_cost, 2: self.label_accessories_29_weight, 3: self.var_accessories_29_qty, 4: self.label_hidden_accessories_hc_29}
        self.accessories_processing_list.append(entry_dict)
        entry_dict: dict = {0: self.selected_accessories_30, 1: self.label_accessories_30_cost, 2: self.label_accessories_30_weight, 3: self.var_accessories_30_qty, 4: self.label_hidden_accessories_hc_30}
        self.accessories_processing_list.append(entry_dict)

    def accessories_special_processing(self):
        """ Examine each Accessories line for any special processing.
            Examples include:
            1) Ramplate value is based off of allocated front armor
            2) HD SHocks/HD Brakes cost is based on number of tires
            3) Active Suspension raises HC
            4) Front WheelGuards lowers HC
            5) Spoiler/Airdram raises HC if there's two of them"""
        local_armor_cost:         float = float(self.label_hidden_body_armor_cost.cget("text"))
        local_armor_weight:       float = float(self.label_hidden_body_armor_weight.cget("text"))
        local_outer_armor_cost:   float = float(self.label_hidden_outer_armor_cost.cget("text"))
        local_outer_armor_weight: float = float(self.label_hidden_outer_armor_weight.cget("text"))
        local_inner_armor_cost:   float = float(self.label_hidden_inner_armor_cost.cget("text"))
        local_inner_armor_weight: float = float(self.label_hidden_inner_armor_weight.cget("text"))
        local_outer_front_armor:    int = int(self.var_outer_front_armor_allocation_qty.get())
        local_inner_front_armor:    int = int(self.var_inner_front_armor_allocation_qty.get())

        total_tire_qty: int = self.var_front_tire_qty.get()
        total_tire_qty = total_tire_qty + self.var_rear_tire_qty.get()
        outer_armor_selection: str = self.label_hidden_outer_armor_selection.cget("text")
        inner_armor_selection: str = self.label_hidden_inner_armor_selection.cget("text")

        count_htm_hdhtm: int = 0
        count_active_suspensions: int = 0
        count_ramplate: int = 0
        count_turrets: int = 0
        count_spoiler_airdam: int = 0
        count_overdrive: int = 0
        count_hd_shocks: int = 0
        count_hd_brakes: int = 0
        for entry in self.accessories_processing_list:
            selected_value = entry[0]
            selected_cost_label = entry[1]
            selected_weight_label = entry[2]
            selected_qty = entry[3]
            selected_hidden_hc = entry[4]
            name: str = selected_value.get()
            qty: int = selected_qty.get()
            if qty > 0: #don't bother looking at this if the qty is zero, just move on
                match name:
                    #HC adjustment
                    case "Active Suspension":
                        selected_hidden_hc.configure(text="1")
                        count_active_suspensions += 1
                        self.hc_addition()
                    case "Wheelguards, Front - Plastic":
                        local_armor_cost_factor: float = 0.0
                        local_armor_weight_factor: float = 0.0
                        if outer_armor_selection.find("Plastic") > -1:
                            local_armor_cost_factor = local_outer_armor_cost
                            local_armor_weight_factor = local_outer_armor_weight
                        elif inner_armor_selection.find("Plastic") > -1:
                            local_armor_cost_factor = local_inner_armor_cost
                            local_armor_weight_factor = local_inner_armor_weight
                        item_cost: float = local_armor_cost_factor * 10.0 * qty
                        item_weight: float = local_armor_weight_factor * 4.0 * qty
                        selected_cost_label.configure(text=self.float_to_str(item_cost))
                        selected_weight_label.configure(text=self.float_to_str(item_weight))
                        selected_hidden_hc.configure(text="-1")
                        self.hc_addition()
                    case "Wheelguards, Front - MET":
                        local_armor_cost_factor: float = 0.0
                        local_armor_weight_factor: float = 0.0
                        if outer_armor_selection.find("MET") > -1:
                            local_armor_cost_factor = local_outer_armor_cost
                            local_armor_weight_factor = local_outer_armor_weight
                        elif inner_armor_selection.find("MET") > -1:
                            local_armor_cost_factor = local_inner_armor_cost
                            local_armor_weight_factor = local_inner_armor_weight
                        item_cost: float = local_armor_cost_factor * 10.0 * qty
                        item_weight: float = local_armor_weight_factor * 4.0 * qty
                        selected_cost_label.configure(text=self.float_to_str(item_cost))
                        selected_weight_label.configure(text=self.float_to_str(item_weight))
                        selected_hidden_hc.configure(text="-1")
                        self.hc_addition()
                    case "Wheelguards, Rear - Plastic" | "Wheelhubs":
                        local_armor_cost_factor: float = 0.0
                        local_armor_weight_factor: float = 0.0
                        if outer_armor_selection.find("Plastic") > -1:
                            local_armor_cost_factor = local_outer_armor_cost
                            local_armor_weight_factor = local_outer_armor_weight
                        elif inner_armor_selection.find("Plastic") > -1:
                            local_armor_cost_factor = local_inner_armor_cost
                            local_armor_weight_factor = local_inner_armor_weight
                        item_cost: float = local_armor_cost_factor * 10.0 * qty
                        item_weight: float = local_armor_weight_factor * 4.0 * qty
                        selected_cost_label.configure(text=self.float_to_str(item_cost))
                        selected_weight_label.configure(text=self.float_to_str(item_weight))
                    case "Wheelguards, Rear - Metal":
                        local_armor_cost_factor: float = 0.0
                        local_armor_weight_factor: float = 0.0
                        if outer_armor_selection.find("MET") > -1:
                            local_armor_cost_factor = local_outer_armor_cost
                            local_armor_weight_factor = local_outer_armor_weight
                        elif inner_armor_selection.find("MET") > -1:
                            local_armor_cost_factor = local_inner_armor_cost
                            local_armor_weight_factor = local_inner_armor_weight
                        item_cost: float = local_armor_cost_factor * 10.0 * qty
                        item_weight: float = local_armor_weight_factor * 4.0 * qty
                        selected_cost_label.configure(text=self.float_to_str(item_cost))
                        selected_weight_label.configure(text=self.float_to_str(item_weight))
                    case "Wheelhubsguards, Rear - Plastic" | "Wheelhubs - Plastic":
                        local_armor_cost_factor: float = 0.0
                        local_armor_weight_factor: float = 0.0
                        if outer_armor_selection.find("Plastic") > -1:
                            local_armor_cost_factor = local_outer_armor_cost
                            local_armor_weight_factor = local_outer_armor_weight
                        elif inner_armor_selection.find("Plastic") > -1:
                            local_armor_cost_factor = local_inner_armor_cost
                            local_armor_weight_factor = local_inner_armor_weight
                        item_cost: float = local_armor_cost_factor * 10.0 * qty
                        item_weight: float = local_armor_weight_factor * 4.0 * qty
                        selected_cost_label.configure(text=self.float_to_str(item_cost))
                        selected_weight_label.configure(text=self.float_to_str(item_weight))
                    case "Wheelguards, Rear - Metal" | "Wheelhubs - Metal":
                        local_armor_cost_factor: float = 0.0
                        local_armor_weight_factor: float = 0.0
                        if outer_armor_selection.find("MET") > -1:
                            local_armor_cost_factor = local_outer_armor_cost
                            local_armor_weight_factor = local_outer_armor_weight
                        elif inner_armor_selection.find("MET") > -1:
                            local_armor_cost_factor = local_inner_armor_cost
                            local_armor_weight_factor = local_inner_armor_weight
                        item_cost: float = local_armor_cost_factor * 10.0 * qty
                        item_weight: float = local_armor_weight_factor * 4.0 * qty
                        selected_cost_label.configure(text=self.float_to_str(item_cost))
                        selected_weight_label.configure(text=self.float_to_str(item_weight))
                    #Cost/Weight adjusted by tire count
                    case "Heavy-duty Brakes":
                        selected_cost_label.configure(text=str(total_tire_qty * 100))
                        count_hd_brakes += qty
                    case "Heavy-duty Shock Absorbers":
                        selected_cost_label.configure(text=str(total_tire_qty * 400))
                        selected_weight_label.configure(text=str(total_tire_qty * 5))
                        count_hd_shocks += qty
                    case "High Torque Motors (HTM)":
                        selected_cost_label.configure(text=str(total_tire_qty * 100))
                        count_htm_hdhtm += qty
                    case "High Torque Motors, Heavy Duty (HDHTM)":
                        selected_cost_label.configure(text=str(total_tire_qty * 200))
                        count_htm_hdhtm += qty
                    case "Overdrive":
                        selected_cost_label.configure(text=str(total_tire_qty * 100))
                        count_overdrive += qty
                    #Cost/weight adjusted by front armor count
                    case "Ramplate":
                        #cost = front armor cost * 1.5
                        #weight = front armor weight * .5
                        total_ramplate_cost: float = float(1.5 * (local_armor_cost * local_outer_armor_cost * local_outer_front_armor + local_armor_cost * local_inner_armor_cost * local_inner_front_armor))
                        total_ramplate_weight: float = float(0.5 * (local_armor_weight * local_outer_armor_weight * local_outer_front_armor + local_armor_weight * local_inner_armor_weight * local_inner_front_armor))
                        selected_cost_label.configure(text=self.float_to_str(total_ramplate_cost))
                        selected_weight_label.configure(text=self.float_to_str(total_ramplate_weight))
                        count_ramplate += qty
                    case "Spoilers and Airdams, plastic":
                        local_armor_cost_factor: float = 0.0
                        local_armor_weight_factor: float = 0.0
                        if outer_armor_selection.find("Plastic") > -1:
                            local_armor_cost_factor = local_outer_armor_cost
                            local_armor_weight_factor = local_outer_armor_weight
                        elif inner_armor_selection.find("Plastic") > -1:
                            local_armor_cost_factor = local_inner_armor_cost
                            local_armor_weight_factor = local_inner_armor_weight
                        item_cost: float = local_armor_cost * local_armor_cost_factor * 25.0 * qty
                        item_weight: float = local_armor_weight * local_armor_weight_factor * 10.0 * qty
                        selected_cost_label.configure(text=self.float_to_str(item_cost))
                        selected_weight_label.configure(text=self.float_to_str(item_weight))
                        count_spoiler_airdam += qty
                    case "Spoilers and Airdams, Metal Airfoil":
                        local_armor_cost_factor: float = 0.0
                        local_armor_weight_factor: float = 0.0
                        if outer_armor_selection.find("MET") > -1:
                            local_armor_cost_factor = local_outer_armor_cost
                            local_armor_weight_factor = local_outer_armor_weight
                        elif inner_armor_selection.find("MET") > -1:
                            local_armor_cost_factor = local_inner_armor_cost
                            local_armor_weight_factor = local_inner_armor_weight
                        item_cost: float = local_armor_cost * local_armor_cost_factor * 10.0 * qty
                        item_weight: float = local_armor_weight * local_armor_weight_factor * 2.0 * qty
                        selected_cost_label.configure(text=self.float_to_str(item_cost))
                        selected_weight_label.configure(text=self.float_to_str(item_weight))
                        count_spoiler_airdam += qty
                    case "Turret - Zero-space":
                        count_turrets += qty
                    case "Turret - One Space":
                        count_turrets += qty
                    case "Turret - Two-space":
                        count_turrets += qty
                    case "Turret - Three-space":
                        count_turrets += qty
                    case "Turret - Four-space":
                        count_turrets += qty
                    case "Turret - Pop-up - Zero-space":
                        count_turrets += qty
                    case "Turret - Pop-up - One-space":
                        count_turrets += qty
                    case "Turret - Pop-up - Two-space":
                        count_turrets += qty
                    case "Turret - Pop-up - Three-space":
                        count_turrets += qty
                    case "Turret - Pop-up - Four-space":
                        count_turrets += qty
            if count_htm_hdhtm > 1:
                self.label_valid_accessories.configure(text="Too Many HTMs")
            elif count_active_suspensions > 1:
                self.label_valid_accessories.configure(text="Too Many Active Suspensions")
            elif count_ramplate > 1:
                self.label_valid_accessories.configure(text="Too Many Ramplates")
            elif count_spoiler_airdam > 2:
                self.label_valid_accessories.configure(text="Too Many Spoilers/Airdams")
            elif count_turrets > 1:
                self.label_valid_accessories.configure(text="Too Many Turrets")
            elif count_overdrive > 1:
                self.label_valid_accessories.configure(text="Too Many Overdrives")
            elif count_hd_shocks > 1:
                self.label_valid_accessories.configure(text="Too Many HD Shocks")
            elif count_hd_brakes > 1:
                self.label_valid_accessories.configure(text="Too Many HD Brakes")
            else:
                self.label_valid_accessories.configure(text="")

    ######################################################################
    # Component Armor Common processing here                             #
    ######################################################################

    def add_dropdown_component_armor_canvas(self, canvas_type):
        self.add_dropdown_component_armor_canvas_1(canvas_type)
        self.add_dropdown_component_armor_canvas_2(canvas_type)
        self.add_dropdown_component_armor_canvas_3(canvas_type)
        self.add_dropdown_component_armor_canvas_4(canvas_type)
        self.add_dropdown_component_armor_canvas_5(canvas_type)
        self.add_dropdown_component_armor_facing_1_canvas(canvas_type)
        self.add_dropdown_component_armor_facing_2_canvas(canvas_type)
        self.add_dropdown_component_armor_facing_3_canvas(canvas_type)
        self.add_dropdown_component_armor_facing_4_canvas(canvas_type)
        self.add_dropdown_component_armor_facing_5_canvas(canvas_type)

    def get_component_armor_dictionaries(self):
        self.component_armor_list = []
        entry_dict: dict = {"Component Armor": "Component Armor",                "Cost": "0",    "Weight": "0",   "Abbr": "None"}
        self.component_armor_list.append(entry_dict)
        entry_dict: dict = {"Component Armor": "Normal Plastic Component Armor", "Cost": "1",    "Weight": "1",   "Abbr": "Normal"}
        self.component_armor_list.append(entry_dict)
        entry_dict: dict = {"Component Armor": "FP Plastic Component Armor",     "Cost": "2",    "Weight": "1",   "Abbr": "FP"}
        self.component_armor_list.append(entry_dict)
        entry_dict: dict = {"Component Armor": "LR Plastic Component Armor",     "Cost": "1.1",  "Weight": "1.1", "Abbr": "LR"}
        self.component_armor_list.append(entry_dict)
        entry_dict: dict = {"Component Armor": "LRFP Plastic Component Armor",   "Cost": "2.5",  "Weight": "1.1", "Abbr": "LRFP"}
        self.component_armor_list.append(entry_dict)
        entry_dict: dict = {"Component Armor": "RP Plastic Component Armor",     "Cost": "2",    "Weight": "1",   "Abbr": "RP"}
        self.component_armor_list.append(entry_dict)
        entry_dict: dict = {"Component Armor": "RPFP Plastic Component Armor",   "Cost": "4",    "Weight": "1",   "Abbr": "RPFP"}
        self.component_armor_list.append(entry_dict)
        entry_dict: dict = {"Component Armor": "MET Component Armor",            "Cost": "2.5",  "Weight": "5",   "Abbr": "MET"}
        self.component_armor_list.append(entry_dict)
        entry_dict: dict = {"Component Armor": "LR MET Component Armor",         "Cost": "2.75", "Weight": "5",   "Abbr": "LR MET"}
        self.component_armor_list.append(entry_dict)

    def get_component_armor_options(self):
        options: list = []
        for entry in self.component_armor_list:
            component_armor_name: str = entry.get("Component Armor")
            options.append(component_armor_name)
        return options

    def add_component_armor_rows(self, canvas_type):
        self.add_labels_buttons_component_armor_row_1(canvas_type)
        self.add_labels_buttons_component_armor_row_2(canvas_type)
        self.add_labels_buttons_component_armor_row_3(canvas_type)
        self.add_labels_buttons_component_armor_row_4(canvas_type)
        self.add_labels_buttons_component_armor_row_5(canvas_type)

    def get_component_armor_facing_dictionaries(self):
        self.component_armor_facing_list = []
        entry_dict: dict = {"Facing": "Facing"}
        self.component_armor_facing_list.append(entry_dict)
        entry_dict: dict = {"Facing": "Front"}
        self.component_armor_facing_list.append(entry_dict)
        entry_dict: dict = {"Facing": "Back"}
        self.component_armor_facing_list.append(entry_dict)
        entry_dict: dict = {"Facing": "Left"}
        self.component_armor_facing_list.append(entry_dict)
        entry_dict: dict = {"Facing": "Right"}
        self.component_armor_facing_list.append(entry_dict)
        entry_dict: dict = {"Facing": "Top"}
        self.component_armor_facing_list.append(entry_dict)
        entry_dict: dict = {"Facing": "Underbody"}
        self.component_armor_facing_list.append(entry_dict)
        entry_dict: dict = {"Facing": "Driver"}
        self.component_armor_facing_list.append(entry_dict)
        entry_dict: dict = {"Facing": "Gunner"}
        self.component_armor_facing_list.append(entry_dict)
        entry_dict: dict = {"Facing": "Driver & Gunner"}
        self.component_armor_facing_list.append(entry_dict)
        entry_dict: dict = {"Facing": "Power Plant"}
        self.component_armor_facing_list.append(entry_dict)
        entry_dict: dict = {"Facing": "Gas Tank"}
        self.component_armor_facing_list.append(entry_dict)

    ######################################################################
    # Component Armor Row 1 processing here                              #
    ######################################################################

    def add_dropdown_component_armor_canvas_1(self, canvas_type):
        self.get_component_armor_dictionaries()
        self.selected_component_armor_1 = tk.StringVar()
        self.selected_component_armor_1.set("Component Armor")
        options = self.get_component_armor_options()
        # Create the dropdown widget
        self.component_armor_dropdown_1 = ttk.OptionMenu(canvas_type, self.selected_component_armor_1, "Component Armor",*options) #filled elsewhere
        self.component_armor_dropdown_1.grid(column=self.grid_col_item, row=self.grid_row_component_armor_1, sticky="w")
        self.selected_component_armor_1.trace_add("write", self.on_select_component_armor_1)

    def add_labels_buttons_component_armor_row_1(self, canvas_type):
        up_arrow = "\u2191"
        down_arrow = "\u2193"

        self.label_hidden_component_armor_1_cost = tk.Label(canvas_type, text="0", anchor="w")
        self.label_hidden_component_armor_1_weight = tk.Label(canvas_type, text="0", anchor="w")
        self.label_hidden_component_armor_1_dp = tk.Label(canvas_type, text="0", anchor="w")
        self.label_hidden_component_armor_1_space = tk.Label(canvas_type, text="0", anchor="w")

        self.label_component_armor_1_cost = tk.Label(canvas_type, text="0", anchor="w")
        self.label_component_armor_1_cost.grid(column=self.grid_col_cost,row=self.grid_row_component_armor_1, sticky="w")
        self.label_component_armor_1_weight = tk.Label(canvas_type, text="0", anchor="w")
        self.label_component_armor_1_weight.grid(column=self.grid_col_weight ,row=self.grid_row_component_armor_1, sticky="w")
        self.label_component_armor_1_space = tk.Label(canvas_type, text="0", anchor="w")
        self.label_component_armor_1_space.grid(column=self.grid_col_spaces,row=self.grid_row_component_armor_1, sticky="w")
        self.label_component_armor_1_dp = tk.Label(canvas_type, text="0", anchor="w")
        self.label_component_armor_1_dp.grid(column=self.grid_col_dp,row=self.grid_row_component_armor_1, sticky="w")

        self.var_component_armor_spaces_qty_1 = tk.IntVar(value=0)
        self.entry_component_armor_spaces_qty = ttk.Entry(canvas_type, textvariable=self.var_component_armor_spaces_qty_1, width=3)
        self.entry_component_armor_spaces_qty.grid(column=self.grid_col_qty,row=self.grid_row_component_armor_1, sticky="w")
        self.var_component_armor_spaces_qty_1.trace_add("write", self.on_changed_component_armor_spaces_1)

        self.button_component_armor_spaces_1_qty_up = tk.Button(canvas_type, text=up_arrow, command=self.on_button_component_armor_spaces_1_qty_up)
        self.button_component_armor_spaces_1_qty_up.grid(column=self.grid_left_up_button,row=self.grid_row_component_armor_1, sticky="w")
        self.button_component_armor_spaces_1_qty_down = tk.Button(canvas_type, text=down_arrow, command=self.on_button_component_armor_spaces_1_qty_down)
        self.button_component_armor_spaces_1_qty_down.grid(column=self.grid_left_down_button,row=self.grid_row_component_armor_1, sticky="w")

        self.var_component_armor_count_qty_1 = tk.IntVar(value=0)
        self.entry_component_armor_count_qty = ttk.Entry(canvas_type, textvariable=self.var_component_armor_count_qty_1, width=3)
        self.entry_component_armor_count_qty.grid(column=self.grid_right_qty,row=self.grid_row_component_armor_1, sticky="w")
        self.var_component_armor_count_qty_1.trace_add("write", self.on_changed_component_armor_count_1)

        self.button_component_armor_count_1_qty_up = tk.Button(canvas_type, text=up_arrow, command=self.on_button_component_armor_count_1_qty_up)
        self.button_component_armor_count_1_qty_up.grid(column=self.grid_right_up_button,row=self.grid_row_component_armor_1, sticky="w")
        self.button_component_armor_count_1_qty_down = tk.Button(canvas_type, text=down_arrow, command=self.on_button_component_armor_count_1_qty_down)
        self.button_component_armor_count_1_qty_down.grid(column=self.grid_right_down_button,row=self.grid_row_component_armor_1, sticky="w")

    def on_select_component_armor_1(self, *args):
        selected_value = self.selected_component_armor_1.get()
        for entry in self.component_armor_list:
            armor_type: str = entry.get("Component Armor")
            if selected_value == armor_type:
                component_armor_adjustment_cost = float(entry.get("Cost"))
                component_armor_adjustment_weight = float(entry.get("Weight"))
                component_armor_cost: float = 5.0
                component_armor_weight:  float = 2.0
                component_armor_spaces_qty = self.var_component_armor_spaces_qty_1.get()
                component_armor_count_qty = self.var_component_armor_count_qty_1.get()

                calculated_armor_cost = component_armor_adjustment_cost * component_armor_cost * component_armor_spaces_qty * component_armor_count_qty
                calculated_armor_weight = component_armor_adjustment_weight * component_armor_weight * component_armor_spaces_qty * component_armor_count_qty

                #calculate that the weight of the armor choice doesn't exceed 20 lbs per space
                if component_armor_weight * component_armor_count_qty * component_armor_adjustment_weight > 20.0:
                    if component_armor_adjustment_weight > 0.0:
                        component_armor_count_qty = min(10, int(10.0/component_armor_adjustment_weight))
                        self.var_component_armor_count_qty_1.set(component_armor_count_qty)


                self.label_hidden_component_armor_1_cost.configure(text=str(component_armor_adjustment_cost*component_armor_cost))
                self.label_hidden_component_armor_1_weight.configure(text=str(component_armor_adjustment_weight*component_armor_weight))
                self.label_hidden_component_armor_1_dp.configure(text=str(component_armor_count_qty))
                self.label_hidden_component_armor_1_space.configure(text=str(1))

                self.label_component_armor_1_cost.configure(text=str(calculated_armor_cost))
                self.label_component_armor_1_weight.configure(text=str(calculated_armor_weight))
                self.label_component_armor_1_space.configure(text=str(1))
                self.label_component_armor_1_dp.configure(text="1")
                self.calculate_component_armor_1(self.canvas_type)
                self.recalculate()

    def on_changed_component_armor_spaces_1(self, *args):
        self.calculate_component_armor_1(self.canvas_type)

    def calculate_component_armor_1(self, canvas_type):
        component_armor_space_qty = self.var_component_armor_spaces_qty_1.get()
        component_armor_count_qty = self.var_component_armor_count_qty_1.get()
        component_armor_cost_adjustment: float = float(self.label_hidden_component_armor_1_cost.cget("text"))
        component_armor_weight_adjustment: float = float(self.label_hidden_component_armor_1_weight.cget("text"))

        if component_armor_space_qty > 0 and component_armor_count_qty > 0:
            component_armor_1_cost:   float = 0.0
            component_armor_1_weight: float = 0.0
            component_armor_1_dp = component_armor_count_qty
            if self.is_cycle:
                component_armor_1_spaces = 0.5
            else:
                component_armor_1_spaces = 1
            component_armor_1_cost =  component_armor_space_qty * component_armor_count_qty * component_armor_cost_adjustment
            component_armor_1_weight =  component_armor_space_qty * component_armor_count_qty * component_armor_weight_adjustment
        else:
            component_armor_1_cost = 0
            component_armor_1_weight = 0
            component_armor_1_dp = 0
            component_armor_1_spaces = 0
        self.label_component_armor_1_cost.configure(text=self.float_to_str(component_armor_1_cost))
        self.label_component_armor_1_weight.configure(text=self.float_to_str(component_armor_1_weight))
        self.label_component_armor_1_dp.configure(text=str(component_armor_1_dp))
        self.label_component_armor_1_space.configure(text=str(component_armor_1_spaces))
        self.recalculate()

    def on_button_component_armor_spaces_1_qty_up(self, *args):
        component_armor_space_qty = self.var_component_armor_spaces_qty_1.get()
        component_armor_space_qty = component_armor_space_qty + 1
        component_armor_space_qty = min(component_armor_space_qty, 10)
        self.var_component_armor_spaces_qty_1.set(component_armor_space_qty)
        self.calculate_component_armor_1(self.canvas_type)

    def on_button_component_armor_spaces_1_qty_down(self, *args):
        component_armor_space_qty = self.var_component_armor_spaces_qty_1.get()
        component_armor_space_qty = component_armor_space_qty - 1
        component_armor_space_qty = max(component_armor_space_qty, 0)
        self.var_component_armor_spaces_qty_1.set(component_armor_space_qty)
        self.calculate_component_armor_1(self.canvas_type)

    def on_changed_component_armor_count_1(self, *args):
        self.calculate_component_armor_1(self.canvas_type)

    def on_button_component_armor_count_1_qty_up(self, *args):
        component_armor_count_qty = self.var_component_armor_count_qty_1.get()
        component_armor_count_qty = component_armor_count_qty + 1
        component_armor_weight_adjustment: float = float(self.label_hidden_component_armor_1_weight.cget("text"))
        #calculate that the weight of the armor choice doesn't exceed 20 lbs per space
        if component_armor_count_qty * component_armor_weight_adjustment > 20.0:
            component_armor_count_qty = component_armor_count_qty - 1
        self.var_component_armor_count_qty_1.set(component_armor_count_qty)
        self.calculate_component_armor_1(self.canvas_type)

    def on_button_component_armor_count_1_qty_down(self, *args):
        component_armor_count_qty = self.var_component_armor_count_qty_1.get()
        component_armor_count_qty = component_armor_count_qty - 1
        component_armor_count_qty = max(component_armor_count_qty, 0)
        self.var_component_armor_count_qty_1.set(component_armor_count_qty)
        self.calculate_component_armor_1(self.canvas_type)

    def add_dropdown_component_armor_facing_1_canvas(self, canvas_type):
        self.selected_component_armor_facing_1 = tk.StringVar()
        self.selected_component_armor_facing_1.set("Component Armor")
        options = ["Facing", "Front", "Back", "Left", "Right", "Top", "Underbody", "Driver", "Gunner", "Driver & Gunner", "Power Plant", "Gas Tank"]
        # Create the dropdown widget
        self.component_armor_facing_dropdown_1 = ttk.OptionMenu(canvas_type, self.selected_component_armor_facing_1, "Facing", *options) #filled elsewhere
        self.component_armor_facing_dropdown_1.grid(column=self.grid_col_max_weight, row=self.grid_row_component_armor_1, sticky="w")

    ######################################################
    # Rocket Booster Common processing                   #
    ######################################################
    def get_rocket_booster_facing_dictionaries(self):
        self.rocket_booster_facing_list = []
        entry_dict: dict = {"Facing": "Facing"}
        self.rocket_booster_facing_list.append(entry_dict)
        entry_dict: dict = {"Facing": "Front"}
        self.rocket_booster_facing_list.append(entry_dict)
        entry_dict: dict = {"Facing": "Back"}
        self.rocket_booster_facing_list.append(entry_dict)
        entry_dict: dict = {"Facing": "Left"}
        self.rocket_booster_facing_list.append(entry_dict)
        entry_dict: dict = {"Facing": "Right"}
        self.rocket_booster_facing_list.append(entry_dict)
        entry_dict: dict = {"Facing": "Top"}
        self.rocket_booster_facing_list.append(entry_dict)
        entry_dict: dict = {"Facing": "Underbody"}
        self.rocket_booster_facing_list.append(entry_dict)

    def add_row_rocket_boosters(self, canvas_type):
        self.add_row_rocket_boosters_1_canvas(canvas_type)
        self.add_row_rocket_boosters_2_canvas(canvas_type)
        self.add_row_rocket_boosters_3_canvas(canvas_type)
        self.add_row_rocket_boosters_4_canvas(canvas_type)
        self.add_row_rocket_boosters_5_canvas(canvas_type)
        self.add_dropdown_rocket_boost_facing_1_canvas(canvas_type)
        self.add_dropdown_rocket_boost_facing_2_canvas(canvas_type)
        self.add_dropdown_rocket_boost_facing_3_canvas(canvas_type)
        self.add_dropdown_rocket_boost_facing_4_canvas(canvas_type)
        self.add_dropdown_rocket_boost_facing_5_canvas(canvas_type)
    ######################################################
    # Rocket Booster Row 1 processing                    #
    ######################################################
    def add_row_rocket_boosters_1_canvas(self, canvas_type):
        up_arrow = "\u2191"
        down_arrow = "\u2193"

        self.label_hidden_rocket_booster_1_cost = tk.Label(canvas_type, text="0", anchor="w")
        self.label_hidden_rocket_booster_1_weight = tk.Label(canvas_type, text="0", anchor="w")
        self.label_hidden_rocket_booster_1_dp = tk.Label(canvas_type, text="0", anchor="w")
        self.label_hidden_rocket_booster_1_space = tk.Label(canvas_type, text="0", anchor="w")

        self.label_rocket_booster_1_cost = tk.Label(canvas_type, text="0", anchor="w")
        self.label_rocket_booster_1_cost.grid(column=self.grid_col_cost,row=self.grid_row_rocket_booster_1, sticky="w")
        self.label_rocket_booster_1_weight = tk.Label(canvas_type, text="0", anchor="w")
        self.label_rocket_booster_1_weight.grid(column=self.grid_col_weight ,row=self.grid_row_rocket_booster_1, sticky="w")
        self.label_rocket_booster_1_space = tk.Label(canvas_type, text="0", anchor="w")
        self.label_rocket_booster_1_space.grid(column=self.grid_col_spaces,row=self.grid_row_rocket_booster_1, sticky="w")
        self.label_rocket_booster_1_dp = tk.Label(canvas_type, text="0", anchor="w")
        self.label_rocket_booster_1_dp.grid(column=self.grid_col_dp,row=self.grid_row_rocket_booster_1, sticky="w")
        self.label_rocket_booster_1_thrust = tk.Label(canvas_type, text="0", anchor="w")
        self.label_rocket_booster_1_thrust.grid(column=self.grid_col_power_factors,row=self.grid_row_rocket_booster_1, sticky="w")

        self.var_rocket_booster_pounds_qty_1 = tk.IntVar(value=0)
        self.entry_rocket_booster_pounds_qty = ttk.Entry(canvas_type, textvariable=self.var_rocket_booster_pounds_qty_1, width=3)
        self.entry_rocket_booster_pounds_qty.grid(column=self.grid_col_qty,row=self.grid_row_rocket_booster_1, sticky="w")
        self.var_rocket_booster_pounds_qty_1.trace_add("write", self.on_changed_rocket_booster_pounds_1)

        self.button_rocket_booster_pounds_1_qty_up = tk.Button(canvas_type, text=up_arrow, command=self.on_button_rocket_booster_pounds_1_qty_up)
        self.button_rocket_booster_pounds_1_qty_up.grid(column=self.grid_left_up_button,row=self.grid_row_rocket_booster_1, sticky="w")
        self.button_rocket_booster_pounds_1_qty_down = tk.Button(canvas_type, text=down_arrow, command=self.on_button_rocket_booster_pounds_1_qty_down)
        self.button_rocket_booster_pounds_1_qty_down.grid(column=self.grid_left_down_button,row=self.grid_row_rocket_booster_1, sticky="w")

    def on_changed_rocket_booster_pounds_1(self, *args):
        rocket_boost_qty_1 = self.var_rocket_booster_pounds_qty_1.get()
        self.label_rocket_booster_1_cost.configure(text=str(25*rocket_boost_qty_1))
        self.label_rocket_booster_1_weight.configure(text=str(rocket_boost_qty_1))
        space_value: int = 0
        if rocket_boost_qty_1 == 0:
            space_value = 0
        elif rocket_boost_qty_1 <= 100:
            space_value = 1
        else:
            space_value = math.ceil(float(rocket_boost_qty_1 / 100.0))
        self.label_rocket_booster_1_space.configure(text=str(space_value))
        self.label_rocket_booster_1_dp.configure(text=str(space_value))
        self.recalculate() # we need the accurate current_total weight to calculate thrust

        current_total_weight: float = float(self.label_total_weight.cget("text")) #this could be a decimal
        if current_total_weight > 0.0:
            thrust_value = int(rocket_boost_qty_1 * 1000 / current_total_weight)
        else:
            thrust_value = 0
        thrust_value = math.floor(thrust_value / 5) * 5
        self.label_rocket_booster_1_thrust.configure(text=str(thrust_value))
        self.recalculate() #and re-re-calculate

    def on_button_rocket_booster_pounds_1_qty_up(self):
        rocket_boost_qty_1 = self.var_rocket_booster_pounds_qty_1.get()
        rocket_boost_qty_1 = rocket_boost_qty_1 + 1
        self.var_rocket_booster_pounds_qty_1.set(rocket_boost_qty_1)
        self.on_changed_rocket_booster_pounds_1()

    def on_button_rocket_booster_pounds_1_qty_down(self):
        rocket_boost_qty_1 = self.var_rocket_booster_pounds_qty_1.get()
        rocket_boost_qty_1 = rocket_boost_qty_1 - 1
        rocket_boost_qty_1 = max(rocket_boost_qty_1, 0)
        self.var_rocket_booster_pounds_qty_1.set(rocket_boost_qty_1)
        self.on_changed_rocket_booster_pounds_1()

    def add_dropdown_rocket_boost_facing_1_canvas(self, canvas_type):
        self.selected_rocket_booster_facing_1 = tk.StringVar()
        self.selected_rocket_booster_facing_1.set("Facing")
        options = ["Facing", "Front", "Back", "Left", "Right", "Top", "Underbody"]
        # Create the dropdown widget
        self.rocket_booster_facing_dropdown_1 = ttk.OptionMenu(canvas_type, self.selected_rocket_booster_facing_1, "Facing", *options) #filled elsewhere
        self.rocket_booster_facing_dropdown_1.grid(column=self.grid_col_max_weight, row=self.grid_row_rocket_booster_1, sticky="w")

    ######################################################################
    # Personal Equipment Common Funtions here                            #
    ######################################################################
    def get_personal_equipment_dictionaries(self):
        self.personal_equipment_list = []
        entry_dict: dict = {"Item": "Personal Equipment",                      "Cost": "0",    "GE": "0",   "Weight":   "0", "To-Hit": "0",   "Damage": "",       "Shots": "0",  "CPS": "0",   "WPS": "0",   "Notes": ""}
        self.personal_equipment_list.append(entry_dict)
        entry_dict: dict = {"Item": "- - - Melee Weapons - - -	",             "Cost": "0",    "GE": "0",   "Weight":   "0", "To-Hit": "0",   "Damage": "",       "Shots": "0",  "CPS": "0",   "WPS": "0",   "Notes": ""}
        self.personal_equipment_list.append(entry_dict)
        entry_dict: dict = {"Item": "Axe",                                     "Cost": "50",   "GE": "3",   "Weight":   "4", "To-Hit": "9",   "Damage": "1d",     "Shots": "0",  "CPS": "0",   "WPS": "0",   "Notes": ""}
        self.personal_equipment_list.append(entry_dict)
        entry_dict: dict = {"Item": "Bowie Knife / Bayonet",                   "Cost": "50",   "GE": "1",   "Weight": "0.5", "To-Hit": "8",   "Damage": "1d-2",   "Shots": "0",  "CPS": "0",   "WPS": "0",   "Notes": ""}
        self.personal_equipment_list.append(entry_dict)
        entry_dict: dict = {"Item": "Chainsaw",                                "Cost": "150",  "GE": "4",   "Weight":  "15", "To-Hit": "9",   "Damage": "1d+1",   "Shots": "0",  "CPS": "0",   "WPS": "0",   "Notes": ""}
        self.personal_equipment_list.append(entry_dict)
        entry_dict: dict = {"Item": "Hatchet",                                 "Cost": "25",   "GE": "1",   "Weight":   "2", "To-Hit": "8",   "Damage": "1d-2",   "Shots": "0",  "CPS": "0",   "WPS": "0",   "Notes": ""}
        self.personal_equipment_list.append(entry_dict)
        entry_dict: dict = {"Item": "Knife",                                   "Cost": "25",   "GE": "1",   "Weight": "0.5", "To-Hit": "5",   "Damage": "1d-4",   "Shots": "0",  "CPS": "0",   "WPS": "0",   "Notes": ""}
        self.personal_equipment_list.append(entry_dict)
        entry_dict: dict = {"Item": "Machete",                                 "Cost": "75",   "GE": "2",   "Weight":   "3", "To-Hit": "7",   "Damage": "1d-3",   "Shots": "0",  "CPS": "0",   "WPS": "0",   "Notes": ""}
        self.personal_equipment_list.append(entry_dict)
        entry_dict: dict = {"Item": "Spear",                                   "Cost": "50",   "GE": "3",   "Weight":   "5", "To-Hit": "7",   "Damage": "1d-2",   "Shots": "0",  "CPS": "0",   "WPS": "0",   "Notes": ""}
        self.personal_equipment_list.append(entry_dict)
        entry_dict: dict = {"Item": "Sword",                                   "Cost": "200",  "GE": "2",   "Weight":   "3", "To-Hit": "7",   "Damage": "1d-1",   "Shots": "0",  "CPS": "0",   "WPS": "0",   "Notes": ""}
        self.personal_equipment_list.append(entry_dict)
        entry_dict: dict = {"Item": "",                                        "Cost": "0",    "GE": "0",   "Weight":   "0", "To-Hit": "0",   "Damage": "",       "Shots": "0",  "CPS": "0",   "WPS": "0",   "Notes": ""}
        self.personal_equipment_list.append(entry_dict)
        entry_dict: dict = {"Item": "- - - Firepower Weapons - - -",           "Cost": "0",    "GE": "0",   "Weight":   "0", "To-Hit": "0",   "Damage": "",       "Shots": "0",  "CPS": "0",   "WPS": "0",   "Notes": ""}
        self.personal_equipment_list.append(entry_dict)
        entry_dict: dict = {"Item": "Portable Flamethrower",                   "Cost": "875",  "GE": "5",   "Weight":  "75", "To-Hit": "6",   "Damage": "1d",     "Shots": "5",  "CPS": "25",  "WPS": "5",   "Notes": ""}
        self.personal_equipment_list.append(entry_dict)                        #Loaded
        entry_dict: dict = {"Item": "Portable Flamethrower, HT Fuel",          "Cost": "1250", "GE": "5",   "Weight":  "87.5", "To-Hit": "6", "Damage": "1d+2",   "Shots": "5",  "CPS": "100", "WPS": "7.5", "Notes": ""}
        self.personal_equipment_list.append(entry_dict)                        #Loaded
        entry_dict: dict = {"Item": "Portable StickyFoam Sprayer",             "Cost": "1100", "GE": "5",   "Weight":  "110", "To-Hit": "6",  "Damage": "*",      "Shots": "10", "CPS": "30",  "WPS": "2",   "Notes": ""}
        self.personal_equipment_list.append(entry_dict)                        #Loaded
        entry_dict: dict = {"Item": "Grenade Launcher",                        "Cost": "300",  "GE": "2",   "Weight":  "11", "To-Hit": "7",   "Damage": "",       "Shots": "5",  "CPS": "0",   "WPS": "0",   "Notes": ""}
        self.personal_equipment_list.append(entry_dict)                        #Loaded
        entry_dict: dict = {"Item": "Rifle Launching for Grenade",             "Cost": "150",  "GE": "0",   "Weight":   "0", "To-Hit": "0",   "Damage": "",       "Shots": "0",  "CPS": "0",   "WPS": "0",   "Notes": ""}
        self.personal_equipment_list.append(entry_dict)                        #Loaded
        entry_dict: dict = {"Item": "Under-Barrel Grenade Launcher",           "Cost": "200",  "GE": "1",   "Weight":   "8", "To-Hit": "7",   "Damage": "",       "Shots": "1",  "CPS": "0",   "WPS": "0",   "Notes": ""}
        self.personal_equipment_list.append(entry_dict)                        #Loaded
        entry_dict: dict = {"Item": "Laser LAW",                               "Cost": "2000", "GE": "3",   "Weight":  "25", "To-Hit": "6",   "Damage": "3d",     "Shots": "1",  "CPS": "0",   "WPS": "0",   "Notes": ""}
        self.personal_equipment_list.append(entry_dict)                        #Loaded
        entry_dict: dict = {"Item": "Laser VLAW",                              "Cost": "1500", "GE": "2",   "Weight":  "18", "To-Hit": "6",   "Damage": "2d",     "Shots": "1",  "CPS": "0",   "WPS": "0",   "Notes": ""}
        self.personal_equipment_list.append(entry_dict)                        #Loaded
        entry_dict: dict = {"Item": "Laser Rifle",                             "Cost": "4500", "GE": "2",   "Weight":  "10", "To-Hit": "6",   "Damage": "1d",     "Shots": "2",  "CPS": "0",   "WPS": "0",   "Notes": ""}
        self.personal_equipment_list.append(entry_dict)                        #Loaded
        entry_dict: dict = {"Item": "Laser Rifle Power Pack",                  "Cost": "1000", "GE": "3",   "Weight":  "30", "To-Hit": "0",   "Damage": "",       "Shots": "20", "CPS": "0",   "WPS": "0",   "Notes": ""}
        self.personal_equipment_list.append(entry_dict)                        #Loaded
        entry_dict: dict = {"Item": "AV Rifle",                                "Cost": "650",  "GE": "3",   "Weight":  "25", "To-Hit": "8",   "Damage": "1d",     "Shots": "10", "CPS": "5",   "WPS": "0",   "Notes": ""}
        self.personal_equipment_list.append(entry_dict)                        #Loaded
        entry_dict: dict = {"Item": "Heavy AV Rifle",                          "Cost": "900",  "GE": "4",   "Weight":  "30", "To-Hit": "8",   "Damage": "1d+3",   "Shots": "10", "CPS": "10",  "WPS": "0",   "Notes": ""}
        self.personal_equipment_list.append(entry_dict)                        #Loaded
        entry_dict: dict = {"Item": "Assault Rifle",                           "Cost": "550",  "GE": "3",   "Weight":  "12", "To-Hit": "7",   "Damage": "1d+1",   "Shots": "10", "CPS": "15",  "WPS": "0",   "Notes": ""}
        self.personal_equipment_list.append(entry_dict)                        #Loaded
        entry_dict: dict = {"Item": "Assault Rifle w/HP Ammo",                 "Cost": "700",  "GE": "3",   "Weight":  "12", "To-Hit": "7",   "Damage": "1d+2",   "Shots": "10", "CPS": "30",  "WPS": "0",   "Notes": ""}
        self.personal_equipment_list.append(entry_dict)                        #Loaded
        entry_dict: dict = {"Item": "Gauss Rifle",                             "Cost": "1800", "GE": "2",   "Weight":   "9", "To-Hit": "6",   "Damage": "1d",     "Shots": "20", "CPS": "15",  "WPS": "0",   "Notes": ""}
        self.personal_equipment_list.append(entry_dict)                        #Loaded
        entry_dict: dict = {"Item": "Needle Gun",                              "Cost": "120",  "GE": "2",   "Weight":   "6", "To-Hit": "6",   "Damage": "",       "Shots": "20", "CPS": "1",   "WPS": "0",   "Notes": ""}
        self.personal_equipment_list.append(entry_dict)                        #Loaded
        entry_dict: dict = {"Item": "Rifle",                                   "Cost": "140",  "GE": "2",   "Weight":  "10", "To-Hit": "7",   "Damage": "3 hits", "Shots": "20", "CPS": "1",   "WPS": "0",   "Notes": ""}
        self.personal_equipment_list.append(entry_dict)                        #Loaded
        entry_dict: dict = {"Item": "Rifle w/HP Ammo",                         "Cost": "160",  "GE": "2",   "Weight":  "10", "To-Hit": "7",   "Damage": "4 hits", "Shots": "20", "CPS": "2",   "WPS": "0",   "Notes": ""}
        self.personal_equipment_list.append(entry_dict)                        #Loaded
        entry_dict: dict = {"Item": "Shotgun",                                 "Cost": "130",  "GE": "2",   "Weight":   "8", "To-Hit": "6",   "Damage": "2 hits", "Shots": "10", "CPS": "1",   "WPS": "0",   "Notes": ""}
        self.personal_equipment_list.append(entry_dict)                        #Loaded
        entry_dict: dict = {"Item": "Double-Barrel Shotgun",                   "Cost": "220",  "GE": "3",   "Weight":  "12", "To-Hit": "6",   "Damage": "2 hits", "Shots": "10", "CPS": "1",   "WPS": "0",   "Notes": ""}
        self.personal_equipment_list.append(entry_dict)                        #Loaded
        entry_dict: dict = {"Item": "Stun Gun",                                "Cost": "750",  "GE": "2",   "Weight":  "15", "To-Hit": "7",   "Damage": "",       "Shots": "0",  "CPS": "0",   "WPS": "0",   "Notes": ""}
        self.personal_equipment_list.append(entry_dict)
        entry_dict: dict = {"Item": "Submachine Gun",                          "Cost": "370",  "GE": "2",   "Weight":   "9", "To-Hit": "6",   "Damage": "1d",     "Shots": "10", "CPS": "12",  "WPS": "0",   "Notes": ""}
        self.personal_equipment_list.append(entry_dict)                        #Loaded
        entry_dict: dict = {"Item": "Submachine Gun w/HP Ammo",                "Cost": "490",  "GE": "2",   "Weight":   "9", "To-Hit": "6",   "Damage": "1d+1",   "Shots": "10", "CPS": "24",  "WPS": "0",   "Notes": ""}
        self.personal_equipment_list.append(entry_dict)                        #Loaded
        entry_dict: dict = {"Item": "Derringer",                               "Cost": "31",   "GE": "0",   "Weight": "0.5", "To-Hit": "8",   "Damage": "2 hits", "Shots": "1",  "CPS": "1",   "WPS": "0",   "Notes": ""}
        self.personal_equipment_list.append(entry_dict)                        #Loaded
        entry_dict: dict = {"Item": "Light Pistol",                            "Cost": "83",   "GE": "1",   "Weight":   "1", "To-Hit": "8",   "Damage": "1 hit",  "Shots": "8",  "CPS": "1",   "WPS": "0",   "Notes": ""}
        self.personal_equipment_list.append(entry_dict)                        #Loaded
        entry_dict: dict = {"Item": "Light Pistol with HP Ammo",               "Cost": "91",   "GE": "1",   "Weight":   "1", "To-Hit": "8",   "Damage": "2 hits", "Shots": "8",  "CPS": "2",   "WPS": "0",   "Notes": ""}
        self.personal_equipment_list.append(entry_dict)                        #Loaded
        entry_dict: dict = {"Item": "Heavy Pistol",                            "Cost": "108",  "GE": "1",   "Weight":   "3", "To-Hit": "7",   "Damage": "2 hits", "Shots": "8",  "CPS": "1",   "WPS": "0",   "Notes": ""}
        self.personal_equipment_list.append(entry_dict)                        #Loaded
        entry_dict: dict = {"Item": "Heavy Pistol with HP Ammo",               "Cost": "116",  "GE": "1",   "Weight":   "3", "To-Hit": "7",   "Damage": "3 hits", "Shots": "8",  "CPS": "2",   "WPS": "0",   "Notes": ""}
        self.personal_equipment_list.append(entry_dict)                        #Loaded
        entry_dict: dict = {"Item": "Gauss Pistol",                            "Cost": "600",  "GE": "1",   "Weight":   "2", "To-Hit": "6",   "Damage": "1d-2",   "Shots": "20", "CPS": "5",   "WPS": "0",   "Notes": ""}
        self.personal_equipment_list.append(entry_dict)                        #Loaded
        entry_dict: dict = {"Item": "Gauss Pistol Power Pack",                 "Cost": "1000", "GE": "3",   "Weight":   "0", "To-Hit": "0",   "Damage": "",       "Shots": "0",  "CPS": "0",   "WPS": "0",   "Notes": ""}
        self.personal_equipment_list.append(entry_dict)
        entry_dict: dict = {"Item": "Needle Pistol",                           "Cost": "50",   "GE": "1",   "Weight":   "2", "To-Hit": "7",   "Damage": "",       "Shots": "0",  "CPS": "0",   "WPS": "0",   "Notes": ""}
        self.personal_equipment_list.append(entry_dict)
        entry_dict: dict = {"Item": "Machine Pistol",                          "Cost": "322",  "GE": "1",   "Weight":   "5", "To-Hit": "7",   "Damage": "1d-2",   "Shots": "6",  "CPS": "12",  "WPS": "0",   "Notes": ""}
        self.personal_equipment_list.append(entry_dict)                        #Loaded
        entry_dict: dict = {"Item": "Handheld Flare Launcher",                 "Cost": "350",  "GE": "1",   "Weight":   "6", "To-Hit": "0",   "Damage": "",       "Shots": "5",  "CPS": "10",  "WPS": "0",   "Notes": ""}
        self.personal_equipment_list.append(entry_dict)                        #Loaded
        entry_dict: dict = {"Item": "Bazooka",                                 "Cost": "1550", "GE": "4",   "Weight":  "20", "To-Hit": "8",   "Damage": "3d",     "Shots": "1",  "CPS": "50",  "WPS": "0",   "Notes": ""}
        self.personal_equipment_list.append(entry_dict)                        #Loaded
        entry_dict: dict = {"Item": "Bazooka w/AP Ammo",                       "Cost": "1575", "GE": "4",   "Weight":  "20", "To-Hit": "8",   "Damage": "3d+3",   "Shots": "1",  "CPS": "75",  "WPS": "0",   "Notes": ""}
        self.personal_equipment_list.append(entry_dict)                        #Loaded
        entry_dict: dict = {"Item": "Gyroslugger, 1 barrel",                   "Cost": "1200", "GE": "2",   "Weight":  "14", "To-Hit": "8",   "Damage": "",       "Shots": "1",  "CPS": "0",   "WPS": "0",   "Notes": ""}
        self.personal_equipment_list.append(entry_dict)
        entry_dict: dict = {"Item": "Gyroslugger, 2 barrel",                   "Cost": "1500", "GE": "3",   "Weight":  "18", "To-Hit": "8",   "Damage": "",       "Shots": "2",  "CPS": "0",   "WPS": "0",   "Notes": ""}
        self.personal_equipment_list.append(entry_dict)
        entry_dict: dict = {"Item": "Under-Barrel Gyroslugger",                "Cost": "1200", "GE": "1",   "Weight":   "8", "To-Hit": "8",   "Damage": "",       "Shots": "1",  "CPS": "0",   "WPS": "0",   "Notes": ""}
        self.personal_equipment_list.append(entry_dict)
        entry_dict: dict = {"Item": "LAW",                                     "Cost": "500",  "GE": "2",   "Weight":  "20", "To-Hit": "8",   "Damage": "2d",     "Shots": "1",  "CPS": "0",   "WPS": "0",   "Notes": ""}
        self.personal_equipment_list.append(entry_dict)
        entry_dict: dict = {"Item": "LAW w/AP Ammo",                           "Cost": "750",  "GE": "2",   "Weight":  "20", "To-Hit": "8",   "Damage": "2d+2",   "Shots": "1",  "CPS": "0",   "WPS": "0",   "Notes": ""}
        self.personal_equipment_list.append(entry_dict)
        entry_dict: dict = {"Item": "VLAW",                                    "Cost": "200",  "GE": "1",   "Weight":  "10", "To-Hit": "8",   "Damage": "1d",     "Shots": "1",  "CPS": "0",   "WPS": "0",   "Notes": ""}
        self.personal_equipment_list.append(entry_dict)
        entry_dict: dict = {"Item": "VLAW w/AP Ammo",                          "Cost": "300",  "GE": "1",   "Weight":  "10", "To-Hit": "8",   "Damage": "1d+1",   "Shots": "1",  "CPS": "0",   "WPS": "0",   "Notes": ""}
        self.personal_equipment_list.append(entry_dict)
        entry_dict: dict = {"Item": "M-P Rocket Launcher",                     "Cost": "1000", "GE": "6",   "Weight":  "35", "To-Hit": "9",   "Damage": "2d",     "Shots": "4",  "CPS": "50",  "WPS": "0",   "Notes": ""}
        self.personal_equipment_list.append(entry_dict)                        #Loaded
        entry_dict: dict = {"Item": "M-P Rocket Launcher w/AP Ammo",           "Cost": "1100", "GE": "6",   "Weight":  "35", "To-Hit": "9",   "Damage": "2d+2",   "Shots": "4",  "CPS": "75",  "WPS": "0",   "Notes": ""}
        self.personal_equipment_list.append(entry_dict)                        #Loaded
        entry_dict: dict = {"Item": "Portable Micromissile Launcher",          "Cost": "900",  "GE": "5",   "Weight":  "30", "To-Hit": "8",   "Damage": "1d",     "Shots": "8",  "CPS": "30",  "WPS": "0",   "Notes": ""}
        self.personal_equipment_list.append(entry_dict)                        #Loaded
        entry_dict: dict = {"Item": "Portable Micromissile Launcher, AP Ammo", "Cost": "1140", "GE": "5",   "Weight":  "30", "To-Hit": "8",   "Damage": "1d+1",   "Shots": "8",  "CPS": "45",  "WPS": "0",   "Notes": ""}
        self.personal_equipment_list.append(entry_dict)                        #Loaded
        entry_dict: dict = {"Item": "Stinger SAM",                             "Cost": "1000", "GE": "5",   "Weight":  "30", "To-Hit": "7/9", "Damage": "4d",     "Shots": "1",  "CPS": "0",   "WPS": "0",   "Notes": ""}
        self.personal_equipment_list.append(entry_dict)
        entry_dict: dict = {"Item": "Stinger SAM w/AP Ammo",                   "Cost": "1500", "GE": "5",   "Weight":  "30", "To-Hit": "7/9", "Damage": "4d+4",   "Shots": "1",  "CPS": "0",   "WPS": "0",   "Notes": ""}
        self.personal_equipment_list.append(entry_dict)
        entry_dict: dict = {"Item": "",                                        "Cost": "0",    "GE": "0",   "Weight":   "0", "To-Hit": "0",   "Damage": "",       "Shots": "0",  "CPS": "0",   "WPS": "0",   "Notes": ""}
        self.personal_equipment_list.append(entry_dict)
        entry_dict: dict = {"Item": "- - - Grenades - - -",                    "Cost": "0",    "GE": "0",   "Weight":   "0", "To-Hit": "0",   "Damage": "",       "Shots": "0",  "CPS": "0",   "WPS": "0",   "Notes": ""}
        self.personal_equipment_list.append(entry_dict)
        entry_dict: dict = {"Item": "Concussion Grenade",                      "Cost": "40",   "GE": "1",   "Weight":   "1", "To-Hit": "0",   "Damage": "Spec.",  "Shots": "0",  "CPS": "0",   "WPS": "0",   "Notes": "See table in UACFH, page 134"}
        self.personal_equipment_list.append(entry_dict)
        entry_dict: dict = {"Item": "Explosive Grenade",                       "Cost": "25",   "GE": "1",   "Weight":   "1", "To-Hit": "0",   "Damage": "1d",	  "Shots": "0",  "CPS": "0",   "WPS": "0",   "Notes": "1d to vehicles within 1 inch, 1d to all else within 2 inches"}
        self.personal_equipment_list.append(entry_dict)
        entry_dict: dict = {"Item": "Fake Grenade",                            "Cost": "5",    "GE": "1",   "Weight":   "1", "To-Hit": "0",   "Damage": "",       "Shots": "0",  "CPS": "0",   "WPS": "0",   "Notes": ""}
        self.personal_equipment_list.append(entry_dict)
        entry_dict: dict = {"Item": "Flaming Oil Grenade",                     "Cost": "75",   "GE": "1",   "Weight":   "1", "To-Hit": "0",   "Damage": "1d-2",	  "Shots": "0",  "CPS": "0",   "WPS": "0",   "Notes": "Creates 1/2 inch x 1/2 inch slick, ignites after 1 phase"}
        self.personal_equipment_list.append(entry_dict)
        entry_dict: dict = {"Item": "High-Temp Flaming Oil Grenade",           "Cost": "300",  "GE": "1",   "Weight":   "1", "To-Hit": "0",   "Damage": "1d",	  "Shots": "0",  "CPS": "0",   "WPS": "0",   "Notes": "Creates 1/2 inch x 1/2 inch slick, ignites after 1 phase"}
        self.personal_equipment_list.append(entry_dict)
        entry_dict: dict = {"Item": "Flash Grenade",                           "Cost": "150",  "GE": "1",   "Weight":   "1", "To-Hit": "0",   "Damage": "Blind",  "Shots": "0",  "CPS": "0",   "WPS": "0",   "Notes": "2 inch  range, blinds for 2 seconds at night. No day effect"}
        self.personal_equipment_list.append(entry_dict)
        entry_dict: dict = {"Item": "Flechette Grenade",                       "Cost": "20",   "GE": "1",   "Weight":   "1", "To-Hit": "0",   "Damage": "1d",	  "Shots": "0",  "CPS": "0",   "WPS": "0",   "Notes": "1d to peds in 2 inch range, no dmg to vehicles or tires"}
        self.personal_equipment_list.append(entry_dict)
        entry_dict: dict = {"Item": "Foam Grenade",                            "Cost": "30",   "GE": "1",   "Weight":   "1", "To-Hit": "0",   "Damage": "",		  "Shots": "0",  "CPS": "0",   "WPS": "0",   "Notes": "1 on 1d6 to put out fire if 1/2 inch from fire; cumulative ea."}
        self.personal_equipment_list.append(entry_dict)
        entry_dict: dict = {"Item": "Paint Grenade",                           "Cost": "20",   "GE": "1",   "Weight":   "1", "To-Hit": "0",   "Damage": "Paint",  "Shots": "0",  "CPS": "0",   "WPS": "0",   "Notes": "1 inch x 1 inch standard paint cloud"}
        self.personal_equipment_list.append(entry_dict)
        entry_dict: dict = {"Item": "Smoke Grenade",                           "Cost": "20",   "GE": "1",   "Weight":   "1", "To-Hit": "0",   "Damage": "Smoke",  "Shots": "0",  "CPS": "0",   "WPS": "0",   "Notes": "1 inch x 1 inch standard smoke cloud"}
        self.personal_equipment_list.append(entry_dict)
        entry_dict: dict = {"Item": "Tear Gas Grenade",                        "Cost": "30",   "GE": "1",   "Weight":   "1", "To-Hit": "0",   "Damage": "Tgas",	  "Shots": "0",  "CPS": "0",   "WPS": "0",   "Notes": "1 inch x 1 inch Tear gas cloud; see rules in UACFG page 135"}
        self.personal_equipment_list.append(entry_dict)
        entry_dict: dict = {"Item": "Thermite Grenade",                        "Cost": "100",  "GE": "1",   "Weight":   "1", "To-Hit": "0",   "Damage": "1d",     "Shots": "0",  "CPS": "0",   "WPS": "0",   "Notes": "1/2 inch range; does full damage to everything; Burn: 2/1"}
        self.personal_equipment_list.append(entry_dict)
        entry_dict: dict = {"Item": "White Phosphorus Grenade",                "Cost": "75",   "GE": "1",   "Weight":   "1", "To-Hit": "0",   "Damage": "1d",     "Shots": "0",  "CPS": "0",   "WPS": "0",   "Notes": "1/2 dam. To vehicles; Burn:2/1; leaves 1/2x1/2 HS cloud"}
        self.personal_equipment_list.append(entry_dict)
        entry_dict: dict = {"Item": "Impact Fuse",                             "Cost": "50",   "GE": "0",   "Weight":   "0", "To-Hit": "0",   "Damage": "",       "Shots": "0",  "CPS": "0",   "WPS": "0",   "Notes": ""}
        self.personal_equipment_list.append(entry_dict)
        entry_dict: dict = {"Item": "",                                        "Cost": "0",    "GE": "0",   "Weight":   "0", "To-Hit": "0",   "Damage": "",       "Shots": "0",  "CPS": "0",   "WPS": "0",   "Notes": ""}
        self.personal_equipment_list.append(entry_dict)
        entry_dict: dict = {"Item": "- - - GyroSlugger Ammo - - -",            "Cost": "0",    "GE": "0",   "Weight":   "0", "To-Hit": "0",   "Damage": "",       "Shots": "0",  "CPS": "0",   "WPS": "0",   "Notes": ""}
        self.personal_equipment_list.append(entry_dict)
        entry_dict: dict = {"Item": "Standard Gyro Round",                     "Cost": "100",  "GE": "1",   "Weight":   "0", "To-Hit": "0",   "Damage": "2d",     "Shots": "0",  "CPS": "0",   "WPS": "0",   "Notes": ""}
        self.personal_equipment_list.append(entry_dict)
        entry_dict: dict = {"Item": "AP Gyro Round",                           "Cost": "150",  "GE": "1",   "Weight":   "0", "To-Hit": "0",   "Damage": "2d+2",   "Shots": "0",  "CPS": "0",   "WPS": "0",   "Notes": ""}
        self.personal_equipment_list.append(entry_dict)
        entry_dict: dict = {"Item": "HESH Gyro Round",                         "Cost": "250",  "GE": "1",   "Weight":   "0", "To-Hit": "0",   "Damage": "2d",     "Shots": "0",  "CPS": "0",   "WPS": "0",   "Notes": ""}
        self.personal_equipment_list.append(entry_dict)
        entry_dict: dict = {"Item": "Incendiary Gyro Round",                   "Cost": "300",  "GE": "1",   "Weight":   "0", "To-Hit": "0",   "Damage": "1d",     "Shots": "0",  "CPS": "0",   "WPS": "0",   "Notes": "Burst Effect, Burn: 2/1"}
        self.personal_equipment_list.append(entry_dict)
        entry_dict: dict = {"Item": "Flare Gyro Round",                        "Cost": "50",   "GE": "1",   "Weight":   "0", "To-Hit": "0",   "Damage": "1/2d",   "Shots": "0",  "CPS": "0",   "WPS": "0",   "Notes": "Lights 10 inch radius; burn 1/0"}
        self.personal_equipment_list.append(entry_dict)
        entry_dict: dict = {"Item": "Smoke Gyro Round",                        "Cost": "50",   "GE": "1",   "Weight":   "0", "To-Hit": "0",   "Damage": "Smoke",  "Shots": "0",  "CPS": "0",   "WPS": "0",   "Notes": "1 inch x 1 inch standard smoke cloud"}
        self.personal_equipment_list.append(entry_dict)
        entry_dict: dict = {"Item": "Paint Gyro Round",                        "Cost": "100",  "GE": "1",   "Weight":   "0", "To-Hit": "0",   "Damage": "Paint",  "Shots": "0",  "CPS": "0",   "WPS": "0",   "Notes": "1 inch x 1 inch standard paint cloud"}
        self.personal_equipment_list.append(entry_dict)
        entry_dict: dict = {"Item": "",                                        "Cost": "0",    "GE": "0",   "Weight":   "0", "To-Hit": "0",   "Damage": "",       "Shots": "0",  "CPS": "0",   "WPS": "0",   "Notes": ""}
        self.personal_equipment_list.append(entry_dict)
        entry_dict: dict = {"Item": "- - - Equipment - - -",                   "Cost": "0",    "GE": "0",   "Weight":   "0", "To-Hit": "0",   "Damage": "",       "Shots": "0",  "CPS": "0",   "WPS": "0",   "Notes": ""}
        self.personal_equipment_list.append(entry_dict)
        entry_dict: dict = {"Item": "Ammo Clip",                               "Cost": "50",   "GE": "0.5", "Weight":   "1", "To-Hit": "0",   "Damage": "",       "Shots": "0",  "CPS": "0",   "WPS": "0",   "Notes": "Must buy ammo separately"}
        self.personal_equipment_list.append(entry_dict)
        entry_dict: dict = {"Item": "SMG and GL Ammo Clip",                    "Cost": "50",   "GE": "1",   "Weight":   "2", "To-Hit": "0",   "Damage": "",       "Shots": "0",  "CPS": "0",   "WPS": "0",   "Notes": "Must buy ammo separately"}
        self.personal_equipment_list.append(entry_dict)
        entry_dict: dict = {"Item": "Extended Ammo Clip",                      "Cost": "80",   "GE": "1",   "Weight":   "1", "To-Hit": "0",   "Damage": "",       "Shots": "0",  "CPS": "0",   "WPS": "0",   "Notes": "Must buy ammo separately, holds 2x normal ammo"}
        self.personal_equipment_list.append(entry_dict)
        entry_dict: dict = {"Item": "SMG Extended Ammo Clip",                  "Cost": "80",   "GE": "2",   "Weight":   "2", "To-Hit": "0",   "Damage": "",       "Shots": "0",  "CPS": "0",   "WPS": "0",   "Notes": "Must buy ammo separately, holds 2x normal ammo"}
        self.personal_equipment_list.append(entry_dict)
        entry_dict: dict = {"Item": "Anti-Toxin Kit",                          "Cost": "25",   "GE": "0.5", "Weight": "0.5", "To-Hit": "0",   "Damage": "",       "Shots": "0",  "CPS": "0",   "WPS": "0",   "Notes": ""}
        self.personal_equipment_list.append(entry_dict)
        entry_dict: dict = {"Item": "Backpack",                                "Cost": "40",   "GE": "5",   "Weight":   "0", "To-Hit": "0",   "Damage": "",       "Shots": "0",  "CPS": "0",   "WPS": "0",   "Notes": "Carries 5 extra GE"}
        self.personal_equipment_list.append(entry_dict)
        entry_dict: dict = {"Item": "Arm. Battle Vest/BA Combo",               "Cost": "475",  "GE": "3",   "Weight":  "15", "To-Hit": "0",   "Damage": "",       "Shots": "0",  "CPS": "0",   "WPS": "0",   "Notes": ""}
        self.personal_equipment_list.append(entry_dict)
        entry_dict: dict = {"Item": "Battle Vest",                             "Cost": "75",   "GE": "3",   "Weight":   "5", "To-Hit": "0",   "Damage": "",       "Shots": "0",  "CPS": "0",   "WPS": "0",   "Notes": "Holds 1 pistol, 2 grenades, 2 ammo clips, 1 knife."}
        self.personal_equipment_list.append(entry_dict)
        entry_dict: dict = {"Item": "Battle Vest, Armored",                    "Cost": "225",  "GE": "3",   "Weight":   "5", "To-Hit": "0",   "Damage": "",       "Shots": "0",  "CPS": "0",   "WPS": "0",   "Notes": "Same as BV, +3 DP, takes damage on 1-4 on 1d"}
        self.personal_equipment_list.append(entry_dict)
        entry_dict: dict = {"Item": "Body Armor",                              "Cost": "250",  "GE": "0",   "Weight":  "10", "To-Hit": "0",   "Damage": "",       "Shots": "0",  "CPS": "0",   "WPS": "0",   "Notes": "+3DP"}
        self.personal_equipment_list.append(entry_dict)
        entry_dict: dict = {"Item": "Body Armor, Blended",                     "Cost": "750",  "GE": "5",   "Weight":   "0", "To-Hit": "0",   "Damage": "",       "Shots": "0",  "CPS": "0",   "WPS": "0",   "Notes": "+3DP, looks like normal clothing"}
        self.personal_equipment_list.append(entry_dict)
        entry_dict: dict = {"Item": "Body Armor, Improved",                    "Cost": "1500", "GE": "1",   "Weight":  "25", "To-Hit": "0",   "Damage": "",       "Shots": "0",  "CPS": "0",   "WPS": "0",   "Notes": "+6DP; reflex reduced by 1"}
        self.personal_equipment_list.append(entry_dict)
        entry_dict: dict = {"Item": "Body Armor, Improved, Blended",           "Cost": "5000", "GE": "1",   "Weight":  "10", "To-Hit": "0",   "Damage": "",       "Shots": "0",  "CPS": "0",   "WPS": "0",   "Notes": "+6DP; reflex reduced by 1', looks like clothing"}
        self.personal_equipment_list.append(entry_dict)
        entry_dict: dict = {"Item": "Impact Armor",                            "Cost": "2000", "GE": "1",   "Weight":  "25", "To-Hit": "0",   "Damage": "",       "Shots": "0",  "CPS": "0",   "WPS": "0",   "Notes": "+6DP, protects against collisions and falls"}
        self.personal_equipment_list.append(entry_dict)
        entry_dict: dict = {"Item": "Spiked Armor",                            "Cost": "100",  "GE": "1",   "Weight":   "0", "To-Hit": "0",   "Damage": "",       "Shots": "0",  "CPS": "0",   "WPS": "0",   "Notes": ""}
        self.personal_equipment_list.append(entry_dict)
        entry_dict: dict = {"Item": "Duellist's Shades",                       "Cost": "25",   "GE": "0",   "Weight":   "0", "To-Hit": "0",   "Damage": "",       "Shots": "0",  "CPS": "0",   "WPS": "0",   "Notes": "Acts like tinted windshield"}
        self.personal_equipment_list.append(entry_dict)
        entry_dict: dict = {"Item": "Fireproof Suit",                          "Cost": "500",  "GE": "0",   "Weight":   "0", "To-Hit": "0",   "Damage": "",       "Shots": "0",  "CPS": "0",   "WPS": "0",   "Notes": ""}
        self.personal_equipment_list.append(entry_dict)
        entry_dict: dict = {"Item": "Flak Jacket",                             "Cost": "150",  "GE": "3",   "Weight":   "5", "To-Hit": "0",   "Damage": "",       "Shots": "0",  "CPS": "0",   "WPS": "0",   "Notes": "+3DP on 1-4 on 1d; Can wear over body armor"}
        self.personal_equipment_list.append(entry_dict)
        entry_dict: dict = {"Item": "Folding Stock",                           "Cost": "10",   "GE": "1",   "Weight":   "3", "To-Hit": "0",   "Damage": "",       "Shots": "0",  "CPS": "0",   "WPS": "0",   "Notes": ""}
        self.personal_equipment_list.append(entry_dict)
        entry_dict: dict = {"Item": "Gas Mask",                                "Cost": "30",   "GE": "1",   "Weight":   "3", "To-Hit": "0",   "Damage": "",       "Shots": "0",  "CPS": "0",   "WPS": "0",   "Notes": ""}
        self.personal_equipment_list.append(entry_dict)
        entry_dict: dict = {"Item": "Gas Mask, No Paint",                      "Cost": "50",   "GE": "1",   "Weight":   "3", "To-Hit": "0",   "Damage": "",       "Shots": "0",  "CPS": "0",   "WPS": "0",   "Notes": ""}
        self.personal_equipment_list.append(entry_dict)
        entry_dict: dict = {"Item": "Hazard Detector",                         "Cost": "250",  "GE": "0",   "Weight":   "0", "To-Hit": "0",   "Damage": "",       "Shots": "0",  "CPS": "0",   "WPS": "0",   "Notes": ""}
        self.personal_equipment_list.append(entry_dict)
        entry_dict: dict = {"Item": "IFF Sender	100",                          "Cost": "1",    "GE": "0",   "Weight":   "0", "To-Hit": "0",   "Damage": "",       "Shots": "0",  "CPS": "0",   "WPS": "0",   "Notes": ""}
        self.personal_equipment_list.append(entry_dict)
        entry_dict: dict = {"Item": "IR Goggles",                              "Cost": "750",  "GE": "1",   "Weight":   "0", "To-Hit": "0",   "Damage": "",       "Shots": "0",  "CPS": "0",   "WPS": "0",   "Notes": ""}
        self.personal_equipment_list.append(entry_dict)
        entry_dict: dict = {"Item": "Laser Targeting Scope",                   "Cost": "500",  "GE": "1",   "Weight":   "0", "To-Hit": "0",   "Damage": "",       "Shots": "0",  "CPS": "0",   "WPS": "0",   "Notes": "+1 to hit; may be tuned to rockets"}
        self.personal_equipment_list.append(entry_dict)
        entry_dict: dict = {"Item": "Light Intensifier Goggles",               "Cost": "300",  "GE": "1",   "Weight":   "0", "To-Hit": "0",   "Damage": "",       "Shots": "0",  "CPS": "0",   "WPS": "0",   "Notes": ""}
        self.personal_equipment_list.append(entry_dict)
        entry_dict: dict = {"Item": "Light Intensifier Goggles/Gas Mask",      "Cost": "400",  "GE": "1",   "Weight":   "3", "To-Hit": "0",   "Damage": "",       "Shots": "0",  "CPS": "0",   "WPS": "0",   "Notes": ""}
        self.personal_equipment_list.append(entry_dict)
        entry_dict: dict = {"Item": "Limpet Mine",                             "Cost": "60",   "GE": "1",   "Weight":   "3", "To-Hit": "0",   "Damage": "",       "Shots": "0",  "CPS": "0",   "WPS": "0",   "Notes": "1d+1 damage"}
        self.personal_equipment_list.append(entry_dict)
        entry_dict: dict = {"Item": "Limpet Mine, Heavy",                      "Cost": "250",  "GE": "2",   "Weight":  "10", "To-Hit": "0",   "Damage": "",       "Shots": "0",  "CPS": "0",   "WPS": "0",   "Notes": "3d damage"}
        self.personal_equipment_list.append(entry_dict)
        entry_dict: dict = {"Item": "Medikit",                                 "Cost": "1000", "GE": "0",   "Weight":  "50", "To-Hit": "0",   "Damage": "",       "Shots": "0",  "CPS": "0",   "WPS": "0",   "Notes": "3 DP, 50 lbs; takes 1 vehicular space"}
        self.personal_equipment_list.append(entry_dict)
        entry_dict: dict = {"Item": "Portable Medikit",                        "Cost": "750",  "GE": "3",   "Weight":   "0", "To-Hit": "0",   "Damage": "",       "Shots": "0",  "CPS": "0",   "WPS": "0",   "Notes": "Worn like a backpack"}
        self.personal_equipment_list.append(entry_dict)
        entry_dict: dict = {"Item": "Mini-Mechanic",                           "Cost": "50",   "GE": "1",   "Weight": "0.5", "To-Hit": "0",   "Damage": "",       "Shots": "0",  "CPS": "0",   "WPS": "0",   "Notes": ""}
        self.personal_equipment_list.append(entry_dict)
        entry_dict: dict = {"Item": "Pedestrian Chaff Discharger",             "Cost": "75",   "GE": "2",   "Weight":   "5", "To-Hit": "0",   "Damage": "",       "Shots": "0",  "CPS": "0",   "WPS": "0",   "Notes": ""}
        self.personal_equipment_list.append(entry_dict)
        entry_dict: dict = {"Item": "Pedestrian Fake Discharger",              "Cost": "30",   "GE": "2",   "Weight":   "5", "To-Hit": "0",   "Damage": "",       "Shots": "0",  "CPS": "0",   "WPS": "0",   "Notes": ""}
        self.personal_equipment_list.append(entry_dict)
        entry_dict: dict = {"Item": "Pedestrian Flame Cloud Discharger",       "Cost": "175",  "GE": "2",   "Weight":   "5", "To-Hit": "0",   "Damage": "",       "Shots": "0",  "CPS": "0",   "WPS": "0",   "Notes": ""}
        self.personal_equipment_list.append(entry_dict)
        entry_dict: dict = {"Item": "Pedestrian Flaming Oil Discharger",       "Cost": "125",  "GE": "2",   "Weight":   "5", "To-Hit": "0",   "Damage": "",       "Shots": "0",  "CPS": "0",   "WPS": "0",   "Notes": ""}
        self.personal_equipment_list.append(entry_dict)
        entry_dict: dict = {"Item": "Pedestrian FO Discharger, Hi-temp Fuel",  "Cost": "500",  "GE": "2",   "Weight":   "8", "To-Hit": "0",   "Damage": "",       "Shots": "0",  "CPS": "0",   "WPS": "0",   "Notes": ""}
        self.personal_equipment_list.append(entry_dict)
        entry_dict: dict = {"Item": "Pedestrian Flechette Discharger",         "Cost": "75",   "GE": "2",   "Weight":   "5", "To-Hit": "0",   "Damage": "",       "Shots": "0",  "CPS": "0",   "WPS": "0",   "Notes": ""}
        self.personal_equipment_list.append(entry_dict)
        entry_dict: dict = {"Item": "Pedestrian Foam Discharger",              "Cost": "50",   "GE": "2",   "Weight":   "5", "To-Hit": "0",   "Damage": "",       "Shots": "0",  "CPS": "0",   "WPS": "0",   "Notes": ""}
        self.personal_equipment_list.append(entry_dict)
        entry_dict: dict = {"Item": "Pedestrian Hot Smoke Discharger",         "Cost": "90",   "GE": "2",   "Weight":   "5", "To-Hit": "0",   "Damage": "",       "Shots": "0",  "CPS": "0",   "WPS": "0",   "Notes": ""}
        self.personal_equipment_list.append(entry_dict)
        entry_dict: dict = {"Item": "Pedestrian Ice Discharger",               "Cost": "100",  "GE": "2",   "Weight":   "5", "To-Hit": "0",   "Damage": "",       "Shots": "0",  "CPS": "0",   "WPS": "0",   "Notes": ""}
        self.personal_equipment_list.append(entry_dict)
        entry_dict: dict = {"Item": "Pedestrian Oil Discharger",               "Cost": "75",   "GE": "2",   "Weight":   "5", "To-Hit": "0",   "Damage": "",       "Shots": "0",  "CPS": "0",   "WPS": "0",   "Notes": ""}
        self.personal_equipment_list.append(entry_dict)
        entry_dict: dict = {"Item": "Pedestrian Paint Discharger",             "Cost": "65",   "GE": "2",   "Weight":   "5", "To-Hit": "0",   "Damage": "",       "Shots": "0",  "CPS": "0",   "WPS": "0",   "Notes": ""}
        self.personal_equipment_list.append(entry_dict)
        entry_dict: dict = {"Item": "Pedestrian Point Defense Discharger",     "Cost": "125",  "GE": "2",   "Weight":   "5", "To-Hit": "0",   "Damage": "",       "Shots": "0",  "CPS": "0",   "WPS": "0",   "Notes": ""}
        self.personal_equipment_list.append(entry_dict)
        entry_dict: dict = {"Item": "Pedestrian Sand Discharger",              "Cost": "50",   "GE": "2",   "Weight":   "5", "To-Hit": "0",   "Damage": "",       "Shots": "0",  "CPS": "0",   "WPS": "0",   "Notes": ""}
        self.personal_equipment_list.append(entry_dict)
        entry_dict: dict = {"Item": "Pedestrian Smoke Discharger",             "Cost": "75",   "GE": "2",   "Weight":   "5", "To-Hit": "0",   "Damage": "",       "Shots": "0",  "CPS": "0",   "WPS": "0",   "Notes": ""}
        self.personal_equipment_list.append(entry_dict)
        entry_dict: dict = {"Item": "Pedestrian Tear Gas Discharger",          "Cost": "100",  "GE": "2",   "Weight":   "5", "To-Hit": "0",   "Damage": "",       "Shots": "0",  "CPS": "0",   "WPS": "0",   "Notes": ""}
        self.personal_equipment_list.append(entry_dict)
        entry_dict: dict = {"Item": "Portable Fire Extiguisher",               "Cost": "150",  "GE": "3",   "Weight":  "20", "To-Hit": "0",   "Damage": "",       "Shots": "0",  "CPS": "0",   "WPS": "0",   "Notes": "Puts out fire on a 1-2 on 1d6"}
        self.personal_equipment_list.append(entry_dict)
        entry_dict: dict = {"Item": "Portable Searchlight",                    "Cost": "100",  "GE": "2",   "Weight":   "4", "To-Hit": "0",   "Damage": "",       "Shots": "0",  "CPS": "0",   "WPS": "0",   "Notes": ""}
        self.personal_equipment_list.append(entry_dict)
        entry_dict: dict = {"Item": "Riot Shield",                             "Cost": "750",  "GE": "3",   "Weight":  "25", "To-Hit": "0",   "Damage": "",       "Shots": "0",  "CPS": "0",   "WPS": "0",   "Notes": "7DP when carried protects on 1-4 on 1d6"}
        self.personal_equipment_list.append(entry_dict)
        entry_dict: dict = {"Item": "Tinted Goggles",                          "Cost": "20",   "GE": "0",   "Weight":   "0", "To-Hit": "0",   "Damage": "",       "Shots": "0",  "CPS": "0",   "WPS": "0",   "Notes": "Acts as tinted windshield"}
        self.personal_equipment_list.append(entry_dict)
        entry_dict: dict = {"Item": "Tool Kit",                                "Cost": "600",  "GE": "6",   "Weight":  "40", "To-Hit": "0",   "Damage": "",       "Shots": "0",  "CPS": "0",   "WPS": "0",   "Notes": ""}
        self.personal_equipment_list.append(entry_dict)
        entry_dict: dict = {"Item": "Walkie Talkie",                           "Cost": "250",  "GE": "1",   "Weight":   "2", "To-Hit": "0",   "Damage": "",       "Shots": "0",  "CPS": "0",   "WPS": "0",   "Notes": ""}
        self.personal_equipment_list.append(entry_dict)

    def get_personal_equipment_options(self):
        options: list = []
        for entry in self.personal_equipment_list:
            personal_equipment_name: str = entry.get("Item")
            options.append(personal_equipment_name)
        return options

    def var_alternate_grenade_equivalent_changed(self):
        """Examine the value of the checkbox and adjust weights of personal equipment, and the total recalc"""
        self.age_value = int(self.var_alternate_grenade_equivalent.get())
        self.personal_equipment_qty_1_update()
        self.personal_equipment_qty_2_update()
        self.personal_equipment_qty_3_update()
        self.personal_equipment_qty_4_update()
        self.personal_equipment_qty_5_update()
        self.personal_equipment_qty_6_update()
        self.personal_equipment_qty_7_update()
        self.personal_equipment_qty_8_update()
        self.personal_equipment_qty_9_update()
        self.personal_equipment_qty_10_update()

    def add_labels_buttons_personal_equipment(self, canvas_type):
        self.var_alternate_grenade_equivalent = tk.IntVar(value=0)
        self.check_alternate_grenade_equivalent = tk.Checkbutton(canvas_type, text="Alternate Grenade Equivalent", variable=self.var_alternate_grenade_equivalent, command=self.var_alternate_grenade_equivalent_changed, anchor="w")
        self.check_alternate_grenade_equivalent.grid(column=self.grid_col_item,row=self.grid_row_alt_ge_equivalent, sticky="w", columnspan=3)

        self.add_labels_buttons_personal_equipment_1_canvas(canvas_type=canvas_type)
        self.add_labels_buttons_personal_equipment_2_canvas(canvas_type=canvas_type)
        self.add_labels_buttons_personal_equipment_3_canvas(canvas_type=canvas_type)
        self.add_labels_buttons_personal_equipment_4_canvas(canvas_type=canvas_type)
        self.add_labels_buttons_personal_equipment_5_canvas(canvas_type=canvas_type)
        self.add_labels_buttons_personal_equipment_6_canvas(canvas_type=canvas_type)
        self.add_labels_buttons_personal_equipment_7_canvas(canvas_type=canvas_type)
        self.add_labels_buttons_personal_equipment_8_canvas(canvas_type=canvas_type)
        self.add_labels_buttons_personal_equipment_9_canvas(canvas_type=canvas_type)
        self.add_labels_buttons_personal_equipment_10_canvas(canvas_type=canvas_type)

    ######################################################################
    # Personal Equipment Row 1 processing here                           #
    ######################################################################
    def add_labels_buttons_personal_equipment_1_canvas(self, canvas_type):
        up_arrow = "\u2191"
        down_arrow = "\u2193"

        self.label_hidden_personal_equipment_1_name   = tk.Label(canvas_type, text="0", anchor="w")
        self.label_hidden_personal_equipment_1_cost   = tk.Label(canvas_type, text="0", anchor="w")
        self.label_hidden_personal_equipment_1_weight = tk.Label(canvas_type, text="0", anchor="w")
        self.label_hidden_personal_equipment_1_ge     = tk.Label(canvas_type, text="0", anchor="w")
        self.label_hidden_personal_equipment_1_to_hit = tk.Label(canvas_type, text="0", anchor="w")
        self.label_hidden_personal_equipment_1_damage = tk.Label(canvas_type, text="0", anchor="w")
        self.label_hidden_personal_equipment_1_shots  = tk.Label(canvas_type, text="0", anchor="w")
        self.label_hidden_personal_equipment_1_cps    = tk.Label(canvas_type, text="0", anchor="w")
        self.label_hidden_personal_equipment_1_wps    = tk.Label(canvas_type, text="0", anchor="w")
        self.label_hidden_personal_equipment_1_notes  = tk.Label(canvas_type, text="0", anchor="w")

        self.label_personal_equipment_1_cost = tk.Label(canvas_type, text="0", anchor="w")
        self.label_personal_equipment_1_cost.grid(column=self.grid_col_cost,row=self.grid_row_personal_equipment_1, sticky="w")
        self.label_personal_equipment_1_weight = tk.Label(canvas_type, text="0", anchor="w")
        self.label_personal_equipment_1_weight.grid(column=self.grid_col_weight ,row=self.grid_row_personal_equipment_1, sticky="w")
        self.label_personal_equipment_1_ge  = tk.Label(canvas_type, text="0", anchor="w")
        self.label_personal_equipment_1_ge.grid(column=self.grid_col_spaces,row=self.grid_row_personal_equipment_1, sticky="w")
        self.label_personal_equipment_1_to_hit = tk.Label(canvas_type, text="0", anchor="w")
        self.label_personal_equipment_1_to_hit.grid(column=self.grid_col_dp,row=self.grid_row_personal_equipment_1, sticky="w")
        self.label_personal_equipment_1_damage = tk.Label(canvas_type, text="", anchor="w")
        self.label_personal_equipment_1_damage.grid(column=self.grid_col_max_weight,row=self.grid_row_personal_equipment_1, sticky="w")
        self.label_personal_equipment_1_shots = tk.Label(canvas_type, text="", anchor="w")
        self.label_personal_equipment_1_shots.grid(column=self.grid_col_power_factors,row=self.grid_row_personal_equipment_1, sticky="w")
        self.label_personal_equipment_1_cps = tk.Label(canvas_type, text="", anchor="w")
        self.label_personal_equipment_1_cps.grid(column=self.grid_col_base_mpg,row=self.grid_row_personal_equipment_1, sticky="w")
        self.label_personal_equipment_1_wps = tk.Label(canvas_type, text="", anchor="w")
        self.label_personal_equipment_1_wps.grid(column=self.grid_col_test_track,row=self.grid_row_personal_equipment_1, sticky="w")
        self.label_personal_equipment_1_notes = tk.Label(canvas_type, text="", anchor="w")
        self.label_personal_equipment_1_notes.grid(column=self.grid_col_test_track_numbers,row=self.grid_row_personal_equipment_1, sticky="w")

        self.var_personal_equipment_1_qty = tk.IntVar(value=0)
        self.entry_personal_equipment_1_qty = ttk.Entry(canvas_type, textvariable=self.var_personal_equipment_1_qty, width=3)
        self.entry_personal_equipment_1_qty.grid(column=self.grid_col_qty, row=self.grid_row_personal_equipment_1, sticky="w")
        self.var_personal_equipment_1_qty.trace_add("write", self.personal_equipment_qty_1_update)

        self.button_personal_equipment_1_qty_up = tk.Button(canvas_type, text=up_arrow, command=self.on_button_personal_equipment_1_qty_up)
        self.button_personal_equipment_1_qty_up.grid(column=self.grid_left_up_button,row=self.grid_row_personal_equipment_1, sticky="w")
        self.button_personal_equipment_1_qty_down = tk.Button(canvas_type, text=down_arrow, command=self.on_button_personal_equipment_1_qty_down)
        self.button_personal_equipment_1_qty_down.grid(column=self.grid_left_down_button,row=self.grid_row_personal_equipment_1, sticky="w")

    def add_dropdown_personal_equipment_1_canvas(self, canvas_type):
        self.selected_personal_equipment_1 = tk.StringVar()
        self.selected_personal_equipment_1.set("Personal Equipment")
        options = self.get_personal_equipment_options()
        # Create the dropdown widget
        self.personal_equipment_1_dropdown = ttk.OptionMenu(canvas_type, self.selected_personal_equipment_1, "Personal Equipment", *options) #filled elsewhere
        self.personal_equipment_1_dropdown.grid(column=self.grid_col_item, row=self.grid_row_personal_equipment_1, sticky="w")
        self.selected_personal_equipment_1.trace_add("write", self.on_select_personal_equipment_1)

    def on_select_personal_equipment_1(self, *args):
        selected_value = self.selected_personal_equipment_1.get()
        for entry in self.personal_equipment_list: #use the same self.personal_equipment_list for every personal_equipment dropdown
            personal_equipment_name: str = entry.get("Item")
            if selected_value == personal_equipment_name:
                personal_equipment_cost:   str = entry.get("Cost")
                personal_equipment_ge:     str = entry.get("GE")
                personal_equipment_weight: str = entry.get("Weight")
                personal_equipment_to_hit: str = entry.get("To-Hit")
                personal_equipment_damage: str = entry.get("Damage")
                personal_equipment_shots:  str = entry.get("Shots")
                personal_equipment_cps:    str = entry.get("CPS")
                personal_equipemnt_wps:    str = entry.get("WPS")
                personal_equipment_notes:  str = entry.get("Notes")

                self.label_hidden_personal_equipment_1_name.configure(text=str(personal_equipment_name))
                self.label_hidden_personal_equipment_1_cost.configure(text=str(personal_equipment_cost))
                self.label_hidden_personal_equipment_1_ge.configure(text=str(personal_equipment_ge))
                self.label_hidden_personal_equipment_1_weight.configure(text=str(personal_equipment_weight))
                self.label_hidden_personal_equipment_1_to_hit.configure(text=str(personal_equipment_to_hit))
                self.label_hidden_personal_equipment_1_damage.configure(text=str(personal_equipment_damage))
                self.label_hidden_personal_equipment_1_shots.configure(text=str(personal_equipment_shots))
                self.label_hidden_personal_equipment_1_cps.configure(text=str(personal_equipment_cps))
                self.label_hidden_personal_equipment_1_wps.configure(text=str(personal_equipemnt_wps))
                self.label_hidden_personal_equipment_1_notes.configure(text=str(personal_equipment_notes))
                self.personal_equipment_qty_1_update()
                return

    def on_button_personal_equipment_1_qty_up(self, *args):
        personal_equipment_1_qty = self.var_personal_equipment_1_qty.get()
        personal_equipment_1_qty = personal_equipment_1_qty + 1
        self.var_personal_equipment_1_qty.set(value=personal_equipment_1_qty)

    def on_button_personal_equipment_1_qty_down(self, *args):
        personal_equipment_1_qty = self.var_personal_equipment_1_qty.get()
        personal_equipment_1_qty = max(personal_equipment_1_qty - 1, 0)
        self.var_personal_equipment_1_qty.set(value=personal_equipment_1_qty)

    def personal_equipment_qty_1_update(self, *args):
        personal_equipment_1_qty = self.var_personal_equipment_1_qty.get()

        personal_equipment_1_cost        = int(self.label_hidden_personal_equipment_1_cost.cget("text"))
        if self.age_value == 1: #use alternate grenade equivalent settings, otherwise set weight to zero
            personal_equipment_1_weight  = int(self.label_hidden_personal_equipment_1_weight.cget("text"))
        else:
            personal_equipment_1_weight  = 0
        personal_equipment_1_ge:     int = int(self.label_hidden_personal_equipment_1_ge.cget("text"))
        personal_equipment_1_to_hit: str = self.label_hidden_personal_equipment_1_to_hit.cget("text")
        personal_equipment_1_damage: str = self.label_hidden_personal_equipment_1_damage.cget("text")
        personal_equipment_1_shots:  str = self.label_hidden_personal_equipment_1_shots.cget("text")
        personal_equipment_1_cps:    str = self.label_hidden_personal_equipment_1_cps.cget("text")
        personal_equipment_1_wps:    str = self.label_hidden_personal_equipment_1_wps.cget("text")
        personal_equipment_1_notes:  str = self.label_hidden_personal_equipment_1_notes.cget("text")

        self.label_personal_equipment_1_cost.configure(text=str(personal_equipment_1_cost * personal_equipment_1_qty))
        self.label_personal_equipment_1_weight.configure(text=str(personal_equipment_1_weight * personal_equipment_1_qty))
        self.label_personal_equipment_1_ge.configure(text=str(personal_equipment_1_ge * personal_equipment_1_qty))
        self.label_personal_equipment_1_to_hit.configure(text=str(personal_equipment_1_to_hit))
        self.label_personal_equipment_1_damage.configure(text=str(personal_equipment_1_damage))
        self.label_personal_equipment_1_shots.configure(text=str(personal_equipment_1_shots))
        self.label_personal_equipment_1_cps.configure(text=str(personal_equipment_1_cps))
        self.label_personal_equipment_1_wps.configure(text=str(personal_equipment_1_wps))
        self.label_personal_equipment_1_notes.configure(text=str(personal_equipment_1_notes))

        self.recalculate()

    def facing_compilations(self) -> str:
        """
        Calculates and validates maximum allowable weapon space configurations per individual vehicle facing.
        Safely tracks initialized attributes and StringVars to avoid startup calculation loop crashes.
        """
        return_facing: str = ""
        
        # 1. FIXED SAFE LABELS EXTRACTOR ENGINE
        def get_lbl_val(attr_name, default_val=0):
            if hasattr(self, attr_name):
                val_obj = getattr(self, attr_name)
                
                # A. If the attribute is ALREADY a native Python integer or float, use it directly!
                if isinstance(val_obj, (int, float)):
                    return int(val_obj)
                    
                # B. If it's a valid Tkinter widget element, extract the string value safely
                if val_obj is not None and hasattr(val_obj, "cget"):
                    try:
                        text_val = val_obj.cget("text").strip()
                        if text_val != "" and text_val != "0": 
                            return int(float(text_val))
                    except (AttributeError, ValueError):
                        pass

            # C. DYNAMIC DATA DICTIONARY FALLBACK PROTECTION SHIELD:
            # Dynamically parses structural constraints straight from your vehicle config pools
            if attr_name == "label_body_spaces":
                if hasattr(self, "selected_body") and getattr(self, "selected_body"):
                    active_body_name = getattr(self, "selected_body").get()
                    
                    # Scan your master vehicle data configurations for the exact Total Spaces dict key
                    bodies_pool = getattr(self, "car_bodies", getattr(self, "bodies_list", []))
                    for b_entry in bodies_pool:
                        if isinstance(b_entry, dict) and b_entry.get("Body") == active_body_name:
                            return int(b_entry.get("Total Spaces", default_val))
            return default_val

        # Execute safe, timing-isolated extractions
        try:
            body_spaces: int = int(self.label_body_spaces.cget("text"))
        except tk.TclError:
            body_spaces = 0
        try:
            cargo_spaces: int = int(self.label_hidden_cargo_spaces.cget("text"))
        except tk.TclError:
            cargo_spaces = 0
        try:
            modification_spaces: int = int(self.label_modificiation_space.cget("text"))
        except tk.TclError:
            modification_spaces = 0
        try:
            modification_cargo_spaces: int = int(self.label_hidden_modification_cargo_space.cget("text"))
        except tk.TclError:
            modification_cargo_spaces = 0
        # Calculate structural space thresholds cleanly using your 13 space metric baseline
        total_allowable_per_facing = int((body_spaces + cargo_spaces - modification_spaces - modification_cargo_spaces) / 3)
        facings_list: list = []

        # 2. SAFE PASS ONE: Dynamic processing for the 10 Weapon Row facings
        loop_max = len(self.weapon_spaces_label_objects)
        for loop_index in range(0,loop_max):
            space_obj = self.weapon_spaces_label_objects[loop_index]
            facing_obj = self.weapon_mount_dropdown_string_vars[loop_index]
            facing_str = facing_obj.get()
            space_val = float(space_obj.cget("text"))
            facings_list.append({facing_str: space_val})

        #for i in range(1, self.weapon_rows_count + 1):
        #    facing_var_name = f"weapon_armor_facing_{i}"
        #    space_lbl_name = f"label_sub_weapon_{i}_space"
        #    facing_str = "Facing"
        #    if hasattr(self, facing_var_name):
        #        var_obj = getattr(self, facing_var_name)
        #        if var_obj is not None and hasattr(var_obj, "get"):
        #            try: facing_str = var_obj.get()
        #            except Exception: facing_str = "Facing"
        #        elif isinstance(var_obj, str):
        #            facing_str = var_obj
                
        #    space_val = 0.0
        #    if hasattr(self, space_lbl_name):
        #        lbl_obj = getattr(self, space_lbl_name)
        #        if lbl_obj is not None and hasattr(lbl_obj, "cget"):
        #            try:
        #                txt = lbl_obj.cget("text").strip()
        #                if txt != "": space_val = float(txt)
        #            except (AttributeError, ValueError):
        #                pass
                    
        #    facings_list.append({facing_str: space_val})

        # 3. SAFE PASS TWO: Dynamic processing for the 5 Component Armor facings
        #for i in range(1, 6):
        #    facing_var_name = f"selected_component_armor_facing_{i}"
        #    space_lbl_name = f"label_component_armor_{i}_space"
            
        #    facing_str = "Facing"
        #    if hasattr(self, facing_var_name):
        #        var_obj = getattr(self, facing_var_name)
        #        if var_obj is not None and hasattr(var_obj, "get"):
        #            try: facing_str = var_obj.get()
        #            except Exception: pass
        #        elif isinstance(var_obj, str):
        #            facing_str = var_obj
                
        #    space_val = 0.0
        #    if hasattr(self, space_lbl_name):
        #        lbl_obj = getattr(self, space_lbl_name)
        #        if lbl_obj is not None and hasattr(lbl_obj, "cget"):
        #            try:
        #                txt = lbl_obj.cget("text").strip()
        #                if txt != "": space_val = float(txt)
        #            except (AttributeError, ValueError):
        #                pass
                    
        #    facings_list.append({facing_str: space_val})

        # 4. SAFE PASS THREE: Dynamic processing for the 5 Rocket Booster facings
        #for i in range(1, 6):
        #    facing_var_name = f"selected_rocket_booster_facing_{i}"
        #    space_lbl_name = f"label_rocket_booster_{i}_space"
            
        #    facing_str = "Facing"
        #    if hasattr(self, facing_var_name):
        #        var_obj = getattr(self, facing_var_name)
        #        if var_obj is not None and hasattr(var_obj, "get"):
        #            try: facing_str = var_obj.get()
        #            except Exception: pass
        #        elif isinstance(var_obj, str):
        #            facing_str = var_obj
                
        #    space_val = 0.0
        #    if hasattr(self, space_lbl_name):
        #        lbl_obj = getattr(self, space_lbl_name)
        #        if lbl_obj is not None and hasattr(lbl_obj, "cget"):
        #            try:
        #                txt = lbl_obj.cget("text").strip()
        #                if txt != "": space_val = float(txt)
        #            except (AttributeError, ValueError):
        #                pass
                    
        #    facings_list.append({facing_str: space_val})

        # 5. AGGREGATION PASS: Tally up cumulative space metrics per vehicle side location
        front_facing:  float = 0.0
        back_facing:   float = 0.0
        left_facing:   float = 0.0
        right_facing:  float = 0.0
        top_facing:    float = 0.0
        bottom_facing: float = 0.0
        
        for facing_entry in facings_list:
            for facing, spaces in facing_entry.items():
                match facing:
                    case "Front":  front_facing += spaces
                    case "Back":   back_facing += spaces
                    case "Left":   left_facing += spaces
                    case "Right":  right_facing += spaces
                    case "Top":    top_facing += spaces
                    case "Bottom" | "Underbody": bottom_facing += spaces

        # 6. CONSTRAINT ENFORCEMENT: Evaluate space boundaries safely
        if front_facing > total_allowable_per_facing:
            return_facing = "Too Many Front Spaces"
        elif back_facing > total_allowable_per_facing:
            return_facing = "Too Many Back Spaces"
        elif left_facing > total_allowable_per_facing:
            return_facing = "Too Many Left Spaces"
        elif right_facing > total_allowable_per_facing:
            return_facing = "Too Many Right Spaces"
        elif top_facing > total_allowable_per_facing:
            return_facing = "Too Many Top Spaces"
        elif bottom_facing > total_allowable_per_facing:
            return_facing = "Too Many Bottom Spaces"
            
        return return_facing

    def show_gas_engine_options(self):
        self.label_gas_header.grid(              column=self.grid_col_item,          row=self.grid_row_gas_engine_mods, sticky="w")
        self.check_engine_gas_super_charger.grid(column=self.grid_col_qty,           row=self.grid_row_gas_engine_mods, sticky="w", columnspan=6)
        self.check_engine_gas_vp_turbo.grid(     column=self.grid_col_cost,          row=self.grid_row_gas_engine_mods, sticky="w", columnspan=6)
        self.check_engine_gas_tube_headers.grid( column=self.grid_col_dp,            row=self.grid_row_gas_engine_mods, sticky="w", columnspan=3)
        self.check_engine_gas_blue_print.grid(   column=self.grid_col_power_factors, row=self.grid_row_gas_engine_mods, sticky="w")
        self.check_engine_gas_turbo.grid(        column=self.grid_col_base_mpg,      row=self.grid_row_gas_engine_mods, sticky="w")
        self.gas_tank_dropdown.grid(             column=self.grid_col_item,          row=self.grid_row_gas_tank, sticky="w")
        self.label_gas_tank_cost.grid(           column=self.grid_col_cost,          row=self.grid_row_gas_tank, sticky="w")
        self.label_gas_tank_weight.grid(         column=self.grid_col_weight,        row=self.grid_row_gas_tank, sticky="w")
        self.label_gas_tank_space.grid(          column=self.grid_col_spaces,        row=self.grid_row_gas_tank, sticky="w")
        self.label_gas_tank_dp.grid(             column=self.grid_col_dp,            row=self.grid_row_gas_tank, sticky="w")
        self.entry_gas_gallon_qty.grid(          column=self.grid_col_qty,           row=self.grid_row_gas_tank, sticky="w")
        self.button_gas_qty_up.grid(             column=self.grid_left_up_button,    row=self.grid_row_gas_tank, sticky="w")
        self.button_gas_qty_down.grid(           column=self.grid_left_down_button,  row=self.grid_row_gas_tank, sticky="w")

    def hide_gas_engine_options(self):
        self.check_engine_gas_super_charger.grid_forget()
        self.check_engine_gas_vp_turbo.grid_forget()
        self.check_engine_gas_tube_headers.grid_forget()
        self.check_engine_gas_blue_print.grid_forget()
        self.check_engine_gas_turbo.grid_forget()
        self.label_gas_header.grid_forget()
        if self.gas_tank_dropdown is not None:
            self.gas_tank_dropdown.grid_forget()
        self.label_gas_tank_cost.grid_forget()
        self.label_gas_tank_weight.grid_forget()
        self.label_gas_tank_space.grid_forget()
        self.label_gas_tank_dp.grid_forget()
        self.entry_gas_gallon_qty.grid_forget()
        self.button_gas_qty_up.grid_forget()
        self.button_gas_qty_down.grid_forget()

    def show_electric_engine_options(self):
        self.label_electric_header.grid(                   column=self.grid_col_item,       row=self.grid_row_electric_mods, sticky="w")
        self.check_engine_electric_super_conductors.grid(  column=self.grid_col_qty,        row=self.grid_row_electric_mods, sticky="w", columnspan=6)
        self.check_engine_electric_platnium_catalysts.grid(column=self.grid_col_cost,       row=self.grid_row_electric_mods, sticky="w", columnspan=3)
        self.check_engine_electric_extra_power_cells.grid( column=self.grid_col_max_weight, row=self.grid_row_electric_mods, sticky="w", columnspan=6)

    def hide_electric_engine_options(self):
        self.label_electric_header.grid_forget()
        self.check_engine_electric_super_conductors.grid_forget()
        self.check_engine_electric_platnium_catalysts.grid_forget()
        self.check_engine_electric_extra_power_cells.grid_forget()

    def print_weapon(self, canvas, weapon_qty, ammo_qty, extra_mags_qty, armor_facing) -> str:
        """Print details for a given weapon selection"""
        return_text: str = ""
        if canvas is not None:
            if weapon_qty.get() > 0:
                return_text = return_text + str(weapon_qty.get())
                return_text = return_text + " " + str(canvas.get())
                if weapon_qty.get() > 1:
                    return_text = return_text + "s"
                if ammo_qty.get() > 0:
                    return_text = return_text + f" with {str(ammo_qty.get())} shot"
                    if ammo_qty.get() > 1:
                        return_text = return_text + "s"
                if extra_mags_qty.get() > 0:
                    return_text = return_text + f" and {extra_mags_qty.get()} extra magazines"
                if armor_facing.get() != "Facing":
                    return_text = return_text + f" facing {armor_facing.get()}"
                return_text = return_text + ".\n"
        return return_text

    def make_pdf(self, input_dict: dict):
        """Create PDF output suitable for printing and use in gameday"""
        now_time: datetime = datetime.now()
        pdf_output_file_name: str = f".\\output_{now_time.strftime("%Y%m%d%H%M%S")}.pdf"
        # Create a PDF object
        pdf = FPDF()
        pdf.set_fill_color(r=200, g=200, b=200) # gray?
        # Add a page
        pdf.add_page()

        self.set_constants()
        self.draw_section_borders(pdf)
        self.draw_header(pdf)
        self.draw_body(pdf, input_dict)
        self.draw_weapons(pdf, input_dict)
        self.draw_accessories(pdf, input_dict)
        self.draw_speed(pdf, input_dict)
        self.draw_car_image(pdf, input_dict)
        self.draw_ca(pdf, input_dict)
        self.draw_engine(pdf, input_dict)
        self.draw_tires(pdf, input_dict)
        self.draw_armor(pdf, input_dict)
        #self.draw_notes(pdf, input_dict)
        self.draw_walkarounds(pdf, input_dict)
        self.end_pdf(pdf, pdf_output_file_name)

    def set_constants(self):
        """Set contants"""
        self.row_height:       int = 5
        self.col_left_edge:    int = 10
        self.col_ca_type:      int = 35
        self.col_ca_dp:        int = 70
        self.col_engine_dp:    int = 40
        self.col_engine_tank:  int = 50
        self.col_engine_tkdp:  int = 70
        self.col_middle_top:   int = 100
        self.col_left_armor:   int = 30
        self.col_middle_armor: int = 40
        self.col_right_armor:  int = 50
        self.col_middle_line:  int = 80
        self.col_facing:       int = 140
        self.col_to_hit:       int = 150
        self.col_damage:       int = 160
        self.col_ammo:         int = 180
        self.col_dp:           int = 180
        self.col_weapon_dp:    int = 190
        self.col_right_edge:   int = 190
        self.width_weapon_name:   int = 60
        self.width_weapon_facing: int = 20
        self.width_weapon_to_hit: int = 10
        self.width_weapon_damage: int = 20
        self.width_weapon_ammo:   int = 10
        self.width_weapon_dp:     int = 10
        self.row_top:          int = 10
        self.row_2:            int = self.row_top + self.row_height
        self.row_3:            int = self.row_2 + self.row_height
        self.row_4:            int = self.row_3 + self.row_height
        self.row_5:            int = self.row_4 + self.row_height
        self.row_6:            int = self.row_5 + self.row_height
        self.row_7:            int = self.row_6 + self.row_height
        self.row_8:            int = self.row_7 + self.row_height
        self.row_9:            int = self.row_8 + self.row_height
        self.row_10:           int = self.row_9 + self.row_height
        self.row_11:           int = self.row_10 + self.row_height
        self.row_12:           int = self.row_11 + self.row_height
        self.row_13:           int = self.row_12 + self.row_height
        self.row_14:           int = self.row_13 + self.row_height
        self.row_15:           int = self.row_14 + self.row_height
        self.row_16:           int = self.row_15 + self.row_height
        self.row_17:           int = self.row_16 + self.row_height
        self.row_18:           int = self.row_17 + self.row_height
        self.row_19:           int = self.row_18 + self.row_height
        self.row_20:           int = self.row_19 + self.row_height
        self.row_21:           int = self.row_20 + self.row_height
        self.row_22:           int = self.row_21 + self.row_height
        self.row_23:           int = self.row_22 + self.row_height
        self.row_24:           int = self.row_23 + self.row_height
        self.row_25:           int = self.row_24 + self.row_height
        self.row_26:           int = self.row_25 + self.row_height
        self.row_27:           int = self.row_26 + self.row_height
        self.row_28:           int = self.row_27 + self.row_height
        self.row_29:           int = self.row_28 + self.row_height
        self.row_30:           int = self.row_29 + self.row_height
        self.row_31:           int = self.row_30 + self.row_height
        self.row_32:           int = self.row_31 + self.row_height
        self.row_33:           int = self.row_32 + self.row_height
        self.row_34:           int = self.row_33 + self.row_height
        self.row_35:           int = self.row_34 + self.row_height
        self.row_36:           int = self.row_35 + self.row_height
        self.row_37:           int = self.row_36 + self.row_height
        self.row_38:           int = self.row_37 + self.row_height
        self.row_39:           int = self.row_38 + self.row_height
        self.row_40:           int = self.row_39 + self.row_height
        self.row_41:           int = self.row_40 + self.row_height

    def draw_section_borders(self, pdf: FPDF):
        """Given an FPDF object, draw the section bordersbody section"""
        #Draw rectangles
        pdf.set_draw_color(0, 0, 0) # Set border color (RGB)
        pdf.rect(x=self.col_left_edge, y=self.row_top, w=self.col_right_edge, h=self.row_height, style="D") #CWVRS line
        pdf.rect(x=self.col_left_edge, y=self.row_2, w=self.col_middle_top, h=self.row_height, style="F") #Vehicle Name
        pdf.rect(x=self.col_middle_top+self.col_left_edge, y=self.row_2, w=self.col_right_edge-self.col_middle_top, h=self.row_height, style="F") #Club Name

        #left column boxes
        pdf.rect(x=self.col_left_edge, y=self.row_3,  w=self.col_middle_line-self.col_left_edge, h=self.row_height*13, style="D") #car picture
        pdf.rect(x=self.col_left_edge, y=self.row_16, w=self.col_middle_line-self.col_left_edge, h=self.row_height,    style="F") #component armor header
        pdf.rect(x=self.col_left_edge, y=self.row_17, w=self.col_middle_line-self.col_left_edge, h=self.row_height*5,  style="D") #component armor
        pdf.rect(x=self.col_left_edge, y=self.row_22, w=self.col_middle_line-self.col_left_edge, h=self.row_height,    style="F") #engine and tank header
        pdf.rect(x=self.col_left_edge, y=self.row_23, w=self.col_middle_line-self.col_left_edge, h=self.row_height,    style="D") #engine and tank
        pdf.rect(x=self.col_left_edge, y=self.row_24, w=self.col_middle_line-self.col_left_edge, h=self.row_height,    style="F") #tires header
        pdf.rect(x=self.col_left_edge, y=self.row_25, w=self.col_middle_line-self.col_left_edge, h=self.row_height*2,  style="D") #tires
        pdf.rect(x=self.col_left_edge, y=self.row_27, w=self.col_middle_line-self.col_left_edge, h=self.row_height,    style="F") #armor header
        pdf.rect(x=self.col_left_edge, y=self.row_28, w=self.col_middle_line-self.col_left_edge, h=self.row_height*8,  style="D") #armor
        pdf.rect(x=self.col_left_edge, y=self.row_35, w=self.col_middle_line-self.col_left_edge, h=self.row_height,    style="F") #Walkaround header
        pdf.rect(x=self.col_left_edge, y=self.row_36, w=self.col_middle_line-self.col_left_edge, h=self.row_height*20, style="D") #Walkaround header

        #right column boxes
        pdf.rect(x=self.col_middle_line, y=self.row_3, w=self.col_right_edge-self.col_middle_line+self.col_left_edge, h=self.row_height*4, style="D") #size et al
        pdf.rect(x=self.col_middle_line, y=self.row_7, w=self.col_right_edge-self.col_middle_line+self.col_left_edge, h=self.row_height, style="F") #Weapons header

        #Weapon columns
        pdf.rect(x=self.col_middle_line, y=self.row_8, w=self.width_weapon_name,   h=self.row_height*10, style="D") #Weapons name
        pdf.rect(x=self.col_facing     , y=self.row_8, w=self.width_weapon_facing, h=self.row_height*10, style="D") #Weapons Facing
        pdf.rect(x=self.col_to_hit     , y=self.row_8, w=self.width_weapon_to_hit, h=self.row_height*10, style="D") #Weapons To Hit
        pdf.rect(x=self.col_damage     , y=self.row_8, w=self.width_weapon_damage, h=self.row_height*10, style="D") #Weapons Damage
        pdf.rect(x=self.col_ammo       , y=self.row_8, w=self.width_weapon_ammo,   h=self.row_height*10, style="D") #Weapons Ammo
        pdf.rect(x=self.col_weapon_dp  , y=self.row_8, w=self.width_weapon_dp,     h=self.row_height*10, style="D") #Weapons Ammo

        #Accessory
        pdf.rect(x=self.col_middle_line, y=self.row_18, w=self.col_right_edge-self.col_middle_line+self.col_left_edge, h=self.row_height, style="F") #Acc header
        pdf.rect(x=self.col_middle_line, y=self.row_19, w=self.col_right_edge-self.col_middle_line+self.col_left_edge, h=self.row_height*16, style="D") #Acc details

        #Speed and Handling
        pdf.rect(x=self.col_middle_line, y=self.row_35, w=self.col_right_edge-self.col_middle_line+self.col_left_edge, h=self.row_height, style="F") #Weapons header
        pdf.rect(x=self.col_middle_line, y=self.row_36, w=self.col_right_edge-self.col_middle_line+self.col_left_edge, h=self.row_height*20, style="D") #Weapons header

    def draw_header(self, pdf: FPDF):
        """Given an FPDF object, draw the body section"""
        # Set font
        pdf.set_font("Helvetica", size=10)
        #Line printings
        pdf.cell(w = self.col_right_edge, h = self.row_height, text="Car Wars Vehicle Record Sheet", ln=True, align='C')
        pdf.set_font("Helvetica", size=8)

    def draw_body(self, pdf: FPDF, input_dict: dict):
        """Given an FPDF object and an input_dict, draw the body section"""
        pdf.cell(w = self.col_middle_top, h = self.row_height, ln=False, align='L', text="Vehicle Name:")
        pdf.cell(w = self.col_middle_top, h = self.row_height, ln=False, align='L', text="Club Name:")
        pdf.cell(w = self.col_right_edge, h = self.row_height, text="", ln=True, align='C')

        line_text = f'Size: {input_dict.get("Body_Name", "")}'
        pdf.set_x(x=self.col_middle_line)
        pdf.cell(w = self.col_middle_top, h = self.row_height, ln=False, align='L', text=line_text)
        line_text = f'Weight: {input_dict.get("Total_Weight", "")}'
        pdf.set_x(x=self.col_facing)
        pdf.cell(w = self.col_middle_top, h = self.row_height, ln=False, align='L', text=line_text)
        line_text = f'Cost: {input_dict.get("Total_Cost", "")}'
        pdf.set_x(x=self.col_dp)
        pdf.cell(w = self.col_middle_top, h = self.row_height, ln=False, align='L', text=line_text)
        pdf.cell(w = self.col_right_edge, h = self.row_height, text="", ln=True, align='C')

        line_text = f'Chassis: {input_dict.get("Chassis", "")}'
        pdf.set_x(x=self.col_middle_line)
        pdf.cell(w = self.col_middle_top, h = self.row_height, ln=False, align='L', text=line_text)
        line_text = f'Suspension: {input_dict.get("Suspension", "")}'
        pdf.set_x(x=self.col_facing)
        pdf.cell(w = self.col_middle_top, h = self.row_height, ln=False, align='L', text=line_text)
        line_text = f'HC: {input_dict.get("HC", "")}'
        pdf.set_x(x=self.col_dp)
        pdf.cell(w = self.col_middle_top, h = self.row_height, ln=False, align='L', text=line_text)
        pdf.cell(w = self.col_right_edge, h = self.row_height, text="", ln=True, align='C')

        line_text = f'Accel: {input_dict.get("Accel", "")}'
        pdf.set_x(x=self.col_middle_line)
        pdf.cell(w = self.col_middle_top, h = self.row_height, ln=False, align='L', text=line_text)
        line_text = f'Top Speed: {input_dict.get("Top_Speed", "")}'
        pdf.set_x(x=self.col_facing)
        pdf.cell(w = self.col_middle_top, h = self.row_height, ln=False, align='L', text=line_text)
        pdf.cell(w = self.col_right_edge, h = self.row_height, text="", ln=True, align='C')

        local_pf = str(input_dict.get("Total_Power_Factors", ""))
        local_mpg = str(input_dict.get("MPG", ""))
        print_me = local_mpg if local_mpg != "0" else local_pf
        line_text = f'Power/MPG: {print_me}'
        pdf.set_x(x=self.col_middle_line)
        pdf.cell(w = self.col_middle_top, h = self.row_height, ln=False, align='L', text=line_text)

        line_text = f'Range: {input_dict.get("Range", "")}'
        pdf.set_x(x=self.col_facing)
        pdf.cell(w = self.col_middle_top, h = self.row_height, ln=False, align='L', text=line_text)

        local_weight = int(input_dict.get("Total_Weight", ""))
        local_dm: str = "1"
        if local_weight < 4000:
            local_dm = "2/3"
        elif local_weight > 7999:
            local_dm = 2
        line_text = f'DM: {local_dm}'
        pdf.set_x(x=self.col_dp)
        pdf.cell(w = self.col_middle_top, h = self.row_height, ln=False, align='L', text=line_text)
        pdf.cell(w = self.col_right_edge, h = self.row_height, text="", ln=True, align='C')

    def draw_weapons(self, pdf: FPDF, input_dict: dict):
        """Given an FPDF object and an input_dict, draw the weapons section"""
        #Weapons details being printed
        pdf.set_x(x=self.col_middle_line)
        pdf.cell(w = self.width_weapon_name,   h = self.row_height, ln=False, align='L', text="Weapons")
        pdf.set_x(x=self.col_facing)
        pdf.cell(w = self.width_weapon_facing, h = self.row_height, ln=False, align='L', text="Facing")
        pdf.set_x(x=self.col_to_hit)
        pdf.cell(w = self.width_weapon_to_hit, h = self.row_height, ln=False, align='L', text="To Hit")
        pdf.set_x(x=self.col_damage)
        pdf.cell(w = self.width_weapon_damage, h = self.row_height, ln=False, align='L', text="Damage")
        pdf.set_x(x=self.col_ammo)
        pdf.cell(w = self.width_weapon_ammo,   h = self.row_height, ln=False, align='L', text="Ammo")
        pdf.set_x(x=self.col_weapon_dp)
        pdf.cell(w = self.width_weapon_dp,     h = self.row_height, ln=False, align='L', text="DP")
        pdf.cell(w = self.col_right_edge,      h = self.row_height, text="", ln=True, align='C') # Weapon Line Header

        for weapon_index in range(1, self.weapon_rows_count + 1):
            qty_index     = f"weapon_{weapon_index}_qty"
            name_index    = f"weapon_{weapon_index}_name"
            facing_index  = f"weapon_{weapon_index}_facing"
            to_hit_index  = f"weapon_{weapon_index}_to_hit"
            damage_index  = f"weapon_{weapon_index}_damage"
            ammo_index    = f"weapon_{weapon_index}_ammo"
            dp_index      = f"weapon_{weapon_index}_dp"
            weapon_qty    = input_dict.get(qty_index, "")
            weapon_name   = input_dict.get(name_index, "")
            weapon_facing = input_dict.get(facing_index, "")
            weapon_to_hit = input_dict.get(to_hit_index, "")
            weapon_damage = input_dict.get(damage_index, "")
            weapon_ammo   = input_dict.get(ammo_index, "")
            weapon_dp     = input_dict.get(dp_index, "")
            if weapon_name != "":
                pdf.set_x(x=self.col_middle_line)
                pdf.cell(w = self.width_weapon_name,  h = self.row_height, ln=False, align='L', text=f"{weapon_qty} {weapon_name}")
                pdf.set_x(x=self.col_facing)
                pdf.cell(w = self.width_weapon_facing, h = self.row_height, ln=False, align='L', text=f"{weapon_facing}")
                pdf.set_x(x=self.col_to_hit)
                pdf.cell(w = self.width_weapon_to_hit, h = self.row_height, ln=False, align='L', text=f"{weapon_to_hit}")
                pdf.set_x(x=self.col_damage)
                pdf.cell(w = self.width_weapon_damage, h = self.row_height, ln=False, align='L', text=f"{weapon_damage}")
                pdf.set_x(x=self.col_ammo)
                pdf.cell(w = self.width_weapon_ammo,   h = self.row_height, ln=False, align='L', text=f"{weapon_ammo}")
                pdf.set_x(x=self.col_weapon_dp)
                pdf.cell(w = self.width_weapon_dp,     h = self.row_height, ln=False, align='L', text=f"{weapon_dp}")
            pdf.cell(w = self.col_right_edge, h = self.row_height, text="", ln=True, align='C') # Weapon Line Header

    def draw_accessories(self, pdf: FPDF, input_dict: dict):
        """Given an FPDF object and an input_dict, draw the accessories section"""
        pdf.set_x(x=self.col_middle_line)
        pdf.cell(w = self.col_facing - self.col_middle_line, h = self.row_height, ln=True, align='L', text="Accessory")
        self.spoiler_airdam_count: int = 0
        self.ramplate_count: int = 0
        self.wheelhub_count: int = 0
        self.wheelguard_count: int = 0
        self.bumper_spike_count: int = 0
        for acc_index in range(1, 31, 2): #print all the accessory entries
            qty_index     = f"accessory_{acc_index}_qty"
            name_index    = f"accessory_{acc_index}_name"
            accessory_qty    = input_dict.get(qty_index, "")
            accessory_name   = input_dict.get(name_index, "")
            if accessory_qty != '0' and accessory_name != "Accessory": #Something meaningful has been selected
                if "Spoiler" in accessory_name:
                    self.spoiler_airdam_count += int(accessory_qty)
                elif "Ramplate" in accessory_name:
                    self.ramplate_count += 1
                elif "Wheelhub" in accessory_name:
                    self.wheelhub_count += int(accessory_qty)
                elif "Wheelguard" in accessory_name:
                    self.wheelguard_count += int(accessory_qty)
                elif "Bumper Spikes" in accessory_name:
                    self.bumper_spike_count += 1
                pdf.set_x(x=self.col_middle_line)
                pdf.cell(w = self.col_facing - self.col_middle_line, h = self.row_height, ln=False, align='L', text=f"{accessory_qty} {accessory_name}")
            qty_index     = f"accessory_{acc_index+1}_qty"
            name_index    = f"accessory_{acc_index+1}_name"
            accessory_qty    = input_dict.get(qty_index, "")
            accessory_name   = input_dict.get(name_index, "")
            if accessory_qty != '0' and accessory_name != "Accessory": #Something meaningful has been selected
                if "Spoiler" in accessory_name:
                    self.spoiler_airdam_count += int(accessory_qty)
                elif "Ramplate" in accessory_name:
                    self.ramplate_count += 1
                elif "Wheelhub" in accessory_name:
                    self.wheelhub_count += int(accessory_qty)
                elif "Wheelguard" in accessory_name:
                    self.wheelguard_count += int(accessory_qty)
                elif "Bumper Spikes" in accessory_name:
                    self.bumper_spike_count += 1
                pdf.set_x(x=self.col_to_hit)
                pdf.cell(w = self.col_facing - self.col_middle_line, h = self.row_height, ln=False, align='L', text=f"{accessory_qty} {accessory_name}")
            pdf.cell(w = self.col_right_edge, h = self.row_height, text="", ln=True, align='C')
        pdf.cell(w = self.col_right_edge, h = self.row_height, text="", ln=True, align='C')

    def draw_speed(self, pdf: FPDF, input_dict: dict):
        """Given an FPDF object and an input_dict, draw the speed section"""
        pdf.set_x(x=self.col_middle_line)
        pdf.cell(w=self.col_middle_line, h = self.row_height, ln=True, align='L', text="Speed and Handling Record")
        for self.row_index in range(1,19):
            line_str: str = f"   {self.row_index:>2} _____  10   9   8   7   6   5   4  3   2   1   0   -1   -2   -3   -4   -5   -6"
            pdf.set_x(x=self.col_middle_line)
            pdf.cell(w = self.col_middle_line, h = self.row_height, ln=True, align='L', text=line_str)

    def draw_car_image(self, pdf: FPDF, input_dict: dict):
        """Given an FPDF object and an input_dict, draw the car image section"""
        #create car image here with checkboxes for damage
        #Draw rectangles
        column_count = 23
        row_count = 20
        cell_width = 2
        cell_height = 2
        pdf.set_draw_color(0, 0, 0) # Set border color (RGB)

        #Draw body
        x_value = self.col_left_edge + cell_width * 1
        y_value = self.row_5
        w_value = cell_width * 33
        h_value = cell_height * 23
        first_quarter_y = cell_height * 7
        mid_point_y     = cell_height * 11
        third_quarter_y = cell_height * 18
        first_quarter_x = cell_width * 10
        turret_x        = cell_width * 15
        mid_point_x     = cell_width * 16
        third_quarter_x = cell_width * 23
        pdf.rect(x = x_value, y = y_value, w = w_value, h = h_value, style = "D") #CWVRS line

        pdf.set_y(y=self.row_3)
        pdf.set_x(x=self.col_left_edge + mid_point_x - cell_width * 4)
        pdf.cell(w = 10, h = self.row_height, text="Front ===>>>>", ln=False, align='L')


        rear_tire_dp: int = int(input_dict.get("rear_tire_dp", "0"))
        front_tire_dp: int = int(input_dict.get("front_tire_dp", "0"))
        #Draw back left tire
        if rear_tire_dp > 0:
            self.draw_block(pdf,
                            x_start = self.col_left_edge + cell_width * 2,
                            y_start = y_value-cell_height,
                            block_count = rear_tire_dp,
                            print_down = False,
                            print_right = True,
                            forced_columns=0)
        #Draw front left tire
        if front_tire_dp > 0:
            self.draw_block(pdf,
                            x_start = self.col_left_edge + cell_width * 32,
                            y_start = y_value-cell_height,
                            block_count = front_tire_dp,
                            print_down = False,
                            print_right = False,
                            forced_columns=0)
        #Draw front right tire
        if front_tire_dp > 0:
            self.draw_block(pdf,
                            x_start = self.col_left_edge + cell_width * 32,
                            y_start = y_value + cell_height*23,
                            block_count = front_tire_dp,
                            print_down = True,
                            print_right = False,
                            forced_columns=0)
        #Draw back right tire
        if rear_tire_dp > 0:
            self.draw_block(pdf,
                            x_start = self.col_left_edge + cell_width * 2,
                            y_start = y_value + cell_height*23,
                            block_count = rear_tire_dp,
                            print_down = True,
                            print_right = True,
                            forced_columns=0)

        #Scan the Accessories list for any wheeguards or hubs
        #Make the following presumptions:
        #1) wheelhubs at or under 20 are intended for the front wheels first
        #2) All values that are even are presumed to be evenly distributed
        #3) Without a very specific allocation of wheel hub and wheel guard armor, this will have to do
        wheel_armor_front_qty: int = 0
        wheel_armor_back_qty: int = 0
        wheel_armor_hub_qty: int = 0
        for wheel_armor_index in range (1,31):
            qty_index    = f"accessory_{wheel_armor_index}_qty"
            qty_str = input_dict.get(qty_index, "0")
            if qty_str == "":
                qty = 0
            else:
                qty = int(qty_str)
            if qty > 0: #not every entry will have a count
                name_index   = f"accessory_{wheel_armor_index}_name"
                name = input_dict.get(name_index, "")
                if 'Wheelguards, Front' in name:
                    wheel_armor_front_qty += qty
                elif 'Wheelguards, Rear' in name:
                    wheel_armor_back_qty += qty
                elif 'Wheelhubs' in name: 
                    wheel_armor_hub_qty += qty
        if wheel_armor_hub_qty > 0:
            if wheel_armor_hub_qty > 20: #presume to divide across all four tires
                # back right
                self.draw_block(pdf, x_start = self.col_left_edge + cell_width,
                                     y_start = y_value + cell_height * 25,
                                     block_count = int(wheel_armor_hub_qty/4),
                                     print_down = True,
                                     print_right = True,
                                     forced_columns = 1)
                # back left
                self.draw_block(pdf, x_start = self.col_left_edge + cell_width,
                                     y_start = y_value-cell_height * 3,
                                     block_count = int(wheel_armor_hub_qty/4),
                                     print_down = False,
                                     print_right = True,
                                     forced_columns = 1)
                #front right
                self.draw_block(pdf, x_start = self.col_left_edge + cell_width * 33,
                                     y_start = y_value + cell_height * 25,
                                     block_count = int(wheel_armor_hub_qty/4),
                                     print_down = True,
                                     print_right = False,
                                     forced_columns = 1)
                #front left
                self.draw_block(pdf, x_start = self.col_left_edge + cell_width * 33,
                                     y_start = y_value-cell_height * 3,
                                     block_count = int(wheel_armor_hub_qty/4),
                                     print_down = False,
                                     print_right = False,
                                     forced_columns = 1)
            else: #presume just the front tires
                #front right
                self.draw_block(pdf, x_start = self.col_left_edge + cell_width * 33,
                                     y_start = y_value + cell_height * 25,
                                     block_count = int(wheel_armor_hub_qty/2),
                                     print_down = True,
                                     print_right = False,
                                     forced_columns = 1)
                #front left
                self.draw_block(pdf, x_start = self.col_left_edge + cell_width * 33,
                                     y_start = y_value-cell_height * 3,
                                     block_count = int(wheel_armor_hub_qty/2),
                                     print_down = False,
                                     print_right = False,
                                     forced_columns = 1)
        if wheel_armor_back_qty > 0:
            # back right
            self.draw_block(pdf, x_start = self.col_left_edge + cell_width,
                                 y_start = y_value + cell_height * 26,
                                 block_count = int(wheel_armor_back_qty/2),
                                 print_down = True,
                                 print_right = True,
                                 forced_columns = 1)
            # back left
            self.draw_block(pdf,
                            x_start = self.col_left_edge + cell_width,
                            y_start = y_value-cell_height * 4,
                            block_count = int(wheel_armor_back_qty/2),
                            print_down = False,
                            print_right = True,
                            forced_columns = 1)
        if wheel_armor_front_qty > 0:
            #front right
            self.draw_block(pdf, x_start = self.col_left_edge + cell_width * 33,
                                 y_start = y_value + cell_height * 26,
                                 block_count = int(wheel_armor_front_qty/2),
                                 print_down = True,
                                 print_right = False,
                                 forced_columns = 1)
            #front left
            self.draw_block(pdf,
                            x_start = self.col_left_edge + cell_width * 33,
                            y_start = y_value-cell_height * 4,
                            block_count = int(wheel_armor_front_qty/2),
                            print_down = False,
                            print_right = False,
                            forced_columns = 1)

        #Weapons list
        front_list:  list = []
        right_list:  list = []
        left_list:   list = []
        back_list:   list = []
        top_list:    list = []
        bottom_list: list = []
        driver_list: list = []
        gunner_list: list = []
        d_g_list:    list = []
        engine_list: list = []
        tank_list:   list = []

        #draw the optional component armor sections, based on which component it is protecting
        for row_index in range(1,6):
            dp_index     = f"ca_{row_index}_dp"
            ca_dp        = int(input_dict.get(dp_index, ""))
            if ca_dp != 0: #skip one if the dp is zero
                facing_index = f"ca_{row_index}_facing"
                type_index   = f"ca_{row_index}_type"
                ca_facing    = input_dict.get(facing_index, "")
                #ca_type      = input_dict.get(type_index, "").replace(" Component Armor", "")
                if ca_facing == "Front":
                    front_list.append(("CA", ca_dp))
                elif ca_facing == "Back":
                    back_list.append(("CA", ca_dp))
                elif ca_facing == "Left":
                    left_list.append(("CA", ca_dp))
                elif ca_facing == "Right":
                    right_list.append(("CA", ca_dp))
                elif ca_facing == "Top":
                    top_list.append(("CA", ca_dp))
                elif ca_facing == "Underbody":
                    bottom_list.append(("CA", ca_dp))
                elif ca_facing == "Driver":
                    driver_list.append(("CA", ca_dp))
                elif ca_facing == "Gunner":
                    gunner_list.append(("CA", ca_dp))
                elif ca_facing == "Driver & Gunner":
                    d_g_list.append(("CA", ca_dp))
                elif ca_facing == "Power Plant":
                    engine_list.append(("CA", ca_dp))
                elif ca_facing == "Gas Tank":
                    tank_list.append(("CA", ca_dp))
        for weapon_index in range (1, self.weapon_rows_count + 1):
            qty_index    = f"weapon_{weapon_index}_qty"
            qty_str = input_dict.get(qty_index, "0")
            if qty_str == "":
                qty = 0
            else:
                qty = int(qty_str)
            if qty > 0: #not every entry will have a count
                name_index   = f"weapon_{weapon_index}_name"
                facing_index = f"weapon_{weapon_index}_facing"
                dp_index     = f"weapon_{weapon_index}_dp"
                name = input_dict.get(name_index, "")
                facing = input_dict.get(facing_index, "")
                dp_str = input_dict.get(dp_index, "0")
                if dp_str == "":
                    dp = 0
                else:
                    dp = int(dp_str)
                if facing == "Top":
                    for _ in range(0,qty):
                        top_list.append((name, dp))
                if facing == "Front":
                    for _ in range(0,qty):
                        front_list.append((name, dp))
                if facing == "Back":
                    for _ in range(0,qty):
                        back_list.append((name, dp))
                if facing == "Right":
                    for _ in range(0,qty):
                        right_list.append((name, dp))
                if facing == "Left":
                    for _ in range(0,qty):
                        left_list.append((name, dp))
                if facing == "Underbody":
                    for _ in range(0,qty):
                        bottom_list.append((name, dp))
        #iterate thru the lists and display the cells based on how many weapons there are on a facing
        if len(front_list) > 0:
            x_start = x_value + w_value - cell_width
            y_start = y_value + mid_point_y - ((len(front_list) - 1) * cell_height * 2)/2
            self.draw_weapon_facing(pdf=pdf, input_list = front_list, facing = "front", x_start = x_start, y_start = y_start, print_down = True, print_right = False, increment_x = False)
        if len(back_list) > 0:
            x_start = x_value
            y_start = y_value + mid_point_y - ((len(back_list) - 1) * cell_height * 2)/2
            self.draw_weapon_facing(pdf=pdf, input_list = back_list, facing = "back", x_start = x_start, y_start = y_start, print_down = True, print_right = True, increment_x = False)
        if len(right_list) > 0:
            x_start = self.col_left_edge + mid_point_x - ((len(right_list) - 1) * cell_width * 2)/2
            y_start = y_value + h_value - cell_height
            self.draw_weapon_facing(pdf=pdf, input_list = right_list,  facing = "right",x_start = x_start, y_start = y_start, print_down = False, print_right = True, increment_x = True)
        if len(left_list) > 0:
            x_start = self.col_left_edge + mid_point_x - ((len(left_list) - 1) * cell_width * 2)/2
            y_start = y_value
            self.draw_weapon_facing(pdf=pdf, input_list = left_list, facing = "left", x_start = x_start, y_start = y_start, print_down = True, print_right = True, increment_x = True)
        if len(top_list) > 0:
            x_start = self.col_left_edge + turret_x
            y_start = y_value + mid_point_y - ((len(top_list) - 1) * cell_height * 2)/2
            self.draw_weapon_facing(pdf = pdf, input_list = top_list,
                            facing = "top",
                            x_start = x_start,
                            y_start = y_start,
                            print_down = True,
                            print_right = False,
                            increment_x = False)
        if len(bottom_list) > 0:
            x_start = self.col_left_edge + turret_x
            y_start = y_value + third_quarter_y - ((len(bottom_list) - 1) * cell_height * 2)/2
            self.draw_weapon_facing(pdf = pdf, input_list = bottom_list,
                            facing = "bottom",
                            x_start = x_start,
                            y_start = y_start,
                            print_down = True,
                            print_right = False,
                            increment_x = False)

        #draw engine and optional gas tank
        engine_dp_str = input_dict.get("Engine_DP", "0")
        engine_dp = int(engine_dp_str)
        if engine_dp > 0:
            pdf.set_y(y=y_value + first_quarter_y - cell_height)
            pdf.set_x(x=self.col_left_edge + third_quarter_x)
            pdf.cell(w = 10, h = self.row_height, text="PP", ln=False, align='L')
        if len(engine_list) > 0:
            for entry_name, entry_dp in engine_list:
                engine_dp += int(entry_dp) # Add the component armor to the engine (this might go slightly wrong with metal)
        divider: int = math.ceil(engine_dp/8)
        if divider == 0:
            divider = 1
        self.draw_block(pdf,
                            x_start = self.col_left_edge + third_quarter_x,
                            y_start = y_value + first_quarter_y + cell_height,
                            block_count = engine_dp,
                            print_down = True,
                            print_right = True,
                            forced_columns=math.ceil(engine_dp/divider))

        gas_tank_dp = int(self.label_hidden_gas_tank_dp.cget("text"))
        if len(tank_list) > 0:
            for entry_name, entry_dp in tank_list:
                gas_tank_dp += int(entry_dp) # Add the component armor to the gas tank (this might go slightly wrong with metal)
        if gas_tank_dp > 0:
            pdf.set_y(y=y_value + first_quarter_y - cell_height)
            pdf.set_x(x=self.col_left_edge + first_quarter_x-cell_width*2)
            pdf.cell(w = 10, h = self.row_height, text="GT", ln=False, align='L')
            self.draw_block(pdf,
                            x_start = self.col_left_edge + first_quarter_x,
                            y_start = y_value + first_quarter_y + cell_height,
                            block_count = gas_tank_dp,
                            print_down = True,
                            print_right = False,
                            forced_columns=int(gas_tank_dp/3))

        #draw driver and optional gunner
        crew_count: int = int(input_dict.get("driver_gunner", 0))
        pass_count: int = int(input_dict.get("passenger", 0))
        driver_dp: int = 3
        gunner_dp: int = 3

        body_armor_count = 0
        body_armor_list: list = []
        for pe_index in range (1,11):
            qty_index  = f"pe_qty_{pe_index}"
            qty_value  = int(input_dict.get(qty_index, "0"))
            if qty_value > 0:
                name_index = f"pe_name_{pe_index}"
                name_str   = input_dict.get(name_index, "")
                if name_str in ['Body Armor', "Body Armor, Blended", "Body Armor, Improved", "Body Armor, Improved, Blended", "Impact Armor", "Spiked Armor"]:
                    body_armor_count += 1
                    if name_str in ["Body Armor, Improved", "Body Armor, Improved, Blended", "Impact Armor", "Spiked Armor"]:
                        for qty_index in range(0, qty_value):
                            body_armor_list.append((name_str, qty_value, 6))
                    else:
                        for qty_index in range(0, qty_value):
                            body_armor_list.append((name_str, qty_value, 3))

        if len(body_armor_list) > 0:
            name_str, qty_value, ba_dp = body_armor_list[0]
            driver_dp += ba_dp
        if len(driver_list) > 0:
            for _, entry_dp in driver_list:
                driver_dp += int(entry_dp) # Add the component armor to the driver (this might go slightly wrong with metal)
        if len(body_armor_list) > 1:
            name_str, qty_value, ba_dp = body_armor_list[1]
            gunner_dp += ba_dp
        if len(gunner_list) > 0:
            for _, entry_dp in gunner_list:
                gunner_dp += int(entry_dp) # Add the component armor to the driver (this might go slightly wrong with metal)

        if crew_count > 0:
            pdf.set_y(y=y_value + first_quarter_y - cell_height)
            pdf.set_x(x=self.col_left_edge + mid_point_x + cell_width * 3)
            pdf.cell(w = 10, h = self.row_height, text="DR", ln=False, align='L')
            self.draw_block(pdf,
                            x_start = self.col_left_edge + third_quarter_x - cell_width * 2,
                            y_start = y_value + mid_point_y,
                            block_count = driver_dp, #expand for body armor and component armor
                            print_down = False,
                            print_right = False,
                            forced_columns=4)
        if crew_count > 1:
            pdf.set_y(y= y_value + mid_point_y + cell_height)
            pdf.set_x(x=self.col_left_edge + mid_point_x + cell_width * 3)
            pdf.cell(w = 10, h = self.row_height, text="GR", ln=False, align='L')
            self.draw_block(pdf,
                            x_start = self.col_left_edge + third_quarter_x - cell_width * 2,
                            y_start = y_value + mid_point_y + cell_height * 3,
                            block_count = gunner_dp, #expand for body armor and component armor
                            print_down = True,
                            print_right = False,
                            forced_columns=4)
        d_g_dp: int = 0
        if len(d_g_list) > 0:
            for entry_name, entry_dp in d_g_list:
                d_g_dp += int(entry_dp) # Add the component armor to the driver (this might go slightly wrong with metal)
        if d_g_dp > 0:
            self.draw_block(pdf,
                            x_start = self.col_left_edge + mid_point_x + cell_width * 2,
                            y_start = y_value + mid_point_y - cell_height * 5,
                            block_count = d_g_dp, #expand for body armor and component armor
                            print_down = True,
                            print_right = False,
                            forced_columns=d_g_dp)

    def draw_weapon_facing(self, pdf: FPDF,
                            input_list: list,
                            facing: str,
                            x_start: int,
                            y_start: int,
                            print_down: bool,
                            print_right: bool,
                            increment_x: bool):
        """given the existing parameters, draw the blocks necessary"""
        ca_found: bool = False
        cell_width = 2
        cell_height = 2
        local_x_start = x_start
        local_y_start = y_start
        x_adjustment = 0
        y_adjustment = 0
        if facing == "front":
            x_adjustment = (-1) * cell_width
        elif facing in ["top", "bottom"]:
            x_adjustment = (-1) * cell_width # force CA to be two columns for space savings
        elif facing == "back":
            x_adjustment = cell_width
        elif facing == "left":
            y_adjustment = cell_height
        elif facing == "right":
            y_adjustment = (-1) * cell_height

        for local_name, local_dp in input_list:
            local_x_start = x_start
            local_y_start = y_start
            forced_columns = 0
            if not ca_found:
                ca_found = local_name == "CA" #only set this once, if ever
                if ca_found:
                    if facing in ["front", "back", "top", "bottom"]: # the local_y_start is adjusted for centering the number of weapons vertically
                        local_y_start = self.row_5 + cell_height * (16 - local_dp)
                        forced_columns = local_dp
                    elif facing in ["left", "right"]:
                        local_x_start = self.col_left_edge + cell_width * (16 - local_dp/2)
                        forced_columns = 1
                else:
                    if facing in ["front", "back"]: # the local_y_start is adjusted for centering the number of weapons vertically
                        forced_columns = 0
                    elif facing in ["top", "bottom"]:
                        forced_columns = 0
                    elif facing in ["left", "right"]:
                        forced_columns = local_dp

            else: #This is for the weapon adjustments after the CA has printed, or if there is no CA at all
                if facing in ["front", "back"]:
                    local_x_start = x_start + x_adjustment
                if facing in ["top", "bottom"]:
                    local_x_start = x_start + x_adjustment
                    forced_columns = 2 # try to make the weapons squared up for space savings
                elif facing in ["left", "right"]:
                    local_y_start = y_start + y_adjustment
                    forced_columns = local_dp

            self.draw_block(pdf,
                        x_start = local_x_start,
                        y_start = local_y_start,
                        block_count = local_dp,
                        print_down = print_down,
                        print_right = print_right,
                        forced_columns = forced_columns)
            if local_name != "CA":
                if increment_x:
                    x_start += cell_width * 2
                else:
                    y_start += cell_height * 2
                    if facing in ["top", "bottom"]:
                        y_start += cell_height

    def draw_block(self, pdf: FPDF, x_start: int, y_start: int, block_count: int, print_down: bool, print_right: bool, forced_columns: int):
        """Given a pdf, starting coordinates and block_count, create a rectangle of identical squares,
           adjust to make the smalles footprint possible"""
        cell_width = 2
        cell_height = 2
        row_max = 1
        row_max_add = 1
        cell_count = 0
        if block_count > 6: #large number
            row_max = 2
        if forced_columns > 0:
            row_max = forced_columns
        if print_down and print_right:
            for row_index in range(0, row_max): #range treats the upper limit as "less than", not "less than or equal to"
                for col_index in range(0, math.ceil(block_count/row_max)): #row_max should never be zero
                    x_value = x_start + (cell_width * col_index)
                    y_value = y_start + (cell_height * row_index)
                    if cell_count < block_count:
                        pdf.rect(x = x_value, y = y_value, w=cell_width, h=cell_height, style="D") #CWVRS line
                    cell_count += 1
        elif print_down and not print_right:
            for row_index in range(0, row_max): #range treats the upper limit as "less than", not "less than or equal to"
                for col_index in reversed(range(0, math.ceil(block_count/row_max))): #row_max should never be zero
                    x_value = x_start - (cell_width * col_index)
                    y_value = y_start + (cell_height * row_index)
                    if cell_count < block_count:
                        pdf.rect(x = x_value, y = y_value, w=cell_width, h=cell_height, style="D") #CWVRS line
                    cell_count += 1
        elif not print_down and print_right:
            for row_index in reversed(range(0, row_max)): #range treats the upper limit as "less than", not "less than or equal to"
                for col_index in range(0, math.ceil(block_count/row_max)): #row_max should never be zero
                    x_value = x_start + (cell_width * col_index)
                    y_value = y_start - (cell_height * row_index)
                    if cell_count < block_count:
                        pdf.rect(x = x_value, y = y_value, w=cell_width, h=cell_height, style="D") #CWVRS line
                    cell_count += 1
        elif not print_down and not print_right:
            for row_index in reversed(range(0, row_max)): #range treats the upper limit as "less than", not "less than or equal to"
                for col_index in reversed(range(0, math.ceil(block_count/row_max))): #row_max should never be zero
                    x_value = x_start - (cell_width * col_index)
                    y_value = y_start - (cell_height * row_index)
                    if cell_count < block_count:
                        pdf.rect(x = x_value, y = y_value, w=cell_width, h=cell_height, style="D") #CWVRS line
                    cell_count += 1

    def draw_ca(self, pdf: FPDF, input_dict: dict):
        """Given an FPDF object and an input_dict, draw the component armor section"""
        #Resest pdf.Y to the proper area once everything on the right is written
        pdf.set_y(y=self.row_16)
        pdf.cell(w=self.col_middle_line, h = self.row_height, ln=False, align='L', text="Component Armor:")
        pdf.set_x(x=self.col_ca_type)
        pdf.cell(w=self.col_middle_line, h = self.row_height, ln=False, align='L', text="Type:")
        pdf.set_x(x=self.col_ca_dp)
        pdf.cell(w=self.col_middle_line, h = self.row_height, ln=True, align='L', text="DP:")
        for self.row_index in range(1,6):
            facing_index = f"ca_{self.row_index}_facing"
            type_index   = f"ca_{self.row_index}_type"
            dp_index     = f"ca_{self.row_index}_dp"
            ca_facing    = input_dict.get(facing_index, "")
            ca_type      = input_dict.get(type_index, "").replace(" Component Armor", "")
            ca_dp        = input_dict.get(dp_index, "")
            if ca_dp != '0':
                pdf.set_x(x=self.col_left_edge)
                pdf.cell(w = self.col_right_edge, h = self.row_height, ln=False, align='L', text=ca_facing)
                pdf.set_x(x=self.col_ca_type)
                pdf.cell(w = self.col_right_edge, h = self.row_height, ln=False, align='L', text=ca_type)
                pdf.set_x(x=self.col_ca_dp)
                pdf.cell(w = self.col_right_edge, h = self.row_height, ln=False, align='L', text=ca_dp)
            pdf.cell(w = self.col_right_edge, h = self.row_height, text="", ln=True, align='C')

    def draw_engine(self, pdf: FPDF, input_dict: dict):
        """Given an FPDF object and an input_dict, draw the engine section"""
        pdf.cell(w=self.col_middle_line, h = self.row_height, ln=True, align='L', text="Engine and Tank DP:")
        pdf.set_x(x=self.col_left_edge)
        pdf.cell(w = self.col_right_edge, h = self.row_height, text=input_dict.get("Engine_Type",""), ln=False, align='L')
        pdf.set_x(x=self.col_engine_dp)
        pdf.cell(w = self.col_right_edge, h = self.row_height, text=input_dict.get("Engine_DP", ""), ln=False, align='L')
        if input_dict.get("GasQty", "") != "":
            pdf.set_x(x=self.col_engine_tank)
            pdf.cell(w = self.col_right_edge, h = self.row_height, text=input_dict.get("GasTank", "").replace(" Gas Tank", ""), ln=False, align='L')
            pdf.set_x(x=self.col_engine_tkdp)
            pdf.cell(w = self.col_right_edge, h = self.row_height, text=input_dict.get("GasDp", ""), ln=False, align='L')
        pdf.cell(w = self.col_right_edge, h = self.row_height, text="", ln=True, align='C')

    def draw_tires(self, pdf: FPDF, input_dict: dict):
        """Given an FPDF object and an input_dict, draw the tires section"""
        pdf.cell(w=self.col_middle_line, h = self.row_height, ln=True, align='L', text="Tires:")
        local_front_tire_qty  = str(input_dict.get("front_tire_qty", ""))
        local_front_tire_name = str(input_dict.get("front_tire", ""))
        local_front_tire_dp   = str(input_dict.get("front_tire_dp", ""))
        local_rear_tire_qty   = str(input_dict.get("rear_tire_qty", ""))
        local_rear_tire_name  = str(input_dict.get("rear_tire", ""))
        local_rear_tire_dp    = str(input_dict.get("rear_tire_dp", ""))
        if local_front_tire_qty != "":
            pdf.set_x(x=self.col_left_edge)
            pdf.cell(h = self.row_height, text=local_front_tire_qty, ln=False, align='L')
            pdf.set_x(x=self.col_ca_type)
            pdf.cell(h = self.row_height, text=local_front_tire_name, ln=False, align='L')
            pdf.set_x(x=self.col_ca_dp)
            pdf.cell(h = self.row_height, text=local_front_tire_dp, ln=False, align='L')
        pdf.cell(w = self.col_right_edge, h = self.row_height, text="", ln=True, align='C')
        if local_rear_tire_qty != "":
            pdf.set_x(x=self.col_left_edge)
            pdf.cell(h = self.row_height, text=local_rear_tire_qty, ln=False, align='L')
            pdf.set_x(x=self.col_ca_type)
            pdf.cell(h = self.row_height, text=local_rear_tire_name, ln=False, align='L')
            pdf.set_x(x=self.col_ca_dp)
            pdf.cell(h = self.row_height, text=local_rear_tire_dp, ln=False, align='L')
        pdf.cell(w = self.col_right_edge, h = self.row_height, text="", ln=True, align='C')

    def draw_armor(self, pdf: FPDF, input_dict: dict):
        """Given an FPDF object and an input_dict, draw the Notes section"""
        pdf.cell(w=self.col_middle_line, h = self.row_height, ln=True, align='L', text="Armor:")

        local_outer_front_qty  = input_dict.get("armor_outer_front_qty","")
        local_inner_front_qty  = input_dict.get("armor_inner_front_qty","")
        local_outer_back_qty   = input_dict.get("armor_outer_back_qty","")
        local_inner_back_qty   = input_dict.get("armor_inner_back_qty","")
        local_outer_left_qty   = input_dict.get("armor_outer_left_qty","")
        local_inner_left_qty   = input_dict.get("armor_inner_left_qty","")
        local_outer_right_qty  = input_dict.get("armor_outer_right_qty","")
        local_inner_right_qty  = input_dict.get("armor_inner_right_qty","")
        local_outer_top_qty    = input_dict.get("armor_outer_top_qty","")
        local_inner_top_qty    = input_dict.get("armor_inner_top_qty","")
        local_outer_bottom_qty = input_dict.get("armor_outer_bottom_qty","")
        local_inner_bottom_qty = input_dict.get("armor_inner_bottom_qty","")

        any_outer: bool = local_outer_front_qty  != "0" or \
                          local_outer_back_qty   != "0" or \
                          local_outer_left_qty   != "0" or \
                          local_outer_right_qty  != "0" or \
                          local_outer_top_qty    != "0" or \
                          local_outer_bottom_qty != "0"
        any_inner: bool = local_inner_front_qty  != "0" or \
                          local_inner_back_qty   != "0" or \
                          local_inner_left_qty   != "0" or \
                          local_inner_right_qty  != "0" or \
                          local_inner_top_qty    != "0" or \
                          local_inner_bottom_qty != "0"

        if any_outer:
            local_outer_armor_name = input_dict.get("Outer_Armor_Name", "").replace(" Outer Armor", "")
            pdf.set_x(x=self.col_left_armor)
            pdf.cell(h = self.row_height, text=local_outer_armor_name, ln=False, align='L')
        if any_inner:
            local_inner_armor_name = input_dict.get("Inner_Armor_Name","").replace(" Inner Armor", "")
            pdf.set_x(x=self.col_middle_armor)
            pdf.cell(h = self.row_height, text=local_inner_armor_name, ln=False, align='L')
        pdf.cell(w = self.col_right_edge, h = self.row_height, text="", ln=True, align='C')

        pdf.set_x(x=self.col_left_edge)
        pdf.cell(h = self.row_height, text="Front", ln=False, align='L')
        if local_outer_front_qty  != "0":
            pdf.set_x(x=self.col_left_armor)
            pdf.cell(h = self.row_height, text=local_outer_front_qty, ln=False, align='L')
        if local_inner_front_qty  != "0":
            pdf.set_x(x=self.col_middle_armor)
            pdf.cell(h = self.row_height, text=local_inner_front_qty, ln=False, align='L')
        pdf.cell(w = self.col_right_edge, h = self.row_height, text="", ln=True, align='C')

        pdf.set_x(x=self.col_left_edge)
        pdf.cell(h = self.row_height, text="Back", ln=False, align='L')
        pdf.set_x(x=self.col_left_edge)
        pdf.cell(h = self.row_height, text="L", ln=False, align='L')
        if local_outer_back_qty   != "0":
            pdf.set_x(x=self.col_left_armor)
            pdf.cell(h = self.row_height, text=local_outer_back_qty, ln=False, align='L')
        if local_inner_back_qty   != "0":
            pdf.set_x(x=self.col_middle_armor)
            pdf.cell(h = self.row_height, text=local_inner_front_qty, ln=False, align='L')
        pdf.cell(w = self.col_right_edge, h = self.row_height, text="", ln=True, align='C')

        pdf.set_x(x=self.col_left_edge)
        pdf.cell(h = self.row_height, text="Left", ln=False, align='L')
        if local_outer_left_qty   != "0":
            pdf.set_x(x=self.col_left_armor)
            pdf.cell(h = self.row_height, text=local_outer_left_qty, ln=False, align='L')
        if local_inner_left_qty   != "0":
            pdf.set_x(x=self.col_middle_armor)
            pdf.cell(h = self.row_height, text=local_inner_left_qty, ln=False, align='L')
        pdf.cell(w = self.col_right_edge, h = self.row_height, text="", ln=True, align='C')

        pdf.set_x(x=self.col_left_edge)
        pdf.cell(h = self.row_height, text="Right", ln=False, align='L')
        if local_outer_right_qty  != "0":
            pdf.set_x(x=self.col_left_armor)
            pdf.cell(h = self.row_height, text=local_outer_right_qty, ln=False, align='L')
        if local_inner_right_qty  != "0":
            pdf.set_x(x=self.col_middle_armor)
            pdf.cell(h = self.row_height, text=local_inner_right_qty, ln=False, align='L')
        pdf.cell(w = self.col_right_edge, h = self.row_height, text="", ln=True, align='C')

        pdf.set_x(x=self.col_left_edge)
        pdf.cell(h = self.row_height, text="Top", ln=False, align='L')
        if local_outer_top_qty    != "0":
            pdf.set_x(x=self.col_left_armor)
            pdf.cell(h = self.row_height, text=local_outer_top_qty, ln=False, align='L')
        if local_inner_top_qty    != "0":
            pdf.set_x(x=self.col_middle_armor)
            pdf.cell(h = self.row_height, text=local_inner_top_qty, ln=False, align='L')
        pdf.cell(w = self.col_right_edge, h = self.row_height, text="", ln=True, align='C')

        pdf.set_x(x=self.col_left_edge)
        pdf.cell(h = self.row_height, text="Bottom", ln=False, align='L')
        if local_outer_bottom_qty != "0":
            pdf.set_x(x=self.col_left_armor)
            pdf.cell(h = self.row_height, text=local_outer_bottom_qty, ln=False, align='L')
        if local_inner_bottom_qty != "0":
            pdf.set_x(x=self.col_middle_armor)
            pdf.cell(h = self.row_height, text=local_inner_bottom_qty, ln=False, align='L')
        pdf.cell(w = self.col_right_edge, h = self.row_height, text="", ln=True, align='C')

    def draw_notes(self, pdf: FPDF, input_dict: dict):
        """Given an FPDF object and an input_dict, draw the Notes section"""
        pdf.cell(w = self.col_middle_line, h = self.row_height, ln=False, align='L', text="Notes:")
        pdf.cell(w = self.col_right_edge, h = self.row_height, text="", ln=True, align='C')
        pdf.cell(w = self.col_right_edge, h = self.row_height, text="", ln=True, align='C')
        pdf.cell(w = self.col_right_edge, h = self.row_height, text="", ln=True, align='C')
        pdf.cell(w = self.col_right_edge, h = self.row_height, text="", ln=True, align='C')
        pdf.cell(w = self.col_right_edge, h = self.row_height, text="", ln=True, align='C')

    def draw_walkarounds(self, pdf: FPDF, input_dict: dict):
        """Given an FPDF object and an input_dict, draw the WalkAround section"""
        pdf.cell(w=self.col_middle_line, h = self.row_height, ln=True, align='L', text="Walkaround:")

        #Walkaround Line 1
        crew_count: int = int(input_dict.get("driver_gunner", 0))
        pass_count: int = int(input_dict.get("passenger", 0))
        tire_count: int = int(input_dict.get("front_tire_qty", 0)) + int(input_dict.get("rear_tire_qty", 0))
        line_text: str = f'{input_dict.get("Body", "")}, {input_dict.get("Engine_Type", "")} Engine, Crew: {crew_count}'
        pdf.set_x(self.col_left_edge)
        pdf.cell(h = self.row_height, text=line_text, ln=True, align='L')

        #Walkaround Line 2
        pass_text: str = ""
        tire_text: str = f'Tire Count: {tire_count}'
        if pass_count > 0: #this is rare
            pass_text = f'Pass: {pass_count} '
        line_text: str = f'{pass_text}{tire_text}'
        pdf.set_x(self.col_left_edge)
        pdf.cell(h = self.row_height, text=line_text, ln=True, align='L')

        #Walkaround Line 3
        spoiler_airdam_text: str = ""
        ramplate_text: str = ""
        wheelhub_text: str = ""
        wheelguard_text: str = ""
        bumper_spike_text: str = ""
        if self.spoiler_airdam_count > 0:
            spoiler_airdam_text = f'Spoiler/airdam: {self.spoiler_airdam_count} '
        if self.ramplate_count > 0:
            ramplate_text = f'Ramplate: {self.ramplate_count} '
        if self.wheelhub_count > 0:
            wheelhub_text = f'Wheelhubs: {self.wheelhub_count} '
        if self.wheelguard_count > 0:
            wheelguard_text = f'Wheel guards: {self.wheelguard_count} '
        if self.bumper_spike_count > 0:
            bumper_spike_text = f'Bumper spikes: {self.bumper_spike_count} '
        line_text: str = f'{spoiler_airdam_text}{ramplate_text}'
        pdf.set_x(self.col_left_edge)
        if len(line_text) > 0: #There's something to print
            pdf.cell(h = self.row_height, text=line_text, ln=True, align='L')
        else:
            pdf.cell(h = self.row_height, text=" ", ln=1)
        line_text: str = f'{wheelhub_text}{wheelguard_text}{bumper_spike_text}'
        pdf.set_x(self.col_left_edge)
        if len(line_text) > 0:
            pdf.cell(h = self.row_height, text=line_text, ln=True, align='L')
        else:
            pdf.cell(h = self.row_height, text=" ", ln=1)

        # Weapons section of WalkAround
        local_weapon_list: list = []
        for weapon_index in range (1, self.weapon_rows_count + 1):
            type_index:   str = str(f'weapon_type_{weapon_index}')
            facing_index: str = str(f'weapon_{weapon_index}_facing')
            qty_index:    str = str(f'weapon_{weapon_index}_qty')
            type_entry:   str = input_dict.get(type_index, "").title()
            facing_entry: str = input_dict.get(facing_index, "")
            qty_entry:    str = input_dict.get(qty_index, "")
            if type_entry != 'Weapon':
                local_weapon_list.append((qty_entry, type_entry, facing_entry))
        if len(local_weapon_list) > 0: #some designs may have no vehicular weapons, and that's ok
            for local_entry in local_weapon_list:
                pdf.set_x(self.col_left_edge)
                line_text = f'{local_entry[0]} {local_entry[1]} {local_entry[2]}'
                pdf.cell(h = self.row_height, text=line_text, ln=True, align='L')
        
        for pe_index in range(1,11):
            name_index: str = str(f'pe_name_{pe_index}')
            qty_index: str  = str(f'pe_qty_{pe_index}')
            name_entry: str = input_dict.get(name_index, "")
            qty_entry: str  = input_dict.get(qty_index, "")
            if name_entry != "" and qty_entry != "" and qty_entry != 0:
                pdf.set_x(self.col_left_edge)
                line_text = f'{qty_entry} {name_entry}'
                pdf.cell(h = self.row_height, text=line_text, ln=True, align='L')

    def end_pdf(self, pdf: FPDF, output_name: str):
        """Given an FPDF object and an output name, finish the file and display it"""
        # Output the PDF to a file
        pdf.output(output_name)
        if os.path.exists(output_name):
            webbrowser.open(output_name)
        print("PDF generated successfully as fpdf_example.pdf")

    def scan_available_firing_actions(self, include_links=False) -> list:
        """Scans weapons, accessories, and boosters to find all valid link targets."""
        actions = ["None"]
    
        # 1. Scan the 10 Weapon rows
        for i in range(1, self.weapon_rows_count + 1):
            # Fallback tracking for common Tkinter naming variations in your file
            wpn_name_attr = f"selected_sub_weapon_{i}_canvas"
            if not hasattr(self, wpn_name_attr):
                wpn_name_attr = f"selected_sub_weapon_{i}"
            
            wpn_facing_attr = f"weapon_armor_facing_{i}"
            if not hasattr(self, wpn_facing_attr):
                wpn_facing_attr = f"selected_weapon_facing_{i}"
            
            # Dynamic lookup for your quantity entry or dropdown variable
            wpn_qty_attr = f"var_sub_weapon_{i}_qty" 
            if not hasattr(self, wpn_qty_attr):
                wpn_qty_attr = f"var_sub_weapon_{i}_qty" # alternate fallback

            if hasattr(self, wpn_name_attr) and getattr(self, wpn_name_attr):
                name = getattr(self, wpn_name_attr).get()

                # Fetch facing cleanly
                #self.weapon_armor_facing_1
                facing = "Facing"
                if hasattr(self, wpn_facing_attr) and getattr(self, wpn_facing_attr):
                    try:
                        facing = getattr(self, wpn_facing_attr).get()
                    except AttributeError: #This might be a string and not a TKinter value
                        facing = str(getattr(self, wpn_facing_attr, "Facing"))

                # Fetch quantity cleanly (default to 1 if not found or blank)
                qty = "1"
                #if hasattr(self, wpn_qty_attr) and getattr(self, wpn_qty_attr):
                #    qty_val = getattr(self, wpn_qty_attr).get()
                #    if qty_val and str(qty_val).strip() not in ["", "0"]:
                #        qty = str(qty_val).strip()
                # 1. Retrieve the variable object safely
                var_obj = getattr(self, wpn_qty_attr, None)
                qty_val = 0 # Default to zero if the object is missing or blank
    
                if var_obj is not None:
                    try:
                        # 2. Extract raw text first to watch for blank field resets
                        raw_text = var_obj.get()
                        if str(raw_text).strip() != "":
                            qty_val = int(raw_text)
                    except (ValueError, tk.TclError):
                        # 3. Prevent crashing if the field is empty or contains non-numeric symbols
                        qty_val = 0
                
                if name and name not in ["Weapon", "", "None", "Choose Weapon"]:
                    # UPDATED: Includes the quantity format marker in the string description
                    actions.append(f"Weapon {i}: {name} (Qty: {qty}) ({facing})")
                
        # 2. Scan the 30 Accessory slots
        linkable_accessories = [
            "Fire Extinguisher", "Improved Fire Extinguisher", 
            "HTM", "HDHTM", "Overdrive", "Nitrous Oxide"
        ]
        for i in range(1, 31):
            acc_attr = f"selected_accessories_{i}"
            if hasattr(self, acc_attr):
                acc_name = getattr(self, acc_attr).get()
                if acc_name in linkable_accessories:
                    actions.append(f"Accessory {i}: {acc_name}")
                
        # 3. Scan Rocket Boosters (up to 5)
        for i in range(1, 6):
            booster_lbs = f"var_rocket_booster_pounds_qty_{i}"
            booster_facing = f"selected_rocket_booster_facing_{i}"
            if hasattr(self, booster_lbs):
                lbs = getattr(self, booster_lbs).get()
                facing = getattr(self, booster_facing).get() if hasattr(self, booster_facing) else "Facing"
                if lbs and int(lbs) > 0:
                    actions.append(f"Rocket Booster {i} ({lbs} lbs - {facing})")

        # 4. NEW: Scan active Links (only available for Bumper Triggers)
        if include_links:
            for i in range(self.link_rows_count):
                if hasattr(self, 'link_selections') and self.link_selections[i]:
                    actions.append(f"Link #{i+1} (Active)")                    
                
        return actions

    def update_link_dropdowns(self, *args):
        """Refreshes options in all link dropdown menus based on current design status."""
        available_actions = self.scan_available_firing_actions()
    
        for i in range(self.link_rows_count):
            if self.link_dropdown_sources[i] and self.link_dropdown_targets[i]:
                # Clear old menu choices
                self.link_dropdown_sources[i]['menu'].delete(0, 'end')
                self.link_dropdown_targets[i]['menu'].delete(0, 'end')
            
                # Repopulate options
                for action in available_actions:
                    self.link_dropdown_sources[i]['menu'].add_command(
                        label=action, command=tk._setit(self.selected_link_source[i], action)
                    )
                    self.link_dropdown_targets[i]['menu'].add_command(
                        label=action, command=tk._setit(self.selected_link_target[i], action)
                    )

    def open_link_selector(self, event, row_index):
        """Opens a pop-up checklist window to select multiple actions for a link row."""
        # Get current available firing actions from your scanner
        available_actions = self.scan_available_firing_actions()
        if len(available_actions) <= 1:  # Only "None" is available
            return

        # Create top-level pop-up window
        popup = tk.Toplevel()
        popup.title(f"Configure Link #{row_index + 1}")
        popup.geometry(f"+{event.x_root}+{event.y_root}") # Open right under the mouse
        popup.grab_set() # Keep focus on this window until closed

        # Frame with scrollbar for long action lists
        frame = tk.Frame(popup)
        frame.pack(fill="both", expand=True, padx=10, pady=10)
    
        canvas = tk.Canvas(frame)
        scrollbar = tk.Scrollbar(frame, orient="vertical", command=canvas.yview)
        scroll_frame = tk.Frame(canvas)
    
        scroll_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        canvas.create_window((0, 0), window=scroll_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
    
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Dictionary to track checkbox variables
        chk_vars = {}
        current_selections = self.link_selections[row_index]

        def save_and_close():
            # Gather all checked items (ignoring "None")
            chosen = [act for act, var in chk_vars.items() if var.get() and act != "None"]
            self.link_selections[row_index] = chosen
        
            # Update UI text field
            if chosen:
                self.link_entry_vars[row_index].set(", ".join(chosen))
            else:
                self.link_entry_vars[row_index].set("No items linked")
            
            self.recalculate() # Trigger cost updates
            popup.destroy()

            # Populate checkboxes
        for action in available_actions:
            if action == "None":
                continue
            var = tk.BooleanVar(value=(action in current_selections))
            chk_vars[action] = var
            cb = tk.Checkbutton(scroll_frame, text=action, variable=var, anchor="w")
            cb.pack(fill="x", anchor="w", pady=2)

        # Save button
        btn_save = tk.Button(popup, text="Apply Link", command=save_and_close, bg="lightgreen")
        btn_save.pack(fill="x", padx=10, pady=(0, 10))

    def open_bt_selector(self, event, row_index):
        """Opens a pop-up checklist window to select multiple actions for a Bumper Trigger row."""
        # Notice the True parameter passed to include active links in the selection checklist
        available_actions = self.scan_available_firing_actions(include_links=True)
        if len(available_actions) <= 1: 
            return

        popup = tk.Toplevel()
        popup.title(f"Configure Bumper Trigger #{row_index + 1}")
        popup.geometry(f"+{event.x_root}+{event.y_root}")
        popup.grab_set()

        frame = tk.Frame(popup)
        frame.pack(fill="both", expand=True, padx=10, pady=10)
    
        canvas = tk.Canvas(frame)
        scrollbar = tk.Scrollbar(frame, orient="vertical", command=canvas.yview)
        scroll_frame = tk.Frame(canvas)
    
        scroll_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=scroll_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        chk_vars = {}
        current_selections = self.bt_selections[row_index]

        def save_and_close():
            chosen = [act for act, var in chk_vars.items() if var.get() and act != "None"]
            self.bt_selections[row_index] = chosen
        
            if chosen:
                self.bt_entry_vars[row_index].set(", ".join(chosen))
            else:
                self.bt_entry_vars[row_index].set("No items linked")
            
            self.recalculate()
            popup.destroy()

        for action in available_actions:
            if action == "None": continue
            var = tk.BooleanVar(value=(action in current_selections))
            chk_vars[action] = var
            cb = tk.Checkbutton(scroll_frame, text=action, variable=var, anchor="w")
            cb.pack(fill="x", anchor="w", pady=2)

        btn_save = tk.Button(popup, text="Apply Bumper Trigger", command=save_and_close, bg="lightgreen")
        btn_save.pack(fill="x", padx=10, pady=(0, 10))

    def _on_mouse_wheel_unified(self, event):
        """
        A single, cross-platform callback that processes mouse wheel movements
        and scrolls the master canvas vertically.
        """
        # 1. Windows and macOS pass the scroll distance via event.delta
        if event.delta:
            # Shift the canvas view based on rotation direction
            self.my_canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
            
        # 2. Linux passes scroll inputs via discrete event buttons (Button 4/5)
        else:
            if event.num == 4: # Scroll Up
                self.my_canvas.yview_scroll(-1, "units")
            elif event.num == 5: # Scroll Down
                self.my_canvas.yview_scroll(1, "units")

    def add_new_weapon_row_tactical(self):
        # 1. FORCE THE INTERNAL WEAPON FRAME TO INNER-LOCK COLUMNS 
        column_track_vars = [
            self.grid_col_item, self.grid_col_qty, self.grid_left_up_button,
            self.grid_left_down_button, self.grid_col_weapon_ammo_entry,
            self.grid_col_extra_mag_entry, self.grid_col_dp, self.grid_col_power_factors,
            self.grid_col_base_mpg, self.grid_col_cost, self.grid_col_weight,
            self.grid_col_spaces, self.grid_col_last_column
        ]
        for c_idx in column_track_vars:
            global_width = self.second_frame.columnconfigure(c_idx, "minsize")
            self.weapon_container_frame.columnconfigure(c_idx, minsize=global_width)

        # 2. TEMPLATE HEADERS GENERATION (RUNS ONLY ON ENTRY 1 AT THE TOP)
        if self.weapon_rows_count == 0:
            headers_matrix = [
                ("Weapon",      self.grid_col_item),
                ("Qty",         self.grid_col_qty),
                ("Ammo Qty",    self.grid_col_weapon_ammo_entry),
                ("Extra Mags",  self.grid_col_extra_mag_entry),
                ("Cost",        self.grid_col_cost),
                ("Weight",      self.grid_col_weight),
                ("Spaces",      self.grid_col_spaces),
                ("Facing",      self.grid_col_dp),
                ("To Hit",      self.grid_col_power_factors),
                ("Damage",      self.grid_col_base_mpg),
                ("DP",          self.grid_col_test_track), 
            ]
            for text, col_idx in headers_matrix:
                lbl = tk.Label(self.weapon_container_frame, text=text, anchor="w")
                lbl.grid(row=1, column=col_idx, sticky="w")

        # Update counter tracking loops
        self.weapon_rows_count += 1
        idx = self.weapon_rows_count

        # Each cluster spans exactly 2 structured row levels
        row_top = 2 + ((idx - 1) * 2)
        row_bottom = row_top + 1

        # 3. ROW A (TOP LAYER): CATEGORY DROPDOWN 
        cat_var = tk.StringVar(value="Weapon")
        self.weapon_dropdown_string_vars.append(cat_var)
        
        categories = self.get_weapon_options_alt()
        cat_drop = ttk.OptionMenu(self.weapon_container_frame, cat_var, "Weapon", *categories)
        cat_drop.grid(row=row_top, column=self.grid_col_item, sticky="w")
        self.weapon_dropdown_objects.append(cat_drop)

        cat_var.trace_add(
            "write", 
            lambda *args, cv=cat_var, r=idx: self.on_weapon_category_changed(
                selected_category=cv.get(), 
                row_number=r, 
                cluster_frame=self.weapon_container_frame
            )
        )

        # 4. ROW B (BOTTOM LAYER): WEAPON QTY TRACK + CALCULATION TRACE
        qty_var = tk.StringVar(value="0")
        self.weapon_qty_string_vars.append(qty_var)
        qty_var.trace_add("write", lambda *args, r=idx: self.on_select_sub_weapon_unified(row_number=idx))

        qty_ent = ttk.Entry(self.weapon_container_frame, textvariable=qty_var, width=3, justify="center")
        qty_ent.grid(row=row_bottom, column=self.grid_col_qty, sticky="w")
        self.weapon_qty_entry_objects.append(qty_ent)

        btn_up = tk.Button(self.weapon_container_frame, text="\u2191", command=lambda r=idx: self.on_button_sub_weapon_qty_unified(idx, direction="up"))
        btn_up.grid(row=row_bottom, column=self.grid_left_up_button, sticky="nsew")
        self.weapon_qty_up_button_objects.append(btn_up)
        
        btn_dn = tk.Button(self.weapon_container_frame, text="\u2193", command=lambda r=idx: self.on_button_sub_weapon_qty_unified(idx, direction="down"))
        btn_dn.grid(row=row_bottom, column=self.grid_left_down_button, sticky="nsew")
        self.weapon_qty_down_button_objects.append(btn_dn)

        # 5. AMMO QTY TRACK + SPIN BUTTONS + CALCULATION TRACE
        ammo_var = tk.StringVar(value="0")
        self.weapon_ammo_qty_string_vars.append(ammo_var)
        ammo_var.trace_add("write", lambda *args, r=idx: self.on_select_sub_weapon_unified(row_number=idx))
        
        ammo_ent = tk.Entry(self.weapon_container_frame, textvariable=ammo_var, width=3, justify="center")
        ammo_ent.grid(row=row_bottom, column=self.grid_col_weapon_ammo_entry, sticky="w")
        self.weapon_ammo_qty_entry_objects.append(ammo_ent)

        ammo_btn_up = tk.Button(self.weapon_container_frame, text="\u2191", command=lambda r=idx: self.on_button_ammo_qty_unified(idx, direction="up"))
        ammo_btn_up.grid(row=row_bottom, column=self.grid_col_weapon_ammo_qty_up, sticky="nsew")
        self.weapon_ammo_qty_up_button_objects.append(ammo_btn_up)

        ammo_btn_dn = tk.Button(self.weapon_container_frame, text="\u2193", command=lambda r=idx: self.on_button_ammo_qty_unified(idx, direction="down"))
        ammo_btn_dn.grid(row=row_bottom, column=self.grid_col_weapon_ammo_qty_down, sticky="nsew")
        self.weapon_ammo_qty_down_button_objects.append(ammo_btn_dn)

        # 6. EXTRA MAGS QTY TRACK + SPIN BUTTONS + CALCULATION TRACE
        mag_var = tk.StringVar(value="0")
        self.weapon_extra_mag_qty_string_vars.append(mag_var)
        mag_var.trace_add("write", self.on_update_extra_mags_qty_unified(row_number=idx))
        
        mag_ent = tk.Entry(self.weapon_container_frame, textvariable=mag_var, width=3, justify="center")
        mag_ent.grid(row=row_bottom, column=self.grid_col_extra_mag_entry, sticky="w")
        self.weapon_extra_mag_qty_entry_objects.append(mag_ent)

        mag_btn_up = tk.Button(self.weapon_container_frame, text="\u2191", command=lambda r=idx: self.on_button_extra_mags_unified(idx, direction="up"))
        mag_btn_up.grid(row=row_bottom, column=self.grid_col_extra_mag_qty_up, sticky="nsew")
        self.weapon_extra_mag_qty_up_button_objects.append(mag_btn_up)

        mag_btn_dn = tk.Button(self.weapon_container_frame, text="\u2193", command=lambda r=idx: self.on_button_extra_mags_unified(idx, direction="down"))
        mag_btn_dn.grid(row=row_bottom, column=self.grid_col_extra_mag_qty_down, sticky="nsew")
        self.weapon_extra_mag_qty_down_button_objects.append(mag_btn_dn)

        # 7. STATISTICS FIELDS SHIFTED BACK INTO THEIR CONSTANT TRACK MARKS
        lbl_cost = tk.Label(self.weapon_container_frame, text="0", width=8, anchor="w")
        lbl_cost.grid(row=row_bottom, column=self.grid_col_cost, sticky="w")
        self.weapon_cost_label_objects.append(lbl_cost)

        lbl_weight = tk.Label(self.weapon_container_frame, text="0", width=8, anchor="w")
        lbl_weight.grid(row=row_bottom, column=self.grid_col_weight, sticky="w")
        self.weapon_weight_label_objects.append(lbl_weight)

        lbl_spaces = tk.Label(self.weapon_container_frame, text="0", width=8, anchor="w")
        lbl_spaces.grid(row=row_bottom, column=self.grid_col_spaces, sticky="w")
        self.weapon_spaces_label_objects.append(lbl_spaces)

        # 8. FACING CONTROLLER 
        facing_var, facing_drop = self.add_weapon_facing_dropdown(canvas_type=self.weapon_container_frame, column_val=self.grid_col_dp, row_val=row_bottom)
        self.weapon_mount_dropdown_string_vars.append(facing_var)
        self.weapon_mount_dropdown_objects.append(facing_drop)

        # 9. DYNAMIC STATISTICS LABELS
        lbl_tohit = tk.Label(self.weapon_container_frame, text="-", width=6, anchor="w")
        lbl_tohit.grid(row=row_bottom, column=self.grid_col_power_factors, sticky="w")
        self.weapon_to_hit_label_objects.append(lbl_tohit)
        
        lbl_dmg = tk.Label(self.weapon_container_frame, text="-", width=6, anchor="w")
        lbl_dmg.grid(row=row_bottom, column=self.grid_col_base_mpg, sticky="w")
        self.weapon_damage_label_objects.append(lbl_dmg)

        lbl_dp = tk.Label(self.weapon_container_frame, text="0", width=8, anchor="w")
        lbl_dp.grid(row=row_bottom, column=self.grid_col_test_track, sticky="w")
        self.weapon_dp_label_objects.append(lbl_dp)

        # Force update scroll region dimensions
        self.root.update_idletasks()
        self.my_canvas.configure(scrollregion=self.my_canvas.bbox("all"))

    def add_new_accessory_row(self):
        """Appends active accessory inputs directly to the matching frame partition row"""

        self.accessory_rows_count += 1
        row_idx = self.accessory_rows_count

        # 1. Structural Identifiers (Dynamic Scannable Labels)
        lbl = tk.Label(self.accessory_container_frame, text=f"Accessory Row {row_idx}:", anchor="w")
        lbl.grid(row=row_idx, column=0, sticky="w", padx=5, pady=2)

        # 2. Map directly into your application's preconfigured variables matrix

        #self.accessory_dropdown_string_vars = []
        #self.accessory_qty_string_vars = []

        qty_var = tk.StringVar(value="0")
        self.accessory_qty_string_vars.append(qty_var)
        qty_var.trace_add("write", lambda *args, r=row_idx: self.on_select_accessory_unified(row_number=row_idx))

        name_var = tk.StringVar(value="Weapon")
        self.accessory_dropdown_string_vars.append(name_var)

        # 3. Dynamic Interactive Control Field Rendering
        # Selectable Accessory Dropdown Box
        cb_accessory = ttk.OptionMenu(self.accessory_container_frame, textvariable=name_var, values=self.accessories_list, width=25)
        cb_accessory.grid(row=row_idx, column=self.grid_col_item)

        # Quantity Entry Selector Field
        ent_qty = ttk.Entry(self.accessory_container_frame, textvariable=qty_var, width=5)
        ent_qty.grid(row=row_idx, column=self.grid_col_qty)
        self.accessory_qty_string_vars.append(ent_qty)

        btn_up = tk.Button(self.accessory_container_frame, text="\u2191", command=lambda r=row_idx: self.on_select_accessory_unified(row_idx, direction="up"))
        btn_up.grid(row=row_idx, column=self.grid_left_up_button, sticky="nsew")
        self.accessory_qty_up_button_objects.append(btn_up)
        
        btn_dn = tk.Button(self.accessory_container_frame, text="\u2193", command=lambda r=row_idx: self.on_select_accessory_unified(row_idx, direction="down"))
        btn_dn.grid(row=row_idx, column=self.grid_left_down_button, sticky="nsew")
        self.accessory_qty_down_button_objects.append(btn_dn)

        # 4. Instant Screen Geometry Sync Pass
        self.root.update_idletasks()
        self.my_canvas.configure(scrollregion=self.my_canvas.bbox("all"))

    def on_accessory_changed(self, event, row_idx):
        """Uses the untouched self.accessories_list master array to change selection
        focus without altering list positions, slicing, or filtering values.
        """
        selected_category = event.widget.get()
    
        # Isolate your row tracking components from your object matrix
        target_item_dropdown = self.ca_dropdown_objects[row_idx - 1]
        target_item_variable = self.ca_dropdown_string_vars[row_idx - 1]

        # Ensure the dropdown contains the complete, unaltered master list
        target_item_dropdown['values'] = self.accessories_list

        # Jump focus directly to the first item matching the category keyword
        if selected_category != "All Items":
            for index, item in enumerate(self.accessories_list):
                if selected_category.lower() in item.lower():
                    # Set the text and highlight the item inside the open list
                    target_item_variable.set(item)
                    target_item_dropdown.current(index)
                    return
                
        # Fallback default if "All Items" is chosen or no keyword matches
        target_item_variable.set("Accessory")

    def on_button_accessory_qty_unified(self, row_number: int, direction: str):
        """
        Handles up/down arrow button clicks for weapon quantities across all rows.
        """
        var_name = self.accessory_qty_string_vars[row_number-1]
            
        try:
            var_value_str = var_name.get()
            current_val = int(var_value_str)
        except (ValueError, tk.TclError):
            current_val = 0

        new_val = current_val + 1 if direction == "up" else max(0, current_val - 1)
        var_name.set(str(new_val))
        if hasattr(self, "on_select_accessory_unified"): 
            self.on_select_accessory_unified(row_number=row_number)        

    def on_select_accessory_unified(self, row_number: int, *args):
        """
        Runs automatically whenever an accessory is picked.
        Calculates cost, weight, and spaces for this row and updates the screen labels.
        """
        if getattr(self, 'is_loading', False):
            return

        # 1. Safely retrieve the selected sub-weapon name string
        # We look it up from the array we built earlier
        if row_number <= len(self.acessory_dropdown_string_vars):
            selected_accessory = self.acessory_dropdown_string_vars[row_number - 1].get()
        else:
            return

        # Get the category type to obtain the sub weapon data dictionary, from there once we know the selected weapon, get the weapon stats
        try: category_name = self.accessory_dropdown_string_vars[row_number -1].get() 
        except (IndexError, ValueError, tk.TclError): return #This is a systemic failure

        # 2. Grab current quantities from the tracking string variables
        try: qty = int(self._qty_string_vars[row_number - 1].get())
        except (IndexError, ValueError, tk.TclError): qty = 0
    
        try: ammo_qty = int(self.weapon_ammo_qty_string_vars[row_number - 1].get())
        except (IndexError, ValueError, tk.TclError): ammo_qty = 0
    
        try: extra_mags = int(self.weapon_extra_mag_qty_string_vars[row_number - 1].get())
        except (IndexError, ValueError, tk.TclError): extra_mags = 0
    
        # 3. FETCH WEAPON BASE STATS FROM YOUR DATABASE
        # (Replace 'self.get_weapon_base_stats' with your actual dictionary/database lookup function)

        accessory_stats = next((entry for entry in self.accessory_list if entry["Drop-Down Name"] == selected_accessory), None)

        #self.accessories_list = []
        #entry_dict: dict = {
        # "Accessory Name": "Accessory",
        # "Cost": "0",
        # "Space": "0",
        # "Weight": "0",
        # "DP": "",
        # "Notes": "",
        # "Turret Size": -2,
        # "Cycle Only": 0}

        if not accessory_stats:
            # Fallback to zero if the item name isn't found
            accessory_stats = {"base_cost": 0, "base_weight": 0, "base_space": 0.0, "ammo_cost_per": 0, "ammo_weight_per": 0}
    
        # 4. MATH ENGINE CALCULATIONS
        total_cost   = int(c_res) if (c_res := float(accessory_stats["Cost"])   * qty).is_integer() else round(c_res, 2)
        total_weight = int(w_res) if (w_res := float(accessory_stats["Weight"]) * qty).is_integer() else round(w_res, 2)
        total_space  = int(s_res) if (s_res := float(accessory_stats["Space"])  * qty).is_integer() else round(s_res, 2)

        dp_str = accessory_stats["DP"]
        notes_str = accessory_stats["Notes"]
    
        # 5. REWRITE THE ROW LABELS ON SCREEN (Breaking the $0 loop!)
        if row_number <= len(self.accessory_cost_label_objects):
            cost_lbl = self.accessory_cost_label_objects[row_number - 1]
            cost_lbl.config(text=f"{total_cost}")

        if row_number <= len(self.accessory_weight_label_objects):
            weight_lbl = self.accessory_weight_label_objects[row_number - 1]
            weight_lbl.config(text=f"{total_weight}")

        if row_number <= len(self.accessory_spaces_label_objects):
            space_lbl = self.accessory_spaces_label_objects[row_number - 1]
            space_lbl.config(text=f"{total_space}")

        if row_number <= len(self.accessory_dp_label_objects):
            dp_lbl = self.accessory_dp_label_objects[row_number - 1]
            dp_lbl.config(text=f"{dp_str}")

        if row_number <= len(self.accessory_to_hit_label_objects):
            to_hit_lbl = self.accessory_to_hit_label_objects[row_number - 1]
            to_hit_lbl.config(text=f"{to_hit_str}")

        if row_number <= len(self.accessory_damage_label_objects):
            dam_lbl = self.accessory_damage_label_objects[row_number - 1]
            dam_lbl.config(text=f"{damage_str}")

        # 6. TRIGGER THE GLOBAL RECALCULATE ENGINE FOR VEHICLE TOTALS
        if hasattr(self, 'recalculate'):
            self.recalculate()

if __name__ == '__main__':
    print("Launching Python_Designer")
    local_designer: Python_Designer = Python_Designer()
    local_designer.launch_it()
    print('Leaving Python_Designer')
