import sys
import io

# Force UTF-8 encoding for stdout to prevent UnicodeEncodeError on Windows console
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

from app.services.database_service import DatabaseService

def verify_db():
    print("=" * 70)
    print("SUPABASE DATABASE VERIFICATION TEST")
    print("=" * 70)
    print()
    
    print("Attempting to connect to Supabase...")
    try:
        client = DatabaseService.get_client()
        print("✓ Connected to Supabase successfully!")
        print()
    except Exception as e:
        print(f"❌ Failed to connect to Supabase: {e}")
        return

    # Mock data to insert
    mock_filename = "mock_test_session.mp3"
    mock_transcript = [
        {"speaker": "Speaker 1: Doctor", "text": "Hello, how are you feeling today?"},
        {"speaker": "Speaker 2: Patient", "text": "I have been having headache since yesterday."}
    ]
    mock_soap = {
        "subjective": "Patient reports headache since yesterday.",
        "objective": "Not recorded.",
        "assessment": "Headache, unspecified.",
        "plan": "Monitor for symptoms."
    }

    print("Attempting to insert a mock consultation record...")
    try:
        record = DatabaseService.save_consultation(
            filename=mock_filename,
            transcript=mock_transcript,
            soap_note=mock_soap
        )
        print("✓ Record saved successfully!")
        print(f"  Saved Record ID: {record.get('id')}")
        print(f"  Saved At: {record.get('created_at')}")
        print()
    except Exception as e:
        print(f"❌ Failed to save consultation: {e}")
        print("\nIMPORTANT: Ensure you have created the 'consultations' table in your Supabase SQL Editor!")
        print("SQL schema:")
        print("create table consultations (")
        print("  id uuid default gen_random_uuid() primary key,")
        print("  created_at timestamp with time zone default timezone('utc'::text, now()) not null,")
        print("  filename text not null,")
        print("  transcript jsonb not null,")
        print("  soap_note jsonb not null")
        print(");")
        print()
        return

    print("Attempting to retrieve history...")
    try:
        history = DatabaseService.get_consultation_history()
        print("✓ History retrieved successfully!")
        print(f"  Total records found: {len(history)}")
        print()
        print("Latest Record Details:")
        if history:
            latest = history[0]
            print(f"  ID: {latest.get('id')}")
            print(f"  Filename: {latest.get('filename')}")
            print(f"  SOAP Plan: {latest.get('soap_note', {}).get('plan')}")
        print()
    except Exception as e:
        print(f"❌ Failed to retrieve history: {e}")
        return

    print("=" * 70)
    print("✓ SUPABASE DATABASE INTEGRATION VERIFIED SUCCESSFULLY")
    print("=" * 70)
    print()

if __name__ == "__main__":
    verify_db()
