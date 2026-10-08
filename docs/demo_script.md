# Five-Minute Demo Script

**Setup (before you present):** `streamlit run app.py` from the `consentguard` folder, Demo mode on, browser full-screen. Practise once; the demos run instantly.

---

### 0:00-0:30 · The hook
> "Raise your hand if you read the last privacy notice you accepted. ConsentGuard helps you **understand what you are agreeing to**. It explains a notice, checks whether each data request fits its purpose, and backs every point with an exact quote."

Show the sidebar: **Demo mode**, with no API key and synthetic documents. Point out the limits text.

### 0:30-2:00 · A problematic policy (QuickBasket, a grocery delivery app)
1. **Demo examples**, then scenario **1**, then **Run this demo**, then the **Report** tab.
2. Read the overall label aloud: **Substantial concerns found**, with the reason "3 high-severity findings supported by quoted text".
3. Open **F01**: contacts and microphone are mandatory for grocery delivery. Read the verified quote: *"If you do not allow these permissions the app will not work."*
4. Scroll to the **permission-purpose map**: location *needs explanation* (it fits delivery, but not always-on), contacts and microphone *disproportionate*.
5. Point to **Legal context: verified, not yet in force (commences 2027-05-13)**.
> "We don't pretend the law already requires this. The DPDP consent duties are notified but phase in next May, and ConsentGuard says so."

### 2:00-3:00 · A more proportionate policy (MeetLoop, video calling)
1. Run scenario **2**, then open **Report**.
2. Overall: **No major concerns found in supplied text**.
3. Show that the microphone is **proportionate** here.
> "Same permission, different verdict. A microphone fits a calling app and doesn't fit grocery delivery. The judgement depends on purpose."
4. Show **CG-CN-04**: marketing is a separate, optional choice.

### 3:00-4:00 · Incomplete evidence (ShopEase excerpt)
1. Run scenario **6**, then open **Report**.
2. Overall: **Insufficient information**.
3. Open the retention finding and show the **adjustment** notes: severity capped to low, confidence lowered, because "absence in an excerpt is weak evidence."
> "Missing information makes us less certain. It doesn't make the company guilty."

### 4:00-4:40 · A follow-up question
1. Switch back to scenario **1** (QuickBasket) and open **Ask ConsentGuard**.
2. Ask: **"How long do they keep my data?"** The answer shows paragraph **P014** with its quote.
3. Ask: **"Is my data stored outside India?"** The answer is *Not found in the document*.
> "If the document doesn't say, ConsentGuard says it can't find it. It doesn't guess." (Note: demo-mode Q&A uses keyword matching and shows related passages; live mode uses Claude with the same quote checks.)

### 4:40-5:00 · Close
- Mention the **Reset and clear session** button and what it clears.
- Mention the **Download** buttons and the notice that exports contain your quotes.
> "One agent, nine reusable skills, every claim checkable. Not a compliance stamp; a way to understand before you agree."

**Backup:** if anything fails, open the pre-generated reports in `examples/expected_outputs/reports/`.
