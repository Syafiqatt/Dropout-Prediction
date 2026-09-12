import streamlit as st
import pandas as pd
import numpy as np
import joblib
import json

st.set_page_config(page_title="Prediksi Dropout - Jaya Jaya Institut", page_icon="🎓", layout="centered")

@st.cache_resource
def load_artifacts():
    model = joblib.load("model/model.joblib")
    scaler = joblib.load("model/scaler.joblib")
    with open("model/feature_names.json") as f:
        feature_names = json.load(f)
    return model, scaler, feature_names

model, scaler, feature_names = load_artifacts()

st.title("🎓 Prediksi Risiko Dropout Siswa")
st.markdown(
    "Prototype ini digunakan oleh tim akademik **Jaya Jaya Institut** untuk memprediksi "
    "kemungkinan seorang siswa akan **dropout**, berdasarkan data akademik, demografis, "
    "dan sosial-ekonomi mereka. Isi data siswa pada form di bawah, lalu klik **Prediksi**."
)

with st.form("input_form"):
    st.subheader("1. Data Demografis & Pendaftaran")
    c1, c2, c3 = st.columns(3)
    with c1:
        Marital_status = st.selectbox("Status Pernikahan", [1,2,3,4,5,6],
            format_func=lambda x: {1:"Single",2:"Married",3:"Widower",4:"Divorced",5:"Facto union",6:"Legally separated"}[x])
        Gender = st.selectbox("Gender", [1,0], format_func=lambda x: "Laki-laki" if x==1 else "Perempuan")
        Age_at_enrollment = st.number_input("Usia saat mendaftar", 15, 70, 20)
    with c2:
        Application_mode = st.number_input("Application mode (kode)", 1, 60, 1)
        Application_order = st.number_input("Application order (0=pilihan pertama)", 0, 9, 0)
        International = st.selectbox("Mahasiswa Internasional?", [0,1], format_func=lambda x:"Ya" if x else "Tidak")
    with c3:
        Course = st.number_input("Kode Program Studi", 1, 9999, 9119)
        Daytime_evening_attendance = st.selectbox("Kelas", [1,0], format_func=lambda x:"Pagi/Siang" if x==1 else "Malam")
        Displaced = st.selectbox("Displaced (pindah domisili)", [0,1], format_func=lambda x:"Ya" if x else "Tidak")

    st.subheader("2. Latar Belakang Pendidikan")
    c1, c2, c3 = st.columns(3)
    with c1:
        Previous_qualification = st.number_input("Kode Kualifikasi Sebelumnya", 1, 50, 1)
        Previous_qualification_grade = st.number_input("Nilai Kualifikasi Sebelumnya (0-200)", 0.0, 200.0, 120.0)
    with c2:
        Admission_grade = st.number_input("Nilai Penerimaan / Admission Grade (0-200)", 0.0, 200.0, 120.0)
        Nacionality = st.number_input("Kode Kewarganegaraan", 1, 200, 1)
    with c3:
        Mothers_qualification = st.number_input("Kode Kualifikasi Ibu", 1, 50, 1)
        Fathers_qualification = st.number_input("Kode Kualifikasi Ayah", 1, 50, 1)

    c1, c2 = st.columns(2)
    with c1:
        Mothers_occupation = st.number_input("Kode Pekerjaan Ibu", 0, 200, 5)
    with c2:
        Fathers_occupation = st.number_input("Kode Pekerjaan Ayah", 0, 200, 5)

    st.subheader("3. Kondisi Sosial-Ekonomi")
    c1, c2, c3 = st.columns(3)
    with c1:
        Displaced2 = None
        Educational_special_needs = st.selectbox("Kebutuhan Khusus?", [0,1], format_func=lambda x:"Ya" if x else "Tidak")
        Debtor = st.selectbox("Memiliki Tunggakan (Debtor)?", [0,1], format_func=lambda x:"Ya" if x else "Tidak")
    with c2:
        Tuition_fees_up_to_date = st.selectbox("SPP Lunas / Up to date?", [1,0], format_func=lambda x:"Ya" if x==1 else "Tidak")
        Scholarship_holder = st.selectbox("Penerima Beasiswa?", [0,1], format_func=lambda x:"Ya" if x else "Tidak")
    with c3:
        Unemployment_rate = st.number_input("Unemployment Rate (%)", 0.0, 30.0, 10.0)
        Inflation_rate = st.number_input("Inflation Rate (%)", -5.0, 20.0, 1.0)
    GDP = st.number_input("GDP (indikator ekonomi)", -10.0, 10.0, 1.0)

    st.subheader("4. Performa Akademik Semester 1")
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        cu1_credited = st.number_input("SKS Diakui (1st sem)", 0, 30, 0)
        cu1_enrolled = st.number_input("SKS Diambil (1st sem)", 0, 30, 6)
    with c2:
        cu1_eval = st.number_input("Jumlah Evaluasi (1st sem)", 0, 30, 6)
        cu1_approved = st.number_input("SKS Lulus (1st sem)", 0, 30, 5)
    with c3:
        cu1_grade = st.number_input("Rata-rata Nilai (1st sem, 0-20)", 0.0, 20.0, 12.0)
    with c4:
        cu1_no_eval = st.number_input("Tanpa Evaluasi (1st sem)", 0, 30, 0)

    st.subheader("5. Performa Akademik Semester 2")
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        cu2_credited = st.number_input("SKS Diakui (2nd sem)", 0, 30, 0)
        cu2_enrolled = st.number_input("SKS Diambil (2nd sem)", 0, 30, 6)
    with c2:
        cu2_eval = st.number_input("Jumlah Evaluasi (2nd sem)", 0, 30, 6)
        cu2_approved = st.number_input("SKS Lulus (2nd sem)", 0, 30, 5)
    with c3:
        cu2_grade = st.number_input("Rata-rata Nilai (2nd sem, 0-20)", 0.0, 20.0, 12.0)
    with c4:
        cu2_no_eval = st.number_input("Tanpa Evaluasi (2nd sem)", 0, 30, 0)

    submitted = st.form_submit_button("🔍 Prediksi Risiko Dropout")

if submitted:
    input_dict = {
        "Marital_status": Marital_status,
        "Application_mode": Application_mode,
        "Application_order": Application_order,
        "Course": Course,
        "Daytime_evening_attendance": Daytime_evening_attendance,
        "Previous_qualification": Previous_qualification,
        "Previous_qualification_grade": Previous_qualification_grade,
        "Nacionality": Nacionality,
        "Mothers_qualification": Mothers_qualification,
        "Fathers_qualification": Fathers_qualification,
        "Mothers_occupation": Mothers_occupation,
        "Fathers_occupation": Fathers_occupation,
        "Admission_grade": Admission_grade,
        "Displaced": Displaced,
        "Educational_special_needs": Educational_special_needs,
        "Debtor": Debtor,
        "Tuition_fees_up_to_date": Tuition_fees_up_to_date,
        "Gender": Gender,
        "Scholarship_holder": Scholarship_holder,
        "Age_at_enrollment": Age_at_enrollment,
        "International": International,
        "Curricular_units_1st_sem_credited": cu1_credited,
        "Curricular_units_1st_sem_enrolled": cu1_enrolled,
        "Curricular_units_1st_sem_evaluations": cu1_eval,
        "Curricular_units_1st_sem_approved": cu1_approved,
        "Curricular_units_1st_sem_grade": cu1_grade,
        "Curricular_units_1st_sem_without_evaluations": cu1_no_eval,
        "Curricular_units_2nd_sem_credited": cu2_credited,
        "Curricular_units_2nd_sem_enrolled": cu2_enrolled,
        "Curricular_units_2nd_sem_evaluations": cu2_eval,
        "Curricular_units_2nd_sem_approved": cu2_approved,
        "Curricular_units_2nd_sem_grade": cu2_grade,
        "Curricular_units_2nd_sem_without_evaluations": cu2_no_eval,
        "Unemployment_rate": Unemployment_rate,
        "Inflation_rate": Inflation_rate,
        "GDP": GDP,
    }

    # Susun sesuai urutan fitur training; isi 0 jika ada nama yang tidak cocok persis
    row = []
    for f in feature_names:
        row.append(input_dict.get(f, 0))
    X_input = pd.DataFrame([row], columns=feature_names)

    X_scaled = scaler.transform(X_input)
    proba = model.predict_proba(X_scaled)[0][1]
    pred = model.predict(X_scaled)[0]

    st.divider()
    st.subheader("Hasil Prediksi")
    st.metric("Probabilitas Dropout", f"{proba*100:.1f}%")

    if pred == 1:
        st.error("⚠️ Siswa ini termasuk **BERISIKO TINGGI DROPOUT**. Disarankan diberikan bimbingan khusus / konseling akademik dan finansial segera.")
    else:
        if proba > 0.3:
            st.warning("🟡 Siswa ini memiliki **risiko dropout moderat**. Perlu dipantau secara berkala.")
        else:
            st.success("✅ Siswa ini termasuk **risiko dropout rendah**.")

    st.progress(min(int(proba*100), 100))
    st.caption(
        "Catatan: Prediksi ini adalah alat bantu (decision support) berbasis model Random Forest "
        "dan bukan keputusan akhir. Tetap perlu ditinjau oleh staf akademik."
    )

st.divider()
st.caption("Prototype Machine Learning — Proyek Akhir Data Science: Jaya Jaya Institut")
