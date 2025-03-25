import os
import sys

from PySide6.QtCore import Qt
from PySide6.QtGui import QFont, QIcon, QFontDatabase
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QCheckBox, QLabel, QLineEdit,
    QMessageBox, QWidget, QVBoxLayout, QInputDialog
)

from ui.my_form import Ui_MainWindow  # Import your UI file


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        # Align to top
        self.in_progress_v_layout.setAlignment(Qt.AlignTop)
        self.completed_v_layout.setAlignment(Qt.AlignTop)

        # Create widgets for the scroll area content.
        self.in_progress_scroll_content_widget = QWidget()
        self.in_progress_scroll_content_layout = QVBoxLayout(self.in_progress_scroll_content_widget)
        self.in_progress_scroll.setWidget(self.in_progress_scroll_content_widget)
        self.in_progress_scroll_content_layout.setAlignment(Qt.AlignTop)

        self.completed_scroll_content_widget = QWidget()
        self.completed_scroll_content_layout = QVBoxLayout(self.completed_scroll_content_widget)
        self.completed_scroll.setWidget(self.completed_scroll_content_widget)
        self.completed_scroll_content_layout.setAlignment(Qt.AlignTop)

        # --- MAKE CONTENT WIDGETS TRANSPARENT ---

        # Make content widgets transparent
        self.in_progress_scroll_content_widget.setStyleSheet("background-color: transparent;")
        self.completed_scroll_content_widget.setStyleSheet("background-color: transparent;")

        # Set search icon
        search_icon = QIcon(":icons/images/search_icon.png")  # Make sure path is correct
        self.search_box.addAction(search_icon, QLineEdit.LeadingPosition)

        # Add a placeholder text
        self.search_box.setPlaceholderText("Search")

        self.add_catagory_button.clicked.connect(self.add_category)
        self.remove_catagory_button.clicked.connect(self.remove_category)

        # --- Category-Item Mapping ---
        self.category_items = {}  # Initialize the dictionary

        # --- Connect currentTextChanged for synchronized filtering ---
        self.progress_catagory.currentTextChanged.connect(self.sync_category_selection)
        self.completed_catagory.currentTextChanged.connect(self.sync_category_selection)

        self.add_button.clicked.connect(self.add_item)
        self.remove_button_2.clicked.connect(self.remove_checked_from_progress)  # Corrected connection
        self.complete_button.clicked.connect(self.move_checked_items)
        self.remove_button.clicked.connect(self.remove_item)  # For "Completed" list
        self.search_button.clicked.connect(self.search_labels)

        self.load_data()
        self.load_fonts()

        # Initial filtering (important!)
        self.filter_by_category(self.progress_catagory.currentText())

    def load_fonts(self):
        font_dir = "fonts"
        if os.path.isdir(font_dir):
            for filename in os.listdir(font_dir):
                if filename.endswith((".ttf", ".otf")):
                    font_path = os.path.join(font_dir, filename)
                    QFontDatabase.addApplicationFont(font_path)

    def get_data_path(self):
        app_name = "ChecklistApp"
        local_app_data = os.path.join(os.getenv('LOCALAPPDATA'), app_name)
        if not os.path.exists(local_app_data):
            os.makedirs(local_app_data)
        return os.path.join(local_app_data, "checklist_data.txt")

        # Corrected add_item() method

    def add_item(self):
        item_text = self.lineEdit.text().strip()
        selected_category = self.progress_catagory.currentText()

        if item_text:  # This is the crucial check
            full_item_text = f"{item_text} [{selected_category}]"
            display_text = item_text

            # Add to category_items *first*
            if selected_category not in self.category_items:
                self.category_items[selected_category] = []
            self.category_items[selected_category].append(full_item_text)

            # Call a helper function to create the checkbox:
            self.create_todo_checkbox(display_text, full_item_text, False)

            self.lineEdit.clear()
            self.filter_by_category(self.progress_catagory.currentText())  # Filter after adding

        else:  # This block is executed ONLY if item_text is empty
            QMessageBox.warning(self, "Warning", "Please enter text in the text field.")

    def remove_checked_from_progress(self):
        """Removes *checked* checkboxes from the 'In Progress' list."""
        checked_items = []
        for i in range(self.in_progress_scroll_content_layout.count()):
            item = self.in_progress_scroll_content_layout.itemAt(i).widget()
            if isinstance(item, QCheckBox) and item.isChecked():  # Check if CHECKED
                checked_items.append(item)

        for checkbox in checked_items:
            display_text = checkbox.text()
            original_full_text = self.find_full_text(display_text, self.progress_catagory.currentText())

            if original_full_text:
                item_category = original_full_text.split(" [")[1].replace("]",
                                                                          "") if " [" in original_full_text else "Uncategorized"
            else:
                item_category = "Uncategorized"  # Fallback

            if item_category in self.category_items:
                if original_full_text in self.category_items[item_category]:
                    self.category_items[item_category].remove(original_full_text)

            self.in_progress_scroll_content_layout.removeWidget(checkbox)
            checkbox.deleteLater()

        self.filter_by_category(self.progress_catagory.currentText())

    def create_todo_checkbox(self, display_text, full_item_text, checked):
        """Helper function to create and add a to-do checkbox."""
        checkbox = QCheckBox(display_text)
        checkbox.setChecked(checked)
        font = QFont()
        font.setPointSize(11)
        checkbox.setFont(font)
        self.in_progress_scroll_content_layout.addWidget(checkbox)

    def create_completed_label(self, display_text):
        """Helper function to create and add a completed label."""
        label = QLabel(display_text)
        font = QFont()
        font.setPointSize(11)
        label.setFont(font)
        label.setFrameStyle(QLabel.StyledPanel | QLabel.Sunken)
        label.setMargin(5)
        label.setWordWrap(True)
        label.setCursor(Qt.PointingHandCursor)
        label.mousePressEvent = lambda event, lb=label: self.label_selected(event, lb)
        self.completed_scroll_content_layout.addWidget(label)

    def edit_item_text(self, event, item):
        original_text = item.text()
        parts = original_text.split(" [")
        if len(parts) != 2:
            return

        task_text = parts[0]
        category_part = " [" + parts[1]

        line_edit = QLineEdit(task_text)
        line_edit.setGeometry(item.geometry())
        item.parent().layout().addWidget(line_edit)
        line_edit.setFocus()
        line_edit.returnPressed.connect(lambda: self.update_item_text(line_edit, item, category_part))
        line_edit.editingFinished.connect(lambda: self.update_item_text(line_edit, item, category_part))

    def update_item_text(self, line_edit, item, category_part):
        new_task_text = line_edit.text().strip()
        if not new_task_text:
            line_edit.deleteLater()
            return

        new_full_text = new_task_text + category_part

        # --- CORRECTED Update in category_items ---
        old_full_text = item.text()  # This is the *displayed* text before edit.  It's WRONG for category lookup!
        old_category = self.progress_catagory.currentText()  # Get the *current* selected category.  This is the CORRECT category
        new_category = category_part.strip(" []")

        # Find the *actual* old full text using find_full_text.  This is essential.
        old_full_text_correct = self.find_full_text(old_full_text.split(" [")[0], old_category)

        if old_full_text_correct:  # Only proceed if found
            if old_category in self.category_items and old_full_text_correct in self.category_items[old_category]:
                self.category_items[old_category].remove(old_full_text_correct)
                if new_category not in self.category_items:
                    self.category_items[new_category] = []
                self.category_items[new_category].append(new_full_text)

        item.setText(new_full_text)
        line_edit.deleteLater()
        # --- Apply Filter ---
        self.filter_by_category(self.progress_catagory.currentText())

    def move_checked_items(self):
        checked_items = []
        for i in range(self.in_progress_scroll_content_layout.count()):
            item = self.in_progress_scroll_content_layout.itemAt(i).widget()
            if isinstance(item, QCheckBox) and item.isChecked():
                checked_items.append(item)

        for checkbox in checked_items:

            # --- CORRECTLY Get full text and extract display text AND original Category---
            display_text = checkbox.text()
            # Find the original full text using find_full_text
            original_full_text = self.find_full_text(display_text, self.progress_catagory.currentText())
            # Get the category
            if original_full_text:  # Check if found
                item_category = original_full_text.split(" [")[1].replace("]",
                                                                          "") if " [" in original_full_text else "Uncategorized"
            else:
                # Fallback (shouldn't normally happen, but good practice)
                item_category = "Uncategorized"

            # --- Remove from category_items FIRST ---
            if item_category in self.category_items:
                if original_full_text in self.category_items[item_category]:  # Check existence
                    self.category_items[item_category].remove(original_full_text)

            # --- Use helper function ---
            self.create_completed_label(display_text)

            # --- Add to category_items (and category if not exists)---
            if item_category not in self.category_items:
                self.category_items[item_category] = []
            self.category_items[item_category].append(original_full_text)

            # --- THEN, Remove from the in_progress list---
            self.in_progress_scroll_content_layout.removeWidget(checkbox)
            checkbox.deleteLater()

        self.filter_by_category(self.progress_catagory.currentText())

    def label_selected(self, event, label):
        if label.frameStyle() == (QLabel.StyledPanel | QLabel.Sunken):
            label.setFrameStyle(QLabel.Panel)
        else:
            label.setFrameStyle(QLabel.StyledPanel | QLabel.Sunken)

    def remove_item(self):
        labels_to_remove = []
        for i in range(self.completed_scroll_content_layout.count()):
            item = self.completed_scroll_content_layout.itemAt(i).widget()
            if isinstance(item, QLabel) and item.frameStyle() == QLabel.Panel:
                labels_to_remove.append(item)

        for label in labels_to_remove:
            self.completed_scroll_content_layout.removeWidget(label)

            # --- Correctly remove from category_items ---
            label_text = label.text()  # Display text
            removed = False
            for category, items in self.category_items.items():
                for full_text in items:
                    if full_text.startswith(label_text + " ["):  # Use startswith
                        self.category_items[category].remove(full_text)
                        removed = True
                        break  # Inner loop break
                if removed:
                    break  # Outer loop break

            label.deleteLater()

    def search_labels(self):
        search_text = self.search_box.text().lower()
        self.search_box.clear()
        for i in range(self.completed_scroll_content_layout.count()):
            item = self.completed_scroll_content_layout.itemAt(i).widget()
            if isinstance(item, QLabel):
                if search_text in item.text().lower():
                    item.show()
                else:
                    item.hide()

    def save_data(self):
        data_path = self.get_data_path()
        try:
            with open(data_path, "w") as f:
                # Save Categories
                f.write("Categories:\n")
                for category in self.category_items:
                    f.write(f"{category}\n")

                # Save To Do Items
                f.write("To Do:\n")
                for category, items in self.category_items.items():
                    for full_text in items:
                        # --- Check if the item is currently a checkbox ---
                        is_checkbox = False
                        for i in range(self.in_progress_scroll_content_layout.count()):
                            widget = self.in_progress_scroll_content_layout.itemAt(i).widget()
                            if isinstance(widget, QCheckBox) and self.find_full_text(widget.text(),
                                                                                     category) == full_text:
                                f.write(f"{full_text},{widget.isChecked()}\n")
                                is_checkbox = True
                                break  # inner loop
                        if not is_checkbox:
                            # --- Check if the item exists as a label ---
                            for i in range(self.completed_scroll_content_layout.count()):
                                widget = self.completed_scroll_content_layout.itemAt(i).widget()
                                if isinstance(widget, QLabel) and self.find_full_text(widget.text(),
                                                                                      category) == full_text:
                                    # If its label it means, it was checked.
                                    f.write(f"{full_text},True\n")
                                    break  # inner loop

                # Save Completed Items
                f.write("Completed:\n")  # This part has no function now.

        except Exception as e:
            print(f"Error saving data: {e}")
            QMessageBox.critical(self, "Error", f"Could not save data.\nError: {e}")

    def load_data(self):
        data_path = self.get_data_path()
        self.category_items = {}  # Reset category_items

        try:
            if os.path.exists(data_path):
                with open(data_path, "r") as f:
                    lines = f.readlines()
                    mode = None
                    for line in lines:
                        line = line.strip()
                        if line == "Categories:":
                            mode = "categories"
                        elif line == "To Do:":
                            mode = "todo"
                        elif line == "Completed:":
                            mode = "completed"
                        elif mode == "categories":
                            category_name = line
                            self.progress_catagory.addItem(category_name)
                            self.completed_catagory.addItem(category_name)
                            if category_name not in self.category_items:
                                self.category_items[category_name] = []

                        elif mode == "todo":
                            parts = line.split(",")
                            if len(parts) != 2:
                                continue
                            full_item_text, checked_str = parts
                            checked = checked_str.lower() == "true"

                            display_text = full_item_text.split(" [")[0] if " [" in full_item_text else full_item_text
                            category_part = full_item_text.split(" [")[1].replace("]",
                                                                                  "") if " [" in full_item_text else "Uncategorized"

                            # --- Use helper functions ---
                            if checked:
                                self.create_completed_label(display_text)  # Call the helper function
                            else:
                                self.create_todo_checkbox(display_text, full_item_text,
                                                          checked)  # Call the helper function

                            # --- Add to category_items *after* creating the widget ---
                            if category_part not in self.category_items:
                                self.category_items[category_part] = []  # Ensure category exists
                            self.category_items[category_part].append(full_item_text)



                        elif mode == "completed":
                            full_item_text = line
                            display_text = full_item_text.split(" [")[0] if " [" in full_item_text else full_item_text

                            # Use helper function
                            self.create_completed_label(display_text)

                            category_part = full_item_text.split(" [")[1].replace("]",
                                                                                  "") if "[" in full_item_text else "Uncategorized"

                            # --- CRITICAL FIX: Check if item ALREADY exists ---
                            if category_part not in self.category_items:
                                self.category_items[category_part] = []

                            # Only add the item if it is not already present in the category_items dictionary
                            if full_item_text not in self.category_items[category_part]:
                                self.category_items[category_part].append(full_item_text)

            else:
                print(f"Data file not found: {data_path}")

        except Exception as e:
            print(f"Error loading data: {e}")
            QMessageBox.critical(self, "Error", "Could not load data.")

    def remove_category(self):
        index = self.progress_catagory.currentIndex()
        if index < 0:
            return

        category_text = self.progress_catagory.currentText()
        reply = QMessageBox.question(
            self,
            "Confirm Removal",
            f"Are you sure you want to remove the category '{category_text}' and all its items?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No,
        )

        if reply == QMessageBox.Yes:
            # --- Remove associated items ---
            if category_text in self.category_items:
                items_to_remove = self.category_items[category_text]

                # Remove from "In Progress" (Corrected)
                for i in reversed(range(self.in_progress_scroll_content_layout.count())):
                    item = self.in_progress_scroll_content_layout.itemAt(i).widget()
                    if isinstance(item, QCheckBox):
                        full_text = self.find_full_text(item.text(), category_text)
                        if full_text and full_text in items_to_remove:
                            self.in_progress_scroll_content_layout.removeWidget(item)
                            item.deleteLater()

                # Remove from "Completed" (Corrected)
                for i in reversed(range(self.completed_scroll_content_layout.count())):
                    item = self.completed_scroll_content_layout.itemAt(i).widget()
                    if isinstance(item, QLabel):
                        full_text = self.find_full_text(item.text(), category_text)
                        if full_text and full_text in items_to_remove:
                            self.completed_scroll_content_layout.removeWidget(item)
                            item.deleteLater()

                del self.category_items[category_text]  # Remove from dictionary

            self.progress_catagory.removeItem(index)

            # Find and remove from completed_catagory
            for i in range(self.completed_catagory.count()):
                if self.completed_catagory.itemText(i) == category_text:
                    self.completed_catagory.removeItem(i)
                    break

    def closeEvent(self, event):
        self.save_data()
        event.accept()

    def add_category(self):
        new_category_text, ok = QInputDialog.getText(
            self, "Add Category", "Enter category name:"
        )
        if ok and new_category_text:
            new_category_text = new_category_text.strip()
            if new_category_text:
                # Check for duplicates in *both* combo boxes
                if (new_category_text in [self.progress_catagory.itemText(i) for i in
                                          range(self.progress_catagory.count())] or
                        new_category_text in [self.completed_catagory.itemText(i) for i in
                                              range(self.completed_catagory.count())]):
                    QMessageBox.warning(self, "Warning", "Category already exists.")
                    return

                self.progress_catagory.addItem(new_category_text)
                self.completed_catagory.addItem(new_category_text)  # Add to completed_catagory too
                new_index = self.progress_catagory.count() - 1
                self.progress_catagory.setCurrentIndex(new_index)  # Set focus


            else:
                QMessageBox.warning(self, "Warning", "Category name cannot be empty.")
                self.add_category()
        elif ok:
            QMessageBox.warning(self, "Warning", "Category name cannot be empty.")
            self.add_category()

        # In remove_category()

    def remove_category(self):
        index = self.progress_catagory.currentIndex()
        if index < 0:
            return

        category_text = self.progress_catagory.currentText()
        reply = QMessageBox.question(
            self,
            "Confirm Removal",
            f"Are you sure you want to remove the category '{category_text}' and all its items?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No,
        )

        if reply == QMessageBox.Yes:
            # --- Remove associated items ---
            if category_text in self.category_items:
                # --- CORRECTED: Iterate over a *copy* of the list ---
                items_to_remove = self.category_items[category_text].copy()

                # Remove from "In Progress"
                for full_text in items_to_remove:  # Iterate over the *full texts*
                    display_text = full_text.split(" [")[0]
                    for i in reversed(range(self.in_progress_scroll_content_layout.count())):
                        item = self.in_progress_scroll_content_layout.itemAt(i).widget()
                        if isinstance(item,
                                      QCheckBox) and item.text() == display_text:  # Compare the display text
                            self.in_progress_scroll_content_layout.removeWidget(item)
                            item.deleteLater()

                # Remove from "Completed"
                for full_text in items_to_remove:
                    display_text = full_text.split(" [")[0]
                    for i in reversed(range(self.completed_scroll_content_layout.count())):
                        item = self.completed_scroll_content_layout.itemAt(i).widget()
                        if isinstance(item, QLabel) and item.text() == display_text:  # Compare the display text
                            self.completed_scroll_content_layout.removeWidget(item)
                            item.deleteLater()

                del self.category_items[category_text]  # Remove from the dictionary

            self.progress_catagory.removeItem(index)

            # Find and remove from completed_catagory
            for i in range(self.completed_catagory.count()):
                if self.completed_catagory.itemText(i) == category_text:
                    self.completed_catagory.removeItem(i)
                    break

    def filter_by_category(self, category_text):
        """Filters both In Progress and Completed items by the selected category."""

        # Filter In Progress items
        for i in range(self.in_progress_scroll_content_layout.count()):
            item = self.in_progress_scroll_content_layout.itemAt(i).widget()
            if isinstance(item, QCheckBox):
                # --- Get full text from category_items ---
                full_text = self.find_full_text(item.text(), category_text)
                if full_text:  # Only proceed if full_text is found
                    item_category = full_text.split(" [")[1].replace("]",
                                                                     "") if " [" in full_text else "Uncategorized"
                    if item_category == category_text:
                        item.show()
                    else:
                        item.hide()
                else:
                    item.hide()  # Hide if not found

        # Filter Completed items
        for i in range(self.completed_scroll_content_layout.count()):
            item = self.completed_scroll_content_layout.itemAt(i).widget()
            if isinstance(item, QLabel):
                # --- Get full text from category_items ---
                full_text = self.find_full_text(item.text(), category_text)
                if full_text:  # Only proceed if full_text is found
                    item_category = full_text.split(" [")[1].replace("]",
                                                                     "") if " [" in full_text else "Uncategorized"
                    if item_category == category_text:
                        item.show()
                    else:
                        item.hide()
                else:
                    item.hide()  # Hide if not found

    def find_full_text(self, display_text, category_text):
        """Helper function to find the full text in category_items."""
        if category_text in self.category_items:
            for full_text in self.category_items[category_text]:
                if full_text.startswith(display_text + " ["):
                    return full_text
        return None

    def sync_category_selection(self, category_text):
        """Synchronizes the category selection between the two ComboBoxes."""

        # Block signals temporarily to prevent infinite recursion
        self.progress_catagory.blockSignals(True)
        self.completed_catagory.blockSignals(True)

        # Set the current index in *both* ComboBoxes
        for i in range(self.progress_catagory.count()):
            if self.progress_catagory.itemText(i) == category_text:
                self.progress_catagory.setCurrentIndex(i)
                break  # Important: stop searching after finding a match

        for i in range(self.completed_catagory.count()):
            if self.completed_catagory.itemText(i) == category_text:
                self.completed_catagory.setCurrentIndex(i)
                break  # Important: stop searching after finding a match
        # Re-enable signals
        self.progress_catagory.blockSignals(False)
        self.completed_catagory.blockSignals(False)

        # --- CRITICAL: Apply the filter *after* setting the index ---
        self.filter_by_category(category_text)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
