from flask import Flask, request, jsonify
import subprocess
import os
import json

app = Flask(__name__)

# تأكيد وجود exiftool على السيرفر
EXIFTOOL_PATH = "exiftool"  # Render يدعم ExifTool مباشرة بدون تثبيت يدوي

@app.route('/')
def home():
    return "🚀 ExifTool API تعمل بشكل صحيح!"

@app.route('/extract_metadata', methods=['POST'])
def extract_metadata():
    if 'file' not in request.files:
        return jsonify({"error": "لم يتم إرسال أي ملف"}), 400

    file = request.files['file']
    file_path = "/tmp/" + file.filename
    file.save(file_path)

    try:
        # تشغيل ExifTool لاستخراج جميع البيانات الوصفية
        result = subprocess.run([EXIFTOOL_PATH, "-json", file_path], capture_output=True, text=True)

        if result.returncode == 0:
            metadata = json.loads(result.stdout)  # تحويل النص إلى JSON حقيقي
            return jsonify({"metadata": metadata})
        else:
            return jsonify({"error": "فشل في استخراج البيانات", "details": result.stderr}), 500

    except Exception as e:
        return jsonify({"error": "حدث خطأ أثناء معالجة الملف", "details": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
