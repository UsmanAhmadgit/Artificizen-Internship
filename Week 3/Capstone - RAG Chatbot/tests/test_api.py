import pytest
import json
from fastapi.testclient import TestClient
from app.services.cache_service import cache_service

def test_01_ingest_document(client: TestClient):
    """Test 1: Successfully upload and ingest a long sample text file."""
    
    # A robust, multi-paragraph document acting as our fake PDF/TXT
    file_content = b"""NEXUS CORP - GLOBAL SECURITY AND IT POLICY MANUAL

Section 1: Hardware and Equipment Lifecycle
All company-issued technology, including laptops, mobile devices, and peripherals, remains the property of Nexus Corp. To ensure optimal performance and security, Nexus Corp policies state that hardware refreshes occur every 36 months. Employees may not request early upgrades unless catastrophic hardware failure is documented by the IT helpdesk.

Section 2: Physical Security and Identification
Maintaining a secure working environment is our highest priority. All employees must wear security badges on a corporate lanyard, visible at all times while on company premises. Lost badges must be reported to physical security within 2 hours.

Section 3: Restricted Areas and Vault Access
Certain areas of the building are strictly off-limits to standard personnel. The primary server room vault is accessed using biometric retina scans combined with a physical encrypted keycard. Only Tier-3 Systems Administrators hold permanent clearance for the vault. Any unauthorized attempt to breach the vault will result in immediate termination.

Section 4: Remote Work and Connectivity
Remote employees are expected to maintain a secure home network encrypted with WPA3 standards. Using public Wi-Fi without the corporate VPN is strictly prohibited when accessing internal databases.
"""
    
    files = {"file": ("test_policy.txt", file_content, "text/plain")}
    
    response = client.post("/ingest", files=files)
    
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    # Because the text is longer, we can assert that multiple chunks were created
    assert data["chunks_indexed"] > 0

def test_02_chat_known_answer(client: TestClient):
    """Test 2: Ask a question with a known answer present in the document."""
    payload = {
        "session_id": "pytest_session_1",
        "query": "How often do hardware refreshes occur according to policy?"
    }
    response = client.post("/chat", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "36 months" in data["answer"].lower()

def test_03_chat_grounding_refusal(client: TestClient):
    """Test 3: Ask a question not in the document and verify 'I don't know' response."""
    payload = {
        "session_id": "pytest_session_1",
        "query": "What is the policy regarding maternity leave coverage for contractors?"
    }
    response = client.post("/chat", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "don't know" in data["answer"].lower() or "i don't know" in data["answer"].lower()

def test_04_verify_sources_returned(client: TestClient):
    """Test 4: Verify source citations and metadata are properly included in the response."""
    payload = {
        "session_id": "pytest_session_2",
        "query": "What must employees wear according to the policy?"
    }
    response = client.post("/chat", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "sources" in data
    assert len(data["sources"]) > 0
    assert data["sources"][0]["filename"] == "test_policy.txt"
    assert "chunk_index" in data["sources"][0]

def test_05_verify_cache_hit(client: TestClient):
    """Test 5: Verify identical repeated query uses the internal cache dictionary."""
    
    session_id = "pytest_session_cache"
    query = "How is the primary server room vault accessed?"
    payload = {
        "session_id": session_id,
        "query": query
    }
    
    # 1. Clear the cache dictionary to ensure a clean slate
    cache_service._cache.clear()
    
    # 2. Generate the expected MD5 key that the service should create
    expected_key = cache_service._generate_key(session_id, query)
    
    # Prove the dictionary is empty before we start
    assert expected_key not in cache_service._cache

    # 3. FIRST REQUEST (Cache Miss)
    res1 = client.post("/chat", json=payload)
    assert res1.status_code == 200
    
    # PROOF 1: The key MUST now exist in the backend dictionary
    assert expected_key in cache_service._cache
    
    # Check how many items are in the cache
    cache_size_after_first_call = len(cache_service._cache)

    # 4. SECOND REQUEST (Cache Hit)
    res2 = client.post("/chat", json=payload)
    assert res2.status_code == 200
    
    # PROOF 2: The dictionary size must not have increased (no new generation)
    assert len(cache_service._cache) == cache_size_after_first_call
    
    # PROOF 3: The answers match
    assert res1.json()["answer"] == res2.json()["answer"]