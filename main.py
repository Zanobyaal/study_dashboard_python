
import tkinter as tk
from tkinter import messagebox
import json
import os


# ==============================
# 1. Data Classes
# ==============================

class Studierender:
    def __init__(self, name, email, semester):
        self.name = name
        self.email = email
        self.semester = semester


class Lernzeit:
    def __init__(self, datum, dauer):
        self.datum = datum
        self.dauer = dauer

    def berechneDauer(self):
        return self.dauer


class Lernziel:
    def __init__(self, bezeichnung, zielzeit, erreichteZeit):
        self.bezeichnung = bezeichnung
        self.zielzeit = zielzeit
        self.erreichteZeit = erreichteZeit
        self.lernzeiten = []

    def berechneFortschritt(self):
        if self.zielzeit == 0:
            return 0
        return min(100, self.erreichteZeit / self.zielzeit * 100)

    def aktualisiereFortschritt(self, stunden):
        lernzeit = Lernzeit("Diese Woche", stunden)
        self.lernzeiten.append(lernzeit)
        self.erreichteZeit += stunden


class Pruefung:
    def __init__(self, fach, datum, status):
        self.fach = fach
        self.datum = datum
        self.status = status


class Note:
    def __init__(self, wert, versuch):
        self.wert = wert
        self.versuch = versuch

    def zeigeNote(self):
        return self.wert


class Notiz:
    def __init__(self, text):
        self.text = text

    def bearbeiteNotiz(self, neuer_text):
        self.text = neuer_text


class Theme:
    def __init__(self, name, primaryColor, secondaryColor):
        self.name = name
        self.primaryColor = primaryColor
        self.secondaryColor = secondaryColor


class MotivationQuote:
    def __init__(self, text):
        self.text = text

    def zeigeQuote(self):
        return self.text


# ==============================
# 2. Dashboard Application
# ==============================

class StudyDashboardApp:

    def load_data(self):
        """Load saved learning goals, notes, and theme."""

        if not os.path.exists(self.data_file):
            return

        try:
            with open(self.data_file, "r", encoding="utf-8") as file:
                data = json.load(file)

            saved_goals = data.get("learning_goals", {})

            for goal in self.lernziele:
                if goal.bezeichnung in saved_goals:
                    goal.erreichteZeit = float(
                        saved_goals[goal.bezeichnung]
                    )

            saved_notes = data.get("notes", [])

            self.notizen = [
                Notiz(note) for note in saved_notes
                if isinstance(note, str)
            ]

            theme_name = data.get("theme")

            if theme_name in self.themes:
                self.current_theme = self.themes[theme_name]

        except (OSError, json.JSONDecodeError, TypeError, ValueError):
            messagebox.showwarning(
                "Data Warning",
                "Saved data could not be loaded. Default data will be used."
            )

    def save_data(self):
        """Save learning goals, notes, and the selected theme."""

        data = {
            "learning_goals": {
                goal.bezeichnung: goal.erreichteZeit
                for goal in self.lernziele
            },
            "notes": [
                note.text for note in self.notizen
            ],
            "theme": self.current_theme.name
        }

        try:
            with open(self.data_file, "w", encoding="utf-8") as file:
                json.dump(data, file, indent=4, ensure_ascii=False)

        except OSError:
            messagebox.showerror(
                "Save Error",
                "Could not save dashboard data."
            )

    def close_app(self):
        """Save the latest data before closing the dashboard."""

        self.save_data()
        self.root.destroy()


    def __init__(self, root):

        self.root = root
        self.root.title("My Study Dashboard")
        self.root.geometry("1000x720")
        self.root.minsize(750, 550)

        # Colors
        self.themes = {
            "Sage Green": Theme(
                "Sage Green", "#35483C", "#A7B99E"
            ),
            "Soft Pink": Theme(
                "Soft Pink", "#80566B", "#D9AFC1"
            ),
            "Lavender": Theme(
                "Lavender", "#62577E", "#B9AED5"
            )
        }

        self.background = "#F7F4EC"
        self.card_color = "#FFFFFF"
        self.text_color = "#667568"
        self.current_theme = self.themes["Sage Green"]

        # Student information
        self.student = Studierender(
            "Student", "student@example.com", 1
        )

        # Learning goals
        self.lernziele = [
            Lernziel("Python", 4, 3),
            Lernziel("Mathematik", 8, 4),
            Lernziel("UML", 6, 5)
        ]

        # Exams
        self.pruefungen = []

        for i in range(8):
            self.pruefungen.append(
                Pruefung("Fach", "-", "Passed")
            )

        for i in range(3):
            self.pruefungen.append(
                Pruefung("Fach", "-", "Open")
            )

        self.pruefungen.append(
            Pruefung("Fach", "-", "Failed")
        )

        # Semester grades
        self.noten = [
            Note(2.7, 1),
            Note(2.5, 2),
            Note(2.2, 3)
        ]

        # Notes
        self.notizen = [
            Notiz("Review Python exercises"),
            Notiz("Prepare for the next exam")
        ]

        # Motivation
        self.quotes = MotivationQuote(
            "Every small step brings you closer to your goals."
        )

        # Load saved data before creating the interface
        self.data_file = os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            "dashboard_data.json"
        )
        self.load_data()

        # Save data when the window is closed
        self.root.protocol("WM_DELETE_WINDOW", self.close_app)

        # Create the interface
        self.create_scroll_area()
        self.create_dashboard()


    # ==============================
    # 3. Scroll Area
    # ==============================

    def create_scroll_area(self):

        self.canvas = tk.Canvas(
            self.root,
            bg=self.background,
            highlightthickness=0
        )

        self.scrollbar = tk.Scrollbar(
            self.root,
            orient="vertical",
            command=self.canvas.yview
        )

        self.canvas.configure(
            yscrollcommand=self.scrollbar.set
        )

        self.scrollbar.pack(
            side="right",
            fill="y"
        )

        self.canvas.pack(
            side="left",
            fill="both",
            expand=True
        )

        self.content = tk.Frame(
            self.canvas,
            bg=self.background
        )

        self.canvas_window = self.canvas.create_window(
            (0, 0),
            window=self.content,
            anchor="nw"
        )

        self.content.bind(
            "<Configure>",
            self.update_scroll_region
        )

        self.canvas.bind(
            "<Configure>",
            self.resize_content
        )

    def update_scroll_region(self, event):
        self.canvas.configure(
            scrollregion=self.canvas.bbox("all")
        )

    def resize_content(self, event):
        self.canvas.itemconfig(
            self.canvas_window,
            width=event.width
        )


    # ==============================
    # 4. Dashboard Layout
    # ==============================

    def create_dashboard(self):

        self.content.columnconfigure(0, weight=1)
        self.content.columnconfigure(1, weight=1)

        # Header
        header = tk.Frame(
            self.content,
            bg=self.background,
            padx=25,
            pady=20
        )

        header.grid(
            row=0,
            column=0,
            columnspan=2,
            sticky="ew"
        )

        title = tk.Label(
            header,
            text="My Study Dashboard",
            bg=self.background,
            fg=self.current_theme.primaryColor,
            font=("Georgia", 26, "bold")
        )

        title.pack(anchor="w")

        welcome = tk.Label(
            header,
            text="Welcome back! Every small step brings you closer to your goals.",
            bg=self.background,
            fg=self.text_color,
            font=("Arial", 11)
        )

        welcome.pack(anchor="w", pady=5)

        theme_row = tk.Frame(
            header,
            bg=self.background
        )

        theme_row.pack(anchor="w", pady=8)

        tk.Label(
            theme_row,
            text="Choose Theme:",
            bg=self.background,
            fg=self.text_color
        ).pack(side="left", padx=(0, 8))

        self.theme_var = tk.StringVar(
            value=self.current_theme.name
        )

        self.theme_menu = tk.OptionMenu(
            theme_row,
            self.theme_var,
            *self.themes.keys(),
            command=self.change_theme
        )

        self.theme_menu.pack(side="left")

        # Cards
        self.create_progress_card()
        self.create_goals_card()
        self.create_focus_card()
        self.create_exams_card()
        self.create_motivation_card()
        self.create_notes_card()


    # ==============================
    # 5. Card Design
    # ==============================

    def create_card(self, title, row, column, columnspan=1):

        card = tk.Frame(
            self.content,
            bg=self.card_color,
            padx=15,
            pady=12
        )

        card.grid(
            row=row,
            column=column,
            columnspan=columnspan,
            sticky="nsew",
            padx=10,
            pady=7
        )

        heading = tk.Label(
            card,
            text=title,
            bg=self.card_color,
            fg=self.current_theme.primaryColor,
            font=("Georgia", 15, "bold")
        )

        heading.pack(anchor="w", pady=(0, 10))

        return card


    # ==============================
    # 6. Study Progress
    # ==============================

    def create_progress_card(self):

        card = self.create_card(
            "Study Progress", 1, 0, 2
        )

        self.progress_text = tk.Label(
            card,
            text="18 of 36 modules completed",
            bg=self.card_color,
            fg=self.text_color,
            font=("Arial", 10)
        )

        self.progress_text.pack(anchor="w")

        self.progress_percentage = tk.Label(
            card,
            text="50% completed",
            bg=self.card_color,
            fg=self.current_theme.primaryColor,
            font=("Arial", 10, "bold")
        )

        self.progress_percentage.pack(
            anchor="w",
            pady=8
        )

        self.progress_canvas = tk.Canvas(
            card,
            height=55,
            bg=self.card_color,
            highlightthickness=0
        )

        self.progress_canvas.pack(
            fill="x",
            pady=5
        )

        self.progress_canvas.bind(
            "<Configure>",
            self.draw_progress
        )

    def draw_progress(self, event=None):

        canvas = self.progress_canvas
        canvas.delete("all")

        width = canvas.winfo_width()

        if width < 50:
            return

        start = 10
        end = width - 10
        progress = 0.5

        canvas.create_rectangle(
            start, 28, end, 40,
            fill="#E9EFE5",
            outline=""
        )

        position = start + (end - start) * progress

        canvas.create_rectangle(
            start, 28, position, 40,
            fill=self.current_theme.secondaryColor,
            outline=""
        )

        # Small walking student
        x = position
        y = 18

        canvas.create_oval(
            x - 6, y - 17,
            x + 6, y - 5,
            fill="#D8B69A",
            outline=""
        )

        canvas.create_line(
            x, y - 5,
            x, y + 12,
            fill=self.current_theme.primaryColor,
            width=3
        )

        canvas.create_line(
            x, y,
            x - 9, y + 7,
            fill=self.current_theme.primaryColor,
            width=2
        )

        canvas.create_line(
            x, y,
            x + 9, y + 5,
            fill=self.current_theme.primaryColor,
            width=2
        )

        canvas.create_line(
            x, y + 12,
            x - 8, y + 23,
            fill=self.current_theme.primaryColor,
            width=2
        )

        canvas.create_line(
            x, y + 12,
            x + 8, y + 23,
            fill=self.current_theme.primaryColor,
            width=2
        )


    # ==============================
    # 7. Weekly Learning Goals
    # ==============================

    def create_goals_card(self):

        card = self.create_card(
            "Weekly Learning Goals", 2, 0
        )

        self.goal_widgets = []

        for goal in self.lernziele:

            row = tk.Frame(
                card,
                bg=self.card_color
            )

            row.pack(
                fill="x",
                pady=5
            )

            name = tk.Label(
                row,
                text=goal.bezeichnung,
                width=12,
                anchor="w",
                bg=self.card_color,
                fg=self.text_color
            )

            name.pack(side="left")

            hours = tk.Label(
                row,
                bg=self.card_color,
                fg=self.text_color
            )

            hours.pack(side="left")

            progress = tk.Frame(
                card,
                bg="#E9EFE5",
                height=9
            )

            progress.pack(
                fill="x",
                pady=(0, 5)
            )

            fill = tk.Frame(
                progress,
                bg=self.current_theme.secondaryColor
            )

            fill.place(
                relx=0,
                rely=0,
                relheight=1,
                relwidth=goal.berechneFortschritt() / 100
            )

            button = tk.Button(
                row,
                text="+1 h",
                command=lambda g=goal: self.add_learning_hour(g),
                font=("Arial", 8)
            )

            button.pack(side="right")

            self.goal_widgets.append(
                (goal, hours, progress, fill)
            )

        self.refresh_goals()

    def refresh_goals(self):

        for goal, hours, progress, fill in self.goal_widgets:

            hours.config(
                text=f"{goal.erreichteZeit:g} / {goal.zielzeit:g} hours"
            )

            fill.place(
                relx=0,
                rely=0,
                relheight=1,
                relwidth=goal.berechneFortschritt() / 100
            )

        self.refresh_focus()

    def add_learning_hour(self, goal):

        goal.aktualisiereFortschritt(1)
        self.refresh_goals()
        self.save_data()


    # ==============================
    # 8. Lernfokus
    # ==============================

    def create_focus_card(self):

        self.focus_card = self.create_card(
            "Lernfokus", 2, 1
        )

        self.focus_labels = []

        for goal in self.lernziele:

            label = tk.Label(
                self.focus_card,
                bg=self.card_color,
                fg=self.text_color,
                font=("Arial", 10),
                anchor="w"
            )

            label.pack(
                fill="x",
                pady=5
            )

            self.focus_labels.append(label)

        self.refresh_focus()

    def refresh_focus(self):

        if not hasattr(self, "focus_labels"):
            return

        for index, goal in enumerate(self.lernziele):

            progress = goal.berechneFortschritt()

            if progress >= 100:
                status = "Goal reached"
            elif progress >= 75:
                status = "Almost reached the weekly goal"
            else:
                status = "Needs more focus"

            self.focus_labels[index].config(
                text=f"{goal.bezeichnung}: {status}"
            )


    # ==============================
    # 9. Exams and Grades
    # ==============================

    def create_exams_card(self):

        card = self.create_card(
            "Exams & Grades", 3, 0
        )

        passed = sum(
            1 for exam in self.pruefungen
            if exam.status == "Passed"
        )

        opened = sum(
            1 for exam in self.pruefungen
            if exam.status == "Open"
        )

        failed = sum(
            1 for exam in self.pruefungen
            if exam.status == "Failed"
        )

        exam_text = tk.Label(
            card,
            text=f"Passed: {passed}     Open: {opened}     Failed: {failed}",
            bg=self.card_color,
            fg=self.text_color,
            font=("Arial", 10)
        )

        exam_text.pack(anchor="w", pady=5)

        grades_title = tk.Label(
            card,
            text="Semester Grades",
            bg=self.card_color,
            fg=self.current_theme.primaryColor,
            font=("Arial", 11, "bold")
        )

        grades_title.pack(anchor="w", pady=(10, 5))

        grades_text = "     ".join(
            str(note.zeigeNote()) for note in self.noten
        )

        tk.Label(
            card,
            text=grades_text,
            bg=self.card_color,
            fg=self.text_color,
            font=("Arial", 11)
        ).pack(anchor="w")


    # ==============================
    # 10. Motivation
    # ==============================

    def create_motivation_card(self):

        card = self.create_card(
            "Motivation", 3, 1
        )

        tk.Label(
            card,
            text=self.quotes.zeigeQuote(),
            bg=self.card_color,
            fg=self.text_color,
            font=("Georgia", 11),
            wraplength=300,
            justify="left"
        ).pack(anchor="w", pady=8)


    # ==============================
    # 11. Personal Notes
    # ==============================

    def create_notes_card(self):

        card = self.create_card(
            "Meine Notizen", 4, 0, 2
        )

        self.note_entry = tk.Entry(
            card,
            font=("Arial", 10)
        )

        self.note_entry.pack(
            fill="x",
            pady=5
        )

        self.notes_list = tk.Listbox(
            card,
            height=4,
            font=("Arial", 10)
        )

        self.notes_list.pack(
            fill="x",
            pady=5
        )

        for note in self.notizen:
            self.notes_list.insert(
                tk.END,
                note.text
            )

        buttons = tk.Frame(
            card,
            bg=self.card_color
        )

        buttons.pack(anchor="w", pady=5)

        tk.Button(
            buttons,
            text="Add Note",
            command=self.add_note
        ).pack(side="left", padx=3)

        tk.Button(
            buttons,
            text="Edit Selected",
            command=self.edit_note
        ).pack(side="left", padx=3)

    def add_note(self):

        text = self.note_entry.get().strip()

        if text == "":
            messagebox.showwarning(
                "Empty Note",
                "Please write a note first."
            )
            return

        note = Notiz(text)
        self.notizen.append(note)

        self.notes_list.insert(
            tk.END,
            note.text
        )

        self.note_entry.delete(0, tk.END)
        self.save_data()

    def edit_note(self):

        selection = self.notes_list.curselection()

        if not selection:
            messagebox.showwarning(
                "No Selection",
                "Please select a note first."
            )
            return

        new_text = self.note_entry.get().strip()

        if new_text == "":
            messagebox.showwarning(
                "Empty Note",
                "Please enter the new text."
            )
            return

        index = selection[0]

        self.notizen[index].bearbeiteNotiz(new_text)

        self.notes_list.delete(index)
        self.notes_list.insert(
            index,
            new_text
        )

        self.note_entry.delete(0, tk.END)
        self.save_data()


    # ==============================
    # 12. Theme Selection
    # ==============================

    def change_theme(self, selected_theme):

        self.current_theme = self.themes[selected_theme]

        self.root.configure(
            bg=self.background
        )

        self.canvas.configure(
            bg=self.background
        )

        self.progress_percentage.config(
            fg=self.current_theme.primaryColor
        )

        self.draw_progress()

        for goal, hours, progress, fill in self.goal_widgets:
            fill.configure(
                bg=self.current_theme.secondaryColor
            )

        for label in self.focus_labels:
            label.config(
                fg=self.current_theme.primaryColor
            )

        self.save_data()


# ==============================
# 13. Start Application
# ==============================

if __name__ == "__main__":

    root = tk.Tk()

    app = StudyDashboardApp(root)

    root.mainloop()
