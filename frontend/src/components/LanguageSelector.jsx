import React from 'react';
import { useTranslation } from 'react-i18next';
import { Globe } from 'lucide-react';

function LanguageSelector() {
  const { i18n } = useTranslation();
  
  const languages = [
    { code: 'en', name: 'English', flag: '🇬🇧' },
    { code: 'hi', name: 'हिन्दी', flag: '🇮🇳' },
    { code: 'es', name: 'Español', flag: '🇪🇸' },
    { code: 'fr', name: 'Français', flag: '🇫🇷' }
  ];
  
  const handleLanguageChange = (langCode) => {
    i18n.changeLanguage(langCode);
  };
  
  return (
    <div className="flex items-center gap-2">
      <Globe className="w-4 h-4 text-cyan-400" />
      <select 
        value={i18n.language} 
        onChange={(e) => handleLanguageChange(e.target.value)}
        className="px-3 py-2 bg-slate-700/50 border border-cyan-500/30 rounded-lg text-cyan-400 focus:outline-none focus:border-cyan-500 transition-colors hover:border-cyan-500/50 cursor-pointer"
      >
        {languages.map(lang => (
          <option key={lang.code} value={lang.code} className="bg-slate-800">
            {lang.flag} {lang.name}
          </option>
        ))}
      </select>
    </div>
  );
}

export default LanguageSelector;
