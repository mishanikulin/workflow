import tkinter as tk
from tkinter import messagebox
from tkinter import simpledialog
from tkinter import ttk
from datetime import datetime

class Task:
    def __init__(self, name, description):
        self.name = name
        self.description = description

class Employee:
    def __init__(self, name, password):
        self.name = name
        self.password = password
        self.tasks = []
        self.work_time = {}

    def add_task(self, task):
        self.tasks.append(task)

    def view_tasks(self):
        task_list = ""
        for task in self.tasks:
            task_list += f"Название задачи: {task.name}\nОписание: {task.description}\n\n"
        messagebox.showinfo("Список задач", task_list)

    def register_work_time(self, task, work_time):
        if task in self.work_time:
            self.work_time[task] += work_time
        else:
            self.work_time[task] = work_time

class AuthWindow(tk.Toplevel):
    def __init__(self, app):
        super().__init__(app)

        self.app = app

        self.title("Авторизация")
        self.geometry("300x200")

        self.label_name = tk.Label(self, text="Введите ваше имя:")
        self.label_name.pack(pady=5)

        self.entry_name = tk.Entry(self)
        self.entry_name.pack(pady=5)

        self.label_password = tk.Label(self, text="Введите пароль:")
        self.label_password.pack(pady=5)

        self.entry_password = tk.Entry(self, show="*")  # Показывать символы пароля как "*"
        self.entry_password.pack(pady=5)

        self.login_button = tk.Button(self, text="Войти", command=self.login)
        self.login_button.pack(pady=10)

    def login(self):
        name = self.entry_name.get()
        password = self.entry_password.get()

        if name in self.app.users and self.app.users[name].password == password:
            self.app.employee = self.app.users[name]
            self.destroy()
        else:
            messagebox.showwarning("Ошибка", "Неверное имя пользователя или пароль!")

class Application(tk.Tk):
    def __init__(self):
        super().__init__()
        self.users = {
            'user1': Employee('user1', 'password1'),
            'user2': Employee('user2', 'password2'),
        }
        self.auth_window = AuthWindow(self)
        self.wait_window(self.auth_window)
        if hasattr(self, 'employee') and self.employee:
            self.title("workflow")
            self.geometry("700x400")
            self.create_widgets()
        self.work_schedule_data = None  # Новая переменная для хранения данных о рабочем времени

    def update_work_schedule_data(self, full_name, start_time, end_time):
        # Функция для обновления данных о рабочем времени
        self.work_schedule_data = f"{full_name} отработал с {start_time} до {end_time}"

    def work_schedule(self):
        full_name = simpledialog.askstring("Рабочее расписание", "Введите имя, фамилию и отчество:")
        start_time = simpledialog.askstring("Рабочее расписание", "Введите дату и время начала работы:")
        end_time = simpledialog.askstring("Рабочее расписание", "Введите дату и время окончания работы:")

        # Обновляем данные о рабочем времени
        self.update_work_schedule_data(full_name, start_time, end_time)

        # Создаем кнопку для просмотра данных о рабочем времени
        self.view_button("Просмотреть рабочее время", self.view_work_schedule_data, y_position=220)

    def view_work_schedule_data(self):
        # Функция для отображения данных о рабочем времени в отдельном окне
        if self.work_schedule_data:
            messagebox.showinfo("Рабочее время", self.work_schedule_data)
        else:
            messagebox.showinfo("Рабочее время", "Данные о рабочем времени отсутствуют.")

    def open_personal_cabinet(self):
        user_info = f"Имя пользователя: {self.employee.name}\n"
        if self.employee.tasks:
            tasks_info = "Список задач:\n"
            for task in self.employee.tasks:
                tasks_info += f"  - {task.name}\n"
        else:
            tasks_info = "Нет активных задач.\n"
        current_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        message = f"{user_info}{tasks_info}\nПоследний вход: недавно\nТекущая дата и время: {current_datetime}\nКонтактная информация: отсутствует"
        messagebox.showinfo("Личный кабинет", message)

    def view_button(self, button_text, command_function, y_position):
        button = tk.Button(self, text=button_text, command=command_function, font=("Arial", 12, "bold"),
                           bg="#f2f2f2", fg="#000", bd=1, highlightbackground="black", highlightthickness=1)
        button.place(x=10, y=y_position)
        view_button = tk.Button(self, text="Просмотреть", command=lambda bt=button_text: self.view_item(bt),
                                font=("Arial", 10, "bold"), bg="#f2f2f2", fg="#000", bd=1,
                                highlightbackground="black", highlightthickness=1)
        view_button.place(x=150, y=y_position)

    def view_item(self, item_name):
        item_name = item_name.strip()
        if item_name == "Электронная почта и календарь":
            email_data = simpledialog.askstring("Электронная почта", "Введите адрес электронной почты:")
            event_name = simpledialog.askstring("Календарь", "Введите название события:")
            event_date = simpledialog.askstring("Календарь", "Введите дату события (формат: ДД.ММ.ГГГГ):")
            messagebox.showinfo("Просмотр", f"Email: {email_data}\nСобытие: {event_name}\nДата события: {event_date}")
        elif item_name == "Учет закупок и расходов":
            expense_type = simpledialog.askstring("Учет расходов",
                                                  "Введите тип расхода (например, офисные расходы, бизнес-поездки и т.д.):")
            amount = simpledialog.askfloat("Учет расходов", "Введите сумму расхода:")
            messagebox.showinfo("Просмотр", f"Тип расхода: {expense_type}\nСумма расхода: {amount}")

    def create_widgets(self):
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill="both", expand=True)
        personal_cabinet_frame = tk.Frame(self.notebook)
        self.notebook.add(personal_cabinet_frame, text="Личный кабинет")
        self.background_image = tk.PhotoImage(file=r"C:\Users\79115\PycharmProjects\num3\123.png")
        self.background_label = tk.Label(self, image=self.background_image)
        self.background_label.place(x=0, y=0, relwidth=1, relheight=1)
        self.work_schedule_button = tk.Button(self, text="Регистрация рабочего времени", command=self.work_schedule,
                                              font=("Arial", 12, "bold"), bg="#f2f2f2", fg="#000", bd=1,
                                              highlightbackground="black", highlightthickness=1)
        self.work_schedule_button.place(x=10, y=140)
        self.add_task_button = tk.Button(self, text="Добавить задачу", command=self.add_task,
                                         font=("Arial", 12, "bold"), bg="#f2f2f2", fg="#000", bd=1,
                                         highlightbackground="black", highlightthickness=1)
        self.add_task_button.place(x=10, y=180)
        self.leave_request_button = tk.Button(self, text="Подать заявку на отпуск", command=self.leave_request,
                                              font=("Arial", 12, "bold"), bg="#f2f2f2", fg="#000", bd=1,
                                              highlightbackground="black", highlightthickness=1)
        self.leave_request_button.place(x=10, y=220)
        self.email_calendar_button = tk.Button(self, text="События и календарь", command=self.email_calendar,
                                               font=("Arial", 12, "bold"), bg="#f2f2f2", fg="#000", bd=1,
                                               highlightbackground="black", highlightthickness=1)
        self.email_calendar_button.place(x=10, y=260)
        personal_cabinet_button = tk.Button(self, text="Личный кабинет", command=self.open_personal_cabinet,
                                            font=("Arial", 12, "bold"), bg="#f2f2f2", fg="#000",
                                            bd=1, highlightbackground="black", highlightthickness=1)
        personal_cabinet_button.place(relx=1, x=-10, y=5, anchor="ne")
        label = tk.Label(self, text="Приветствую, " + self.employee.name, font=("Arial", 14, "bold"), bg="#f2f2f2",
                         fg="#000", bd=1, highlightbackground="black",
                         highlightthickness=1)
        label.place(x=250, y=5)
        self.purchase_button = tk.Button(self, text="Учет закупок и расходов", command=self.track_purchases_expenses,
                                         font=("Arial", 12, "bold"), bg="#f2f2f2", fg="#000", bd=1,
                                         highlightbackground="black", highlightthickness=1)
        self.purchase_button.place(x=10, y=300)
        developer_button = tk.Button(self, text="О приложении", command=self.show_developer_info,
                                     font=("Arial", 8, "bold"), bg="#f2f2f2", fg="#000", bd=1,
                                     highlightbackground="black", highlightthickness=1)
        developer_button.place(relx=1, x=-10, rely=1, y=-10, anchor="se")

    def show_developer_info(self):
        # Функция для отображения информации о разработчике
        developer_info = "О приложении:\nНикулин Михаил Андреевич\nКонтактная информация: Номер телефона +79953051687\nПочта: m-nikulin00@mail.ru"
        messagebox.showinfo("Разработчик приложения", developer_info)
        self.mainloop()

    def email_calendar(self):
        email_address = simpledialog.askstring("События в календаре", "Введите событие:")
        event_date = simpledialog.askstring("Календарь", "Введите дату события (формат: ДД.ММ.ГГГГ):")

        # Обновляем данные об электронной почте и календаре
        self.update_email_calendar_data(email_address, event_date)

        # Создаем кнопку для просмотра данных об электронной почте и календаре
        if hasattr(self, 'view_email_calendar_button'):
            self.view_email_calendar_button.destroy()

        self.view_email_calendar_button = tk.Button(self, text="Просмотреть почту и календарь", command=self.view_email_calendar_data,
                                                    font=("Arial", 12, "bold"), bg="#f2f2f2", fg="#000", bd=1,
                                                    highlightbackground="black", highlightthickness=1)
        self.view_email_calendar_button.place(x=400, y=260)

    def update_email_calendar_data(self, email_address, calendar_events):
        # Функция для обновления данных об электронной почте и календаре
        self.email_calendar_data = f"Событие: {email_address}\nДата: {calendar_events}"

    def view_email_calendar_data(self):
        # Функция для отображения данных об электронной почте и календаре в отдельном окне
        if self.email_calendar_data:
            messagebox.showinfo("События в календаре", self.email_calendar_data)
        else:
            messagebox.showinfo("События в календаре", "Данные об электронной почте и календаре отсутствуют.")

    def track_purchases_expenses(self):
        purchase_details = simpledialog.askstring("Учет закупок и расходов",
                                                  "Введите информацию о покупках и расходах:")

        # Обновляем данные о закупках и расходах
        self.update_purchase_expense_data(purchase_details)

        # Создаем кнопку для просмотра данных о закупках и расходах
        if hasattr(self, 'view_purchase_expense_button'):
            self.view_purchase_expense_button.destroy()

        self.view_purchase_expense_button = tk.Button(self, text="Просмотреть закупки и расходы",
                                                      command=self.view_purchase_expense_data,
                                                      font=("Arial", 12, "bold"), bg="#f2f2f2", fg="#000", bd=1,
                                                      highlightbackground="black", highlightthickness=1)
        self.view_purchase_expense_button.place(x=400, y=300)

    def update_purchase_expense_data(self, purchase_details):
        # Функция для обновления данных о закупках и расходах
        self.purchase_expense_data = f"Информация о закупках и расходах: {purchase_details}"

    def view_purchase_expense_data(self):
        # Функция для отображения данных о закупках и расходах в отдельном окне
        if self.purchase_expense_data:
            messagebox.showinfo("Учет закупок и расходов", self.purchase_expense_data)
        else:
            messagebox.showinfo("Учет закупок и расходов", "Информация о закупках и расходах отсутствует.")

    def leave_request(self):
        leave_type = simpledialog.askstring("Заявка на отпуск", "Введите тип отпуска (оплачиваемый/неоплачиваемый):")
        leave_duration = simpledialog.askstring("Заявка на отпуск", "Введите продолжительность отпуска:")

        # Обновляем данные о заявке на отпуск
        self.update_leave_request_data(leave_type, leave_duration)

        # Создаем кнопку для просмотра данных о заявке на отпуск
        if hasattr(self, 'view_leave_request_button'):
            self.view_leave_request_button.destroy()

        self.view_leave_request_button = tk.Button(self, text="Просмотреть заявку на отпуск", command=self.view_leave_request_data,
                                                   font=("Arial", 12, "bold"), bg="#f2f2f2", fg="#000", bd=1,
                                                   highlightbackground="black", highlightthickness=1)
        self.view_leave_request_button.place(x=400, y=220)

    def update_leave_request_data(self, leave_type, leave_duration):
        # Функция для обновления данных о заявке на отпуск
        self.leave_request_data = f"Тип отпуска: {leave_type}\nПродолжительность отпуска: {leave_duration}"

    def view_leave_request_data(self):
        # Функция для отображения данных о заявке на отпуск в отдельном окне
        if self.leave_request_data:
            messagebox.showinfo("Заявка на отпуск", self.leave_request_data)
        else:
            messagebox.showinfo("Заявка на отпуск", "Данные о заявке на отпуск отсутствуют.")

    def view_leave_status(self):
        leave_status = "Статус вашей заявки: утверждена"
        messagebox.showinfo("Статус отпуска", leave_status)

    def task_management(self):
        task_name = simpledialog.askstring("Управление задачами", "Введите название задачи:")
        task_description = simpledialog.askstring("Управление задачами", "Введите описание задачи:")

    def view_tasks(self):
        task_list = "Задача 1: Закончить отчет\nЗадача 2: Подготовить презентацию"
        messagebox.showinfo("Список задач", task_list)

    def add_task(self):
        task_name = simpledialog.askstring("Добавление задачи", "Введите название задачи:")
        task_description = simpledialog.askstring("Добавление задачи", "Введите описание задачи:")

        # Обновляем данные о задаче
        self.update_task_data(task_name, task_description)

        # Создаем кнопку для просмотра данных о задаче
        if hasattr(self, 'view_task_button'):
            self.view_task_button.destroy()

        self.view_task_button = tk.Button(self, text="Просмотреть задачу", command=self.view_task_data,
                                          font=("Arial", 12, "bold"), bg="#f2f2f2", fg="#000", bd=1,
                                          highlightbackground="black", highlightthickness=1)
        self.view_task_button.place(x=400, y=180)

    def update_task_data(self, task_name, task_description):
        # Функция для обновления данных о задаче
        self.task_data = f"Название задачи: {task_name}\nОписание задачи: {task_description}"

    def view_task_data(self):
        # Функция для отображения данных о задаче в отдельном окне
        if self.task_data:
            messagebox.showinfo("Задача", self.task_data)
        else:
            messagebox.showinfo("Задача", "Данные о задаче отсутствуют.")

    def work_schedule(self):
        full_name = simpledialog.askstring("Рабочее расписание", "Введите имя, фамилию и отчество:")
        start_time = simpledialog.askstring("Рабочее расписание", "Введите дату и время начала работы:")
        end_time = simpledialog.askstring("Рабочее расписание", "Введите дату и время окончания работы:")

        # Обновляем данные о рабочем времени
        self.update_work_schedule_data(full_name, start_time, end_time)

        # Создаем кнопку для просмотра данных о рабочем времени
        if hasattr(self, 'view_work_schedule_button'):
            self.view_work_schedule_button.destroy()

        self.view_work_schedule_button = tk.Button(self, text="Просмотреть рабочее время", command=self.view_work_schedule_data,
                                                   font=("Arial", 12, "bold"), bg="#f2f2f2", fg="#000", bd=1,
                                                   highlightbackground="black", highlightthickness=1)
        self.view_work_schedule_button.place(x=400, y=140)

        def view_work_schedule_data(self):
            # Функция для отображения данных о рабочем времени в отдельном окне
            if self.work_schedule_data:
                messagebox.showinfo("Рабочее время", self.work_schedule_data)
            else:
                messagebox.showinfo("Рабочее время", "Данные о рабочем времени отсутствуют.")

if __name__ == "__main__":
    app = Application()
    app.mainloop()
