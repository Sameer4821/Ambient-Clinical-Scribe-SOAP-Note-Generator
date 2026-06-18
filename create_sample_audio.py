"""
Create sample audio file with doctor-patient conversation for testing.
Uses pyttsx3 for text-to-speech (no internet required).
"""

import pyttsx3
import os
from pathlib import Path

# Initialize text-to-speech engine
engine = pyttsx3.init()
engine.setProperty('rate', 150)  # Speech rate

# Ensure audio directory exists
audio_dir = Path("data/audio")
audio_dir.mkdir(parents=True, exist_ok=True)

# Sample doctor-patient dialogue
doctor_text = "Good morning, I'm Dr. Smith. How are you feeling today?"
patient_text = "Hi doctor. I've been having some chest pain for about a week now."
doctor_text_2 = "I'm sorry to hear that. Can you describe the pain? Is it sharp, dull, or pressure-like?"
patient_text_2 = "It's a dull ache, mostly when I walk or exert myself."
doctor_text_3 = "How long does each episode last?"
patient_text_3 = "Maybe five to ten minutes. It gets better when I sit down and rest."

output_file = str(audio_dir / "sample_consultation.mp3")

print("Creating sample audio file...")
print(f"Output: {output_file}")

# Generate audio
engine.save_to_file(doctor_text, output_file)
engine.runAndWait()

print(f"✓ Sample audio created: {output_file}")
print(f"✓ File size: {os.path.getsize(output_file) / 1024:.1f} KB")
print("\nSample dialogue:")
print(f"Doctor: {doctor_text}")
print(f"Patient: {patient_text}")
print(f"Doctor: {doctor_text_2}")
print(f"Patient: {patient_text_2}")
print(f"Doctor: {doctor_text_3}")
print(f"Patient: {patient_text_3}")
