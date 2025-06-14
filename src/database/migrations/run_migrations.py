from add_payment_fields import upgrade
from src.utils.logger import log_info, log_error

def run_migrations():
    try:
        log_info("Starting database migration...")
        upgrade()
        log_info("Migration completed successfully")
    except Exception as e:
        log_error(f"Migration failed: {str(e)}")
        raise

if __name__ == '__main__':
    run_migrations() 