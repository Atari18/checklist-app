import os
import sys

import resourse_rc

from PySide6.QtCore import Qt
from PySide6.QtGui import QFont, QIcon, QFontDatabase
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QCheckBox, QLabel, QLineEdit,
    QMessageBox, QWidget, QVBoxLayout, QComboBox, QInputDialog
)

from ui.my_form import Ui_MainWindow  # Import your UI file


class MainWindow(QMainWindow, Ui_MainWindow):
    import os
    import sys

    import resourse_rc

    from PySide6.QtCore import Qt
    from PySide6.QtGui import QFont, QIcon, QFontDatabase
    from PySide6.QtWidgets import (
        QApplication, QMainWindow, QCheckBox, QLabel, QLineEdit,
        QMessageBox, QWidget, QVBoxLayout, QComboBox, QInputDialog
    )

    from ui.my_form import Ui_MainWindow  # Import your UI file

    class MainWindow(QMainWindow, Ui_MainWindow):
        def __init__(self):
            super().__init__()
            self.setupUi(self)
            self.add_button.clicked.connect(self.add_item)
            self.remove_button.clicked.connect(self.remove_item)
            self.complete_button.clicked.connect(self.move_checked_items)
            self.search_button.clicked.connect(self.search_labels)

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
            self.category_items = {}

            # --- Connect currentTextChanged for synchronized filtering ---
            self.progress_catagory.currentTextChanged.connect(self.sync_category_selection)
            self.completed_catagory.currentTextChanged.connect(self.sync_category_selection)  # ADD THIS

            self.load_data()
            self.load_fonts()

            # Initial filtering (important!)
            self.filter_by_category(self.progress_catagory.currentText())  # Call the combined filter function

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

        def add_item(self):
            item_text = self.lineEdit.text().strip()
            selected_category = self.progress_catagory.currentText()
            if item_text:
                full_item_text = f"{item_text} [{selected_category}]"  # Keep full text for internal use
                display_text = item_text  # Use only the item_text for display

                checkbox = QCheckBox(display_text)  # Use display_text here
                font = QFont()
                font.setPointSize(11)
                checkbox.setFont(font)
                self.in_progress_scroll_content_layout.addWidget(checkbox)
                self.lineEdit.clear()

                if selected_category not in self.category_items:
                    self.category_items[selected_category] = []
                self.category_items[selected_category].append(full_item_text)  # Store *full* text

                self.filter_by_category(self.progress_catagory.currentText())

            else:
                QMessageBox.warning(self, "Warning", "Please enter text in the text field.")

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

            # --- Update in category_items ---
            old_full_text = item.text()
            old_category_part = old_full_text.split(" [")[1].replace("]",
                                                                     "") if " [" in old_full_text else "Uncategorized"
            new_category_part = new_full_text.split(" [")[1].replace("]",
                                                                     "") if " [" in new_full_text else "Uncategorized"

            if old_category_part in self.category_items and old_full_text in self.category_items[old_category_part]:
                self.category_items[old_category_part].remove(old_full_text)
                if new_category_part not in self.category_items:
                    self.category_items[new_category_part] = []
                self.category_items[new_category_part].append(new_full_text)

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
                self.in_progress_scroll_content_layout.removeWidget(checkbox)
                checkbox.deleteLater()

                # --- Get full text and extract display text ---
                full_item_text = checkbox.text() + " [" + self.progress_catagory.currentText() + "]"  # Need to recreate full text
                display_text = checkbox.text()  # Display text is *just* the checkbox text

                label = QLabel(display_text)  # Use display_text here
                font = QFont()
                font.setPointSize(11)
                label.setFont(font)
                label.setFrameStyle(QLabel.StyledPanel | QLabel.Sunken)
                label.setMargin(5)
                label.setWordWrap(True)
                label.setCursor(Qt.PointingHandCursor)
                label.mousePressEvent = lambda event, lb=label: self.label_selected(event, lb)
                self.completed_scroll_content_layout.addWidget(label)

                item_category = full_item_text.split(" [")[1].replace("]",
                                                                      "") if " [" in full_item_text else "Uncategorized"
                if item_category not in self.category_items:
                    self.category_items[item_category] = []
                self.category_items[item_category].append(full_item_text)  # Store *full* text

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

                # --- Remove from category_items (Corrected) ---
                # We need to find the *full* text in self.category_items.
                label_text = label.text()  # This is the *display* text
                removed = False  # Flag
                for category, items in self.category_items.items():
                    for full_text in items:
                        if full_text.startswith(label_text + " ["):  # Check if it *starts with* the display text
                            self.category_items[category].remove(full_text)
                            removed = True
                            break  # Break inner loop
                    if removed:
                        break  # Break outer loop.

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
                    for i in range(self.progress_catagory.count()):
                        f.write(f"{self.progress_catagory.itemText(i)}\n")

                    # Save To Do Items (with full text and checked state)
                    f.write("To Do:\n")
                    for i in range(self.in_progress_scroll_content_layout.count()):
                        item = self.in_progress_scroll_content_layout.itemAt(i).widget()
                        if isinstance(item, QCheckBox):
                            # Find the full text corresponding to this checkbox
                            full_text = self.find_full_text(item.text(), self.progress_catagory.currentText())
                            if full_text:  # Save only if full_text is found
                                f.write(f"{full_text},{item.isChecked()}\n")

                    # Save Completed Items (with full text)
                    f.write("Completed:\n")
                    for i in range(self.completed_scroll_content_layout.count()):
                        item = self.completed_scroll_content_layout.itemAt(i).widget()
                        if isinstance(item, QLabel):
                            # Find full text.
                            full_text = self.find_full_text(item.text(), self.completed_catagory.currentText())
                            if full_text:
                                f.write(f"{full_text}\n")


            except Exception as e:
                print(f"Error saving data: {e}")
                QMessageBox.critical(self, "Error", f"Could not save data.\nError: {e}")

        def load_data(self):
            data_path = self.get_data_path()
            self.category_items = {}  # Reset category_items!  CRUCIAL (Make sure this is here)
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
                                # --- CORRECTED CATEGORY LOADING ---
                                category_name = line
                                self.progress_catagory.addItem(category_name)
                                self.completed_catagory.addItem(category_name)
                                # Add the category to self.category_items *here*
                                if category_name not in self.category_items:
                                    self.category_items[category_name] = []


                            elif mode == "todo":
                                parts = line.split(",")
                                if len(parts) != 2:
                                    continue
                                full_item_text, checked_str = parts
                                checked = checked_str.lower() == "true"

                                display_text = full_item_text.split(" [")[
                                    0] if " [" in full_item_text else full_item_text

                                checkbox = QCheckBox(display_text)
                                checkbox.setChecked(checked)
                                font = QFont()
                                font.setPointSize(11)
                                checkbox.setFont(font)
                                self.in_progress_scroll_content_layout.addWidget(checkbox)

                                category_part = full_item_text.split(" [")[1].replace("]",
                                                                                      "") if " [" in full_item_text else "Uncategorized"
                                # No need to check existence here, it's handled above
                                self.category_items[category_part].append(full_item_text)

                            elif mode == "completed":
                                full_item_text = line  # Full text for completed items
                                display_text = full_item_text.split(" [")[
                                    0] if " [" in full_item_text else full_item_text

                                label = QLabel(display_text)
                                font = QFont()
                                font.setPointSize(11)
                                label.setFont(font)
                                label.setFrameStyle(QLabel.StyledPanel | QLabel.Sunken)
                                label.setMargin(5)
                                label.setWordWrap(True)
                                self.completed_scroll_content_layout.addWidget(label)
                                label.setCursor(Qt.PointingHandCursor)
                                label.mousePressEvent = lambda event, lb=label: self.label_selected(event, lb)

                                category_part = full_item_text.split(" [")[1].replace("]",
                                                                                      "") if "[" in full_item_text else "Uncategorized"
                                # No need to check existence here, it's handled above.
                                self.category_items[category_part].append(full_item_text)

                else:
                    print(f"Data file not found: {data_path}")
            except Exception as e:
                print(f"Error loading data: {e}")
                QMessageBox.critical(self, "Error", "Could not load data.")

        def remove_category(self):
            index = self.progress_catagory.currentIndex()
            if index < 0:
                return  # No category selected

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

                    del self.category_items[category_text]  # Remove from the dictionary

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

        def remove_category(self):
            index = self.progress_catagory.currentIndex()
            if index < 0:
                return  # No category selected

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

                    # Remove from "In Progress"
                    for i in reversed(range(self.in_progress_scroll_content_layout.count())):
                        item = self.in_progress_scroll_content_layout.itemAt(i).widget()
                        if isinstance(item, QCheckBox) and item.text() in items_to_remove:
                            self.in_progress_scroll_content_layout.removeWidget(item)
                            item.deleteLater()

                    # Remove from "Completed"
                    for i in reversed(range(self.completed_scroll_content_layout.count())):
                        item = self.completed_scroll_content_layout.itemAt(i).widget()
                        if isinstance(item, QLabel) and item.text() in items_to_remove:
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
                    if full_text.startswith(display_text + " ["):  # Check if it starts with display text
                        return full_text
            return None  # Return None if not found

        def sync_category_selection(self, category_text):
            """Synchronizes the category selection between the two ComboBoxes."""

            # Block signals temporarily to prevent infinite recursion
            self.progress_catagory.blockSignals(True)
            self.completed_catagory.blockSignals(True)

            # Set the current index in *both* ComboBoxes
            for i in range(self.progress_catagory.count()):
                if self.progress_catagory.itemText(i) == category_text:
                    self.progress_catagory.setCurrentIndex(i)
                    break

            for i in range(self.completed_catagory.count()):
                if self.completed_catagory.itemText(i) == category_text:
                    self.completed_catagory.setCurrentIndex(i)
                    break

            # Re-enable signals
            self.progress_catagory.blockSignals(False)
            self.completed_catagory.blockSignals(False)

            # Apply the filter
            self.filter_by_category(category_text)


    if __name__ == "__main__":
        app = QApplication(sys.argv)
        window = MainWindow()
        window.show()
        sys.exit(app.exec())
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())