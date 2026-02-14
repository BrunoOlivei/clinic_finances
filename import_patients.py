"""Script to import patients from CSV into the database."""

from core import SessionLocal, create_tables, settings
from services import PatientService


def main():
    """Main script to import patients from CSV."""
    print("=" * 60)
    print("PATIENT IMPORT - PostgreSQL + SQLAlchemy")
    print("=" * 60 + "\n")

    try:
        print(
            f"Connecting to: {settings.postgres_host}:{settings.postgres_port}/{settings.postgres_db}"
        )

        print("\nCreating/verifying tables...")
        create_tables()
        print()

        with SessionLocal() as session:
            service = PatientService(session)

            print("Importing patients from current month CSV...")
            service.import_from_csv()
            print()

            total = service.count()
            print(f"Total patients in database: {total}")

        print("\n" + "=" * 60)
        print("IMPORT COMPLETED SUCCESSFULLY!")
        print("=" * 60)

    except FileNotFoundError as e:
        print(f"\nError: {e}")
        print("Make sure the CSV file exists for the current year/month.")
    except Exception as e:
        print(f"\nError: {e}")
        raise


if __name__ == "__main__":
    main()
