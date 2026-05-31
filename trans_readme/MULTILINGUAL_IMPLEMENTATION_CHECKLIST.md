# Multilingual Implementation Checklist

Use this checklist to track your implementation progress.

---

## Phase 1: Preparation (15 minutes)

- [ ] Read `MULTILINGUAL_SUMMARY.md` for overview
- [ ] Read `MULTILINGUAL_SETUP_GUIDE.md` for detailed steps
- [ ] Review `MULTILINGUAL_IMPLEMENTATION_GUIDE.md` for architecture
- [ ] Backup your current code
- [ ] Create a new git branch for multilingual features
  ```bash
  git checkout -b feature/multilingual-support
  ```

---

## Phase 2: Frontend Setup (20 minutes)

### 2.1: Install Dependencies
- [ ] Navigate to frontend folder
  ```bash
  cd frontend/isro-hackathon
  ```
- [ ] Install i18n packages
  ```bash
  npm install i18next i18next-browser-languagedetector i18next-http-backend react-i18next
  ```
- [ ] Verify installation
  ```bash
  npm list i18next react-i18next
  ```

### 2.2: Copy Files
- [ ] Verify `src/i18n/config.js` exists
- [ ] Verify `src/locales/en/translation.json` exists
- [ ] Verify `src/locales/hi/translation.json` exists
- [ ] Verify `src/locales/es/translation.json` exists
- [ ] Verify `src/locales/fr/translation.json` exists
- [ ] Verify `src/components/LanguageSelector.jsx` exists
- [ ] Verify `src/components/ChatboxWithMultilingual.jsx` exists

### 2.3: Update Entry Point
- [ ] Open `src/main.jsx`
- [ ] Add this line at the top:
  ```javascript
  import './i18n/config';
  ```
- [ ] Save and verify no errors

### 2.4: Update Navbar Component
- [ ] Open `src/components/Navbar.jsx`
- [ ] Add import:
  ```javascript
  import LanguageSelector from './LanguageSelector';
  ```
- [ ] Add component to navbar:
  ```jsx
  <LanguageSelector />
  ```
- [ ] Save and verify component appears

### 2.5: Update Chatbox Component
**Choose ONE option:**

**Option A: Use new ChatboxWithMultilingual.jsx**
- [ ] In your main App/Home component, import:
  ```javascript
  import ChatboxWithMultilingual from './components/ChatboxWithMultilingual';
  ```
- [ ] Replace old Chatbox with ChatboxWithMultilingual
- [ ] Save and test

**Option B: Update existing Chatbox.jsx**
- [ ] Open `src/components/Chatbox.jsx`
- [ ] Add import at top:
  ```javascript
  import { useTranslation } from 'react-i18next';
  ```
- [ ] Add inside component:
  ```javascript
  const { t, i18n } = useTranslation();
  ```
- [ ] Replace hardcoded strings with translation keys:
  ```javascript
  // Old: "Welcome to MOSDAC..."
  // New: t('chatbot.welcome')
  ```
- [ ] Update API call to include language:
  ```javascript
  body: JSON.stringify({ 
    query: inputMessage,
    language: i18n.language
  })
  ```
- [ ] Save and verify

### 2.6: Frontend Testing
- [ ] Start dev server
  ```bash
  npm run dev
  ```
- [ ] Open http://localhost:5173 in browser
- [ ] Verify language selector appears
- [ ] Click language selector
- [ ] Verify all languages shown (English, हिन्दी, Español, Français)
- [ ] Select different language
- [ ] Verify UI text changes (at minimum, button should change)
- [ ] Check browser console for errors
  - [ ] No red errors in console
  - [ ] i18next should show initialization message

---

## Phase 3: Backend Setup (15 minutes)

### 3.1: Install Dependencies
- [ ] Navigate to backend folder
  ```bash
  cd backend
  ```
- [ ] Install translation packages
  ```bash
  pip install langdetect googletrans==3.1.0a0
  ```
- [ ] Verify installation
  ```bash
  python -c "import langdetect; import googletrans; print('OK')"
  ```

### 3.2: Set Up Backend
**Choose ONE option:**

**Option A: Use new backend_multilingual.py (Recommended)**
- [ ] Verify `backend_multilingual.py` exists
- [ ] Check if you have `.env` file with:
  - [ ] NEO4J_URI
  - [ ] NEO4J_USERNAME
  - [ ] NEO4J_PASSWORD
  - [ ] GROQ_API_KEY
- [ ] Run the new backend:
  ```bash
  python backend_multilingual.py
  ```
- [ ] Verify it starts without errors

**Option B: Update existing backend.py**
- [ ] Open `backend.py`
- [ ] Add imports:
  ```python
  from langdetect import detect, LangDetectException
  import googletrans
  ```
- [ ] Copy these functions from `backend_multilingual.py`:
  - [ ] `detect_language(text)`
  - [ ] `translate_text(text, source_lang, target_lang)`
  - [ ] Updated `generate_cypher()` with language parameter
  - [ ] Updated `generate_answer()` with language parameter
- [ ] Update `/ask` endpoint to handle language parameter
- [ ] Save and test

### 3.3: Backend Testing
- [ ] Test health endpoint
  ```bash
  curl http://localhost:5000/health
  ```
- [ ] Test supported languages endpoint
  ```bash
  curl http://localhost:5000/supported-languages
  ```
- [ ] Test English query
  ```bash
  curl -X POST http://localhost:5000/ask \
    -H "Content-Type: application/json" \
    -d '{"query": "What satellites do you have?", "language": "en"}'
  ```
- [ ] Test Hindi query
  ```bash
  curl -X POST http://localhost:5000/ask \
    -H "Content-Type: application/json" \
    -d '{"query": "आपके पास कौन से उपग्रह हैं?", "language": "hi"}'
  ```
- [ ] Verify responses contain:
  - [ ] `answer` field
  - [ ] `source_language` field
  - [ ] `target_language` field

---

## Phase 4: Integration Testing (15 minutes)

### 4.1: Full System Test
- [ ] Both frontend and backend running
- [ ] Frontend: http://localhost:5173
- [ ] Backend: http://localhost:5000

### 4.2: Language Selector Test
- [ ] Language selector visible in navbar
- [ ] Can select English
- [ ] Can select Hindi
- [ ] Can select Spanish
- [ ] Can select French

### 4.3: Chat Test - English
- [ ] Type question in English
- [ ] Click Send
- [ ] Wait for response
- [ ] Verify answer appears
- [ ] No errors in console

### 4.4: Chat Test - Hindi
- [ ] Select Hindi from language selector
- [ ] UI updates to Hindi
- [ ] Type question in Hindi
- [ ] Click Send (or भेजें)
- [ ] Verify answer appears in Hindi
- [ ] No errors in console

### 4.5: Chat Test - Other Languages
- [ ] Repeat for Spanish
- [ ] Repeat for French

### 4.6: Mixed Language Test
- [ ] Set UI to English
- [ ] Type question in Hindi
- [ ] Verify answer in English (source language detected)
- [ ] Set UI to Spanish
- [ ] Type question in Spanish
- [ ] Verify answer in Spanish

### 4.7: Edge Cases
- [ ] Send empty query - should show error
- [ ] Send special characters - should work
- [ ] Send very long text - should work
- [ ] Rapid language switching - should work
- [ ] Browser refresh - language preference saved? ✓

---

## Phase 5: Browser Testing (10 minutes)

Test on multiple browsers:

### Chrome/Edge
- [ ] Works correctly
- [ ] Console clean
- [ ] Language selector functional

### Firefox
- [ ] Works correctly
- [ ] Console clean
- [ ] Language selector functional

### Safari
- [ ] Works correctly
- [ ] Console clean
- [ ] Language selector functional

### Mobile (Chrome Mobile)
- [ ] Works correctly
- [ ] Touch/Tap functional
- [ ] Language selector visible
- [ ] Chat readable on small screen

---

## Phase 6: Deployment Preparation (10 minutes)

### 6.1: Frontend Build
- [ ] Test production build
  ```bash
  npm run build
  ```
- [ ] Verify build succeeds
- [ ] Check build size
- [ ] Preview build
  ```bash
  npm run preview
  ```

### 6.2: Backend Configuration
- [ ] Verify `.env` file exists and has all variables
- [ ] Test with production settings
- [ ] Check error handling
- [ ] Verify translation service works

### 6.3: Documentation
- [ ] Update README.md with multilingual info
- [ ] Document supported languages
- [ ] Document how to add new languages
- [ ] Document API changes

### 6.4: Version Control
- [ ] Stage all changes
  ```bash
  git add .
  ```
- [ ] Commit with message
  ```bash
  git commit -m "feat: Add multilingual support for 8 languages"
  ```
- [ ] Push branch
  ```bash
  git push origin feature/multilingual-support
  ```

---

## Phase 7: Performance Verification (5 minutes)

- [ ] Frontend load time: < 3 seconds
- [ ] API response time: < 2 seconds
- [ ] Language switch time: < 500ms
- [ ] No memory leaks (DevTools)
- [ ] Network requests optimized

---

## Phase 8: Documentation (10 minutes)

- [ ] Review `MULTILINGUAL_SUMMARY.md`
- [ ] Review `MULTILINGUAL_SETUP_GUIDE.md`
- [ ] Review `ADVANCED_MULTILINGUAL_FEATURES.md`
- [ ] Share with team
- [ ] Add to project wiki/docs

---

## Phase 9: Monitoring (Ongoing)

- [ ] Monitor translation accuracy
- [ ] Track user language preferences
- [ ] Check for translation errors
- [ ] Monitor API response times
- [ ] Gather user feedback

---

## Phase 10: Future Enhancements (Optional)

- [ ] [ ] Add more languages
- [ ] [ ] Implement translation memory (caching)
- [ ] [ ] Add RTL language support (Arabic, Hebrew)
- [ ] [ ] Custom translation service integration
- [ ] [ ] Translation quality scoring
- [ ] [ ] Multi-language search
- [ ] [ ] Language-specific formatting
- [ ] [ ] User preference storage (database)

---

## Quick Reference: Commands

```bash
# Frontend Setup
cd frontend/isro-hackathon
npm install i18next i18next-browser-languagedetector i18next-http-backend react-i18next
npm run dev

# Backend Setup
cd backend
pip install langdetect googletrans==3.1.0a0
python backend_multilingual.py

# Testing
curl http://localhost:5000/health
curl http://localhost:5000/supported-languages

# Build
npm run build
npm run preview

# Git
git checkout -b feature/multilingual-support
git add .
git commit -m "feat: Add multilingual support"
git push origin feature/multilingual-support
```

---

## Success Criteria

- [x] All languages appear in selector
- [x] UI text changes with language selection
- [x] Chatbot accepts queries in multiple languages
- [x] Responses translate correctly
- [x] No console errors
- [x] Works on mobile
- [x] Language preference persists
- [x] API responds in < 2 seconds
- [x] All browsers supported
- [x] Documentation complete

---

## Troubleshooting Quick Links

If you encounter issues:

1. **Translations not appearing**: Check `MULTILINGUAL_SETUP_GUIDE.md` → Troubleshooting → Issue 1
2. **Backend translation failing**: Check `MULTILINGUAL_SETUP_GUIDE.md` → Troubleshooting → Issue 2
3. **Language selector not showing**: Check `MULTILINGUAL_SETUP_GUIDE.md` → Troubleshooting → Issue 3
4. **Translations stuck in English**: Check `MULTILINGUAL_SETUP_GUIDE.md` → Troubleshooting → Issue 4

---

## Support Resources

- Documentation: `MULTILINGUAL_IMPLEMENTATION_GUIDE.md`
- Setup Guide: `MULTILINGUAL_SETUP_GUIDE.md`
- Advanced Features: `ADVANCED_MULTILINGUAL_FEATURES.md`
- Summary: `MULTILINGUAL_SUMMARY.md`

---

## Notes

Use this space to track additional notes or customizations:

```
- 
- 
- 
- 
```

---

**Start Date**: _____________
**Completion Date**: _____________
**Team Members**: _____________

Good luck with your multilingual implementation! 🌍🗣️✨
