from flask import render_template, request, session, jsonify, send_file, current_app
from . import app
from .utils.story_generator import StoryGenerator
import logging
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib import colors
import os
from datetime import datetime

logger = logging.getLogger(__name__)
story_generator = StoryGenerator()

@app.route('/')
def home():
    """Ana sayfa"""
    try:
        session.clear()
        return render_template('index.html')
    except Exception as e:
        logger.error(f"Ana sayfa hatası: {e}")
        return render_template('error.html', error="Bir hata oluştu.")

@app.route('/start_story', methods=['POST'])
def start_story():
    """Hikayeyi başlat"""
    try:
        character = request.form.get('character')
        if not character:
            raise ValueError("Karakter seçilmedi")

        # Oturum bilgilerini başlat
        session['character'] = character
        session['stage'] = "introduction"
        session['story_parts'] = []
        session['choices_made'] = []

        # İlk hikaye bölümünü oluştur
        story_data = story_generator.generate_story_part(character_name=character)
        
        # Hikaye bölümünü kaydet
        story_part = {
            'text': story_data['text'],
            'choices': story_data.get('choices', {}),
            'stage': 'introduction',
            'previous_choice': None,
            'previous_choice_emoji': None
        }
        session['story_parts'] = [story_part]

        return render_template('story.html',
                             character=character,
                             story_parts=session['story_parts'],
                             current_part=story_part,
                             progress=1,
                             total_parts=3)
    except Exception as e:
        logger.error(f"Hikaye başlatma hatası: {e}")
        return render_template('error.html', error="Hikaye başlatılamadı.")

@app.route('/continue_story', methods=['POST'])
def continue_story():
    """Hikayeyi devam ettir"""
    try:
        character = session.get('character')
        current_stage = session.get('stage')
        story_parts = session.get('story_parts', [])
        choices_made = session.get('choices_made', [])

        if not all([character, current_stage, story_parts]):
            raise ValueError("Geçersiz oturum durumu")

        choice = request.form.get('choice')
        if not choice:
            raise ValueError("Geçersiz seçim")

        # Seçimi kaydet
        current_choices = story_parts[-1].get('choices', {})
        choice_data = current_choices.get(choice)
        if not choice_data:
            raise ValueError("Geçersiz seçim")

        # Seçim bilgisini kaydet
        choice_text = choice_data['text']['title']
        choices_made.append(choice_text)
        session['choices_made'] = choices_made

        # Hikayeyi devam ettir
        next_stage = "conclusion" if current_stage == "development" else "development"
        story_data = story_generator.generate_story_part(
            character_name=character,
            stage=next_stage,
            choice=choice_text
        )

        # Hikaye bölümünü kaydet
        story_part = {
            'text': story_data['text'],
            'choices': story_data.get('choices', {}),
            'stage': story_data['stage'],
            'previous_choice': choice_text,
            'previous_choice_emoji': choice_data['emoji']
        }
        
        story_parts.append(story_part)
        session['story_parts'] = story_parts
        session['stage'] = story_data['stage']

        return render_template('story.html',
                             character=character,
                             story_parts=story_parts,
                             current_part=story_part,
                             progress=len(story_parts),
                             total_parts=3,
                             choices_made=choices_made)
    except Exception as e:
        logger.error(f"Hikaye devam hatası: {e}")
        return render_template('error.html', error="Hikaye devam ettirilemedi.")

@app.route('/save_story_pdf', methods=['POST'])
def save_story_pdf():
    """Hikayeyi PDF olarak kaydet"""
    try:
        story_parts = session.get('story_parts', [])
        character = session.get('character')
        
        if not story_parts or not character:
            raise ValueError("Hikaye bulunamadi")

        # PDF dosya adı
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"destan_{character.lower().replace(' ', '_').replace('ğ', 'g').replace('ı', 'i')}_{timestamp}.pdf"
        
        # PDF'i oluştur ve kaydet
        downloads_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'static', 'downloads')
        os.makedirs(downloads_dir, exist_ok=True)
        filepath = os.path.join(downloads_dir, filename)

        # PDF oluştur
        c = canvas.Canvas(filepath, pagesize=A4)
        width, height = A4
        
        # Başlık
        c.setFont("Helvetica-Bold", 24)
        title = f"{character}'in Destani"
        title = title.replace('ğ', 'g').replace('ı', 'i')
        c.drawCentredString(width/2, height-50, title)
        
        # İçerik
        y = height-100
        for i, part in enumerate(story_parts, 1):
            # Bölüm başlığı
            if y < 100:  # Sayfa sonuna yaklaşıldıysa
                c.showPage()
                y = height-50
            
            c.setFont("Helvetica-Bold", 16)
            c.drawString(50, y, f"Bolum {i}")
            y -= 30
            
            # Bölüm metni
            c.setFont("Helvetica", 12)
            text = part['text'].replace('ğ', 'g').replace('ı', 'i').replace('ş', 's').replace('ö', 'o').replace('ü', 'u').replace('ç', 'c')
            
            # Metni satırlara böl
            words = text.split()
            line = []
            for word in words:
                line.append(word)
                line_text = ' '.join(line)
                if c.stringWidth(line_text, "Helvetica", 12) > width-100:
                    line.pop()
                    c.drawString(50, y, ' '.join(line))
                    line = [word]
                    y -= 20
                    if y < 50:  # Sayfa sonuna yaklaşıldıysa
                        c.showPage()
                        y = height-50
            if line:
                c.drawString(50, y, ' '.join(line))
                y -= 30
            
            # Seçim
            if 'previous_choice' in part and part['previous_choice']:
                c.setFont("Helvetica-Oblique", 12)
                choice_text = f"➤ {part['previous_choice']}".replace('ğ', 'g').replace('ı', 'i')
                c.drawString(50, y, choice_text)
                y -= 40
        
        c.save()
        
        # PDF'i indir
        return send_file(
            filepath,
            as_attachment=True,
            download_name=filename,
            mimetype='application/pdf'
        )

    except Exception as e:
        logger.error(f"PDF oluşturma hatası: {e}")
        return jsonify({"success": False, "error": str(e)})

@app.route('/reset_story', methods=['POST'])
def reset_story():
    """Hikayeyi sıfırla"""
    try:
        session.clear()
        return jsonify({"success": True})
    except Exception as e:
        logger.error(f"Sıfırlama hatası: {e}")
        return jsonify({"success": False, "error": str(e)})