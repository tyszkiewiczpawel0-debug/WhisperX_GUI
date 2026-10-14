"""Tk runs only on the main thread; engine output arrives through a queue."""
import os
import queue
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from tkinter.scrolledtext import ScrolledText

from configuration import load, profile
from controller import Controller

STAGES = {'starting': 'Uruchamianie', 'probe': 'Rozpoznawanie pliku', 'preflight': 'Kontrola zasobów offline',
          'prepare': 'Przygotowanie WAV', 'asr_loading': 'Ładowanie ASR i VAD', 'asr': 'Transkrypcja',
          'alignment_loading': 'Ładowanie alignmentu', 'alignment': 'Alignment', 'export': 'Eksport'}
STATES = {'succeeded': 'Gotowe — komplet wyników', 'prepared': 'WAV przygotowany',
          'inspected': 'Rozpoznano plik', 'failed': 'Błąd', 'cancelled': 'Anulowano'}


class App:
    def __init__(self, root, config):
        self.root, self.config = root, config
        self.controller = Controller(config)
        self.profile = profile()
        self.closing = False
        root.title('WhisperX — lokalna transkrypcja')
        root.geometry('940x720')
        root.minsize(760, 580)
        frame = ttk.Frame(root, padding=14)
        frame.pack(fill='both', expand=True)
        frame.columnconfigure(1, weight=1)
        frame.rowconfigure(8, weight=1)
        ttk.Label(frame, text=self.profile['name'], font=('Segoe UI', 15, 'bold')).grid(row=0, column=0, columnspan=3, sticky='w', pady=(0, 14))
        self.source = tk.StringVar()
        self.controls = []
        ttk.Label(frame, text='Nagranie').grid(row=1, column=0, sticky='w')
        entry = ttk.Entry(frame, textvariable=self.source)
        entry.grid(row=1, column=1, sticky='ew', padx=8)
        self.controls.append((entry, 'normal'))
        self.button(frame, 'Wybierz plik…', self.choose).grid(row=1, column=2)
        params = ttk.Frame(frame)
        params.grid(row=2, column=0, columnspan=3, sticky='ew', pady=12)
        self.values = {}
        for col, (key, label, choices) in enumerate([
            ('model', 'Model', ('large-v3',)), ('language', 'Język', ('pl',)),
            ('device', 'Urządzenie', ('cuda', 'cpu')), ('compute_type', 'Obliczenia', ('float16', 'float32', 'int8')),
            ('batch_size', 'Batch', ('1', '2', '4', '8', '16', '32', '64'))]):
            self.values[key] = tk.StringVar(value=str(self.profile[key]))
            ttk.Label(params, text=label).grid(row=0, column=col, sticky='w')
            box = ttk.Combobox(params, textvariable=self.values[key], values=choices, state='readonly', width=15)
            box.grid(row=1, column=col, padx=(0, 10))
            self.controls.append((box, 'readonly'))
        self.alignment = tk.BooleanVar(value=self.profile['alignment'])
        check = ttk.Checkbutton(frame, text='Alignment (dokładniejsze znaczniki czasu)', variable=self.alignment)
        check.grid(row=3, column=0, columnspan=3, sticky='w')
        self.controls.append((check, 'normal'))
        ttk.Label(frame, text='Tryb offline • jedno nagranie • diarizacja wyłączona • pośrednie WAV są zachowywane').grid(row=4, column=0, columnspan=3, sticky='w', pady=6)
        buttons = ttk.Frame(frame)
        buttons.grid(row=5, column=0, columnspan=3, sticky='w', pady=8)
        for text, mode in [('Sprawdź plik', 'inspect'), ('Przygotuj WAV', 'prepare'), ('Transkrybuj', 'transcribe')]:
            self.button(buttons, text, lambda m=mode: self.start(m)).pack(side='left', padx=(0, 8))
        self.cancel_button = ttk.Button(buttons, text='Przerwij', command=self.cancel, state='disabled')
        self.cancel_button.pack(side='left', padx=8)
        ttk.Button(buttons, text='Otwórz wyniki', command=self.open_results).pack(side='left')
        self.status = tk.StringVar(value='Wybierz nagranie. Każda operacja tworzy osobny katalog zadania.')
        ttk.Label(frame, textvariable=self.status).grid(row=6, column=0, columnspan=3, sticky='w', pady=6)
        self.metadata = tk.StringVar(value='Metadane pojawią się po sprawdzeniu pliku.')
        ttk.Label(frame, textvariable=self.metadata, wraplength=880).grid(row=7, column=0, columnspan=3, sticky='w', pady=6)
        self.log = ScrolledText(frame, height=18, wrap='word', state='disabled')
        self.log.grid(row=8, column=0, columnspan=3, sticky='nsew')
        root.protocol('WM_DELETE_WINDOW', self.close)
        root.after(100, self.poll)

    def button(self, parent, label, callback):
        btn = ttk.Button(parent, text=label, command=callback)
        self.controls.append((btn, 'normal'))
        return btn

    def choose(self):
        path = filedialog.askopenfilename(initialdir=self.config['paths']['input_dir'], title='Wybierz audio lub wideo')
        if path:
            self.source.set(path)
            self.metadata.set('Wybrano nowy plik — kliknij Sprawdź plik.')

    def start(self, mode):
        try:
            p = dict(self.profile)
            p.update({k: v.get() for k, v in self.values.items()})
            p['batch_size'] = int(p['batch_size'])
            p['alignment'] = self.alignment.get()
            run = self.controller.start(self.source.get(), p, mode)
            for control, _ in self.controls:
                control.configure(state='disabled')
            self.cancel_button.configure(state='normal')
            self.status.set('Uruchamianie…')
            self.append(f'\nKatalog zadania: {run}\n')
        except Exception as exc:
            messagebox.showerror('Nie można rozpocząć', str(exc))

    def cancel(self):
        try:
            self.controller.cancel()
            self.status.set('Anulowanie — oczekiwanie na zakończenie procesów…')
        except Exception as exc:
            messagebox.showerror('Błąd anulowania', str(exc))

    def append(self, text):
        self.log.configure(state='normal')
        self.log.insert('end', text)
        if int(self.log.index('end-1c').split('.')[0]) > 3000:
            self.log.delete('1.0', '1000.0')
        self.log.see('end')
        self.log.configure(state='disabled')

    def poll(self):
        # Bound each UI tick so verbose engine output cannot starve Tk.
        for _ in range(100):
            try:
                kind, value = self.controller.events.get_nowait()
            except queue.Empty:
                break
            if kind == 'log':
                self.append(value)
            elif kind == 'stage':
                self.status.set(STAGES.get(value, value))
            elif kind in ('done', 'fatal'):
                for control, state in self.controls:
                    control.configure(state=state)
                self.cancel_button.configure(state='disabled')
                if kind == 'fatal':
                    self.status.set('Błąd zapisu stanu')
                    self.append(value + '\n')
                    continue
                self.status.set(STATES.get(value['status'], value['status']))
                m = value.get('source', {}).get('metadata')
                if m:
                    self.metadata.set(f"Format: {m['format']} | kodek: {m['codec']} | czas: {m['duration']} s | {m['sample_rate']} Hz | kanały: {m['channels']}")
                for warning in value['warnings']:
                    self.append('OSTRZEŻENIE: ' + warning + '\n')
                if value.get('error'):
                    self.append(value['error'] + '\n')
                    if not self.closing:
                        messagebox.showerror('Zadanie nie zostało ukończone', value['error'])
        if self.closing and not self.controller.active:
            self.root.destroy()
            return
        self.root.after(100, self.poll)

    def open_results(self):
        if self.controller.run:
            os.startfile(self.controller.run)

    def close(self):
        self.closing = True
        if self.controller.active:
            self.cancel()
        else:
            self.root.destroy()


def main():
    root = tk.Tk()
    try:
        App(root, load())
    except Exception as exc:
        root.withdraw()
        messagebox.showerror('Konfiguracja WhisperX', f'{exc}\n\nUzupełnij config/local.toml według README.')
        root.destroy()
        return
    root.mainloop()


if __name__ == '__main__':
    main()
