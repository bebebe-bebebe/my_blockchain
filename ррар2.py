import os
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from googleapiclient.discovery import build
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import pandas as pd

class YouTubeAnalyzerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("YouTube Channel Analyzer")
        self.root.geometry("1200x800")
        
        # Переменные
        self.api_key = tk.StringVar()
        self.channel_ids = []
        self.channel_stats = pd.DataFrame()
        self.video_stats = {}
        
        # Создаем интерфейс
        self.create_widgets()
        
    def create_widgets(self):
        # Панель управления
        control_frame = ttk.LabelFrame(self.root, text="Управление", padding=10)
        control_frame.pack(fill=tk.X, padx=5, pady=5)
        
        # Поле для API ключа
        ttk.Label(control_frame, text="API ключ:").grid(row=0, column=0, sticky=tk.W)
        api_entry = ttk.Entry(control_frame, textvariable=self.api_key, width=50)
        api_entry.grid(row=0, column=1, padx=5)
        
        # Поле для ID каналов
        ttk.Label(control_frame, text="ID каналов (через запятую):").grid(row=1, column=0, sticky=tk.W)
        self.channel_entry = ttk.Entry(control_frame, width=50)
        self.channel_entry.grid(row=1, column=1, padx=5)
        
        # Кнопки
        ttk.Button(control_frame, text="Загрузить данные", command=self.load_data).grid(row=0, column=2, padx=5)
        ttk.Button(control_frame, text="Сравнить каналы", command=self.plot_channel_comparison).grid(row=1, column=2, padx=5)
        ttk.Button(control_frame, text="Экспорт в CSV", command=self.export_to_csv).grid(row=0, column=3, padx=5)
        
        # Вкладки
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Вкладка с таблицей
        self.table_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.table_frame, text="Данные")
        
        # Вкладка с графиками
        self.plot_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.plot_frame, text="Графики")
        
        # Дерево для отображения данных
        self.tree = ttk.Treeview(self.table_frame)
        self.tree.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Полоса прокрутки
        scrollbar = ttk.Scrollbar(self.table_frame, orient="vertical", command=self.tree.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        # Область для графиков
        self.figure = plt.figure(figsize=(10, 6), dpi=100)
        self.canvas = FigureCanvasTkAgg(self.figure, master=self.plot_frame)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        # Статус бар
        self.status = tk.StringVar()
        self.status.set("Готов к работе")
        ttk.Label(self.root, textvariable=self.status, relief=tk.SUNKEN).pack(fill=tk.X, padx=5, pady=5)
    
    def load_data(self):
        api_key = self.api_key.get()
        if not api_key:
            messagebox.showerror("Ошибка", "Введите API ключ")
            return
            
        channel_ids = self.channel_entry.get().split(',')
        channel_ids = [cid.strip() for cid in channel_ids if cid.strip()]
        
        if not channel_ids:
            messagebox.showerror("Ошибка", "Введите ID каналов")
            return
            
        self.status.set("Загрузка данных...")
        self.root.update()
        
        try:
            youtube = build('youtube', 'v3', developerKey=api_key)
            all_data = []
            
            for channel_id in channel_ids:
                request = youtube.channels().list(
                    part="snippet,contentDetails,statistics",
                    id=channel_id
                )
                response = request.execute()
                
                if 'items' in response and len(response['items']) > 0:
                    channel = response['items'][0]
                    stats = {
                        'Channel': channel['snippet']['title'],
                        'Subscribers': int(channel['statistics']['subscriberCount']),
                        'Views': int(channel['statistics']['viewCount']),
                        'TotalVideos': int(channel['statistics']['videoCount']),
                        'PlaylistId': channel['contentDetails']['relatedPlaylists']['uploads']
                    }
                    all_data.append(stats)
                else:
                    messagebox.showwarning("Предупреждение", f"Нет данных для канала ID: {channel_id}")
            
            self.channel_stats = pd.DataFrame(all_data)
            self.display_data()
            self.status.set(f"Загружено {len(self.channel_stats)} каналов")
            
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось загрузить данные: {str(e)}")
            self.status.set("Ошибка загрузки")
    
    def display_data(self):
        # Очищаем дерево
        for i in self.tree.get_children():
            self.tree.delete(i)
        
        # Устанавливаем колонки
        self.tree["columns"] = list(self.channel_stats.columns)
        for col in self.channel_stats.columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=100)
        
        # Добавляем данные
        for _, row in self.channel_stats.iterrows():
            self.tree.insert("", tk.END, values=list(row))
    
    def plot_channel_comparison(self):
        if self.channel_stats.empty:
            messagebox.showwarning("Предупреждение", "Нет данных для отображения")
            return
            
        self.figure.clear()
        
        # Создаем 2x2 сетку графиков
        ax1 = self.figure.add_subplot(221)
        ax2 = self.figure.add_subplot(222)
        ax3 = self.figure.add_subplot(223)
        ax4 = self.figure.add_subplot(224)
        
        # График 1: Подписчики
        self.channel_stats.plot.bar(x='Channel', y='Subscribers', ax=ax1, color='red')
        ax1.set_title('Количество подписчиков')
        ax1.ticklabel_format(style='plain', axis='y')
        
        # График 2: Просмотры
        self.channel_stats.plot.bar(x='Channel', y='Views', ax=ax2, color='blue')
        ax2.set_title('Общее количество просмотров')
        ax2.ticklabel_format(style='plain', axis='y')
        
        # График 3: Видео
        self.channel_stats.plot.bar(x='Channel', y='TotalVideos', ax=ax3, color='green')
        ax3.set_title('Количество видео')
        
        # График 4: Соотношение
        self.channel_stats['SubsToViewRatio'] = self.channel_stats['Subscribers'] / self.channel_stats['Views']
        self.channel_stats.plot.bar(x='Channel', y='SubsToViewRatio', ax=ax4, color='purple')
        ax4.set_title('Соотношение подписчиков к просмотрам')
        
        self.figure.tight_layout()
        self.canvas.draw()
        self.status.set("Графики построены")
    
    def export_to_csv(self):
        if self.channel_stats.empty:
            messagebox.showwarning("Предупреждение", "Нет данных для экспорта")
            return
            
        file_path = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
        )
        
        if file_path:
            try:
                self.channel_stats.to_csv(file_path, index=False)
                self.status.set(f"Данные сохранены в {file_path}")
            except Exception as e:
                messagebox.showerror("Ошибка", f"Не удалось сохранить файл: {str(e)}")

if __name__ == "__main__":
    root = tk.Tk()
    app = YouTubeAnalyzerApp(root)
    root.mainloop()
