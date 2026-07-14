import React, { useState } from 'react';
import './App.css';

function App() {
  const [phoneNumber, setPhoneNumber] = useState('');
  const [loading, setLoading] = useState(false);
  const [record, setRecord] = useState(null);
  const [message, setMessage] = useState('');
  const [messageType, setMessageType] = useState('info'); // info, success, error
  const [finalizing, setFinalizing] = useState(false);

  // SOAP fields state
  const [subjective, setSubjective] = useState('');
  const [objective, setObjective] = useState('');
  const [assessment, setAssessment] = useState('');
  const [plan, setPlan] = useState('');
  const [icdCode, setIcdCode] = useState('');

  const showNotification = (text, type = 'info') => {
    setMessage(text);
    setMessageType(type);
    setTimeout(() => setMessage(''), 5000);
  };

  const handleSearch = async (e) => {
    e.preventDefault();
    if (!phoneNumber.trim()) {
      showNotification('Please enter a valid phone number', 'error');
      return;
    }

    setLoading(true);
    setRecord(null);
    try {
      const response = await fetch(`http://127.0.0.1:8000/consultations/search?phone=${encodeURIComponent(phoneNumber)}`);
      if (!response.ok) {
        throw new Error('Failed to retrieve record');
      }
      const data = await response.json();
      setRecord(data);
      
      // Load SOAP note fields
      const soap = data.soap_note || {};
      setSubjective(soap.subjective || '');
      setObjective(soap.objective || '');
      setAssessment(soap.assessment || '');
      setPlan(soap.plan || '');
      setIcdCode(data.icd10_code || 'J02.0 - Streptococcal pharyngitis');

      if (data.id === "00000000-0000-0000-0000-000000000000") {
        showNotification('No database record found. Loaded sandbox clinical mock dataset.', 'info');
      } else {
        showNotification('Patient record retrieved successfully from Supabase!', 'success');
      }
    } catch (err) {
      showNotification(`Error: ${err.message}`, 'error');
    } finally {
      setLoading(false);
    }
  };

  const handleFinalize = async () => {
    if (!record) return;

    setFinalizing(true);
    try {
      const payload = {
        consultation_id: record.id,
        soap_note: {
          subjective,
          objective,
          assessment,
          plan
        },
        icd10_code: icdCode,
        patient_phone: phoneNumber
      };

      const response = await fetch('http://127.0.0.1:8000/consultations/finalize', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(payload)
      });

      if (!response.ok) {
        throw new Error('Server returned error response');
      }

      const data = await response.json();
      
      if (data.status === 'success') {
        showNotification(data.message || 'Consultation finalized and saved successfully!', 'success');
        // Update local record data ID if mock converted
        if (data.data && data.data.id) {
          setRecord(prev => ({ ...prev, id: data.data.id }));
        }
      } else {
        throw new Error(data.message || 'Finalization failed');
      }
    } catch (err) {
      showNotification(`Error finalising: ${err.message}`, 'error');
    } finally {
      setFinalizing(false);
    }
  };

  return (
    <div className="app-container">
      <header className="dashboard-header">
        <div className="logo-container">
          <span className="logo-pulse"></span>
          <h1>ClinicalScribe <span>Portal</span></h1>
        </div>
        <div className="status-badge">
          <span className="badge-dot"></span> System Online
        </div>
      </header>

      {message && (
        <div className={`notification-banner banner-${messageType}`}>
          <p>{message}</p>
        </div>
      )}

      <main className="dashboard-main">
        {/* Search Panel */}
        <section className="search-section">
          <h2>Patient Record Retrieval</h2>
          <p className="search-instruction">Enter patient phone number to retrieve transcript, SOAP note and ICD codes.</p>
          <form onSubmit={handleSearch} className="search-form">
            <input
              type="text"
              placeholder="e.g. 123-456-7890"
              value={phoneNumber}
              onChange={(e) => setPhoneNumber(e.target.value)}
              className="search-input"
              disabled={loading || finalizing}
            />
            <button type="submit" className="search-button" disabled={loading || finalizing}>
              {loading ? <span className="spinner"></span> : 'Retrieve Record'}
            </button>
          </form>
        </section>

        {/* Content Area */}
        {record && (
          <div className="layout-grid">
            
            {/* Raw Transcript Column */}
            <section className="column-card transcript-column">
              <div className="card-header">
                <h3>Raw Audio Transcript</h3>
                <span className="card-badge">{record.filename}</span>
              </div>
              <div className="card-content transcript-list">
                {record.transcript && record.transcript.map((block, idx) => {
                  const isDoctor = block.speaker.toLowerCase().includes('doctor');
                  return (
                    <div 
                      key={idx} 
                      className={`transcript-bubble ${isDoctor ? 'bubble-doctor' : 'bubble-patient'}`}
                    >
                      <div className="bubble-speaker">
                        {isDoctor ? '🩺 ' : '👤 '}{block.speaker}
                      </div>
                      <div className="bubble-text">{block.text}</div>
                    </div>
                  );
                })}
              </div>
            </section>

            {/* Editable SOAP Column */}
            <section className="column-card editor-column">
              <div className="card-header">
                <h3>SOAP Note Editor (Human-in-the-Loop)</h3>
                <span className="card-badge edit-badge">Draft Mode</span>
              </div>
              <div className="card-content editor-form">
                
                {/* Subjective */}
                <div className="editor-group">
                  <label htmlFor="subjective">Subjective (Symptoms, complaints, history)</label>
                  <textarea
                    id="subjective"
                    value={subjective}
                    onChange={(e) => setSubjective(e.target.value)}
                    placeholder="Enter patient reports..."
                    disabled={finalizing}
                  />
                </div>

                {/* Objective */}
                <div className="editor-group">
                  <label htmlFor="objective">Objective (Vital signs, physical examinations)</label>
                  <textarea
                    id="objective"
                    value={objective}
                    onChange={(e) => setObjective(e.target.value)}
                    placeholder="Enter exam findings..."
                    disabled={finalizing}
                  />
                </div>

                {/* Assessment */}
                <div className="editor-group">
                  <label htmlFor="assessment">Assessment (Diagnoses, clinical impressions)</label>
                  <textarea
                    id="assessment"
                    value={assessment}
                    onChange={(e) => setAssessment(e.target.value)}
                    placeholder="Enter diagnosis..."
                    disabled={finalizing}
                  />
                </div>

                {/* Plan */}
                <div className="editor-group">
                  <label htmlFor="plan">Plan (Treatments, prescriptions, tests)</label>
                  <textarea
                    id="plan"
                    value={plan}
                    onChange={(e) => setPlan(e.target.value)}
                    placeholder="Enter plan details..."
                    disabled={finalizing}
                  />
                </div>

                {/* ICD-10 Billing Code */}
                <div className="editor-group icd-group">
                  <label htmlFor="icd-code">Primary ICD-10 Billing Recommendation</label>
                  <input
                    type="text"
                    id="icd-code"
                    value={icdCode}
                    onChange={(e) => setIcdCode(e.target.value)}
                    placeholder="Code - Description"
                    className="icd-input"
                    disabled={finalizing}
                  />
                </div>

                {/* Finalize Button */}
                <div className="action-row">
                  <button 
                    onClick={handleFinalize} 
                    className="finalize-button"
                    disabled={finalizing}
                  >
                    {finalizing ? (
                      <>
                        <span className="spinner btn-spinner"></span> Finalizing Note...
                      </>
                    ) : (
                      'Finalize & Save to Supabase'
                    )}
                  </button>
                </div>
              </div>
            </section>
          </div>
        )}
      </main>
    </div>
  );
}

export default App;
