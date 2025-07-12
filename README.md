# 🚨 SecureCheck: Police Check Post Digital Ledger

**SecureCheck** is a digital record management system designed for law enforcement agencies to **track**, **analyze**, and **manage traffic stop logs**.
Built using **Python**, **MySQL**, and **Streamlit**, it provides interactive dashboards, real-time data visualization, and intelligent predictions to enhance decision-making and transparency.

---

## 🔧 Features

* ✅ Streamlit-based interactive dashboard
* 🔍 Query interface for **medium & complex SQL analytics**
* 📈 Charts and metrics (e.g., arrest rates, drug-related stops)
* 📊 Visual insights by **gender**, **violation type**, and **region**
* 🧠 Prediction module for stop outcome and likely violation based on driver input
* 🔄 Data caching using `@st.cache_data` for faster access

---

## 📁 Tech Stack

| Layer    | Technology                         |
| -------- | ---------------------------------- |
| Frontend | Streamlit                          |
| Backend  | Python (Pandas, Plotly, Streamlit) |
| Database | MySQL                              |
| ORM      | SQLAlchemy + PyMySQL               |

---

## 📸 Screenshots

<img width="1366" height="768" alt="Streamlit Output(1)" src="https://github.com/user-attachments/assets/23011077-a954-4c46-8e39-8d9d2c29b981" />
<img width="1366" height="768" alt="StreamlitOutput(2)" src="https://github.com/user-attachments/assets/272cf351-5273-45ad-9f3f-8ab18b272742" />
<img width="1366" height="768" alt="StreamlitOutput(3)" src="https://github.com/user-attachments/assets/1adab8b5-49c3-4c2d-a7db-79bafc687583" />
<img width="1366" height="768" alt="StreamlitOutput(4)" src="https://github.com/user-attachments/assets/92862569-e952-426a-8fd8-2c2a1f3e6274" />
<img width="1366" height="768" alt="StreamlitOutput(5)" src="https://github.com/user-attachments/assets/1d9072d3-7200-4db3-81b6-80db0ef8b77b" />
<img width="1366" height="768" alt="StreamlitOutput(6)" src="https://github.com/user-attachments/assets/58a14a08-292a-47df-a2d6-2c42825fe2c8" />
<img width="1366" height="768" alt="StreamlitOutput(7)" src="https://github.com/user-attachments/assets/f59895c2-d7ea-4318-a982-07a93d7cffc2" />
---

## 📂 Folder Structure

```
securecheck/
│
├── securepolicelog.py           # Main Streamlit App
├── clean_data.py                # Script to clean and preprocess raw data
├── data_insert.py               # Script to load cleaned data into MySQL
├── cleaned_traffic_data.csv     # Cleaned CSV data file
├── requirements.txt             # Python dependencies
└── README.md                    # Project documentation
```

---

## ⚙️ How to Run

### 1. Clone the Repository

```bash
git clone https://github.com/ThilagavathyVenkatesan/policesecurelog.git
cd policesecurelog
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Set Up MySQL

* Create a database:

```sql
CREATE DATABASE securecheck1;
```

* Then create the `traffic_stops` table:

```sql
CREATE TABLE traffic_stops (
    id INT AUTO_INCREMENT PRIMARY KEY,
    stop_date DATE,
    stop_time TIME,
    country_name VARCHAR(100),
    driver_gender VARCHAR(10),
    driver_age INT,
    driver_race VARCHAR(50),
    search_conducted TINYINT(1),
    search_type VARCHAR(100),
    drugs_related_stop TINYINT(1),
    stop_duration VARCHAR(50),
    stop_outcome VARCHAR(100),
    violation VARCHAR(100),
    vehicle_number VARCHAR(20)
);
```

### 4. Load Data into MySQL

```bash
python data_insert.py
```

### 5. Run the Streamlit Dashboard

```bash
streamlit run securepolicelog.py
```

---

## 📌 Sample SQL Queries (Medium & Complex)

* **Top 10 vehicles in drug-related stops**
* **Arrest rates by age and gender**
* **Time-of-day analysis for stops**
* **Violation types leading to searches**
* **Country-wise stop breakdown**

---

## 📝 Prediction Example

> “A 27-year-old male driver was stopped for **Speeding** at **10:35 PM**.
> No search was conducted and the stop was not drug-related.
> **The likely outcome is a Warning.**”

---

## 🔒 Future Scope

* 🔐 Admin/Officer **role-based login**
* 🚨 Automatic **flagged vehicle detection**
* 📡 Real-time **alerts and notifications**
* 🧾 Export reports as **PDF**

---

## ❇️ Credits

Built with ❤️ using [Streamlit](https://streamlit.io/), [SQLAlchemy](https://www.sqlalchemy.org/), and [MySQL](https://www.mysql.com/)

---

