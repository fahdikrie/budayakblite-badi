#!/usr/bin/env python3
"""

TEMPLATE TP4 DDP1 Semester Gasal 2019/2020

Author: 
Ika Alfina (ika.alfina@cs.ui.ac.id)
Evi Yulianti (evi.yulianti@cs.ui.ac.id)
Meganingrum Arista Jiwanggi (meganingrum@cs.ui.ac.id)

Last update: 23 November 2019

"""
from budayaKB_model import BudayaItem, BudayaCollection
from flask import Flask, request, render_template, redirect, flash
from wtforms import Form, validators, TextField

app = Flask(__name__)
app.secret_key ="tp4"

#inisialisasi objek budayaData
databasefilename = ""
budayaData = BudayaCollection()


# Bagian ini merender tampilan landingpage
@app.route('/')
def landingpage():
	return render_template("landingpage.html")

# Bagian ini merender tampilan home (index.html)
# - berisi mengenai informasi dan deskripsi singkat mengenai program BudayaKB Lite v2.0
@app.route('/home')
def index():
	return render_template("index.html")
	
# Bagian ini adalah implementasi fitur Impor Budaya, yaitu:
# - merender tampilan saat menu Impor Budaya diklik	
# - melakukan pemrosesan terhadap isian form setelah tombol "Import Data" diklik
# - menampilkan notifikasi bahwa data telah berhasil diimport 	
@app.route('/imporBudaya', methods=['GET', 'POST'])
def importData():
	if request.method == "GET":
		return render_template("imporBudaya.html")

	elif request.method == "POST":
		global databasefilename
		f = request.files['file']
		f.save(f.filename)

		if f.filename.split(".")[-1] != "csv":
			warning = 1
			return render_template("imporBudaya.html", warning=warning)
		else:
			databasefilename=f.filename
			result_impor=budayaData.importFromCSV(databasefilename)
			budayaData.exportToCSV(databasefilename) #setiap perubahan data langsung disimpan ke file
			warning = 0
			return render_template("imporBudaya.html", result=result_impor, fname=f.filename, warning=warning)

# Bagian ini adalah implementasi fitur Tambah Budaya, yaitu:
# - merender tampilan saat menu Tambah Budaya diklik	
# - meminta user untuk memasukkan isian form mengenai data budaya yang ingin ditambahkan
# - menampilkan notifikasi bahwa data telah berhasil ditambahkan ke database 	
@app.route('/tambahBudaya', methods=['GET','POST'])
def tambahBudaya():
	if request.method == "GET":
		return render_template("tambahBudaya.html")

	elif request.method == "POST":
		nama = request.form['nama']
		tipe = request.form['tipe']
		provinsi = request.form['provinsi']
		url = request.form['url']

		if databasefilename != "":
			tambahState = budayaData.tambah(nama,tipe,provinsi,url)
		else:
			tambahState = 0

		try:
			budayaData.exportToCSV(databasefilename) #setiap perubahan data langsung disimpan ke file
			warning = 0
		except FileNotFoundError:
			warning = 1
		return render_template("tambahBudaya.html", tambahState=tambahState, nama=nama, warning=warning)	

# Bagian ini adalah implementasi fitur Ubah Budaya, yaitu:
# - merender tampilan saat menu Ubah Budaya diklik	
# - meminta user untuk memasukkan isian form mengenai data budaya yang ingin diubah
# - menampilkan notifikasi bahwa data telah berhasil diubah 
@app.route('/ubahBudaya', methods=['GET','POST'])
def ubahBudaya():
	if request.method == "GET":
		return render_template("ubahBudaya.html")

	elif request.method == "POST":
		nama = request.form['nama']
		tipe = request.form['tipe']
		provinsi = request.form['provinsi']
		url = request.form['url']

		if databasefilename != "":
			ubahState = budayaData.ubah(nama,tipe,provinsi,url)
		else:
			ubahState = 0

		try:
			budayaData.exportToCSV(databasefilename) #setiap perubahan data langsung disimpan ke file
			warning = 0
		except FileNotFoundError:
			warning = 1
		return render_template("ubahBudaya.html", ubahState=ubahState, nama=nama, warning=warning)

# Bagian ini adalah implementasi fitur Hapus Budaya, yaitu:
# - merender tampilan saat menu Hapus Budaya diklik	
# - meminta user untuk memasukkan nama budaya yang ingin dihapus
# - menampilkan notifikasi bahwa data telah berhasil dihapus 
@app.route('/hapusBudaya', methods=['GET','POST'])
def hapusBudaya():
	if request.method == "GET":
		return render_template("hapusBudaya.html")

	elif request.method == "POST":
		nama = request.form['nama']

		if databasefilename != "":
			hapusState = budayaData.hapus(nama)
		else:
			hapusState = 0

		try:
			budayaData.exportToCSV(databasefilename) #setiap perubahan data langsung disimpan ke file
			warning = 0
		except FileNotFoundError:
			warning = 1
		return render_template("hapusBudaya.html", hapusState=hapusState, nama=nama, warning=warning)

# Bagian ini adalah implementasi fitur Cari Budaya, yaitu:
# - merender tampilan saat menu Cari Budaya diklik	
# - meminta user untuk memasukkan nama budaya yang ingin ditampilkan
# - terdapat fitur tambahan yakni memunculkan semua budaya dengan memasukkan input kosong
# - menampilkan data yang ingin ditampilkan dalam penyajian tabel
@app.route('/cariBudaya', methods=['GET','POST'])
def cariBudaya():
	if request.method == "GET":
		return render_template("cariBudaya.html")

	elif request.method == "POST":
		nama = request.form['nama']

		if nama.split() != []:
			if request.form['metode pencarian'] == "nama":
				cariState = budayaData.cariByNama(nama)
			elif request.form['metode pencarian'] == "tipe":
				cariState = budayaData.cariByTipe(nama)
			elif request.form['metode pencarian'] == "provinsi":
				cariState = budayaData.cariByProv(nama)
		else:
			cariState = budayaData.cariSemua()

		length = len(cariState)
		return render_template("cariBudaya.html",length=length, cariState=cariState, nama=nama)

# Bagian ini adalah implementasi fitur Statistik Budaya, yaitu:
# - merender tampilan saat menu Statistik Budaya diklik	
# - meminta user untuk memilih jenis statistik yang ingin ditampilkan
# - menampilkan data statistik yang ingin ditampilkan dalam penyajian tabel
@app.route('/statsBudaya', methods=['GET','POST'])
def statsBudaya():
	if request.method == "GET":
		return render_template("statsBudaya.html")

	elif request.method == "POST":
		nama = request.form['metode pencarian']

		if request.form['metode pencarian'] == "nama":
			cariState = budayaData.stat()
			length = cariState
			nama = "Nama"
		elif request.form['metode pencarian'] == "tipe":
			cariState = budayaData.statByTipe()
			length = len(cariState)
			nama = "Tipe"
		elif request.form['metode pencarian'] == "provinsi":
			cariState = budayaData.statByProv()
			length = len(cariState)
			nama = "Provinsi"
		return render_template("statsBudaya.html",length=length, cariState=cariState, nama=nama)

# run main app
if __name__ == "__main__":
	app.run(debug=True)



