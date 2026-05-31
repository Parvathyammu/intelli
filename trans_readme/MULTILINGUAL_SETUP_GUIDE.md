# Quick Setup Guide: Multilingual AskMOS Chatbot

## What's Included

This implementation adds full multilingual support to your AskMOS chatbot:

✅ **Languages Supported**: English, Hindi, Spanish, French (easily extensible)
✅ **Automatic Language Detection**: Detects user input language
✅ **Translation**: Queries and responses translated automatically
✅ **UI Localization**: All frontend text translatable
✅ **Language Persistence**: User's language choice saved
✅ **Language Selector**: Easy dropdown to switch languages

---

## Installation Steps

### 1. Frontend Setup

#### Step 1.1: Install Dependencies
```bash
cd frontend/isro-hackathon
npm install i18next i18next-browser-languagedetector i18next-http-backend react-i18next
```

#### Step 1.2: Update `main.jsx`
Add this line at the top of your `main.jsx`:
```javascript
import './i18n/config';
```

Complete `main.jsx` example:
```javascript
import React from 'react'
import ReactDOM from 'react-dom/client'
import './i18n/config'  // Add this line
import App from './App.jsx'
import './index.css'

ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>,
)
```

#### Step 1.3: Update Your Navbar Component
Add the `LanguageSelector` component to your Navbar:

```javascript
import LanguageSelector from './components/LanguageSelector';

function Navbar() {
  return (
    <nav className="navbar">
      {/* ... existing nav items ... */}
      <LanguageSelector />
    </nav>
  );
}
```

#### Step 1.4: Update Chatbox Component
Replace your existing Chatbox with the new `ChatboxWithMultilingual.jsx`:

Option A: Use the new component directly
```javascript
import ChatboxWithMultilingual from './components/ChatboxWithMultilingual';

// In your App.jsx or wherever you use Chatbox:
<ChatboxWithMultilingual />
```

Option B: Update existing Chatbox.jsx with i18n support
Add at the top:
```javascript
import { useTranslation } from 'react-i18next';
```

Inside the component:
```javascript
function Chatbox() {
  const { t, i18n } = useTranslation();
  
  // Replace hardcoded strings with translations
  // Example: 
  // Old: "Welcome to MOSDAC..."
  // New: t('chatbot.welcome')
```

---

### 2. Backend Setup

#### Step 2.1: Install Dependencies
```bash
cd backend
pip install -r requirements_multilingual.txt
```

Or manually:
```bash
pip install langdetect==1.0.9 googletrans==3.1.0a0
```

#### Step 2.2: Use New Backend
**Option A: Use the new multilingual backend**
```bash
python backend_multilingual.py
```

**Option B: Update existing backend.py**
Copy the relevant functions from `backend_multilingual.py`:
- `detect_language(text)`
- `translate_text(text, source_lang, target_lang)`
- `generate_cypher()` with language parameter
- `generate_answer()` with language parameter
- Updated `/ask` endpoint to handle language parameter

#### Step 2.3: Test the Backend
```bash
curl -X POST http://localhost:5000/ask \
  -H "Content-Type: application/json" \
  -d '{"query": "What satellites do you have?", "language": "en"}'
```

---

## File Structure

After implementation, your structure will be:

```
frontend/isro-hackathon/
├── src/
│   ├── i18n/
│   │   └── config.js                          # i18n configuration
│   ├── locales/
│   │   ├── en/
│   │   │   └── translation.json               # English translations
│   │   ├── hi/
│   │   │   └── translation.json               # Hindi translations
│   │   ├── es/
│   │   │   └── translation.json               # Spanish translations
│   │   └── fr/
│   │       └── translation.json               # French translations
│   ├── components/
│   │   ├── Chatbox.jsx                        # (Updated or keep original)
│   │   ├── ChatboxWithMultilingual.jsx        # (New)
│   │   ├── LanguageSelector.jsx               # (New)
│   │   └── Navbar.jsx                         # (Update to include LanguageSelector)
│   ├── main.jsx                               # (Add i18n import)
│   └── ...

backend/
├── backend.py                                 # (Original or updated)
├── backend_multilingual.py                    # (New - can replace backend.py)
├── requirements.txt
├── requirements_multilingual.txt              # (New)
└── ...
```

---

## API Changes

### Request Format (After Implementation)
```json
{
  "query": "What satellites does MOSDAC have?",
  "language": "en"
}
```

### Response Format
```json
{
  "answer": "MOSDAC operates several satellites...",
  "source_language": "en",
  "target_language": "en",
  "original_query": "What satellites does MOSDAC have?",
  "processed_query": "What satellites does MOSDAC have?"
}
```

---

## Usage Examples

### User switches to Hindi
1. Clicks language selector dropdown
2. Selects "हिन्दी"
3. UI updates to Hindi
4. Types question in Hindi: "MOSDAC के पास कौन से उपग्रह हैं?"
5. Question is detected as Hindi, processed in English, answer returned in Hindi

### User types in Spanish but UI is in English
1. UI language: English
2. Selects dropdown language: English
3. Types: "¿Qué satélites tiene MOSDAC?"
4. Auto-detected as Spanish, processed in English, returned in English
5. User sees English response

---

## Adding New Languages

### Step 1: Create Translation File
Add file: `src/locales/[lang-code]/translation.json`

Example for German (`src/locales/de/translation.json`):
```json
{
  "chatbot": {
    "title": "Satellitenassistent",
    "welcome": "Willkommen bei MOSDAC!...",
    "placeholder": "Fragen Sie nach Satellitendaten...",
    "send": "Senden",
    "error": "Fehler beim Verbinden...",
    "noAnswer": "Entschuldigung, ich habe nichts Relevantes gefunden.",
    "loading": "Wird geladen..."
  },
  "navbar": {
    "home": "Startseite",
    "language": "Sprache"
  },
  "knowledge_graph": {
    "load": "Grafik laden",
    "title": "Wissensgraph",
    "description": "Klicken Sie auf \"Grafik laden\", um das Wissensnetz zu visualisieren"
  }
}
```

### Step 2: Add to Language Selector
Update `src/components/LanguageSelector.jsx`:
```javascript
const languages = [
  { code: 'en', name: 'English', flag: '🇬🇧' },
  { code: 'hi', name: 'हिन्दी', flag: '🇮🇳' },
  { code: 'es', name: 'Español', flag: '🇪🇸' },
  { code: 'fr', name: 'Français', flag: '🇫🇷' },
  { code: 'de', name: 'Deutsch', flag: '🇩🇪' },  // Add this
];
```

### Step 3: Update Backend Language Support
Update `backend_multilingual.py` `LANGUAGE_CODES` dict:
```python
LANGUAGE_CODES = {
    'en': 'en',
    'hi': 'hi',
    'es': 'es',
    'fr': 'fr',
    'de': 'de',  # Add this
    'zh-cn': 'zh-CN',
    'ja': 'ja',
    'pt': 'pt'
}
```

---

## Troubleshooting

### Issue: Translations not appearing
**Solution**: 
1. Clear browser cache
2. Check console for i18n errors
3. Verify translation JSON files are valid
4. Check `public/locales/` folder exists with all files

### Issue: Backend translation failing
**Solution**:
1. Verify `langdetect` and `googletrans` are installed
2. Check internet connection (needed for translation API)
3. Review error logs in terminal

### Issue: Language selector not showing
**Solution**:
1. Verify `LanguageSelector.jsx` is imported in Navbar
2. Check CSS classes are available (Tailwind)
3. Verify component syntax is correct

### Issue: Translations stuck in English
**Solution**:
1. Check localStorage is enabled in browser
2. Try deleting localStorage: `localStorage.clear()` in console
3. Refresh page
4. Try different browser

---

## Performance Tips

1. **Lazy Load Translations**: Translations are loaded only when needed
2. **Cache API Responses**: Consider caching translated answers
3. **Batch Translations**: For multiple strings, batch translation requests
4. **CDN Distribution**: Host translation files on a CDN for faster loading

---

## Testing Checklist

After implementation, verify:

- [ ] Language selector appears in navbar
- [ ] Can switch between all languages
- [ ] UI text updates when language changes
- [ ] Translations persist after page refresh
- [ ] Backend correctly detects input language
- [ ] Responses are translated correctly
- [ ] Works in mobile view
- [ ] No console errors
- [ ] Performance is acceptable
- [ ] Special characters display correctly

---

## Monitoring & Analytics

Add language tracking to understand user preferences:
```javascript
// Log language change
i18n.on('languageChanged', (lng) => {
  console.log('Language changed to:', lng);
  // Send to analytics
  analytics.track('language_changed', { language: lng });
});
```

---

## References

- [i18next Docs](https://www.i18next.com/)
- [React i18next](https://react.i18next.com/)
- [Langdetect Docs](https://github.com/Mimino666/langdetect)
- [Googletrans Docs](https://py-googletrans.readthedocs.io/)

---

## Support

For issues or questions:
1. Check the troubleshooting section
2. Review browser console for errors
3. Check backend logs for translation errors
4. Verify all files are in correct locations

