# 🚀 Gramin-Setu Agentic Deployment: Testing Guide

This guide contains the exact terminal commands needed to showcase the three "No-UI" deployment interfaces of the Antyodaya Semantic Engine.

> **Important Note:**
> To run these deployments, make sure your global Python environment has all dependencies installed by running:
> `pip install -r requirements.txt`

---

## 🎙️ 1. The AI-PCO (Desktop Voice Box)
*Simulates a standalone Bhashini Box or Smart Speaker placed at a Gram Panchayat.*

**How to Test:**
1. Open your terminal inside the project folder (`antyodaya_semantic_engine`).
2. Run the deployment script:
   ```powershell
   python ai_pco_terminal.py
   ```
3. Press **Enter**, and speak your query into your laptop microphone in English or Hindi (e.g., *"Kisan Samman Nidhi kya hai?"*).
4. The terminal will process the Agentic RAG pipeline and **speak the answer back out loud** via your speakers.

---

## 💻 2. The Assisted Digital Kiosk (Web Dashboard)
*Simulates the portal a CSC (Common Service Center) operator would use to help farmers.*

**How to Test:**
1. Open your terminal inside the project folder.
2. Start the FastAPI Brain server (keep this running!):
   ```powershell
   uvicorn app.main:app --reload
   ```
3. Open your web browser (Chrome/Edge) and navigate to:
   **[http://localhost:8000/web](http://localhost:8000/web)**
4. Click the green **Voice Button** on the screen. Speak your query, then click it again to stop. The dashboard will instantly generate the AI response and play it audibly.

---

## ☎️ 3. The Missed Call / IVR Bot
*Simulates a toll-free farmer helpline powered by Bhashini AI.*

**How to Test:**
1. Keep the FastAPI server from Test 2 running in one terminal.
2. Open a **new, separate terminal tab** and run `ngrok` to expose your local code to Twilio:
   ```powershell
   ngrok http 8000
   ```
3. Copy the secure Forwarding URL (e.g., `https://abc-123.ngrok-free.app`).
4. Log into your **Twilio Console** -> Phone Numbers -> Manage -> Active Numbers.
5. Under the **"Voice & Fax"** section, paste the URL into the "A CALL COMES IN (Webhook)" field, and add `/incoming-call` to the end.
   *(Example: `https://abc-123.ngrok-free.app/incoming-call`)*
6. Save the Twilio settings and **call that Twilio number from your real cell phone.** The AI will greet you, and you can speak to it!
