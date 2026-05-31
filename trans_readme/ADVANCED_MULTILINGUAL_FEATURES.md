# Advanced Multilingual Features

This guide covers advanced features for the multilingual AskMOS chatbot.

---

## 1. Language-Aware Knowledge Graph

Update the graph query engine to provide language-specific context:

```python
# RAG/graph_query_engine.py

def process_query_multilingual(self, query, language='en'):
    """
    Process query with language context for better results
    """
    language_context = {
        'en': "Answer in English with clear structure.",
        'hi': "जवाब हिंदी में दें स्पष्ट संरचना के साथ।",
        'es': "Responde en español con estructura clara.",
        'fr': "Répondez en français avec une structure claire.",
    }
    
    # Get base answer
    answer = self.process_query(query)
    
    # Add language-specific instructions
    context = language_context.get(language, language_context['en'])
    
    # Enhance with language awareness
    enhanced_answer = self._enhance_with_language(answer, context)
    
    return enhanced_answer

def _enhance_with_language(self, answer, context):
    """Enhance answer based on language context"""
    # Add language-specific formatting, examples, etc.
    return answer
```

---

## 2. Multilingual Chat History

Store and retrieve chat history with language information:

```javascript
// Frontend: useEffect hook for chat history

useEffect(() => {
  // Load chat history from localStorage
  const savedHistory = localStorage.getItem('chatHistory');
  if (savedHistory) {
    try {
      const history = JSON.parse(savedHistory);
      setMessages(history);
    } catch (e) {
      console.error('Failed to load chat history:', e);
    }
  }
}, []);

// Save chat history whenever messages change
useEffect(() => {
  localStorage.setItem('chatHistory', JSON.stringify(messages));
}, [messages]);

// Function to export chat in current language
const exportChatHistory = () => {
  const history = messages.map(msg => ({
    time: msg.timestamp.toISOString(),
    language: msg.language,
    sender: msg.sender,
    text: msg.text
  }));
  
  const dataStr = JSON.stringify(history, null, 2);
  const dataBlob = new Blob([dataStr], { type: 'application/json' });
  const url = URL.createObjectURL(dataBlob);
  const link = document.createElement('a');
  link.href = url;
  link.download = `chat-history-${new Date().toISOString()}.json`;
  link.click();
};
```

---

## 3. RTL (Right-to-Left) Support

For Arabic, Hebrew, Urdu, etc.:

```javascript
// useEffect to handle RTL languages
useEffect(() => {
  const rtlLanguages = ['ar', 'he', 'ur'];
  const isRTL = rtlLanguages.includes(i18n.language);
  
  if (isRTL) {
    document.documentElement.dir = 'rtl';
    document.documentElement.lang = i18n.language;
  } else {
    document.documentElement.dir = 'ltr';
    document.documentElement.lang = i18n.language;
  }
}, [i18n.language]);
```

CSS for RTL:
```css
[dir="rtl"] {
  direction: rtl;
  text-align: right;
}

[dir="rtl"] .chat-message-user {
  justify-content: flex-start;
}

[dir="rtl"] .chat-message-bot {
  justify-content: flex-end;
}

[dir="rtl"] input,
[dir="rtl"] textarea {
  text-align: right;
}
```

---

## 4. Multilingual Search/Autocomplete

Add search suggestions in multiple languages:

```python
# Backend autocomplete endpoint
@app.route('/autocomplete', methods=['POST'])
def autocomplete():
    """Provide autocomplete suggestions in user's language"""
    data = request.get_json()
    query = data.get('query', '').strip()
    language = data.get('language', 'en')
    
    # Get suggestions based on knowledge graph
    suggestions = get_suggestions_for_language(query, language)
    
    return jsonify({'suggestions': suggestions})

def get_suggestions_for_language(query, language):
    """Get language-specific suggestions"""
    # Query Neo4j for entities matching query
    cypher = f"""
    MATCH (n:Entity) 
    WHERE n.name CONTAINS '{query}' 
    OR n.description CONTAINS '{query}'
    RETURN n.name as name, n.description as description
    LIMIT 10
    """
    
    # Execute query and translate if needed
    results = run_cypher(cypher)
    
    if language != 'en':
        for result in results:
            result['name'] = translate_text(result['name'], 'en', language)
    
    return results
```

Frontend autocomplete:
```javascript
import { Autocomplete } from '@mui/material';

function ChatboxWithAutocomplete() {
  const [suggestions, setSuggestions] = useState([]);
  const { i18n } = useTranslation();
  
  const handleInputChange = async (event, value) => {
    if (value.length < 2) {
      setSuggestions([]);
      return;
    }
    
    try {
      const response = await fetch(`${import.meta.env.VITE_BACKEND_URL}/autocomplete`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ 
          query: value,
          language: i18n.language 
        })
      });
      
      const data = await response.json();
      setSuggestions(data.suggestions);
    } catch (error) {
      console.error('Autocomplete error:', error);
    }
  };
  
  return (
    <Autocomplete
      freeSolo
      options={suggestions.map(s => s.name)}
      onInputChange={handleInputChange}
      renderInput={(params) => <TextField {...params} placeholder="Search..." />}
    />
  );
}
```

---

## 5. Translation Quality Metrics

Track translation quality:

```python
# Add to backend
from fuzzywuzzy import fuzz

class TranslationQualityTracker:
    def __init__(self):
        self.translations = []
    
    def log_translation(self, original, translated, source_lang, target_lang):
        """Log translation with metadata"""
        self.translations.append({
            'original': original,
            'translated': translated,
            'source_language': source_lang,
            'target_language': target_lang,
            'timestamp': datetime.now(),
            'quality_score': None  # Filled by human review
        })
    
    def get_quality_report(self):
        """Generate quality metrics"""
        if not self.translations:
            return {}
        
        language_pairs = {}
        for trans in self.translations:
            pair = f"{trans['source_language']}-{trans['target_language']}"
            if pair not in language_pairs:
                language_pairs[pair] = {'total': 0, 'reviewed': 0, 'avg_score': 0}
            
            language_pairs[pair]['total'] += 1
            if trans['quality_score']:
                language_pairs[pair]['reviewed'] += 1
                language_pairs[pair]['avg_score'] += trans['quality_score']
        
        return language_pairs

tracker = TranslationQualityTracker()

@app.route('/translation-quality', methods=['GET'])
def translation_quality():
    """Get translation quality metrics"""
    report = tracker.get_quality_report()
    return jsonify(report)
```

---

## 6. Language-Specific Response Formatting

Customize response format based on language:

```python
def format_answer_by_language(answer, language):
    """Format answer based on language preferences"""
    formatting = {
        'en': lambda a: a,
        'hi': lambda a: a.replace('।', '।'),  # Devanagari punctuation
        'ja': lambda a: a,  # Japanese specific formatting
        'ar': lambda a: a,  # Arabic specific formatting
    }
    
    formatter = formatting.get(language, lambda a: a)
    return formatter(answer)
```

---

## 7. Fallback Language Handling

Graceful fallbacks for unsupported languages:

```python
SUPPORTED_LANGUAGES = ['en', 'hi', 'es', 'fr', 'de', 'zh-CN', 'ja', 'pt']
FALLBACK_LANGUAGE = 'en'

def get_fallback_language(requested_lang):
    """Get fallback language if requested not supported"""
    if requested_lang in SUPPORTED_LANGUAGES:
        return requested_lang
    
    # Check if variant exists (e.g., 'hi' for 'hi-IN')
    base_lang = requested_lang.split('-')[0]
    if base_lang in SUPPORTED_LANGUAGES:
        return base_lang
    
    # Fallback to English
    return FALLBACK_LANGUAGE
```

---

## 8. Analytics & Monitoring

Track multilingual usage:

```python
from collections import defaultdict
import json

class MultilingualAnalytics:
    def __init__(self):
        self.language_usage = defaultdict(int)
        self.translation_counts = defaultdict(int)
        self.response_times = defaultdict(list)
    
    def log_query(self, source_lang, target_lang, response_time):
        """Log query metadata"""
        self.language_usage[source_lang] += 1
        key = f"{source_lang}->{target_lang}"
        self.translation_counts[key] += 1
        self.response_times[key].append(response_time)
    
    def get_stats(self):
        """Get analytics summary"""
        return {
            'language_usage': dict(self.language_usage),
            'translation_patterns': dict(self.translation_counts),
            'avg_response_times': {
                k: sum(v) / len(v) if v else 0 
                for k, v in self.response_times.items()
            }
        }

analytics = MultilingualAnalytics()

@app.route('/analytics', methods=['GET'])
def get_analytics():
    """Get multilingual usage analytics"""
    return jsonify(analytics.get_stats())
```

---

## 9. Batch Translation for Performance

Optimize by translating multiple items at once:

```python
def batch_translate(texts, source_lang='en', target_lang='en', max_batch_size=100):
    """Translate multiple texts efficiently"""
    if source_lang == target_lang:
        return texts
    
    translated = []
    for i in range(0, len(texts), max_batch_size):
        batch = texts[i:i + max_batch_size]
        # Translate batch
        batch_result = translator.translate(
            '\n'.join(batch),
            src_language=source_lang,
            dest_language=target_lang
        )
        
        # Split result back
        translated.extend(batch_result['translatedText'].split('\n'))
    
    return translated
```

---

## 10. Custom Translation Memory

Implement translation memory for common phrases:

```python
from sqlite3 import connect

class TranslationMemory:
    def __init__(self, db_path='translation_memory.db'):
        self.conn = connect(db_path)
        self._init_db()
    
    def _init_db(self):
        self.conn.execute('''
            CREATE TABLE IF NOT EXISTS translations (
                id INTEGER PRIMARY KEY,
                source_text TEXT NOT NULL,
                source_lang TEXT NOT NULL,
                target_lang TEXT NOT NULL,
                translated_text TEXT NOT NULL,
                confidence REAL DEFAULT 1.0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        self.conn.commit()
    
    def lookup(self, text, source_lang, target_lang):
        """Look up translation in memory"""
        cursor = self.conn.execute('''
            SELECT translated_text, confidence FROM translations
            WHERE source_text = ? AND source_lang = ? AND target_lang = ?
            ORDER BY confidence DESC LIMIT 1
        ''', (text, source_lang, target_lang))
        
        result = cursor.fetchone()
        return result
    
    def store(self, source_text, source_lang, target_lang, translated_text, confidence=1.0):
        """Store translation in memory"""
        self.conn.execute('''
            INSERT INTO translations 
            (source_text, source_lang, target_lang, translated_text, confidence)
            VALUES (?, ?, ?, ?, ?)
        ''', (source_text, source_lang, target_lang, translated_text, confidence))
        self.conn.commit()

tm = TranslationMemory()

def translate_with_memory(text, source_lang='en', target_lang='en'):
    """Translate using memory first, then API"""
    # Check memory
    result = tm.lookup(text, source_lang, target_lang)
    if result:
        translated_text, confidence = result
        return translated_text
    
    # Translate via API
    translated = translate_text(text, source_lang, target_lang)
    
    # Store in memory
    tm.store(text, source_lang, target_lang, translated)
    
    return translated
```

---

## 11. Multilingual Error Handling

Provide error messages in user's language:

```python
ERROR_MESSAGES = {
    'en': {
        'query_required': 'Query is required',
        'invalid_language': 'Invalid language specified',
        'translation_failed': 'Translation service temporarily unavailable',
        'backend_error': 'Error processing your request'
    },
    'hi': {
        'query_required': 'प्रश्न आवश्यक है',
        'invalid_language': 'अमान्य भाषा निर्दिष्ट',
        'translation_failed': 'अनुवाद सेवा अस्थायी रूप से उपलब्ध नहीं',
        'backend_error': 'आपके अनुरोध को प्रक्रिया करने में त्रुटि'
    }
}

def get_error_message(error_key, language='en'):
    """Get error message in specified language"""
    messages = ERROR_MESSAGES.get(language, ERROR_MESSAGES['en'])
    return messages.get(error_key, 'An error occurred')
```

---

## Configuration Best Practices

Create a config file for multilingual settings:

```python
# config.py
from dataclasses import dataclass
from typing import Dict, List

@dataclass
class MultilingualConfig:
    # Supported languages
    SUPPORTED_LANGUAGES: List[str] = ['en', 'hi', 'es', 'fr', 'de', 'zh-CN', 'ja', 'pt']
    
    # Fallback language
    FALLBACK_LANGUAGE: str = 'en'
    
    # Translation service
    TRANSLATION_SERVICE: str = 'google'  # 'google', 'deepl', 'azure'
    
    # Cache TTL (seconds)
    TRANSLATION_CACHE_TTL: int = 86400  # 24 hours
    
    # Max characters per translation
    MAX_TRANSLATION_LENGTH: int = 5000
    
    # Enable translation memory
    USE_TRANSLATION_MEMORY: bool = True
    
    # RTL languages
    RTL_LANGUAGES: List[str] = ['ar', 'he', 'ur', 'fa']
    
    # Language variants
    LANGUAGE_VARIANTS: Dict[str, str] = {
        'zh': 'zh-CN',
        'pt': 'pt-BR',
        'en': 'en-US'
    }

config = MultilingualConfig()
```

---

These advanced features will make your multilingual chatbot production-ready with better performance, reliability, and user experience.
