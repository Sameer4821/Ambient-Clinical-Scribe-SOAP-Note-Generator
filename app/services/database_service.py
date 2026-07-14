import os
from dotenv import load_dotenv
from supabase import create_client, Client

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_SERVICE_ROLE_KEY")

class DatabaseService:
    _client: Client = None

    @classmethod
    def get_client(cls) -> Client:
        """Initialize and return the Supabase client."""
        if cls._client is None:
            if not SUPABASE_URL or not SUPABASE_KEY:
                raise ValueError("SUPABASE_URL and SUPABASE_SERVICE_ROLE_KEY must be set in the environment.")
            cls._client = create_client(SUPABASE_URL, SUPABASE_KEY)
        return cls._client

    @classmethod
    def save_consultation(cls, filename: str, transcript: list, soap_note: dict, patient_phone: str = None, icd10_code: str = "J02.0") -> dict:
        """
        Save a new consultation (transcript, SOAP note, phone, and ICD-10 code) to the consultations table.
        """
        try:
            client = cls.get_client()
            data = {
                "filename": filename,
                "transcript": transcript,
                "soap_note": soap_note,
                "patient_phone": patient_phone,
                "icd10_code": icd10_code
            }
            # Insert into database
            response = client.table("consultations").insert(data).execute()
            # Return the first inserted record metadata
            if response.data:
                return response.data[0]
            return {}
        except Exception as e:
            print(f"Error saving consultation to Supabase: {str(e)}")
            raise e

    @classmethod
    def get_consultation_history(cls) -> list:
        """
        Retrieve all consultations ordered by creation date descending.
        """
        try:
            client = cls.get_client()
            response = client.table("consultations").select("*").order("created_at", desc=True).execute()
            return response.data or []
        except Exception as e:
            print(f"Error fetching consultation history from Supabase: {str(e)}")
            raise e

    @classmethod
    def get_consultation_by_phone(cls, phone: str) -> list:
        """
        Retrieve all consultations for a patient phone number ordered by creation date descending.
        """
        try:
            client = cls.get_client()
            response = client.table("consultations").select("*").eq("patient_phone", phone).order("created_at", desc=True).execute()
            return response.data or []
        except Exception as e:
            print(f"Error fetching consultation by phone from Supabase: {str(e)}")
            raise e

    @classmethod
    def finalize_consultation(cls, consultation_id: str, soap_note: dict, icd10_code: str) -> dict:
        """
        Update an existing consultation record with revised SOAP note and ICD-10 code.
        """
        try:
            client = cls.get_client()
            data = {
                "soap_note": soap_note,
                "icd10_code": icd10_code
            }
            response = client.table("consultations").update(data).eq("id", consultation_id).execute()
            if response.data:
                return response.data[0]
            return {}
        except Exception as e:
            print(f"Error finalizing consultation in Supabase: {str(e)}")
            raise e
