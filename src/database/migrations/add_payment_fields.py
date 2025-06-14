import sqlite3
from config.config import get_settings

settings = get_settings()

def upgrade():
    # Подключаемся к базе данных напрямую через sqlite3
    conn = sqlite3.connect('doctor_gpt.db')
    cursor = conn.cursor()
    
    try:
        # Добавляем новые колонки
        cursor.execute('ALTER TABLE subscriptions ADD COLUMN payment_amount REAL')
        cursor.execute('ALTER TABLE subscriptions ADD COLUMN payment_status TEXT')
        cursor.execute('ALTER TABLE subscriptions ADD COLUMN payment_created_at TIMESTAMP')
        cursor.execute('ALTER TABLE subscriptions ADD COLUMN payment_paid_at TIMESTAMP')
        cursor.execute('ALTER TABLE subscriptions ADD COLUMN payment_method TEXT')
        cursor.execute('ALTER TABLE subscriptions ADD COLUMN payment_description TEXT')
        
        conn.commit()
        print("Migration completed successfully")
    except sqlite3.OperationalError as e:
        if "duplicate column name" in str(e):
            print("Columns already exist, skipping...")
        else:
            raise
    finally:
        conn.close()

if __name__ == '__main__':
    upgrade() 