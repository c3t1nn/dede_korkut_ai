import google.generativeai as genai
import time
import logging
import re
from functools import lru_cache
from tenacity import retry, stop_after_attempt, wait_exponential
from flask import session
from ..config import Config
from .text_processor import TextProcessor

logger = logging.getLogger(__name__)

class RateLimiter:
    def __init__(self):
        self.requests = []
        self.window = 60
        
    def can_make_request(self):
        now = time.time()
        self.requests = [req for req in self.requests if now - req < self.window]
        return len(self.requests) < Config.API_RATE_LIMIT
        
    def add_request(self):
        self.requests.append(time.time())

class StoryGenerator:
    def __init__(self):
        self.rate_limiter = RateLimiter()
        self.text_processor = TextProcessor()
        genai.configure(api_key=Config.GOOGLE_API_KEY)

    def _build_initial_prompt(self, character_name):
        """İlk bölüm için prompt oluştur"""
        return f"""
        Hey hey, hanım hey! {character_name} hakkında bir destan anlatayım:
        
        Kurallar:
        1. Dede Korkut üslubuyla anlat
        2. "Hey hey!", "Mere!", "Hanum hey!" gibi ünlemler kullan
        3. Oğuz Türkçesi deyişler ve benzetmeler ekle
        4. Kahramanın iç dünyasını yansıt
        5. Hikayeyi bir karar anına getir
        
        Hikayenin sonunda tam olarak bu formatta üç seçenek sun:
        SEÇENEKLER:
        • [Eylem]: [Detaylı açıklama]
        • [Eylem]: [Detaylı açıklama]
        • [Eylem]: [Detaylı açıklama]
        """

    def _build_continuation_prompt(self, character_name, previous_text, choice):
        """Devam bölümü için prompt oluştur"""
        return f"""
        [Önceki Bölüm Özeti: {previous_text[-300:]}]
        [Kahramanın Seçimi: {choice}]
        
        {character_name}'in destanı seçimine göre devam ediyor.
        
        Kurallar:
        1. İlk paragrafta seçimin sonuçlarını göster
        2. Yeni zorluklar ortaya çıkar
        3. Kahramanın değişimini yansıt
        4. Hikayeyi yeni bir karar anına getir
        
        Hikayenin sonunda tam olarak bu formatta üç seçenek sun:
        SEÇENEKLER:
        • [Eylem]: [Detaylı açıklama]
        • [Eylem]: [Detaylı açıklama]
        • [Eylem]: [Detaylı açıklama]
        """

    def _build_final_prompt(self, character_name, all_choices, previous_text):
        """Son bölüm için özel prompt"""
        return f"""
        [Tüm Seçimler: {', '.join(all_choices)}]
        [Son Durum: {previous_text[-300:]}]
        
        {character_name}'in destanının son bölümü.
        
        Kurallar:
        1. Önceki seçimlerin sonuçlarını özetle
        2. Kahramanın yaşadığı değişimi anlat
        3. Destandan çıkarılacak dersi göster
        4. Hikayeyi şu şekilde bitir:
        
        "Dedem Korkut geldi, kopuz çaldı, boy boyladı. Dedi ki: [Destanın öğüdü]"
        """

    def generate_story_content(self, prompt):
        """API çağrısı yaparak hikaye üret"""
        try:
            if not self.rate_limiter.can_make_request():
                time.sleep(4)
            
            self.rate_limiter.add_request()
            
            model = genai.GenerativeModel('gemini-pro',
                generation_config={
                    'temperature': 0.9,
                    'top_p': 0.9,
                    'top_k': 40,
                    'max_output_tokens': Config.MAX_OUTPUT_TOKENS,
                }
            )
            
            response = model.generate_content(prompt)
            
            if not response or not response.text:
                raise Exception("Boş yanıt alındı")
                
            return response.text
            
        except Exception as e:
            logger.error(f"Hikaye üretme hatası: {e}")
            return "Dedem Korkut der ki: Bir hata oluştu, hikayeyi anlatamadım..."

    def _extract_story_and_choices(self, text):
        """Hikaye metnini ve seçenekleri standart formatta ayır"""
        try:
            parts = text.split('SEÇENEKLER:')
            story = parts[0].strip()
            
            choices = {}
            if len(parts) > 1:
                options = re.findall(r'•\s*([^•\n]+)', parts[1])
                for i, option in enumerate(options[:3], 1):
                    # Başlık ve açıklamayı ayır
                    if ':' in option:
                        title, description = [part.strip() for part in option.split(':', 1)]
                    else:
                        # Eğer : ile ayrılmamışsa, ilk kelimeyi başlık yap
                        words = option.strip().split()
                        title = words[0]
                        description = ' '.join(words[1:]) if len(words) > 1 else ''

                    # Başlıktaki gereksiz parantezli kısmı temizle
                    title = re.sub(r'\s*\([^)]*\)\s*$', '', title)
                    
                    # Emoji seç
                    emoji = self.text_processor.get_choice_emoji(title)
                    
                    choices[str(i)] = {
                        "text": {
                            "title": f"{title}:",
                            "description": description
                        },
                        "emoji": emoji
                    }
            
            return story, choices
            
        except Exception as e:
            logger.error(f"Seçenek ayrıştırma hatası: {e}")
            return text, {}

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10))
    def generate_story_part(self, character_name, stage="introduction", choice=None):
        """Hikayenin bir bölümünü oluştur"""
        try:
            # Prompt oluştur
            if stage == "introduction":
                prompt = self._build_initial_prompt(character_name)
            elif stage == "conclusion":
                all_choices = session.get('choices_made', [])
                previous_text = session.get('story_parts', [{}])[-1].get('text', '')
                prompt = self._build_final_prompt(character_name, all_choices, previous_text)
            else:
                previous_text = session.get('story_parts', [{}])[-1].get('text', '')
                prompt = self._build_continuation_prompt(character_name, previous_text, choice)
            
            # Hikayeyi üret
            story_text = self.generate_story_content(prompt)
            
            # Son bölüm değilse hikaye ve seçenekleri ayır
            if stage != "conclusion":
                story_text, choices = self._extract_story_and_choices(story_text)
            else:
                story_text = self.text_processor.clean_text(story_text)
                choices = {}
            
            return {
                'text': story_text,
                'choices': choices,
                'stage': stage
            }
            
        except Exception as e:
            logger.error(f"Hikaye bölümü oluşturma hatası: {e}")
            return {
                'text': "Dedem Korkut der ki: Hikayeyi devam ettiremedim...",
                'choices': {
                    "1": {
                        "text": {
                            "title": "Yeniden dene:",
                            "description": "Hikayeyi baştan başlat"
                        },
                        "emoji": "🔄"
                    }
                },
                'stage': stage
            }

    def continue_story(self, character, current_stage, choice):
        """Hikayeyi seçime göre devam ettir"""
        next_stage = "conclusion" if current_stage == "development" else "development"
        return self.generate_story_part(character, next_stage, choice)