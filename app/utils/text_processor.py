import re
import logging

logger = logging.getLogger(__name__)

class TextProcessor:
    @staticmethod
    def clean_text(text):
        """Metni temizle ve düzenle"""
        try:
            # SEÇENEKLER: kısmını ve sonrasını temizle
            if 'SEÇENEKLER:' in text:
                text = text.split('SEÇENEKLER:')[0]

            # "Üç yol vardı önünde:" gibi ifadeleri temizle
            text = re.sub(r'(?i)[\.\s]*(?:üç|3)\s*yol\s*vardı\s*önünde\s*[:\.]+.*$', '', text)
            text = re.sub(r'(?i)[\.\s]*(?:üç|3)\s*seçenek\s*vardı\s*[:\.]+.*$', '', text)
            text = re.sub(r'(?i)[\.\s]*(?:düşündü|karar\s*verdi).*?(?:önünde|seçenek).*?[:\.]+.*$', '', text)

            # Gereksiz etiketleri temizle
            text = re.sub(r'\*\*.*?\*\*', '', text)
            text = re.sub(r'Kurallar:', '', text)
            text = re.sub(r'ÖNEMLİ:', '', text)
            text = re.sub(r'\d+\.\s', '', text)
            
            # Fazla boşlukları temizle
            text = re.sub(r'\s+', ' ', text)
            
            # Paragrafları düzenle
            sentences = []
            current_sentence = []
            
            for word in text.split():
                current_sentence.append(word)
                if word.endswith(('.', '!', '?')):
                    sentence = ' '.join(current_sentence)
                    # Dede Korkut üslubuna uygun cümle düzenlemeleri
                    if any(marker in sentence.lower() for marker in ['hey', 'mere', 'hanum']):
                        sentences.append(sentence)
                        sentences.append('')  # Boş satır ekle
                    else:
                        sentences.append(sentence)
                    current_sentence = []
            
            if current_sentence:
                sentences.append(' '.join(current_sentence))
            
            # Paragrafları birleştir
            text = '\n\n'.join(s for s in sentences if s)
            
            # Dede Korkut üslubunu güçlendir
            text = TextProcessor.enhance_story_style(text)
            
            # Son noktalama kontrolü
            if not text.endswith(('.', '!', '?')):
                text += '.'
            
            return text.strip()
            
        except Exception as e:
            logger.error(f"Metin temizleme hatası: {e}")
            return text

    @staticmethod
    def enhance_story_style(text):
        """Hikaye metnini Dede Korkut üslubuna uygun hale getir"""
        try:
            # Tekrarlayan kalıpları ekle
            story_patterns = {
                # Başlangıç kalıpları
                r'^(?!Hey hey|Hanum hey|Mere)': 'Hey hey, hanım hey! ',
                
                # Konuşma kalıpları
                r'\b(dedi)\b(?! ki)': r'\1 ki',
                r'\b(söyledi)\b(?! ki)': r'\1 ki',
                
                # Geleneksel betimlemeler
                r'\b(güçlü|kuvvetli)\b': 'göğsü kavi',
                r'\b(cesur|yiğit)\b': 'alp',
                r'\b(kızgın|öfkeli)\b': 'acıkmış aslan gibi',
                r'\b(savaşmak|dövüşmek)\b': 'cenk etmek',
                r'\b(düşman|hasım)\b': 'yağı',
                r'\b(kılıç)\b': 'çelik',
                r'\b(at)\b': 'yağız at',
                r'\b(yay)\b': 'katı yay',
                r'\b(ok)\b': 'kayın ok',
                
                # Eylem kalıpları
                r'\b(düşündü)\b': 'kara kara düşündü',
                r'\b(baktı)\b': 'nazar eyledi',
                r'\b(gitti)\b': 'vardı',
                r'\b(geldi)\b': 'çıkageldi',
                r'\b(anladı)\b': 'fehm eyledi',
                r'\b(ağladı)\b': 'yaş döktü',
                r'\b(sevindi)\b': 'şad oldu',
                
                # Bağlaç ve geçiş ifadeleri
                r'\b(sonra)\b': 'andan sonra',
                r'\b(şimdi)\b': 'şimdiki halde',
                r'\b(birden)\b': 'ansızın',
                r'\b(hemen)\b': 'tez',
            }
            
            for pattern, replacement in story_patterns.items():
                text = re.sub(pattern, replacement, text)
            
            return text
            
        except Exception as e:
            logger.error(f"Üslup geliştirme hatası: {e}")
            return text

    @staticmethod
    def get_choice_emoji(choice_text):
        """Seçeneğe uygun emoji seç"""
        emoji_map = {
            # Savaş ve Mücadele
            'savaş': '⚔️',
            'kılıç': '⚔️',
            'mücadele': '⚔️',
            'dövüş': '⚔️',
            'vuruş': '⚔️',
            'cenk': '⚔️',
            'yiğit': '⚔️',
            'alp': '⚔️',
            
            # Hareket ve Kaçış
            'kaç': '🏃',
            'koş': '🏃',
            'ilerle': '🏃',
            'git': '🏃',
            'var': '🏃',
            'atıl': '🏃',
            
            # Gizlilik ve Strateji
            'gizlen': '👥',
            'saklan': '👥',
            'pusu': '👥',
            'sinsi': '👥',
            
            # Zaman ve Bekleme
            'bekle': '⏳',
            'sabır': '⏳',
            'dur': '⏳',
            'dinlen': '⏳',
            
            # Düşünce ve Plan
            'düşün': '🤔',
            'plan': '🤔',
            'akıl': '🤔',
            'fikir': '🤔',
            'strateji': '🤔',
            'hikmet': '🤔',
            
            # İletişim
            'konuş': '💭',
            'söyle': '💭',
            'anlat': '💭',
            'dile': '💭',
            'sohbet': '💭',
            
            # Yardım ve İşbirliği
            'yardım': '🤝',
            'destek': '🤝',
            'birlik': '🤝',
            'dostluk': '🤝',
            
            # Güç ve Cesaret
            'güç': '💪',
            'cesaret': '🦁',
            'yürek': '❤️',
            'cesur': '🦁',
            
            # Silah ve Savaş
            'ok': '🏹',
            'yay': '🏹',
            'at': '🐎',
            'kalkan': '🛡️',
            'silah': '⚔️',
            
            # Barış ve Dostluk
            'barış': '🕊️',
            'sulh': '🕊️',
            'uzlaş': '🕊️',
            
            # Yolculuk ve Arayış
            'yolculuk': '🗺️',
            'sefer': '🗺️',
            'yol': '🗺️',
            'ara': '🗺️',
            'keşif': '🗺️',
            
            # Diğer
            'merhamet': '🙏',
            'dua': '🙏',
            'tövbe': '🙏',
            'tuzak': '🎯',
            'hile': '🎭',
            'büyü': '✨',
            'sihir': '✨',
        }
        
        choice_text = choice_text.lower()
        for key, emoji in emoji_map.items():
            if key in choice_text:
                return emoji
        return '📜'  # Varsayılan emoji