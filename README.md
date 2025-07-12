🚨 SecureCheck: Police Check Post Digital Ledger
SecureCheck is a digital record management system designed for law enforcement agencies to track, analyze, and manage traffic stop logs. Built with Python, MySQL, and Streamlit, it enables interactive dashboards, real-time data visualization, and intelligent predictions to support decision-making and enhance transparency.
________________________________________
##🔧 Features
•	✅ Streamlit-based interactive dashboard
•	🔍 Query interface for medium & complex SQL analytics
•	📈 Charts and metrics for key statistics (e.g., arrest rates, drug-related stops)
•	📊 Visual insights by gender, violation type, and region
•	🧠 Prediction module for stop outcome and likely violation based on driver input
•	🔄 Data caching for fast access
________________________________________
📁 Tech Stack
| Layer           | Technology                         |
| --------------- | ---------------------------------- |
| Frontend        | [Streamlit](https://streamlit.io/) |
| Backend (Logic) | Python (Pandas, Plotly)            |
| Database        | MySQL with SQLAlchemy              |
| ORM             | SQLAlchemy + PyMySQL               |

________________________________________
📸 Screenshots
![Streamlit Output(1)](https://github.com/user-attachments/assets/6928f8be-cff1-40e8-bce4-0be565fc4d7e)
![StreamlitOutput(2)](https://github.com/user-attachments/assets/446b051e-2f34-4e9e-8229-b0b32ec1c216)
![StreamlitOutput(3)](https://github.com/user-attachments/assets/096f94d9-b95b-4cbb-9310-64e08f1911c4)
![StreamlitOutput(4)](https://github.com/user-attachments/assets/060112de-7d61-49af-96a6-2d2d3d331ffb)
![StreamlitOutput(5)](https://github.com/user-attachments/assets/2ec07d7a-cf2b-44ae-86cb-dd26499d0982)
![StreamlitOutput(6)](https://github.com/user-attachments/assets/577103de-4adf-46bb-93ac-c51bf02309ae)
![StreamlitOutput(7)](https://github.com/user-attachments/assets/f4c83e40-4e77-454f-9bfd-ddab5ce4b6ad)
________________________________________
![Folder Structure](https://github.com/user-attachments/assets/4864eb9f-d274-451e-9ce8-0b8f9290c4af)
______________________________________
⚙️ How to Run
1. Clone this repo
bash
git clone https://github.com/ThilagavathyVenkatesan/policeseurelog.git
cd policesecurelog
2. Set up Python environment
bash
pip install streamlit pandas streamlit sqlalchemy pymysql plotly
3. Set up MySQL
•	Create a database securecheck1
•	Run the police_logs table creation SQL (see below)
sql
CopyEdit
CREATE TABLE police_logs (
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
4. clean data
bash
python clean_data.py
4. Load data
bash
python data_insert.py
5. Run the dashboard
bash
streamlit run securepolicelog.py
________________________________________
![Screenshot (24)](https://github.com/user-attachments/assets/c5204d05-fe98-4f47-94ee-677e970bd36a)
________________________________________
🤖 Prediction Example
“A 27-year-old male driver was stopped for Speeding at 10:35 PM. No search was conducted and the stop was not drug-related. The likely outcome is a Warning.”
________________________________________
![f](https://github.com/user-attachments/assets/bda26b89-fffc-4dfc-9d98-5c8c89ef0780)
________________________________________
🧠 Credits
Built with ❤️ using Streamlit, SQLAlchemy, and MySQL.
________________________________________

