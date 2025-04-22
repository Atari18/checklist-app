import os
import sys

from PySide6.QtCore import Qt
from PySide6.QtGui import QFont, QIcon, QFontDatabase
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QCheckBox, QLabel, QLineEdit,
    QMessageBox, QWidget, QVBoxLayout, QInputDialog, QFrame
)

from ui.my_form import Ui_MainWindow

import sys
import os

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(os.path.dirname(__file__))

    return os.path.join(base_path, relative_path)


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        """
        Initializes the main window of the checklist application.

        Sets up the user interface, establishes signal-slot connections,
        loads data from file, loads fonts, and filters the initial view.
        """
        super().__init__()
        self.setupUi(self)

        self.category_items = {}

        # --- UI Setup ---
        self._setup_ui()

        # --- Connections ---
        self._setup_connections()

        # --- Data Loading and Initial Display ---
        self.load_data()
        MainWindow.load_fonts()  # Call static method using class name
        self.filter_by_category(self.progress_catagory.currentText())

    def _setup_ui(self):
        """Sets up the basic UI elements and their properties."""
        self.in_progress_v_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.completed_v_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        self.in_progress_scroll_content_widget = QWidget()
        self.in_progress_scroll_content_layout = QVBoxLayout(self.in_progress_scroll_content_widget)
        self.in_progress_scroll.setWidget(self.in_progress_scroll_content_widget)
        self.in_progress_scroll_content_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        self.completed_scroll_content_widget = QWidget()
        self.completed_scroll_content_layout = QVBoxLayout(self.completed_scroll_content_widget)
        self.completed_scroll.setWidget(self.completed_scroll_content_widget)
        self.completed_scroll_content_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        self.in_progress_scroll_content_widget.setStyleSheet("background-color: transparent;")
        self.completed_scroll_content_widget.setStyleSheet("background-color: transparent;")

        search_icon = QIcon(":icons/images/search_icon.png")
        self.search_box.addAction(search_icon, QLineEdit.LeadingPosition)
        self.search_box.setPlaceholderText("Search")

    def _setup_connections(self):
        """Establishes signal-slot connections for UI elements."""
        self.add_catagory_button.clicked.connect(self.add_category)
        self.remove_catagory_button.clicked.connect(self.remove_category)
        self.progress_catagory.currentTextChanged.connect(self.sync_category_selection)
        self.completed_catagory.currentTextChanged.connect(self.sync_category_selection)
        self.add_button.clicked.connect(self.add_item)
        self.remove_button_2.clicked.connect(self.remove_checked_from_progress)
        self.complete_button.clicked.connect(self.move_checked_items)
        self.remove_button.clicked.connect(self.remove_item)
        self.search_button.clicked.connect(self.search_labels)

    @staticmethod
    def load_fonts():
        """Loads custom fonts from the 'fonts' directory."""

        font_dir = resource_path("fonts")
        print(f"Looking for fonts in: {font_dir}")
        if os.path.isdir(font_dir):
            for filename in os.listdir(font_dir):
                if filename.endswith((".ttf", ".otf")):
                    font_path = os.path.join(font_dir, filename)
                    print(f"Adding font: {font_path}")
                    QFontDatabase.addApplicationFont(font_path)
        else:
            print(f"Font directory not found: {font_dir}")

    @staticmethod
    def get_data_path():
        """Gets the path to the data file, creating the directory if it doesn't exist."""
        app_name = "ChecklistApp"
        local_app_data = os.path.join(os.getenv('LOCALAPPDATA'), app_name)
        if not os.path.exists(local_app_data):
            os.makedirs(local_app_data)
        return os.path.join(local_app_data, "checklist_data.txt")

    def add_item(self):
        """Adds a new to-do item to the 'In Progress' list."""
        item_text = self.lineEdit.text().strip()
        selected_category = self.progress_catagory.currentText()

        if item_text:
            full_item_text = f"{item_text} [{selected_category}]"
            display_text = item_text

            if selected_category not in self.category_items:
                self.category_items[selected_category] = []
            self.category_items[selected_category].append(full_item_text)

            self.create_todo_checkbox(display_text, False)

            self.lineEdit.clear()
            self.filter_by_category(self.progress_catagory.currentText())

        else:
            QMessageBox.warning(self, "Warning", "Please enter text in the text field.")

    def remove_checked_from_progress(self):
        """Removes checked items from the 'In Progress' list."""
        checked_items = []
        for i in range(self.in_progress_scroll_content_layout.count()):
            item = self.in_progress_scroll_content_layout.itemAt(i).widget()
            if isinstance(item, QCheckBox) and item.isChecked():
                checked_items.append(item)

        for checkbox in checked_items:
            display_text = checkbox.text()
            original_full_text = self.find_full_text(display_text, self.progress_catagory.currentText())

            if original_full_text:
                item_category = original_full_text.split(" [")[1].replace("]",
                                                                          "") if " [" in original_full_text else "Uncategorized"
            else:
                item_category = "Uncategorized"

            if item_category in self.category_items:
                if original_full_text in self.category_items[item_category]:
                    self.category_items[item_category].remove(original_full_text)

            self.in_progress_scroll_content_layout.removeWidget(checkbox)
            checkbox.deleteLater()

        self.filter_by_category(self.progress_catagory.currentText())

    def create_todo_checkbox(self, display_text, checked):
        """Helper function to create and add a to-do checkbox."""
        checkbox = QCheckBox(display_text)
        checkbox.setChecked(checked)
        font = QFont()
        font.setPointSize(11)
        checkbox.setFont(font)
        self.in_progress_scroll_content_layout.addWidget(checkbox)

    def create_completed_label(self, display_text):
        """Helper function to create and add a completed item label alphabetically."""
        label = QLabel(display_text)
        font = QFont()
        font.setPointSize(11)
        label.setFont(font)
        label.setFrameStyle(QFrame.Shape.StyledPanel | QFrame.Shadow.Sunken)
        label.setMargin(5)
        label.setWordWrap(True)
        label.setCursor(Qt.CursorShape.PointingHandCursor)
        label.mousePressEvent = lambda event, lb=label: self.label_selected(lb)

        # --- Insertion Logic for Alphabetical Order ---
        insert_index = 0
        new_text_lower = display_text.lower()

        for i in range(self.completed_scroll_content_layout.count()):
            widget = self.completed_scroll_content_layout.itemAt(i).widget()
            if isinstance(widget, QLabel):
                existing_text_lower = widget.text().lower()
                if new_text_lower < existing_text_lower:
                    insert_index = i
                    break
            insert_index = i + 1

        self.completed_scroll_content_layout.insertWidget(insert_index, label)

    def edit_item_text(self, _, item):
        """Allows the user to edit the text of a to-do item."""
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
        """Updates the text of a to-do item after editing."""
        new_task_text = line_edit.text().strip()
        if not new_task_text:
            line_edit.deleteLater()
            return

        new_full_text = new_task_text + category_part

        old_full_text = item.text()
        old_category = self.progress_catagory.currentText()
        new_category = category_part.strip(" []")

        old_full_text_correct = self.find_full_text(old_full_text.split(" [")[0], old_category)

        if old_full_text_correct:
            if old_category in self.category_items and old_full_text_correct in self.category_items[old_category]:
                self.category_items[old_category].remove(old_full_text_correct)
                if new_category not in self.category_items:
                    self.category_items[new_category] = []
                self.category_items[new_category].append(new_full_text)

        item.setText(new_full_text)
        line_edit.deleteLater()
        self.filter_by_category(self.progress_catagory.currentText())

    def move_checked_items(self):
        """Moves checked items from 'In Progress' to 'Completed'."""
        checked_items = []
        for i in range(self.in_progress_scroll_content_layout.count()):
            item = self.in_progress_scroll_content_layout.itemAt(i).widget()
            if isinstance(item, QCheckBox) and item.isChecked():
                checked_items.append(item)

        for checkbox in checked_items:
            display_text = checkbox.text()
            original_full_text = self.find_full_text(display_text, self.progress_catagory.currentText())

            if original_full_text:
                item_category = original_full_text.split(" [")[1].replace("]",
                                                                          "") if " [" in original_full_text else "Uncategorized"
            else:
                item_category = "Uncategorized"

            if item_category in self.category_items:
                if original_full_text in self.category_items[item_category]:
                    self.category_items[item_category].remove(original_full_text)

            self.create_completed_label(display_text)

            if item_category not in self.category_items:
                self.category_items[item_category] = []
            self.category_items[item_category].append(original_full_text)

            self.in_progress_scroll_content_layout.removeWidget(checkbox)
            checkbox.deleteLater()

        self.filter_by_category(self.progress_catagory.currentText())

    def label_selected(self, label):
        """Highlights a completed item label when clicked."""
        if label.frameStyle() == (QFrame.Shape.StyledPanel | QFrame.Shadow.Sunken):
            label.setFrameStyle(QFrame.Shape.Panel)
        else:
            label.setFrameStyle(QFrame.Shape.StyledPanel | QFrame.Shadow.Sunken)

    def remove_item(self):
        """Removes selected items from the 'Completed' list."""
        labels_to_remove = []
        for i in range(self.completed_scroll_content_layout.count()):
            item = self.completed_scroll_content_layout.itemAt(i).widget()
            if isinstance(item, QLabel) and item.frameStyle() == QFrame.Shape.Panel:
                labels_to_remove.append(item)

        for label in labels_to_remove:
            self.completed_scroll_content_layout.removeWidget(label)

            label_text = label.text()
            removed = False
            for category, items in self.category_items.items():
                for full_text in items:
                    if full_text.startswith(label_text + " ["):
                        self.category_items[category].remove(full_text)
                        removed = True
                        break
                if removed:
                    break

            label.deleteLater()

    def search_labels(self):
        """Filters the 'Completed' list based on the search text."""
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
        """Saves the current state of the checklist to a file."""
        data_path = self.get_data_path()
        try:
            with open(data_path, "w") as f:
                f.write("Categories:\n")
                for category in self.category_items:
                    f.write(f"{category}\n")

                f.write("To Do:\n")
                for category, items in self.category_items.items():
                    for full_text in items:
                        is_checkbox = False
                        for i in range(self.in_progress_scroll_content_layout.count()):
                            widget = self.in_progress_scroll_content_layout.itemAt(i).widget()
                            if isinstance(widget, QCheckBox) and self.find_full_text(widget.text(),
                                                                                     category) == full_text:
                                f.write(f"{full_text},{widget.isChecked()}\n")
                                is_checkbox = True
                                break
                        if not is_checkbox:
                            for i in range(self.completed_scroll_content_layout.count()):
                                widget = self.completed_scroll_content_layout.itemAt(i).widget()
                                if isinstance(widget, QLabel) and self.find_full_text(widget.text(),
                                                                                      category) == full_text:
                                    f.write(f"{full_text},True\n")
                                    break

                f.write("Completed:\n")

        except Exception as e:
            print(f"Error saving data: {e}")
            QMessageBox.critical(self, "Error", f"Could not save data.\nError: {e}")


    def load_data(self):
        """Loads the checklist data from a file."""
        data_path = self.get_data_path()
        self.category_items = {}  # Clear existing data

        try:
            if os.path.exists(data_path):
                with open(data_path, "r") as f:
                    lines = f.readlines()
                    mode = None
                    categories_list = [] # Temporary list to store categories

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
                            categories_list.append(category_name) # Add to list
                            if category_name not in self.category_items:
                                self.category_items[category_name] = []

                        elif mode == "todo":
                            parts = line.split(",")
                            if len(parts) != 2:  # Handle malformed lines
                                continue
                            full_item_text, checked_str = parts
                            checked = checked_str.lower() == "true"

                            display_text = full_item_text.split(" [")[0] if " [" in full_item_text else full_item_text
                            category_part = full_item_text.split(" [")[1].replace("]", "") if " [" in full_item_text else "Uncategorized"

                            if checked:
                                self.create_completed_label(display_text)
                            else:
                                self.create_todo_checkbox(display_text, checked)

                            if category_part not in self.category_items:
                                self.category_items[category_part] = []
                            self.category_items[category_part].append(full_item_text)

                        elif mode == "completed":
                            full_item_text = line
                            display_text = full_item_text.split(" [")[0] if " [" in full_item_text else full_item_text
                            self.create_completed_label(display_text)
                            category_part = full_item_text.split(" [")[1].replace("]", "") if "[" in full_item_text else "Uncategorized"

                            if category_part not in self.category_items:
                                self.category_items[category_part] = []

                            if full_item_text not in self.category_items[category_part]:
                                self.category_items[category_part].append(full_item_text)
                    # Sort and add categories after reading them all
                    categories_list.sort(key=str.lower) # Sort alphabetically (case-insensitive)
                    for category_name in categories_list:
                        self.progress_catagory.addItem(category_name)
                        self.completed_catagory.addItem(category_name)
            else:
                print(f"Data file not found: {data_path}")

        except Exception as e:
            print(f"Error loading data: {e}")
            QMessageBox.critical(self, "Error", "Could not load data.")

    def remove_category(self):
        """Removes the currently selected category and all its items."""
        index = self.progress_catagory.currentIndex()
        if index < 0:  # No category selected
            return

        category_text = self.progress_catagory.currentText()
        reply = QMessageBox.question(
            self,
            "Confirm Removal",
            f"Are you sure you want to remove the category '{category_text}' and all its items?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No,
        )

        if reply == QMessageBox.StandardButton.Yes:
            if category_text in self.category_items:
                items_to_remove = self.category_items[category_text].copy()  # Iterate over a copy

                # Remove from "In Progress" UI
                for full_text in items_to_remove:
                    display_text = full_text.split(" [")[0]
                    for i in reversed(range(self.in_progress_scroll_content_layout.count())):
                        item = self.in_progress_scroll_content_layout.itemAt(i).widget()
                        if isinstance(item, QCheckBox) and item.text() == display_text:
                            self.in_progress_scroll_content_layout.removeWidget(item)
                            item.deleteLater()  # Important: prevent memory leaks

                # Remove from "Completed" UI
                for full_text in items_to_remove:
                    display_text = full_text.split(" [")[0]
                    for i in reversed(range(self.completed_scroll_content_layout.count())):
                        item = self.completed_scroll_content_layout.itemAt(i).widget()
                        if isinstance(item, QLabel) and item.text() == display_text:
                            self.completed_scroll_content_layout.removeWidget(item)
                            item.deleteLater()

                del self.category_items[category_text]  # Remove from data structure

            # Remove from ComboBoxes
            self.progress_catagory.removeItem(index)
            for i in range(self.completed_catagory.count()):
                if self.completed_catagory.itemText(i) == category_text:
                    self.completed_catagory.removeItem(i)
                    break

    def closeEvent(self, event):
        """Handles the window close event (saves data)."""
        self.save_data()
        event.accept()

    def add_category(self):
        """Adds a new category to the ComboBoxes, maintaining alphabetical order."""
        new_category_text, ok = QInputDialog.getText(
            self, "Add Category", "Enter category name:"
        )
        if ok and new_category_text:
            new_category_text = new_category_text.strip()
            if new_category_text:
                if (new_category_text in [self.progress_catagory.itemText(i) for i in
                                          range(self.progress_catagory.count())] or
                        new_category_text in [self.completed_catagory.itemText(i) for i in
                                              range(self.completed_catagory.count())]):
                    QMessageBox.warning(self, "Warning", "Category already exists.")
                    return

                # --- Insert alphabetically into progress_catagory ---
                inserted = False
                for i in range(self.progress_catagory.count()):
                    if new_category_text.lower() < self.progress_catagory.itemText(i).lower():
                        self.progress_catagory.insertItem(i, new_category_text)
                        inserted = True
                        break
                if not inserted:
                    self.progress_catagory.addItem(new_category_text)
                self.progress_catagory.setCurrentText(new_category_text)  # Set as current

                # --- Insert alphabetically into completed_catagory ---
                inserted = False
                for i in range(self.completed_catagory.count()):
                    if new_category_text.lower() < self.completed_catagory.itemText(i).lower():
                        self.completed_catagory.insertItem(i, new_category_text)
                        inserted = True
                        break
                if not inserted:
                    self.completed_catagory.addItem(new_category_text)


            else:
                QMessageBox.warning(self, "Warning", "Category name cannot be empty.")
                self.add_category()  # Re-open dialog
        elif ok:
            QMessageBox.warning(self, "Warning", "Category name cannot be empty.")
            self.add_category()

    def filter_by_category(self, category_text):
        """Filters the displayed items (both lists) based on the selected category."""

        # Filter "In Progress" items
        for i in range(self.in_progress_scroll_content_layout.count()):
            item = self.in_progress_scroll_content_layout.itemAt(i).widget()
            if isinstance(item, QCheckBox):
                full_text = self.find_full_text(item.text(), category_text)
                if full_text:
                    item_category = full_text.split(" [")[1].replace("]",
                                                                     "") if " [" in full_text else "Uncategorized"
                    item.setVisible(item_category == category_text)  # Use setVisible for efficiency
                else:
                    item.hide()

        # Filter "Completed" items
        for i in range(self.completed_scroll_content_layout.count()):
            item = self.completed_scroll_content_layout.itemAt(i).widget()
            if isinstance(item, QLabel):
                full_text = self.find_full_text(item.text(), category_text)
                if full_text:
                    item_category = full_text.split(" [")[1].replace("]",
                                                                     "") if " [" in full_text else "Uncategorized"
                    item.setVisible(item_category == category_text)
                else:
                    item.hide()

    def find_full_text(self, display_text, category_text):
        """Helper function to find the full text of an item given its display text and category."""
        if category_text in self.category_items:
            for full_text in self.category_items[category_text]:
                if full_text.startswith(display_text + " ["):
                    return full_text
        return None

    def sync_category_selection(self, category_text):
        """Synchronizes the selected category between the two ComboBoxes."""
        self.progress_catagory.blockSignals(True)  # Prevent infinite loops
        self.completed_catagory.blockSignals(True)

        for i in range(self.progress_catagory.count()):
            if self.progress_catagory.itemText(i) == category_text:
                self.progress_catagory.setCurrentIndex(i)
                break

        for i in range(self.completed_catagory.count()):
            if self.completed_catagory.itemText(i) == category_text:
                self.completed_catagory.setCurrentIndex(i)
                break

        self.progress_catagory.blockSignals(False)
        self.completed_catagory.blockSignals(False)

        self.filter_by_category(category_text)  # Update the display


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
