import tkinter as tk
from tkinter import ttk, messagebox

class MapApplication:
    def __init__(self, root):
        self.root = root
        self.root.title("Ứng dụng Bản đồ Hà Nội")
        self.root.geometry("800x600")
        
        # Biến để lưu trữ danh sách đường cấm
        self.prohibited_roads = []
        
        # Tạo giao diện
        self.create_widgets()
    
    def create_widgets(self):
        # Frame chính
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Frame cho phần tìm kiếm và điều khiển
        control_frame = ttk.LabelFrame(main_frame, text="Điều khiển")
        control_frame.pack(side=tk.TOP, fill=tk.X, padx=5, pady=5)
        
        # Frame cho phần bản đồ
        self.map_frame = ttk.LabelFrame(main_frame, text="Bản đồ")
        self.map_frame.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Canvas để hiển thị bản đồ
        self.map_canvas = tk.Canvas(self.map_frame, bg="lightgray")
        self.map_canvas.pack(fill=tk.BOTH, expand=True)
        self.map_canvas.create_text(400, 300, text="Bản đồ sẽ được hiển thị ở đây", font=("Arial", 14))
        
        # Nhãn và ô nhập cho khu vực
        area_label = ttk.Label(control_frame, text="Khu vực:")
        area_label.grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
        
        self.area_entry = ttk.Entry(control_frame, width=30)
        self.area_entry.grid(row=0, column=1, padx=5, pady=5)
        self.area_entry.insert(0, "Ba Đình, Hà Nội, Việt Nam")
        
        area_button = ttk.Button(control_frame, text="Tải bản đồ", command=self.load_map)
        area_button.grid(row=0, column=2, padx=5, pady=5)
        
        # Nhãn và ô nhập cho điểm bắt đầu
        start_label = ttk.Label(control_frame, text="Điểm bắt đầu:")
        start_label.grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)
        
        self.start_entry = ttk.Entry(control_frame, width=30)
        self.start_entry.grid(row=1, column=1, padx=5, pady=5)
        
        # Nhãn và ô nhập cho điểm kết thúc
        end_label = ttk.Label(control_frame, text="Điểm đến:")
        end_label.grid(row=2, column=0, padx=5, pady=5, sticky=tk.W)
        
        self.end_entry = ttk.Entry(control_frame, width=30)
        self.end_entry.grid(row=2, column=1, padx=5, pady=5)
        
        # Nút tìm đường
        route_button = ttk.Button(control_frame, text="Tìm đường", command=self.find_route)
        route_button.grid(row=2, column=2, padx=5, pady=5)
        
        # Nút thêm đường cấm
        prohibited_label = ttk.Label(control_frame, text="Tên đường cấm:")
        prohibited_label.grid(row=3, column=0, padx=5, pady=5, sticky=tk.W)
        
        self.prohibited_entry = ttk.Entry(control_frame, width=30)
        self.prohibited_entry.grid(row=3, column=1, padx=5, pady=5)
        
        add_prohibited_button = ttk.Button(control_frame, text="Thêm đường cấm", 
                                          command=self.add_prohibited_road)
        add_prohibited_button.grid(row=3, column=2, padx=5, pady=5)
        
        # Danh sách đường cấm
        prohibited_list_label = ttk.Label(control_frame, text="Danh sách đường cấm:")
        prohibited_list_label.grid(row=4, column=0, padx=5, pady=5, sticky=tk.W)
        
        self.prohibited_listbox = tk.Listbox(control_frame, width=30, height=3)
        self.prohibited_listbox.grid(row=4, column=1, padx=5, pady=5)
        
        remove_prohibited_button = ttk.Button(control_frame, text="Xóa đường cấm", 
                                             command=self.remove_prohibited_road)
        remove_prohibited_button.grid(row=4, column=2, padx=5, pady=5)
        
        # Nút để xóa tất cả
        clear_button = ttk.Button(control_frame, text="Xóa tất cả", command=self.clear_all)
        clear_button.grid(row=5, column=1, padx=5, pady=5)
        
        # Trạng thái
        self.status_var = tk.StringVar()
        self.status_var.set("Sẵn sàng")
        status_label = ttk.Label(control_frame, textvariable=self.status_var, 
                                font=("Arial", 10, "italic"))
        status_label.grid(row=6, column=0, columnspan=3, padx=5, pady=5)
    
    def load_map(self):
        area = self.area_entry.get()
        if area:
            # Tạm thời chỉ hiển thị thông báo, chúng ta sẽ triển khai chức năng này sau
            self.status_var.set(f"Đang tải bản đồ cho khu vực: {area}...")
            messagebox.showinfo("Thông báo", f"Đang tải bản đồ cho khu vực: {area}")
    
    def find_route(self):
        start_point = self.start_entry.get()
        end_point = self.end_entry.get()
        
        if not start_point or not end_point:
            messagebox.showwarning("Cảnh báo", "Vui lòng nhập điểm bắt đầu và điểm đến!")
            return
        
        # Tạm thời chỉ hiển thị thông báo
        self.status_var.set("Đang tìm đường...")
        messagebox.showinfo("Thông báo", f"Tìm đường từ {start_point} đến {end_point}")
    
    def add_prohibited_road(self):
        road_name = self.prohibited_entry.get()
        if road_name and road_name not in self.prohibited_roads:
            self.prohibited_roads.append(road_name)
            self.prohibited_listbox.insert(tk.END, road_name)
            self.prohibited_entry.delete(0, tk.END)
            self.status_var.set(f"Đã thêm đường cấm: {road_name}")
        elif road_name in self.prohibited_roads:
            messagebox.showinfo("Thông báo", "Đường này đã có trong danh sách cấm!")
    
    def remove_prohibited_road(self):
        selection = self.prohibited_listbox.curselection()
        if selection:
            index = selection[0]
            road_name = self.prohibited_listbox.get(index)
            self.prohibited_roads.remove(road_name)
            self.prohibited_listbox.delete(index)
            self.status_var.set(f"Đã xóa đường cấm: {road_name}")
    
    def clear_all(self):
        self.start_entry.delete(0, tk.END)
        self.end_entry.delete(0, tk.END)
        self.prohibited_entry.delete(0, tk.END)
        self.prohibited_listbox.delete(0, tk.END)
        self.prohibited_roads = []
        self.status_var.set("Đã xóa tất cả")

def main():
    root = tk.Tk()
    app = MapApplication(root)
    root.mainloop()

if __name__ == "__main__":
    main()