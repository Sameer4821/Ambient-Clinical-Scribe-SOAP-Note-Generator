"""
Test script to verify Week 2 Prompt Engineering and Clinical Structuring.
Feeds a raw, diarized transcript to the LLM pipeline and validates SOAP note extraction.
"""

import sys
import io

# Force UTF-8 encoding for stdout to prevent UnicodeEncodeError on Windows console
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

from app.services.soap_service import SOAPService

def verify_week2():
    print("=" * 70)
    print("WEEK 2 VERIFICATION TEST - Prompt Engineering & Clinical Structuring")
    print("=" * 70)
    print()
    
    # 1. Define the test transcript provided in the requirement
    transcript = (
        "Speaker 1: Doctor - Good morning. What brings you in today?\n"
        "Speaker 2: Patient - I've had a severe headache and a sore throat for three days.\n"
        "Speaker 1: Doctor - Let me check your vitals. Your temperature is 101.2°F and your "
        "blood pressure is 120/80. Based on your symptoms, it looks like you have a bacterial "
        "strep infection. I'm going to prescribe you Amoxicillin and I want you to get plenty of rest."
    )
    
    print("Sample Transcript Input:")
    print("-" * 70)
    print(transcript)
    print("-" * 70)
    print()
    
    # 2. Run the transcript through our LLM SOAP generation service
    print("Sending transcript to Gemini SOAP service...")
    try:
        soap_note = SOAPService.generate_soap(transcript)
        print("SUCCESS: SOAP note extracted successfully!")
        print()
    except Exception as e:
        print(f"FAILED: SOAP note extraction failed with error: {e}")
        return
    
    # 3. Print the generated SOAP Note
    print("Structured SOAP Note Output (JSON):")
    print("-" * 70)
    import json
    print(json.dumps(soap_note.model_dump(), indent=2))
    print("-" * 70)
    print()
    
    # 4. Perform assertion checks for Success Criteria
    print("Verifying Success Criteria:")
    print("-" * 70)
    
    # Subjective checks
    subj = soap_note.subjective.lower()
    has_headache = "headache" in subj
    has_throat = "throat" in subj
    has_three_days = "three" in subj or "3" in subj
    print(f"Subjective: {'[OK]' if (has_headache and has_throat and has_three_days) else '[FAIL]'}")
    print(f"  - Extracted: \"{soap_note.subjective}\"")
    print(f"  - Details: Headache? {has_headache}, Sore Throat? {has_throat}, Duration? {has_three_days}")
    print()
    
    # Objective checks
    obj = soap_note.objective.lower()
    has_temp = "101.2" in obj
    has_bp = "120/80" in obj
    print(f"Objective: {'[OK]' if (has_temp and has_bp) else '[FAIL]'}")
    print(f"  - Extracted: \"{soap_note.objective}\"")
    print(f"  - Details: Temp 101.2? {has_temp}, BP 120/80? {has_bp}")
    print()
    
    # Assessment checks
    assess = soap_note.assessment.lower()
    has_strep = "strep" in assess or "bacterial" in assess
    print(f"Assessment: {'[OK]' if has_strep else '[FAIL]'}")
    print(f"  - Extracted: \"{soap_note.assessment}\"")
    print(f"  - Details: Diagnosis bacterial strep infection? {has_strep}")
    print()
    
    # Plan checks
    plan = soap_note.plan.lower()
    has_amoxicillin = "amoxicillin" in plan
    has_rest = "rest" in plan
    print(f"Plan: {'[OK]' if (has_amoxicillin and has_rest) else '[FAIL]'}")
    print(f"  - Extracted: \"{soap_note.plan}\"")
    print(f"  - Details: Amoxicillin? {has_amoxicillin}, Rest? {has_rest}")
    print()
    
    # Overall summary
    all_passed = (has_headache and has_throat and has_three_days and 
                  has_temp and has_bp and has_strep and has_amoxicillin and has_rest)
    
    print("=" * 70)
    if all_passed:
        print("SUCCESS: ALL WEEK 2 SUCCESS CRITERIA VERIFIED AND PASSED!")
    else:
        print("FAILED: Some Week 2 success criteria failed verification.")
    print("=" * 70)
    print()

if __name__ == "__main__":
    verify_week2()
