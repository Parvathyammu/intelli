# Multilingual Accessibility Implementation Guide for AskMOS Chatbot

## Overview
This guide provides step-by-step instructions to add multilingual support to your AskMOS chatbot application.

## Architecture

### Frontend Components
1. **Language Selector** - User can choose preferred language
2. **Translation System** - Using i18n libraries
3. **Language Persistence** - Store user's language preference
4. **Dynamic UI Updates** - All text updates when language changes

### Backend Components
1. **Language Detection** - Detect user's query language
2. **Translation Service** - Translate queries and responses
3. **Multi-language LLM Prompts** - Context-aware language handling

---

## Implementation Steps

### Step 1: Frontend Setup (React/Vite)

#### Install Dependencies
```bash
npm install i18next i18next-browser-languagedetector i18next-http-backend react-i18next
```

#### Create Translation Files Structure
```
frontend/isro-hackathon/src/
├── locales/
│   ├── en/
│   │   └── translation.json
│   ├── hi/
│   │   └── translation.json
│   ├── es/
│   │   └── translation.json
│   └── fr/
│       └── translation.json
└── i18n/
    └── config.js
```

#### Create `i18n/config.js`
```javascript
import i18n from 'i18next';
import LanguageDetector from 'i18next-browser-languagedetector';
import HttpBackend from 'i18next-http-backend';
import { initReactI18next } from 'react-i18next';

i18n
  .use(HttpBackend)
  .use(LanguageDetector)
  .use(initReactI18next)
  .init({
    fallbackLng: 'en',
    debug: true,
    interpolation: {
      escapeValue: false
    },
    backend: {
      loadPath: '/locales/{{lng}}/translation.json'
    }
  });

export default i18n;
```

#### Initialize i18n in `main.jsx`
```javascript
import './i18n/config';
```

#### Create Translation Files

**`locales/en/translation.json`**
```json
{
  "chatbot": {
    "title": "Satellite Data Assistant",
    "welcome": "Welcome to MOSDAC! How can I help you explore our satellite data archive?",
    "placeholder": "Ask about satellite data...",
    "send": "Send",
    "error": "Error connecting to backend. Please try again.",
    "noAnswer": "Sorry, I couldn't find anything relevant.",
    "loading": "Loading..."
  },
  "navbar": {
    "home": "Home",
    "language": "Language"
  }
}
```

**`locales/hi/translation.json`**
```json
{
  "chatbot": {
    "title": "उपग्रह डेटा सहायक",
    "welcome": "MOSDAC में आपका स्वागत है! मैं आपको अपने उपग्रह डेटा संग्रह का पता लगाने में कैसे मदद कर सकता हूं?",
    "placeholder": "उपग्रह डेटा के बारे में पूछें...",
    "send": "भेजें",
    "error": "बैकएंड से जुड़ने में त्रुटि। कृपया फिर से प्रयास करें।",
    "noAnswer": "क्षमा करें, मुझे कुछ भी प्रासंगिक नहीं मिल सका।",
    "loading": "लोड हो रहा है..."
  },
  "navbar": {
    "home": "होम",
    "language": "भाषा"
  }
}
```

### Step 2: Update Chatbox Component

Key changes:
1. Import `useTranslation` hook
2. Replace hardcoded strings with translation keys
3. Add language parameter to API requests

```javascript
import { useTranslation } from 'react-i18next';

function Chatbox() {
  const { t, i18n } = useTranslation();
  
  // Pass language to backend
  const handleSendMessage = async () => {
    // ... existing code ...
    
    const response = await fetch(`${import.meta.env.VITE_BACKEND_URL}/ask`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ 
        query: inputMessage,
        language: i18n.language  // Add language
      })
    });
    
    // Use translation keys for UI text
    // Instead of hardcoded "Welcome to MOSDAC..."
    // Use t('chatbot.welcome')
  };
  
  return (
    <div>
      <h2>{t('chatbot.title')}</h2>
      <input placeholder={t('chatbot.placeholder')} />
      <button>{t('chatbot.send')}</button>
    </div>
  );
}
```

### Step 3: Create Language Selector Component

Create `src/components/LanguageSelector.jsx`:
```javascript
import { useTranslation } from 'react-i18next';

function LanguageSelector() {
  const { i18n } = useTranslation();
  
  const languages = [
    { code: 'en', name: 'English' },
    { code: 'hi', name: 'हिन्दी' },
    { code: 'es', name: 'Español' },
    { code: 'fr', name: 'Français' }
  ];
  
  return (
    <select 
      value={i18n.language} 
      onChange={(e) => i18n.changeLanguage(e.target.value)}
      className="language-selector"
    >
      {languages.map(lang => (
        <option key={lang.code} value={lang.code}>
          {lang.name}
        </option>
      ))}
    </select>
  );
}

export default LanguageSelector;
```

### Step 4: Backend Modifications (Python/Flask)

#### Install Dependencies
```bash
pip install google-cloud-translate
# OR
pip install googletrans==3.1.0a0
```

#### Update Backend API

Modify `backend.py`:
```python
from flask import Flask, request, jsonify
from googletrans import Translator
from langdetect import detect

app = Flask(__name__)
translator = Translator()

@app.route('/ask', methods=['POST'])
def ask():
    try:
        data = request.get_json()
        query = data.get('query', '').strip()
        target_language = data.get('language', 'en')  # Get language from frontend
        
        # Detect source language
        try:
            source_language = detect(query)
        except:
            source_language = 'en'
        
        # Translate query to English for processing if needed
        if source_language != 'en':
            query_en = translator.translate(query, src_language=source_language, dest_language='en')['translatedText']
        else:
            query_en = query
        
        # Generate Cypher and get answer (in English)
        cypher_query = generate_cypher(query_en)
        graph_data = run_cypher(cypher_query) if cypher_query else []
        answer_en = generate_answer(query_en, graph_data)
        
        # Translate answer to target language
        if target_language != 'en':
            answer = translator.translate(answer_en, src_language='en', dest_language=target_language)['translatedText']
        else:
            answer = answer_en
        
        return jsonify({
            'answer': answer,
            'source_language': source_language,
            'target_language': target_language
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500
```

### Step 5: Enhanced LLM Prompts with Language Context

```python
def generate_cypher(nl_query, language='en'):
    language_context = {
        'en': "English",
        'hi': "Hindi",
        'es': "Spanish",
        'fr': "French"
    }
    
    prompt = f"""
You are a Cypher expert. Convert the following natural language question into a single valid Cypher query.

The question is in {language_context.get(language, 'English')}.

Only output the query — do NOT add explanation, markdown, or commentary.

Question: {nl_query}
"""
    # ... rest of the function
```

---

## Features to Implement

### 1. Automatic Language Detection
- Detect user's browser language
- Automatically set UI to that language

### 2. Language Persistence
- Store user's language preference in localStorage
- Restore on next visit

### 3. Right-to-Left (RTL) Support
For Arabic, Hebrew, Urdu:
```css
[dir="rtl"] {
  direction: rtl;
  text-align: right;
}
```

### 4. Multi-language Chat History
- Store language info with each message
- Display language badges if needed

### 5. Translation Quality Improvements
- Use professional translation APIs (Google Cloud Translation)
- Implement caching for common phrases
- Add human review workflow for translations

---

## API Endpoint Changes

### Updated Request Format
```json
{
  "query": "What satellites does MOSDAC have?",
  "language": "en"
}
```

### Updated Response Format
```json
{
  "answer": "MOSDAC has satellites including INSAT-3A, INSAT-3D...",
  "source_language": "en",
  "target_language": "en",
  "confidence": 0.95
}
```

---

## Testing Checklist

- [ ] Language selector works in all browsers
- [ ] Text changes when language is switched
- [ ] Translations are accurate
- [ ] Backend correctly detects source language
- [ ] Responses are translated to target language
- [ ] Language preference persists on refresh
- [ ] RTL languages display correctly
- [ ] Special characters display properly
- [ ] No performance degradation
- [ ] Mobile responsiveness maintained

---

## Supported Languages (Initial)
- English (en)
- Hindi (hi)
- Spanish (es)
- French (fr)
- German (de)
- Chinese Simplified (zh)
- Japanese (ja)
- Portuguese (pt)

---

## Performance Considerations

1. **Translation Caching**: Cache frequently translated phrases
2. **Lazy Loading**: Load translation files on demand
3. **CDN Distribution**: Use CDN for translation files
4. **Batch Translation**: Batch multiple strings for translation APIs
5. **Offline Support**: Pre-load critical UI translations

---

## References

- [i18next Documentation](https://www.i18next.com/)
- [React i18next](https://react.i18next.com/)
- [Google Cloud Translation](https://cloud.google.com/translate)
- [Langdetect](https://github.com/Mimino666/langdetect)

