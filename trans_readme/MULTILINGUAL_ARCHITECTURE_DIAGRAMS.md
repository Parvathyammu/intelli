# AskMOS Multilingual Architecture Diagrams

## 1. System Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                         USER INTERFACE                           │
│                    (React/Vite Frontend)                         │
├─────────────────────────────────────────────────────────────────┤
│                                                                   │
│  ┌──────────────────────────┐      ┌──────────────────────────┐ │
│  │   Language Selector      │      │    Chatbox Component     │ │
│  │  [EN] [हिं] [ES] [FR]    │      │  "Ask about satellites" │ │
│  └──────────────────────────┘      └──────────────────────────┘ │
│         │ (language change)                  │ (user query)      │
│         │                                    │                   │
└─────────┼────────────────────────────────────┼───────────────────┘
          │                                    │
          └────────────────────┬───────────────┘
                               │ (JSON request with language)
                    ┌──────────▼──────────┐
                    │  API /ask endpoint  │
                    └────────────────────┘
                               │
          ┌────────────────────┴───────────────────┐
          │                                        │
┌─────────▼──────────────────────────────────────▼───────────────┐
│                    FLASK BACKEND                                │
├────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │  1. Language Detection (Langdetect)                       │  │
│  │     Input: "आपके पास कौन से उपग्रह हैं?"               │  │
│  │     Output: "hi" (Hindi)                                  │  │
│  └──────────────────────────────────────────────────────────┘  │
│                                                                  │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │  2. Query Translation (Google Translate)                  │  │
│  │     Input: "आपके पास कौन से उपग्रह हैं?" (hi)          │  │
│  │     Output: "What satellites do you have?" (en)           │  │
│  └──────────────────────────────────────────────────────────┘  │
│                                                                  │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │  3. Query Processing                                      │  │
│  │     ├─ Generate Cypher Query (LLM)                        │  │
│  │     ├─ Execute on Neo4j Graph Database                    │  │
│  │     └─ Extract Relevant Data                              │  │
│  └──────────────────────────────────────────────────────────┘  │
│                                                                  │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │  4. Answer Generation (LLM - Groq/Llama)                 │  │
│  │     Input: Question + Graph Data                          │  │
│  │     Output: Answer in English                             │  │
│  └──────────────────────────────────────────────────────────┘  │
│                                                                  │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │  5. Response Translation (Google Translate)               │  │
│  │     Input: Answer in English                              │  │
│  │     Output: Answer in User's Language (hi, es, fr, etc)  │  │
│  └──────────────────────────────────────────────────────────┘  │
│                                                                  │
└────────────────────────────────────────────────────────────────┘
          │
          │ (JSON response with translated answer)
          │
┌─────────▼──────────────────────────────────────────────────────┐
│                    FRONTEND (React)                             │
├──────────────────────────────────────────────────────────────────┤
│                                                                   │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │  Update Chat History                                     │   │
│  │  - Add user message                                      │   │
│  │  - Add bot response (translated)                         │   │
│  │  - Display with language metadata                        │   │
│  └──────────────────────────────────────────────────────────┘   │
│                                                                   │
│  Display to User in Selected Language                            │
│                                                                   │
└──────────────────────────────────────────────────────────────────┘
```

---

## 2. Frontend Component Hierarchy

```
App.jsx
├── Navbar.jsx
│   ├── Logo
│   ├── Home Link
│   └── LanguageSelector.jsx  ⭐
│       ├── Globe Icon
│       └── Select Dropdown
│           ├── English (EN) 🇬🇧
│           ├── Hindi (HI) 🇮🇳
│           ├── Spanish (ES) 🇪🇸
│           └── French (FR) 🇫🇷
│
├── Home/Main Page
│   ├── Title (translated: t('chatbot.title'))
│   ├── ChatboxWithMultilingual.jsx  ⭐
│   │   ├── Header (translated)
│   │   ├── Messages Container
│   │   │   └── Message Item
│   │   │       ├── Text (in current language)
│   │   │       └── Language Metadata
│   │   └── Input Area
│   │       ├── Text Input (translated placeholder)
│   │       └── Send Button
│   │
│   └── Knowledge Graph Component
│       └── (also translated via i18n)
│
└── i18n Config  ⭐
    ├── Language Detector
    ├── Translation Files Loader
    └── localStorage Persistence
```

---

## 3. Data Flow Diagram

```
USER INTERACTION
      │
      ▼
┌─────────────────────────────────┐
│  User Types in Chatbox          │
│  "What satellites exist?"       │
└─────────────────────────────────┘
      │
      ▼
┌─────────────────────────────────┐
│  Send Button Click              │
│  - Current Language: "en"       │
│  - Query: "What satellites..." │
└─────────────────────────────────┘
      │
      ▼
┌─────────────────────────────────┐
│  Create API Request             │
│  {                              │
│    "query": "...",              │
│    "language": "en"             │
│  }                              │
└─────────────────────────────────┘
      │
      ▼ (HTTP POST to /ask)
┌────────────────────────────────────┐
│  BACKEND PROCESSING                │
├────────────────────────────────────┤
│  1. Detect Language (detect_lang)  │
│     Input: "What satellites..."    │
│     Output: "en"                   │
│  2. Translate Query (if needed)    │
│     Input: query (en)              │
│     Output: query_en (en)          │
│  3. Generate Cypher                │
│     Input: query_en                │
│     Output: MATCH...               │
│  4. Query Neo4j                    │
│     Input: Cypher                  │
│     Output: Graph Data             │
│  5. Generate Answer (LLM)          │
│     Input: query + data            │
│     Output: answer_en              │
│  6. Translate Answer (if needed)   │
│     Input: answer_en               │
│     Output: answer (target_lang)   │
│  7. Return Response                │
│     {                              │
│       "answer": "...",             │
│       "source_language": "en",     │
│       "target_language": "en"      │
│     }                              │
└────────────────────────────────────┘
      │
      ▼ (JSON Response)
┌─────────────────────────────────┐
│  Frontend Receives Response     │
│  - Extract answer               │
│  - Extract metadata             │
└─────────────────────────────────┘
      │
      ▼
┌─────────────────────────────────┐
│  Update UI                      │
│  - Add message to chat          │
│  - Display in current language  │
│  - Show timestamp               │
└─────────────────────────────────┘
      │
      ▼
┌─────────────────────────────────┐
│  User Sees Response             │
│  ✓ Answer displayed             │
│  ✓ In their language            │
│  ✓ In real-time                 │
└─────────────────────────────────┘
```

---

## 4. Language Detection & Translation Flow

```
                    USER INPUT
                         │
                         ▼
        ┌────────────────────────────────┐
        │  Input Text Analysis           │
        │  "আপনার কাছে কী স্যাটেলাইট?" │
        └────────────────────────────────┘
                         │
                         ▼
        ┌────────────────────────────────┐
        │  Langdetect Library            │
        │  Analyze character patterns    │
        │  Check probability             │
        └────────────────────────────────┘
                         │
                         ▼
        ┌────────────────────────────────┐
        │  Detected Language Result      │
        │  Language: Bengali (bn)        │
        │  Confidence: 0.95              │
        └────────────────────────────────┘
                         │
           ┌─────────────┼─────────────┐
           │             │             │
           ▼             ▼             ▼
    ┌──────────┐  ┌──────────┐  ┌──────────────┐
    │ English? │  │ English? │  │ Skip Trans?  │
    │ (en)     │  │ (detect) │  │              │
    │   NO     │  │   NO     │  │   YES        │
    └──────────┘  └──────────┘  └──────────────┘
           │             │             │
           └─────────────┼─────────────┘
                         │
                    YES  ▼  NO
           ┌─────────────────────────────┐
           │  Translate to English?      │
           │  (for processing)           │
           └─────────────────────────────┘
                    YES  │
                         ▼
    ┌──────────────────────────────────────┐
    │  Google Translate API                │
    │  bn → en                             │
    │  Input: "আপনার কাছে কী স্যাটেলাইট?" │
    │  Output: "What satellites do you...?│
    └──────────────────────────────────────┘
                         │
                         ▼
    ┌──────────────────────────────────────┐
    │  Process in English                  │
    │  1. Generate Cypher                  │
    │  2. Query Database                   │
    │  3. Generate Answer                  │
    │  Output: Answer in English           │
    └──────────────────────────────────────┘
                         │
                         ▼
    ┌──────────────────────────────────────┐
    │  Check Target Language               │
    │  User selected: "hi" (Hindi)         │
    │  Current answer: English             │
    │  Need translation? YES               │
    └──────────────────────────────────────┘
                         │
                         ▼
    ┌──────────────────────────────────────┐
    │  Google Translate API                │
    │  en → hi                             │
    │  Input: Answer in English            │
    │  Output: Answer in Hindi             │
    └──────────────────────────────────────┘
                         │
                         ▼
    ┌──────────────────────────────────────┐
    │  Return to Frontend                  │
    │  {                                   │
    │    "answer": "...",  (in Hindi)      │
    │    "source_lang": "bn",              │
    │    "target_lang": "hi"               │
    │  }                                   │
    └──────────────────────────────────────┘
                         │
                         ▼
    ┌──────────────────────────────────────┐
    │  Display to User                     │
    │  ✓ In Hindi (user's selected lang)   │
    │  ✓ With language metadata            │
    │  ✓ In real-time                      │
    └──────────────────────────────────────┘
```

---

## 5. i18n Configuration Flow

```
APP INITIALIZATION
      │
      ▼
┌──────────────────────────────────┐
│  Import i18n Config              │
│  (main.jsx)                      │
└──────────────────────────────────┘
      │
      ▼
┌──────────────────────────────────┐
│  i18next Initialization           │
│  (i18n/config.js)                │
├──────────────────────────────────┤
│ • Load HttpBackend               │
│ • Load Language Detector         │
│ • Initialize React i18next       │
│ • Set fallback language (en)     │
└──────────────────────────────────┘
      │
      ▼
┌──────────────────────────────────┐
│  Language Detection               │
├──────────────────────────────────┤
│ 1. Check localStorage            │
│    └─ i18nextLng key             │
│ 2. Check browser language        │
│    └─ navigator.language         │
│ 3. Fallback to 'en'              │
└──────────────────────────────────┘
      │
      ▼
┌──────────────────────────────────┐
│  Load Translation Files           │
├──────────────────────────────────┤
│ GET /locales/{lng}/translation   │
│ E.g., /locales/hi/translation.json
│                                   │
│ {                                │
│   "chatbot": {                   │
│     "title": "...",              │
│     "welcome": "...",            │
│     ...                          │
│   }                              │
│ }                                │
└──────────────────────────────────┘
      │
      ▼
┌──────────────────────────────────┐
│  i18n Ready                       │
│  - useTranslation() hook ready   │
│  - Components can render         │
│  - Language persistence active   │
└──────────────────────────────────┘
      │
      ▼
┌──────────────────────────────────┐
│  Component Rendering             │
│  const { t, i18n } = useI18n()   │
│  <h1>{t('chatbot.title')}</h1>  │
└──────────────────────────────────┘
      │
      ▼
┌──────────────────────────────────┐
│  User Changes Language            │
│  <select onChange={               │
│    i18n.changeLanguage()          │
│  }>                               │
└──────────────────────────────────┘
      │
      ▼
┌──────────────────────────────────┐
│  Translation Update               │
│ • Load new translation file      │
│ • Save to localStorage           │
│ • Re-render components           │
│ • All text updates               │
└──────────────────────────────────┘
```

---

## 6. File Organization

```
AskMOS/
│
├── frontend/
│   └── isro-hackathon/
│       ├── src/
│       │   ├── i18n/                    ⭐ NEW
│       │   │   └── config.js            ⭐ NEW
│       │   │
│       │   ├── locales/                 ⭐ NEW
│       │   │   ├── en/
│       │   │   │   └── translation.json ⭐ NEW
│       │   │   ├── hi/
│       │   │   │   └── translation.json ⭐ NEW
│       │   │   ├── es/
│       │   │   │   └── translation.json ⭐ NEW
│       │   │   └── fr/
│       │   │       └── translation.json ⭐ NEW
│       │   │
│       │   ├── components/
│       │   │   ├── Navbar.jsx           (UPDATED)
│       │   │   ├── Chatbox.jsx          (UPDATED/OPTIONAL)
│       │   │   ├── LanguageSelector.jsx ⭐ NEW
│       │   │   └── ChatboxWithMultilingual.jsx ⭐ NEW
│       │   │
│       │   ├── main.jsx                 (UPDATED)
│       │   └── ...
│       │
│       ├── package.json                 (UPDATED - new deps)
│       └── ...
│
├── backend/
│   ├── backend.py                       (ORIGINAL)
│   ├── backend_multilingual.py          ⭐ NEW
│   ├── requirements.txt                 (ORIGINAL)
│   ├── requirements_multilingual.txt    ⭐ NEW
│   └── ...
│
├── MULTILINGUAL_SUMMARY.md              ⭐ NEW
├── MULTILINGUAL_SETUP_GUIDE.md          ⭐ NEW
├── MULTILINGUAL_IMPLEMENTATION_GUIDE.md ⭐ NEW
├── ADVANCED_MULTILINGUAL_FEATURES.md    ⭐ NEW
├── MULTILINGUAL_IMPLEMENTATION_CHECKLIST.md ⭐ NEW
└── ...
```

---

## 7. API Endpoint Architecture

```
┌─────────────────────────────────────┐
│     CLIENT (React Frontend)         │
└────────────────────┬────────────────┘
                     │
       ┌─────────────┴─────────────┐
       │                           │
       ▼ POST                      ▼ GET
┌──────────────────────────┐  ┌─────────────────┐
│  /ask                    │  │  /health        │
│  Request:                │  │  Response:      │
│  {                       │  │  {              │
│   "query": "...",        │  │   "status":     │
│   "language": "en"       │  │   "healthy"     │
│  }                       │  │  }              │
│  Response:               │  │                 │
│  {                       │  │                 │
│   "answer": "...",       │  │                 │
│   "source_language":     │  │                 │
│   "target_language":     │  │                 │
│  }                       │  │                 │
└──────────────────────────┘  └─────────────────┘
                │                        │
                └────────────┬───────────┘
                             │
                       ┌─────▼─────────────┐
                       │  GET               │
                       │  /supported-       │
                       │  languages         │
                       │  Response:         │
                       │  {                 │
                       │   "supported_":    │
                       │   {                │
                       │    "en": "English",│
                       │    "hi": "Hindi",  │
                       │    ...             │
                       │   }                │
                       │  }                 │
                       └────────────────────┘
```

---

## 8. Technology Stack

```
┌────────────────────────────────────────────────────┐
│            FRONTEND STACK                          │
├────────────────────────────────────────────────────┤
│                                                     │
│  React ────────┐                                   │
│                │                                   │
│  Vite ─────────┼─► Frontend Bundle                 │
│                │                                   │
│  Tailwind CSS ─┘                                   │
│                                                     │
│  ┌─────────────────────────────────────────────┐  │
│  │  i18n Library Stack                         │  │
│  ├─────────────────────────────────────────────┤  │
│  │  • i18next (core)                           │  │
│  │  • react-i18next (React bindings)           │  │
│  │  • i18next-http-backend (Load translations) │  │
│  │  • i18next-browser-languagedetector         │  │
│  │    (Auto-detect user language)              │  │
│  └─────────────────────────────────────────────┘  │
│                                                     │
└────────────────────────────────────────────────────┘
                         │
                         │
┌────────────────────────────────────────────────────┐
│            BACKEND STACK                           │
├────────────────────────────────────────────────────┤
│                                                     │
│  Flask ──────────────┐                             │
│                      │                             │
│  Flask-CORS ─────────┼─► Backend Server            │
│                      │                             │
│  Python 3.9+ ────────┘                             │
│                                                     │
│  ┌─────────────────────────────────────────────┐  │
│  │  Language Processing                        │  │
│  ├─────────────────────────────────────────────┤  │
│  │  • langdetect (Language detection)          │  │
│  │  • googletrans (Translation API)            │  │
│  └─────────────────────────────────────────────┘  │
│                                                     │
│  ┌─────────────────────────────────────────────┐  │
│  │  RAG & Knowledge                            │  │
│  ├─────────────────────────────────────────────┤  │
│  │  • Neo4j (Knowledge Graph Database)         │  │
│  │  • LangChain (RAG Framework)                │  │
│  │  • Groq/Llama (LLM for Answer Generation)  │  │
│  │  • FAISS (Vector DB for Semantic Search)    │  │
│  └─────────────────────────────────────────────┘  │
│                                                     │
└────────────────────────────────────────────────────┘
```

---

These diagrams provide a comprehensive visual reference for the multilingual architecture!
