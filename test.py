import tkinter as tk
from tkinter import ttk


def create_table(root):
    tree = ttk.Treeview(root, columns=("Name", "Age", "City"), show="headings", height=5)

    tree.heading("Name", text="Name")
    tree.heading("Age", text="Age")
    tree.heading("City", text="City")

    tree.column("Name", width=100)
    tree.column("Age", width=50)
    tree.column("City", width=100)

    # Inserting sample data
    data = [("John Doe", 30, "New York"),
            ("Jane Smith", 25, "San Francisco"),
            ("Bob Johnson", 40, "Chicago")]

    for row in data:
        tree.insert("", "end", values=row)

    # Increase the font size for the Treeview
    font = ("Arial", 12)  # You can adjust the font family and size
    tree.tag_configure("tree_font", font=font)

    for column in tree["columns"]:
        tree.heading(column, anchor=tk.CENTER, text=column, image="",
                     command=lambda col=column: sort_treeview(tree, col))
        tree.column(column, anchor=tk.CENTER, width=tkFont.Font().measure(column), stretch=tk.NO)

    tree.tag_configure("tree_font", font=font)

    tree.pack(pady=10, padx=10)


def sort_treeview(tree, col):
    items = [(tree.set(k, col), k) for k in tree.get_children("")]
    items.sort()
    for index, (val, k) in enumerate(items):
        tree.move(k, "", index)


if __name__ == "__main__":
    root = tk.Tk()
    root.title("Table with Increased Text Size")
    root.configure(bg="black")

    create_table(root)

    root.mainloop()
