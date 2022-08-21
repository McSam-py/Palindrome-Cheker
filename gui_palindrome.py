from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtWidgets import *
import re
import sys
import os
import codecs
import pytesseract
import cv2
import pdfplumber

class class_stack:
	#method to declare variables in class and create a list.
	def __init__(self):
		self.items = []
		self.items_2 = []
		self.items_3 =[]

	#method to push items into stack.
	def push(self, data, stack):
		if stack == "stack_1":
			self.items.append(data)
		elif stack == "stack_2":
			self.items_2.append(data)
		elif stack == "stack_3":
			self.items_3.append(data)

	#method to check the size of the stack.
	def size(self, stack):
		if stack == "stack_1":
			return len(self.items)
		elif stack == "stack_2":
			return len(self.items)
		elif stack == "stack_3":
			return len(self.items)

	#method to show the items or characters contained in the stack.
	def show(self, stack):
		if stack == "stack_1":
			print(self.items)
		elif stack == "stack_2":
			print(self.items)
		elif stack == "stack_3":
			print(self.items)

	#method to pop items from stack.
	def pop(self, stack):
		if stack == "stack_1":
			return self.items.pop()
		elif stack == "stack_2":
			return self.items_2.pop()
		elif stack == "stack_3":
			return self.items_3.pop()

	#method to join all items in the stack to form one string.
	def together(self, stack):
		if stack == "stack_1":
			return "".join(self.items)
		elif stack == "stack_2":
			return "".join(self.items_3)
		elif stack == "stack_3":
			return "".join(self.items_3)

class Window(QMainWindow):
	def __init__(self):
		super(Window, self).__init__()
		self.title = "Palindrome Checker"
		self.left = 100
		self.top = 150
		self.width = 1200
		self.height = 650
		self.setWindowTitle(self.title)
		self.setGeometry(self.left, self.top, self.width, self.height)
		self.setStyleSheet("background-color: rgba(0, 128, 128, 1)")
		self.label_1 = QLabel(self)
		self.setAcceptDrops(True)
		self.text_input()
		self.heading()
		self.cwd = os.getcwd()
		self.show()

	def dragEnterEvent(self, event):
		if event.mimeData().hasUrls():
			event.accept()
		else:
			event.ignore()

	def dragMovement(self, event):
		if event.mimeData().hasUrls():
			event.accept()
		else:
			event.ignore()

	def dropEvent(self, event):
		global drag_drop_file_path
		files = [u.toLocalFile() for u in event.mimeData().urls()]
		drag_drop_file_path = files[0]
		label_4.setText(drag_drop_file_path)
		if drag_drop_file_path[-4:].lower() == ".txt":
			check_bttn_2.clicked.connect(lambda: self.read_text_file(drag_drop_file_path))

		elif drag_drop_file_path[-4:].lower() == ".pdf":
			check_bttn_4.clicked.connect(lambda: self.pdf_read(drag_drop_file_path))

		elif drag_drop_file_path[-4:].lower() == ".jpg" or drag_drop_file_path[-4:].lower() == ".png":
			check_bttn_3.clicked.connect(lambda: self.photo_extract(drag_drop_file_path))

		else:
			msg_box_4.setText("Unsupported File Type")
			msg_box_4.show()

	def text_input(self):
		global check_bttn
		global check_bttn_2
		global check_bttn_3
		global check_bttn_4
		global msg_box
		global msg_box_2
		global msg_box_3
		global msg_box_4
		global msg_box_5
		global label_3
		global label_4
		global word

		word = QtWidgets.QLineEdit(self)
		word.setGeometry(300, 150, 550, 50)
		word.setFont(QtGui.QFont("Times New Roman", 15))
		word.setPlaceholderText("Enter word or sentence here")
		word.setStyleSheet("QLineEdit {border: 5px solid gray;border-radius: 10px;padding-left: 15px; "
                                "background-color: rgba(200, 255,255, 1); font: 25px;}"
                                "QLineEdit:focus {background-color: rgba(255, 255, 255, 1)}")

		label_2 = QLabel(self)
		label_2.setText("For text files,images and pdfs click Select File.\nSupported file types (*.txt,*.png,*.jpg,*pdf)")
		label_2.setGeometry(300, 250, 420, 50)
		label_2.setFont(QtGui.QFont("Times New Roman", 15))
		label_2.setStyleSheet("QLabel {border: 1px solid gray"
                                "QLabel:focus {background-color: rgba(255, 255, 255, 1)}")

		label_3 = QLabel(self)
		label_3.setGeometry(300, 300, 550, 50)
		label_3.setFont(QtGui.QFont("Times New Roman", 15))
		label_3.setStyleSheet("QLabel {border: 1px solid gray;border-radius: 10px;padding-left: 15px; "
                                "background-color: rgba(200, 255,255, 1); font: 25px;}"
                                "QLineEdit:focus {background-color: rgba(255, 255, 255, 1)}")

		label_4 = QLabel(self)
		label_4.setGeometry(300, 400, 550, 200)
		label_4.setFont(QtGui.QFont("Times New Roman", 15))
		label_4.setText("         Drag and drop image or text file here")
		label_4.setStyleSheet("QLabel {border: 1px solid gray;border-radius: 10px;padding-left: 15px; "
                                "background-color: rgba(200, 255,255, 1); font: 25px;}"
                                "QLineEdit:focus {background-color: rgba(255, 255, 255, 1)}")

		check_bttn_2 = QtWidgets.QPushButton(self)
		check_bttn_2.setGeometry(870, 400, 125, 50)
		check_bttn_2.setFont(QtGui.QFont("Times New Roman", 10))
		check_bttn_2.setText("Check\n For text files(.txt)")
		check_bttn_2.setStyleSheet("QPushButton {margin:1px; padding: 3px; border: 1px solid gray; "
                                    "border-radius: 20px;background-color: rgba(200, 255, 255, 1); "
                                    "border-width: 2px;}"
                                    "QPushButton:hover:!pressed {background-color: rgba(255, 255, 255, 1)}")

		check_bttn_3 = QtWidgets.QPushButton(self)
		check_bttn_3.setGeometry(870, 470, 125, 50)
		check_bttn_3.setFont(QtGui.QFont("Times New Roman", 10))
		check_bttn_3.setText("Check\n For Images(.jpg/.png)")
		check_bttn_3.setStyleSheet("QPushButton {margin:1px; padding: 3px; border: 1px solid gray; "
                                    "border-radius: 20px;background-color: rgba(200, 255, 255, 1); "
                                    "border-width: 2px;}"
                                    "QPushButton:hover:!pressed {background-color: rgba(255, 255, 255, 1)}")

		check_bttn_4 = QtWidgets.QPushButton(self)
		check_bttn_4.setGeometry(870, 540, 125, 50)
		check_bttn_4.setFont(QtGui.QFont("Times New Roman", 10))
		check_bttn_4.setText("Check\n For Pdfs (.pdf)")
		check_bttn_4.setStyleSheet("QPushButton {margin:1px; padding: 3px; border: 1px solid gray; "
                                    "border-radius: 20px;background-color: rgba(200, 255, 255, 1); "
                                    "border-width: 2px;}"
                                    "QPushButton:hover:!pressed {background-color: rgba(255, 255, 255, 1)}")


		check_bttn = QtWidgets.QPushButton(self)
		check_bttn.setGeometry(870, 150, 125, 50)
		check_bttn.setFont(QtGui.QFont("Times New Roman", 15))
		check_bttn.setText("Check")
		check_bttn.setStyleSheet("QPushButton {margin:1px; padding: 3px; border: 1px solid gray; "
                                    "border-radius: 20px;background-color: rgba(200, 255, 255, 1); "
                                    "border-width: 2px;}"
                                    "QPushButton:hover:!pressed {background-color: rgba(255, 255, 255, 1)}")
		msg_box = QtWidgets.QMessageBox(self)
		msg_box.setDefaultButton(QMessageBox.Ok)
		msg_box.setStyleSheet("QMessageBox {border: 1px solid gray;border-radius: 10px;padding-left: 15px; "
                "background-color: rgba(125, 255,255, 1); font: 25px;}"
                "QPushButton {font-size: 20px; background-color: rgba(200, 255,255, 1); border-radius: "
                "10px; border: 1px solid gray; padding-left: 20px; padding-right: 20px; padding-top: 5px;"
                "padding-bottom: 5px;} "
                "QPushButton:hover:!pressed {background-color: rgba(255, 255, 255, 1)}"
                "QLabel {background-color: rgba(125, 255,255, 1); font: 25px;}")

		msg_box_2 = QtWidgets.QMessageBox(self)
		msg_box_2.setDefaultButton(QMessageBox.Ok)
		msg_box_2.setStyleSheet("QMessageBox {border: 1px solid gray;border-radius: 10px;padding-left: 15px; "
                "background-color: rgba(125, 255,255, 1); font: 25px;}"
                "QPushButton {font-size: 20px; background-color: rgba(200, 255,255, 1); border-radius: "
                "10px; border: 1px solid gray; padding-left: 20px; padding-right: 20px; padding-top: 5px;"
                "padding-bottom: 5px;} "
                "QPushButton:hover:!pressed {background-color: rgba(255, 255, 255, 1)}"
                "QLabel {background-color: rgba(125, 255,255, 1); font: 25px;}")

		msg_box_3 = QtWidgets.QMessageBox(self)
		msg_box_3.setDefaultButton(QMessageBox.Ok)
		msg_box_3.setStyleSheet("QMessageBox {border: 1px solid gray;border-radius: 10px;padding-left: 15px; "
                "background-color: rgba(125, 255,255, 1); font: 25px;}"
                "QPushButton {font-size: 20px; background-color: rgba(200, 255,255, 1); border-radius: "
                "10px; border: 1px solid gray; padding-left: 20px; padding-right: 20px; padding-top: 5px;"
                "padding-bottom: 5px;} "
                "QPushButton:hover:!pressed {background-color: rgba(255, 255, 255, 1)}"
                "QLabel {background-color: rgba(125, 255,255, 1); font: 25px;}")

		msg_box_4 = QtWidgets.QMessageBox(self)
		msg_box_4.setDefaultButton(QMessageBox.Ok)
		msg_box_4.setStyleSheet("QMessageBox {border: 1px solid gray;border-radius: 10px;padding-left: 15px; "
                "background-color: rgba(125, 255,255, 1); font: 25px;}"
                "QPushButton {font-size: 20px; background-color: rgba(200, 255,255, 1); border-radius: "
                "10px; border: 1px solid gray; padding-left: 20px; padding-right: 20px; padding-top: 5px;"
                "padding-bottom: 5px;} "
                "QPushButton:hover:!pressed {background-color: rgba(255, 255, 255, 1)}"
                "QLabel {background-color: rgba(125, 255,255, 1); font: 25px;}")
		msg_box_5 = QtWidgets.QMessageBox(self)
		msg_box_5.setDefaultButton(QMessageBox.Ok)
		msg_box_5.setStyleSheet("QMessageBox {border: 1px solid gray;border-radius: 10px;padding-left: 15px; "
                "background-color: rgba(125, 255,255, 1); font: 25px;}"
                "QPushButton {font-size: 20px; background-color: rgba(200, 255,255, 1); border-radius: "
                "10px; border: 1px solid gray; padding-left: 20px; padding-right: 20px; padding-top: 5px;"
                "padding-bottom: 5px;} "
                "QPushButton:hover:!pressed {background-color: rgba(255, 255, 255, 1)}"
                "QLabel {background-color: rgba(125, 255,255, 1); font: 25px;}")

		#btn_choosefile
		btn_chooseFile = QPushButton(self)  
		btn_chooseFile.setFont(QtGui.QFont("Times New Roman", 15))
		btn_chooseFile.setGeometry(870, 300, 125, 50)
		btn_chooseFile.setText("Select File")
		btn_chooseFile.setStyleSheet("QPushButton {margin:1px; padding: 3px; border: 1px solid gray; "
                                    "border-radius: 20px;background-color: rgba(200, 255, 255, 1); "
                                    "border-width: 2px;}"
                                    "QPushButton:hover:!pressed {background-color: rgba(255, 255, 255, 1)")

		def save_input(self):
			global word_to_check
			word_to_check = word.text()


		check_bttn.clicked.connect(save_input)
		check_bttn.clicked.connect(lambda: self.palindrome_check(word_to_check))
		btn_chooseFile.clicked.connect(self.browse_file)

		
	def heading(self):
		self.label_1.setFont(QtGui.QFont("Arial", 15))
		self.label_1.setText("                      Palindrome Checker")
		self.label_1.setGeometry(300, 20, 550, 100)
		self.label_1.setStyleSheet("QLabel {border: 1px solid gray;border-radius: 10px;padding-left: 15px; "
                                "background-color: rgba(200, 255,255, 1); font: 25px;}"
                                "QLineEdit:focus {background-color: rgba(255, 255, 255, 1)}")
		


	def palindrome_check(self, text):
		
		self.words = []
		self.palindromes_list = []
		self.count_palindromes = 0

		text = text.replace("\n"," ")
		text2 = re.sub('[{}.\n\r,/?""-#$;:()@*_!%+]','',text)
		for i in text2.strip().split(" "):
			self.words.append(i)


		for i in self.words:
			stack = class_stack()
			for char in i:
				stack.push(char.lower(),"stack_1")
			

			for char in i:
				stack.push(char.lower(),"stack_2")

			for things in range(stack.size("stack_2")):
				stack.push(stack.pop("stack_2"),"stack_3")
			

			if len(self.words) == 1:
				if stack.together("stack_1") == stack.together("stack_3") == "":
					msg_box_3.setText("You inputed an empty string.")
					msg_box_3.show()
					pass

				elif stack.together("stack_1") == stack.together("stack_3") and stack.together("stack_1") != "":
					self.count_palindromes += 1
					msg_box.setInformativeText(f"""True\nFirst Stack: {stack.together("stack_1")}\nThird Stack: {stack.together("stack_3")}""")
					msg_box.show()

				else:
					msg_box.setInformativeText(f"""False \nFirst Stack: {stack.together("stack_1")}\nThird Stack: {stack.together("stack_3")}""")
					msg_box.show()
					pass

			else:
				if stack.together("stack_1") == stack.together("stack_3") and stack.together("stack_1") != "" and stack.size("stack_1") != 1:
					self.count_palindromes += 1
					self.palindromes_list.append(i)
				else:
					pass

		if len(self.words) > 1 and self.count_palindromes != 0:
			msg_box_2.setText(f"\nNumber of palindrome(s): {self.count_palindromes}\n     Palindromes\n--------------------------")
			msg_box_2.setInformativeText('\n'.join(map(str, self.palindromes_list)))
			msg_box_2.show()
			pass

		elif self.count_palindromes == 0 and len(self.words) > 1:
			msg_box_5.setText("\n***No palindromes found.***")
			msg_box_5.show()

	def read_text_file(self, file_path):
		with codecs.open(file_path, 'r',encoding='utf-8',errors='ignore') as file:
			text = file.read()
			self.palindrome_check(text)

	def photo_extract(self, path_to_photo):
		try:
			pytesseract.pytesseract.tesseract_cmd='C:\\Program Files (x86)\\Tesseract-OCR\\tesseract.exe'
			img = cv2.imread(path_to_photo)
			img = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
			text_in_image = pytesseract.image_to_string(img)
			self.palindrome_check(text_in_image)
		except cv2.error:
			pass

	def pdf_read(self, pdf_path):
		try:
			all_text = ''
			with pdfplumber.open(pdf_path) as pdf:
				for page in pdf.pages:
					single_page_text = page.extract_text()
					all_text = all_text + '\n' + single_page_text
				self.palindrome_check(all_text)
		except:
			pass

	def browse_file(self):
			global fileName_chosen
			global filetype
			fileName_chosen, filetype = QFileDialog.getOpenFileName(self,  "Select File",  
	                                    self.cwd, # Start path 
	                                    "All Files (*);;Text Files (*.txt);;Image Files (*.jpg, *.png);;Pdf files(*.pdf)")
			if fileName_chosen == "":
				print("\nCancel selection")

			else:
				label_3.setText(fileName_chosen)
				if fileName_chosen[-4:].lower() == ".txt":
					check_bttn_2.clicked.connect(lambda: self.read_text_file(fileName_chosen))

				elif fileName_chosen[-4:].lower() == ".jpg" or fileName_chosen[-4:].lower() == ".png":
					check_bttn_3.clicked.connect(lambda: self.photo_extract(fileName_chosen))

				elif fileName_chosen[-4:].lower() == ".pdf":
					check_bttn_4.clicked.connect(lambda: self.pdf_read(fileName_chosen))

				else:
					msg_box_4.setText("Unsupported File Type")
					msg_box_4.show()

if __name__ == '__main__':
	app = QApplication(sys.argv)
	execute = Window()
	sys.exit(app.exec_())