# AskMOS Multilingual - Quick Reference Card

## 🚀 TL;DR (Getting Started in 5 Minutes)

### Frontend
```bash
cd frontend/isro-hackathon
npm install i18next i18next-browser-languagedetector i18next-http-backend react-i18next
```

Add to `main.jsx`: `import './i18n/config';`

Update your Navbar to include `<LanguageSelector />` component.

### Backend
```bash
cd backend
pip install langdetect googletrans==3.1.0a0
python backend_multilingual.py
```

### Test
- Frontend: http://localhost:5173 → Check if language selector appears
- Backend: `curl http://localhost:5000/health`

---

## 📚 Documentation Files

| File | Purpose | Read When |
|------|---------|-----------|
| `MULTILINGUAL_SUMMARY.md` | Overview & quick start | First (5 min) |
| `MULTILINGUAL_SETUP_GUIDE.md` | Detailed setup instructions | Setting up (20 min) |
| `MULTILINGUAL_IMPLEMENTATION_GUIDE.md` | Architecture & design | Understanding system (15 min) |
| `ADVANCED_MULTILINGUAL_FEATURES.md` | Advanced features | After basic setup works |
| `MULTILINGUAL_IMPLEMENTATION_CHECKLIST.md` | Step-by-step checklist | During implementation |
| `MULTILINGUAL_ARCHITECTURE_DIAGRAMS.md` | Visual diagrams | Visual learners |

---

## 🗂️ New Files Created

### Frontend
- `src/i18n/config.js` - i18n configuration
- `src/components/LanguageSelector.jsx` - Language switcher component
- `src/components/ChatboxWithMultilingual.jsx` - Enhanced chatbox
- `src/locales/[lang]/translation.json` - Translation files (en, hi, es, fr)

### Backend
- `backend_multilingual.py` - New backend with translation support
- `requirements_multilingual.txt` - New dependencies

### Documentation
- `MULTILINGUAL_SUMMARY.md`
- `MULTILINGUAL_SETUP_GUIDE.md`
- `MULTILINGUAL_IMPLEMENTATION_GUIDE.md`
- `ADVANCED_MULTILINGUAL_FEATURES.md`
- `MULTILINGUAL_IMPLEMENTATION_CHECKLIST.md`
- `MULTILINGUAL_ARCHITECTURE_DIAGRAMS.md` (this file)

---

## 🔄 Data Flow (Simple Version)

```
User Types in Language X
        ↓
Detect Language X
        ↓
Translate to English
        ↓
Process Query (Graph + LLM)
        ↓
Get Answer in English
        ↓
Translate to Language X
        ↓
Display to User in Language X
```

---

## 🌐 Supported Languages

| Code | Language | Flag |
|------|----------|------|
| en | English | 🇬🇧 |
| hi | हिन्दी (Hindi) | 🇮🇳 |
| es | Español (Spanish) | 🇪🇸 |
| fr | Français (French) | 🇫🇷 |
| de | Deutsch (German) | 🇩🇪 |
| zh-CN | 中文 (Chinese) | 🇨🇳 |
| ja | 日本語 (Japanese) | 🇯🇵 |
| pt | Português (Portuguese) | 🇵🇹 |

---

## 💻 Key Components

### Frontend
- **LanguageSelector**: Dropdown to change languages
- **ChatboxWithMultilingual**: Chat component with language support
- **i18n Config**: Translation system setup

### Backend
- **detect_language()**: Identifies input language
- **translate_text()**: Translates text between languages
- **generate_cypher()**: Creates database queries
- **/ask endpoint**: Main API with language support

---

## 📝 Common Tasks

### Add a New Language
1. Create `src/locales/[code]/translation.json`
2. Update `LanguageSelector.jsx` languages array
3. Done! (Backend auto-detects new language)

### Change UI Text
1. Edit translation files in `src/locales/[lang]/translation.json`
2. Use `t('key.name')` in React components
3. Restart frontend to see changes

### Test Backend Manually
```bash
# English
curl -X POST http://localhost:5000/ask \
  -H "Content-Type: application/json" \
  -d '{"query": "What satellites exist?", "language": "en"}'

# Hindi
curl -X POST http://localhost:5000/ask \
  -H "Content-Type: application/json" \
  -d '{"query": "कौन से उपग्रह हैं?", "language": "hi"}'
```

---

## ⚡ Performance Tips

| Issue | Solution |
|-------|----------|
| Slow translation | Check internet (uses Google Translate API) |
| Language not changing | Clear browser cache & localStorage |
| Translations missing | Check JSON file exists in correct folder |
| API slow | Normal - translation takes ~1 second |
| Special characters broken | Ensure JSON files saved as UTF-8 |

---

## 🐛 Troubleshooting Flowchart

```
Problem: Language selector not showing
├─ Check: File exists? `LanguageSelector.jsx` ✓
├─ Check: Imported in Navbar? ✓
├─ Check: CSS working? (Uses Tailwind) ✓
└─ Solution: Clear cache, restart dev server

Problem: Translations not appearing
├─ Check: Translation files exist? ✓
├─ Check: JSON valid? (use jsonlint.com) ✓
├─ Check: i18n import in main.jsx? ✓
└─ Solution: Check console for i18n errors

Problem: Backend translation failing
├─ Check: Dependencies installed? ✓
├─ Check: Internet connection? ✓
├─ Check: API key valid? ✓
└─ Solution: Check error logs

Problem: Language preference not saved
├─ Check: localStorage enabled? ✓
├─ Check: Not in private/incognito mode? ✓
└─ Solution: Clear localStorage, try again
```

---

## 🔗 API Contract

### POST /ask
```json
Request:
{
  "query": "What satellites do you have?",
  "language": "en"
}

Response:
{
  "answer": "MOSDAC operates several satellites...",
  "source_language": "en",
  "target_language": "en",
  "original_query": "What satellites do you have?",
  "processed_query": "What satellites do you have?"
}
```

### GET /health
```json
Response:
{
  "status": "healthy",
  "service": "AskMOS Backend"
}
```

### GET /supported-languages
```json
Response:
{
  "supported_languages": {
    "en": "English",
    "hi": "Hindi",
    "es": "Spanish",
    ...
  }
}
```

---

## 📊 File Statistics

| Category | Count | Files |
|----------|-------|-------|
| Frontend Components | 3 | LanguageSelector, ChatboxWithMultilingual, Updated Navbar |
| Translation Files | 4 | en, hi, es, fr |
| Backend Files | 2 | backend_multilingual.py, requirements_multilingual.txt |
| Documentation | 6 | Guides, checklist, diagrams, summary |
| **Total New Files** | **15** | All in this implementation |

---

## 🎯 Success Checklist

- [ ] Frontend dependencies installed
- [ ] Backend dependencies installed
- [ ] i18n config in main.jsx
- [ ] Language selector in Navbar
- [ ] Chatbox updated with i18n
- [ ] Both servers running
- [ ] Language selector visible
- [ ] Can switch languages
- [ ] UI text changes
- [ ] Chat works in multiple languages
- [ ] No console errors
- [ ] Mobile responsive
- [ ] Language preference persists

---

## 💡 Quick Tips

1. **Clear Cache**: `Ctrl+Shift+Delete` to clear browser cache
2. **Check Console**: `F12` → Console tab for errors
3. **Test API**: Use curl commands to test backend
4. **View Network**: `F12` → Network tab to see API calls
5. **Check Storage**: `F12` → Application → localStorage to see i18n settings
6. **Validate JSON**: Use jsonlint.com to check translation files

---

## 🔑 Key Concepts

| Concept | Explanation |
|---------|-------------|
| **i18n** | Internationalization - framework for multi-language support |
| **Translation File** | JSON with `key: "translated text"` pairs |
| **Language Code** | 2-3 letter code (en, hi, es, fr) |
| **Langdetect** | Python library that detects language of text |
| **Googletrans** | Python library for translating text via Google Translate API |
| **locale** | Folder containing translations for a specific language |

---

## 📞 Support Resources

### Problem Type | Resource
|---|---|
| Setup issues | `MULTILINGUAL_SETUP_GUIDE.md` |
| Architecture questions | `MULTILINGUAL_IMPLEMENTATION_GUIDE.md` |
| Advanced features | `ADVANCED_MULTILINGUAL_FEATURES.md` |
| Step-by-step help | `MULTILINGUAL_IMPLEMENTATION_CHECKLIST.md` |
| Visual explanation | `MULTILINGUAL_ARCHITECTURE_DIAGRAMS.md` |
| Quick overview | `MULTILINGUAL_SUMMARY.md` |

---

## 🎓 Learning Path

1. **5 min**: Read `MULTILINGUAL_SUMMARY.md`
2. **20 min**: Follow `MULTILINGUAL_SETUP_GUIDE.md`
3. **15 min**: Test implementation
4. **10 min**: Read `MULTILINGUAL_IMPLEMENTATION_GUIDE.md` for understanding
5. **Optional**: Explore `ADVANCED_MULTILINGUAL_FEATURES.md`

---

## 🚀 Next Steps After Setup

1. Customize translations for your content
2. Add more languages
3. Implement translation memory caching
4. Add analytics to track language usage
5. User testing in different languages
6. Deploy to production
7. Monitor translation quality

---

## 📋 Remember

- ✅ All files are already created
- ✅ Just need to install dependencies
- ✅ Update entry point (main.jsx)
- ✅ Include components in your pages
- ✅ Test and deploy
- ❌ Don't forget to set up .env file

---

## 🎉 You're All Set!

You have:
- ✅ Complete multilingual architecture
- ✅ 4 languages pre-configured
- ✅ Comprehensive documentation
- ✅ Step-by-step guides
- ✅ Architecture diagrams
- ✅ Troubleshooting help
- ✅ Advanced features reference

**Start with `MULTILINGUAL_SETUP_GUIDE.md` and follow the steps!**

---

**Questions?** Check the relevant documentation file above. Every scenario is covered!

**Ready to deploy?** Run through `MULTILINGUAL_IMPLEMENTATION_CHECKLIST.md` ✓

**Want to understand how it works?** Read `MULTILINGUAL_ARCHITECTURE_DIAGRAMS.md` 📊
