# Glycemic Index Detection from Food Images

## 📌 Project Overview

This project aims to **identify the glycemic index (GI)** of a food item using **image-based food recognition** and **predict whether the food is safe for consumption** by diabetic patients. By combining **computer vision**, **nutritional data**, and **predictive modeling**, the system evaluates whether a particular food item is likely to cause a spike in blood glucose levels.

---

## 🎯 Objectives

* Detect and classify food items from an image.
* Predict estimated **Glycemic Index (GI)** based on identified food.
* Predict whether the food is **safe**, **moderate**, or **unsafe** for diabetic patients.
* Provide reasoning based on GI, GL (Glycemic Load), and known nutritional properties.

---

## 🧠 Key Features

### 1. **Food Recognition using Computer Vision**

* Utilizes a deep learning model (e.g., **ResNet-50**, EfficientNet, or MobileNet) trained on food datasets.
* Input: Food image
* Output: Predicted food label

### 2. **Glycemic Index Prediction**

* Each recognized food maps to a nutritional database containing:

  * GI (Glycemic Index)
  * Carbohydrate content
  * Portion size

### 3. **Blood Sugar Spike Prediction**

* Model estimates **Glycemic Load (GL)**:

  **GL = (GI × Carbs per serving) ÷ 100**

* Decision criteria:

  * **Safe** → GI < 55 and GL < 10
  * **Moderate** → GI 55–69 or GL 11–19
  * **Unsafe** → GI ≥ 70 or GL ≥ 20

### 4. **Patient Safety Recommendation**

Based on GI & GL values, output:

* "Safe for diabetic consumption"
* "Consume in moderation"
* "Avoid – may cause glucose spike"

---

## 🛠️ Tech Stack

### **Frontend**

* React / HTML / Flutter (optional)
* Camera/image upload support

### **Backend**

* Python (FastAPI / Flask)
* Deep learning model (PyTorch / TensorFlow)
* Nutritional dataset lookup

### **Machine Learning / AI**

* Food image classification model
* GI/GL prediction logic
* Optional: LLM for explanation generation

### **Database**

* SQLite / PostgreSQL
* Contains mapping: `Food Item → GI → Carbs → Category`

---

## 🧩 Workflow

1. User uploads food image
2. Model identifies food item
3. System fetches GI & Carb data
4. GL is calculated
5. System predicts if the food will spike blood sugar
6. Final result + explanation provided

---

## 📂 Project Structure

```
project-folder/
│── models/                # Trained food classifier
│── data/                  # GI database & nutritional info
│── backend/               # API for prediction
│── frontend/              # Web or mobile app
│── utils/                 # Image preprocessing & helpers
│── README.md              # Documentation file
```

---

## 🔍 Data Sources (Suggested)

* GI Database: University of Sydney — Glycemic Index Research
* USDA Food Nutrient Database
* Open source datasets for food classification:

  * Food-101
  * IndianFood-Images
  * UEC Food Dataset

---

## 🚀 Future Enhancements

* Personalized predictions using patient history
* Combining continuous glucose monitor (CGM) data
* Multiple food item recognition in one image
* Portion size estimation using depth estimation

---

## 🧪 Example Output

**Input:** Image of "White Rice"

**Prediction:**

* GI: 72
* Carbs per serving: 28g
* GL: 20.16
* **Status:** Unsafe

**Recommendation:** "White rice has a high GI and GL, which can significantly raise blood sugar levels. It is not recommended for diabetic patients."

---

## 📧 Contact

For improvements or queries, feel free to reach out.

---

This README summarizes the entire project concept based on the previous threads and your requirements.
