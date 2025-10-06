import requests
import tkinter as tk
from tkinter import ttk, messagebox
import threading
from functools import partial

# -----------------------------
# 🗣️ แปลสภาพอากาศอังกฤษ → ไทย
# -----------------------------
def translate_weather(desc):
    mapping = {
        "Sunny": "แดดจัด",
        "Clear": "ท้องฟ้าแจ่มใส",
        "Partly cloudy": "มีเมฆบางส่วน",
        "Cloudy": "มีเมฆมาก",
        "Overcast": "ท้องฟ้าครึ้ม",
        "Mist": "หมอก",
        "Patchy rain nearby": "ฝนตกบริเวณใกล้เคียง",
        "Light rain": "ฝนตกเล็กน้อย",
        "Moderate rain": "ฝนปานกลาง",
        "Heavy rain": "ฝนตกหนัก",
        "Thunderstorm": "พายุฝนฟ้าคะนอง",
        "Fog": "หมอกหนา",
        "Snow": "หิมะตก"
    }
    for key in mapping:
        if key.lower() in desc.lower():
            return mapping[key]
    return desc  # ถ้าไม่พบ ให้คืนค่าเดิม

# -----------------------------
# 🔹 ดึงข้อมูลจาก wttr.in
# -----------------------------
def get_weather(city_name):
    url = f"https://wttr.in/{city_name}?format=j1"
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()

        current = data["current_condition"][0]
        forecast = data["weather"]

        weather_info = {
            "city": city_name.capitalize(),
            "temp": current["temp_C"],
            "humidity": current["humidity"],
            "desc": translate_weather(current["weatherDesc"][0]["value"]),
            "forecast": forecast
        }
        return weather_info

    except requests.exceptions.RequestException:
        messagebox.showerror("ข้อผิดพลาด", "ไม่สามารถเชื่อมต่อ API ได้")
        return None

# -----------------------------
# 🔹 ดึงรายชื่อเมือง (Auto Suggest)
# -----------------------------
def get_city_suggestions(query):
    if not query:
        return []
    try:
        url = f"https://geocoding-api.open-meteo.com/v1/search?name={query}&count=6&language=th"
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        data = response.json()
        if "results" not in data:
            return []
        return [r["name"] for r in data["results"]]
    except requests.exceptions.RequestException:
        return []

# -----------------------------
# 🔹 Suggestion System
# -----------------------------
search_after_id = None
suggestion_window = None
suggestion_listbox = None

def on_city_typing(event):
    global search_after_id
    query = city_entry.get().strip()
    if search_after_id:
        root.after_cancel(search_after_id)
    if not query:
        hide_suggestions()
        return
    # 🔸 delay เพื่อไม่ให้ spam API
    search_after_id = root.after(300, lambda: threading.Thread(target=fetch_suggestions, args=(query,)).start())

def fetch_suggestions(query):
    suggestions = get_city_suggestions(query)
    root.after(0, partial(show_suggestions, suggestions))

def show_suggestions(suggestions):
    global suggestion_window, suggestion_listbox

    hide_suggestions()
    if not suggestions:
        return

    # 🔹 คำนวณตำแหน่ง popup ให้อยู่ตรง text box
    x = root.winfo_rootx() + frame_input.winfo_x() + city_entry.winfo_x()
    y = root.winfo_rooty() + frame_input.winfo_y() + city_entry.winfo_y() + city_entry.winfo_height()
    width = city_entry.winfo_width()

    suggestion_window = tk.Toplevel(root)
    suggestion_window.wm_overrideredirect(True)
    suggestion_window.geometry(f"{width}x{min(150, len(suggestions)*25)}+{x}+{y}")
    suggestion_window.configure(bg="white")

    suggestion_listbox = tk.Listbox(
        suggestion_window,
        font=("Segoe UI", 10),
        activestyle="none",
        highlightthickness=0,
        relief="flat",
        selectbackground="#0078D7",
        selectforeground="white",
        borderwidth=1
    )
    suggestion_listbox.pack(fill="both", expand=True)

    for s in suggestions:
        suggestion_listbox.insert(tk.END, s)

    # 🖱️ คลิกเลือก suggestion
    suggestion_listbox.bind("<ButtonRelease-1>", lambda e: select_city_from_list())
    # ⌨️ ลูกศรและ Enter
    city_entry.bind("<Down>", move_selection_down)
    city_entry.bind("<Up>", move_selection_up)
    city_entry.bind("<Return>", on_enter_key)
    root.bind("<Button-1>", click_outside)

def hide_suggestions():
    global suggestion_window
    if suggestion_window:
        suggestion_window.destroy()
        suggestion_window = None

def move_selection_down(event):
    if suggestion_listbox and suggestion_listbox.size() > 0:
        cur = suggestion_listbox.curselection()
        next_index = 0 if not cur else (cur[0] + 1) % suggestion_listbox.size()
        suggestion_listbox.selection_clear(0, tk.END)
        suggestion_listbox.selection_set(next_index)
        suggestion_listbox.activate(next_index)

def move_selection_up(event):
    if suggestion_listbox and suggestion_listbox.size() > 0:
        cur = suggestion_listbox.curselection()
        prev_index = suggestion_listbox.size() - 1 if not cur else (cur[0] - 1) % suggestion_listbox.size()
        suggestion_listbox.selection_clear(0, tk.END)
        suggestion_listbox.selection_set(prev_index)
        suggestion_listbox.activate(prev_index)

def on_enter_key(event):
    if suggestion_window:
        cur = suggestion_listbox.curselection()
        if not cur:
            suggestion_listbox.selection_set(0)
        select_city_from_list()
    else:
        show_weather()

def select_city_from_list():
    if suggestion_window and suggestion_listbox:
        selected = suggestion_listbox.get(tk.ACTIVE)
        city_entry.delete(0, tk.END)
        city_entry.insert(0, selected)
        hide_suggestions()
        show_weather()

def click_outside(event):
    if suggestion_window:
        if not (suggestion_window.winfo_containing(event.x_root, event.y_root)
                or city_entry == root.winfo_containing(event.x_root, event.y_root)):
            hide_suggestions()

# -----------------------------
# 🔹 แสดงข้อมูลสภาพอากาศ
# -----------------------------
def show_weather():
    city = city_entry.get().strip()
    if not city:
        messagebox.showwarning("แจ้งเตือน", "กรุณากรอกชื่อเมือง")
        return

    hide_suggestions()
    weather = get_weather(city)
    if weather:
        result_text.set(
            f"📍 เมือง: {weather['city']}\n"
            f"🌡️ อุณหภูมิ: {weather['temp']} °C\n"
            f"💧 ความชื้น: {weather['humidity']}%\n"
            f"☁️ สภาพอากาศ: {weather['desc']}"
        )
        show_forecast_table(weather["forecast"])

def show_forecast_table(forecast_data):
    for row in forecast_tree.get_children():
        forecast_tree.delete(row)

    for day in forecast_data[:3]:
        date = day["date"]
        maxtemp = day["maxtempC"]
        mintemp = day["mintempC"]
        desc = translate_weather(day["hourly"][4]["weatherDesc"][0]["value"])
        forecast_tree.insert("", "end", values=(date, maxtemp, mintemp, desc))

# -----------------------------
# 🌈 UI Layout
# -----------------------------
root = tk.Tk()
root.title("🌦️ Weather Dashboard")
root.geometry("520x540")
root.resizable(False, False)
root.configure(bg="#EAF4FC")

# Header
header_label = ttk.Label(root, text="Weather Dashboard", font=("Segoe UI", 16, "bold"))
header_label.pack(pady=10)

# Input
frame_input = ttk.Frame(root)
frame_input.pack(pady=10)
ttk.Label(frame_input, text="ชื่อเมือง:").grid(row=0, column=0, padx=5)
city_entry = ttk.Entry(frame_input, width=28, font=("Segoe UI", 10))
city_entry.grid(row=0, column=1)
city_entry.bind("<KeyRelease>", on_city_typing)
search_btn = ttk.Button(frame_input, text="ค้นหา", command=show_weather)
search_btn.grid(row=0, column=2, padx=5)

# Result
result_text = tk.StringVar()
result_label = ttk.Label(root, textvariable=result_text, font=("Segoe UI", 11),
                         background="#EAF4FC", justify="left")
result_label.pack(pady=10)

# Forecast Table
columns = ("วันที่", "สูงสุด (°C)", "ต่ำสุด (°C)", "สภาพอากาศ")
forecast_tree = ttk.Treeview(root, columns=columns, show="headings", height=6)
for col in columns:
    forecast_tree.heading(col, text=col)
    forecast_tree.column(col, width=110, anchor="center")
forecast_tree.pack(pady=10)

root.mainloop()
