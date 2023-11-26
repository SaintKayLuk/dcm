import os
import customtkinter
from tkinter import filedialog
from dcm import my_mysql
import windnd

# customtkinter.set_appearance_mode("dark")
from dcm import desensitization

name_set = set()


class MyApp(customtkinter.CTk):

    def __init__(self):
        super().__init__()

        self.title("dicom 脱敏工具")
        self.geometry("850x500")

        # 两列相同的比重，没有部件的列则会隐藏
        self.grid_columnconfigure((0, 1), weight=1)
        self.grid_rowconfigure(0, weight=1)

        # 第一个画布
        frame1 = customtkinter.CTkFrame(self)
        # sticky 东南西北方向，东east；南south；西west；北north
        frame1.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        frame1.grid_columnconfigure((0, 1, 2), weight=2)
        # frame1.grid_rowconfigure((0, 1, 2), weight=2)
        windnd.hook_dropfiles(frame1, func=self.dragged_files1)

        # 标签
        self.label = customtkinter.CTkLabel(frame1, text="输入需要脱敏的 dicom 文件/目录 路径")
        self.label.grid(row=0, column=0, columnspan=3, sticky='nsew')

        # 路径输入框
        self.entry1 = customtkinter.CTkEntry(frame1)
        self.entry1.grid(row=1, column=0, padx=(10, 10), columnspan=3, sticky='nsew')

        # 按钮
        self.button = customtkinter.CTkButton(frame1, text="选择路径", command=self.button_0)
        self.button.grid(row=2, column=0, padx=(10, 10), pady=(10, 10), sticky="nsew")

        # 医院选择框
        # self.hospital_dict = dict(my_mysql.select_hospital())
        # values = list(self.hospital_dict.keys())
        # self.option_menu = customtkinter.CTkOptionMenu(frame1, values=values)
        self.option_menu = customtkinter.CTkOptionMenu(frame1)
        self.option_menu.set("选择医院")
        self.option_menu.grid(row=2, column=1, padx=(10, 10), pady=(10, 10), sticky="nsew")

        # 按钮1
        self.button = customtkinter.CTkButton(frame1, text="脱敏", command=self.button_1)
        self.button.grid(row=2, column=2, padx=(10, 10), pady=(10, 10), sticky="nsew")

        # 文本输出
        self.textbox1 = customtkinter.CTkTextbox(frame1, height=350)
        self.textbox1.configure(state="normal")
        self.textbox1.grid(row=3, column=0, padx=10, pady=10, columnspan=3, sticky='nsew')
        #
        # 第二个画布
        frame2 = customtkinter.CTkFrame(self)
        # sticky 东南西北方向，东east；南south；西west；北north
        frame2.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")
        frame2.grid_columnconfigure((0, 1), weight=2)

        windnd.hook_dropfiles(frame2, func=self.dragged_files2)

        # 标签
        self.label = customtkinter.CTkLabel(frame2, text="输入需要查看源内容的 dicom 文件路径")
        self.label.grid(row=0, column=0, columnspan=2, sticky='nsew')

        self.entry2 = customtkinter.CTkEntry(frame2)
        self.entry2.grid(row=1, column=0, padx=(10, 10), columnspan=2, sticky='nsew')

        # 按钮
        self.button = customtkinter.CTkButton(frame2, text="选择文件", command=self.button_3)
        self.button.grid(row=2, column=0, padx=(50, 50), pady=(10, 10), sticky="nsew")

        # 按钮2
        self.button = customtkinter.CTkButton(frame2, text="查看", command=self.button_2)
        self.button.grid(row=2, column=1, padx=(50, 50), pady=(10, 10), sticky="nsew")

        # 文本输出
        self.textbox2 = customtkinter.CTkTextbox(frame2, height=350)
        self.textbox2.configure(state="normal")
        self.textbox2.grid(row=3, column=0, padx=10, pady=10, columnspan=2, sticky='nsew')

    def dragged_files1(self, files):
        msg = '\n'.join((item.decode('gbk') for item in files))
        # print(msg)
        self.entry1.delete('0', 'end')
        self.entry1.insert('end', msg)
        # self.button_1()

    def dragged_files2(self, files):
        msg = '\n'.join((item.decode('gbk') for item in files))
        # print(msg)
        self.entry2.delete('0', 'end')
        self.entry2.insert('end', msg)
        self.button_2()

    # 打开资源，选择目录
    def button_0(self):
        path = filedialog.askdirectory(title='选择需要脱敏的目录')
        self.entry1.delete('0', 'end')
        self.entry1.insert('end', path)

    # 打开资源，选择文件
    def button_3(self):
        file_path = filedialog.askopenfilename()
        self.entry2.delete('0', 'end')
        self.entry2.insert('end', file_path)

    # 脱敏按钮
    def button_1(self):
        name_set.clear()
        self.textbox1.delete('0.0', 'end')

        # 路径
        path = self.entry1.get()
        if os.path.exists(path):
            # 医院
            hospital_name = self.option_menu.get()
            hospital_id = self.hospital_dict.get(hospital_name)

            if hospital_name == '选择医院':
                self.textbox1.insert('end', '请选择一个医院 \n')
                return
            else:
                self.get_file(path, hospital_id)
                self.textbox1.insert('end', '脱敏完成\n')
        else:
            self.textbox1.insert('end', '路径不对, 哈哈 \n')

    # 查看按钮
    def button_2(self):
        path = self.entry2.get()
        name = desensitization.dcm_decryption(path)
        self.textbox2.delete('0.0', 'end')
        self.textbox2.insert('end', name)

    def get_file(self, path, hospital_id):
        # 路径是目录
        if os.path.isdir(path):
            dcm_list = os.listdir(path)
            for i in dcm_list:
                # 文件路径
                dcm_path = os.path.join(path, i)
                self.get_file(dcm_path, hospital_id)
        # 路径是文件
        elif os.path.isfile(path) and path.split('.')[-1] == 'dcm':
            try:
                name = desensitization.dcm_encryption(path, hospital_id)
                if name not in name_set:
                    name_set.add(name)
                    self.textbox1.insert('end', name)
                    self.update()
            except Exception as e:
                print(e)
                # self.textbox1.insert('end', path)
                self.textbox1.insert('end', e)

    # def get_file(self, path, hospital_id):
    #     self.textbox1.insert('end', path + '\n')
    #     # 路径是目录
    #     if os.path.isdir(path):
    #         dcm_list = os.listdir(path)
    #         for i in dcm_list:
    #             # 文件路径
    #             dcm_path = os.path.join(path, i)
    #             # 目录继续遍历
    #             if os.path.isdir(dcm_path):
    #                 self.get_file(dcm_path, hospital_id)
    #             # 判断是否为dcm文件，以后缀为 .dcm 来判断
    #             elif os.path.isfile(dcm_path) and i.split('.')[-1] == 'dcm':
    #                 try:
    #                     # 一次一个
    #                     name = desensitization.dcm_encryption(dcm_path, hospital_id)
    #                     if name not in name_set:
    #                         name_set.add(name)
    #                         self.textbox1.insert('end', name)
    #                         self.update()
    #                 except Exception as e:
    #                     self.textbox1.insert('end', dcm_path)
    #                     self.textbox1.insert('end', e)
    #     # 路径是文件
    #     elif os.path.isfile(path) and path.split('.')[-1] == 'dcm':
    #         name = desensitization.dcm_encryption(path, hospital_id)
    #         if name not in name_set:
    #             name_set.add(name)
    #             self.textbox1.insert('end', name)
