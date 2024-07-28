import tkinter as tk
from tkinter import ttk
import os

def setup_window():
    root = tk.Tk()
    root.title("Basic File Explorer")
    root.geometry("600x400")
    return root

def create_tree_view(root):
    tree_frame = ttk.Frame(root)
    tree_frame.pack(fill="both", expand=True)
    
    tree_scroll = ttk.Scrollbar(tree_frame)
    tree_scroll.pack(side="right", fill="y")
    
    file_tree = ttk.Treeview(tree_frame, yscrollcommand=tree_scroll.set)
    file_tree.pack(fill="both", expand=True)
    
    tree_scroll.config(command=file_tree.yview)
    
    file_tree.heading("#0", text="File Explorer", anchor="w")
    
    return file_tree

def populate_tree_view(parent, path):
    for item in os.listdir(path):
        item_path = os.path.join(path, item)
        if os.path.isdir(item_path):
            folder_id = parent.insert("", "end", text=item, values=[item_path], open=False)
            parent.insert(folder_id, "end")  # Dummy insert to create expand arrow
        else:
            parent.insert("", "end", text=item, values=[item_path])

def on_tree_expand(event):
    node = event.widget.focus()
    abs_path = event.widget.item(node)["values"][0]
    
    if not os.path.isdir(abs_path):
        return
    
    # Remove dummy node and populate children
    event.widget.delete(event.widget.get_children(node))
    populate_tree_view(event.widget, abs_path)

def create_info_label(root):
    info_label = tk.Label(root, text="", anchor="w")
    info_label.pack(fill="x")
    return info_label

def on_tree_select(event):
    selected_item = event.widget.focus()
    file_path = event.widget.item(selected_item)["values"][0]
    
    if os.path.isdir(file_path):
        info_text = f"Directory: {file_path}"
    else:
        info_text = f"File: {file_path}\nSize: {os.path.getsize(file_path)} bytes"
    
    event.widget.master.master.info_label.config(text=info_text)

def main():
    root = setup_window()
    file_tree = create_tree_view(root)
    info_label = create_info_label(root)
    
    root.info_label = info_label
    
    file_tree.bind("<<TreeviewOpen>>", on_tree_expand)
    file_tree.bind("<<TreeviewSelect>>", on_tree_select)
    
    populate_tree_view(file_tree, os.path.expanduser("~"))
    
    root.mainloop()

if __name__ == "__main__":
    main()
