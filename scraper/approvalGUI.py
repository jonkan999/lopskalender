import tkinter as tk
from tkinter import ttk, messagebox
from scraper_package.race_classes import Race, RaceCollection

#GLOBAL CONFIG VARIABLES
STAGED_FOR_APPROVAL_FILE_PATH = 'staged_for_approval.json'
CURRENT_ACTIVE_FILE_PATH = 'current_active_races.json'
APPROVED_RACES_FILE_PATH = 'approved_races_raw.json'


class RaceGUI(tk.Tk):
    def __init__(self, races_for_approval, current_races):
        super().__init__()

        self.race_collection = current_races
        self.approval_collection = races_for_approval
        self.race_for_approval = None
        self.relevant_races = None
        self.selected_id = None

        # Initialize GUI components
        self.create_widgets()

        #load first race into gui
        self.load_next_race_for_approval()

    def load_next_race_for_approval(self):
        # Clear previous text in the GUI
        self.race_text.delete(1.0, tk.END)
        self.race_summary_listbox.delete(0, tk.END)
        # Load the next race for approval from the source file
        if len(self.approval_collection.races) > 0:
            self.race_for_approval = self.approval_collection.pop_race()
            self.load_races_into_gui()
        else:
            # No more races in staging
            self.race_for_approval = None
            self.race_text.delete(1.0, tk.END)  # Clear the race_text
            self.race_summary_listbox.delete(0, tk.END)  # Clear the race_summary_listbox
            tk.messagebox.showinfo("No More Races", "No more races in staging.")
    
    def create_widgets(self):
        # Left Frame for displaying and editing individual race information
        left_frame = ttk.Frame(self)
        left_frame.grid(row=0, column=0, padx=10, pady=10, sticky='ns')

        self.race_text = tk.Text(left_frame, wrap='word', height=40, width=40)
        self.race_text.pack(fill='both', expand=True)

        # Right Frame for displaying the summary of races
        right_frame = ttk.Frame(self)
        right_frame.grid(row=0, column=1, padx=10, pady=10, sticky='ns')

        self.race_summary_listbox = tk.Listbox(right_frame, selectmode=tk.SINGLE, height=40, width=80)
        self.race_summary_listbox.pack(fill='both', expand=True)

        # Discard button to the left with light red highlight
        discard_button = tk.Button(self, text="Discard", command=self.discard_current_race, bg="#FFCDD2", padx=10)
        discard_button.grid(row=1, column=0, pady=5, padx=5)

        # Approve button a bit to the right with light green highlight
        approve_button = tk.Button(self, text="Approve", command=self.approve_current_race, bg="#C8E6C9", padx=10)
        approve_button.grid(row=1, column=1, pady=5, padx=5)

        # Replace button to the right of the approve with light blue highlight
        replace_button = tk.Button(self, text="Replace Race", command=self.replace_current_race, bg="#BBDEFB", padx=10)
        replace_button.grid(row=1, column=2, pady=5, padx=5)

        # Adjust the width of the right frame and expand the window size
        self.geometry("1000x700")  # Update the size accordingly



    def load_races_into_gui(self):
        # Display detailed information of the staged race on the left
        race_details = [
            f"Date: {self.race_for_approval['date']}",
            f"\nType: {self.race_for_approval['type']}",
            f"\nName: {self.race_for_approval['name']}",
            f"\nDistance (m): {self.race_for_approval['distance_m']}",
            f"\nPlace: {self.race_for_approval['place']}",
            f"\nOrganizer: {self.race_for_approval['organizer']}",
            f"\nWebsite: {self.race_for_approval['website']}",
            f"\nCounty: {self.race_for_approval['county']}",
            f"\nRace Categories: {self.race_for_approval['race_categories']}",
            f"\nSUMMARY: {self.race_for_approval['summary']}",
            f"\nLONG SUMMARY: {self.race_for_approval['long_summary']}",
        ]
        self.race_text.insert(tk.END, "\n".join(race_details))

        # Display the relevant information of races in current_active_races.json on the right
        self.display_related_races_summary(self.race_for_approval['date'])

    def display_related_races_summary(self, selected_race_date):
        # Get races from current_active_races.json that match the selected race's date
        print(f"filtering races for {selected_race_date}")
        self.relevant_races = self.race_collection.filter_races('date', selected_race_date)

        # Display the relevant information (name, place, distance_m, and summary) on the right
        self.race_summary_listbox.delete(0, tk.END)  # Clear previous content

        for index, race in enumerate(self.relevant_races):
            info_line = f"{race['name']} - {race['place']} - {race['distance_m']}m - id:{race['id']}"
            summary_line = f"    Summary: {race['summary']}"
            # Insert the info line with a unique identifier
            self.race_summary_listbox.insert(tk.END, info_line)
            # Insert the summary line with a unique identifier
            self.race_summary_listbox.insert(tk.END, summary_line)
        # Bind selection event to a function
        self.race_summary_listbox.bind("<<ListboxSelect>>", self.selected_id_changed)
    
    def selected_id_changed(self, event):
        # Get the selected index
        selected_index = self.race_summary_listbox.curselection()

        # Check if an item is selected
        if selected_index:
            # Get the selected race using the index
            selected_race_index = selected_index[0] // 2  # Divide by 2 to get the index of the info line
            selected_race = self.relevant_races[selected_race_index]

            # Set the selected_id to the 'id' of the selected race
            self.selected_id = selected_race.get('id', None)
            print(f"Selected Race ID: {self.selected_id}")
        

    def approve_current_race(self):
        if self.race_for_approval:
            # Display a confirmation dialog
            response = tk.messagebox.askyesno("Confirmation", f"Are you sure you want to approve race {self.race_for_approval['name']}?")

            if response:
                # Additional logic for approval
                print(f"Approving race: {self.race_for_approval['name']}")
                # Create a new collection with the approved race and store it in approved_races_raw.json
                store_collection = RaceCollection()
                store_collection.races.append(self.race_for_approval)
                store_collection.append_or_create_json(APPROVED_RACES_FILE_PATH)

                # Update the race details
                self.race_for_approval.update_updated_date()
                self.race_for_approval.set_is_approved(True, True)

                # Remove the race from the staged_for_approval.json file
                self.race_for_approval.remove_from_file(STAGED_FOR_APPROVAL_FILE_PATH)
                
                self.load_next_race_for_approval()
            else:
                print("Approval canceled.")

    def discard_current_race(self):
        if self.race_for_approval:
            # Display a confirmation dialog
            response = tk.messagebox.askyesno("Confirmation", f"Are you sure you want to discard race {self.race_for_approval['name']}?")

            if response:
                # Additional logic for discarding
                print(f"Discarding race: {self.race_for_approval['name']}")
                print(self.race_for_approval)

                # Update the race details
                self.race_for_approval.update_updated_date()
                self.race_for_approval.set_is_discarded(True, True)

                # Remove the race from the staged_for_approval.json file
                self.race_for_approval.remove_from_file(STAGED_FOR_APPROVAL_FILE_PATH)

                self.load_next_race_for_approval()
            else:
                print("Discard canceled.")

    def replace_current_race(self):
      if self.race_for_approval:
        
        # Load races from current_active_races.json
        current_collection = RaceCollection()
        current_collection.load_from_json(CURRENT_ACTIVE_FILE_PATH)

        # Find the index of the race to be replaced
        index_to_remove = None
        for i, race in enumerate(current_collection.races):
            if race['id'] == self.selected_id:
                index_to_remove = i
                break

        # Remove the race to be replaced from current_active_races.json
        if index_to_remove is not None:
            removed_race = current_collection.races.pop(index_to_remove)
            print(f"Removed race from current_active_races.json: {removed_race['name']}")

            # Load races from approved_races_raw.json
            approved_collection = RaceCollection()
            approved_collection.load_from_json(APPROVED_RACES_FILE_PATH)

            index_to_replace = None
            for i, race in enumerate(approved_collection.races):
                if race['id'] == self.selected_id:
                  index_to_replace = i
                  break
            if index_to_replace is not None:
                replaced_race = approved_collection.races.pop(index_to_replace)
                print(f"Replaced race from approved_races_raw.json: {replaced_race['name']}")
            # Add the new race to approved_races_raw.json
            approved_collection.races.append(self.race_for_approval)

            # Display a confirmation dialog
            response = tk.messagebox.askyesno(
                "Confirmation",
                f"Do you want to replace the {removed_race['name']} with {self.race_for_approval['name']} in approved_races_raw.json?"
            )
            if response:
                # Additional logic for replacing
                print(f"Replacing race: {self.race_for_approval['name']}")
                print(self.race_for_approval)

                # Save the updated current_active_races.json
                current_collection.save_to_json(CURRENT_ACTIVE_FILE_PATH)

                # Update the race details
                self.race_for_approval.update_updated_date()
                self.race_for_approval.set_is_approved(True, True)


                # Save the updated approved_races_raw.json
                approved_collection.save_to_json(APPROVED_RACES_FILE_PATH)

                # Remove the race from staged_for_approval.json
                self.race_for_approval.remove_from_file(STAGED_FOR_APPROVAL_FILE_PATH)

                # Update the source JSON file
                self.race_for_approval.update_source_json('is_approved', True)

                self.load_next_race_for_approval()
            else:
                print("Replacement canceled.")
        else:
            print(f"Race with ID {self.selected_id} not found in current_active_races.json.")


# Example usage
if __name__ == "__main__":
    # Assuming race_collection is an instance of RaceCollection loaded from staged_for_approval
    races_for_approval = RaceCollection()
    races_for_approval.load_from_json(STAGED_FOR_APPROVAL_FILE_PATH)
    
    #race_for_approval = race_collection.pop_race()
    #print(race_for_approval.data)

    current_races = RaceCollection()
    current_races.load_from_json(CURRENT_ACTIVE_FILE_PATH)
    
    app = RaceGUI(races_for_approval, current_races)
    app.title("Race Approval GUI")
    app.mainloop()
