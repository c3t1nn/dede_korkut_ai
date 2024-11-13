class StoryStage:
    def __init__(self, stage_name, purpose, must_end_with, prompt_template):
        self.stage_name = stage_name
        self.purpose = purpose
        self.must_end_with = must_end_with
        self.prompt_template = prompt_template

STORY_STRUCTURE = {
    1: StoryStage(
        "Giriş",
        "Kahramanı ve durumu tanıt",
        "ilk zorluk/çatışma",
        """
        Hey hey, hanım hey! {character_name} hakkında bir destan söyleyeyim:
        
        [Sahne: {location}]
        [Durum: {initial_situation}]
        
        Hikaye şu unsurları içermeli:
        1. Kahramanın tanıtımı
        2. Mekanın ve durumun betimlemesi
        3. İlk çatışma/zorluğun ortaya çıkışı
        """
    ),
    2: StoryStage(
        "Gelişme - İlk Çatışma",
        "İlk mücadele ve sonuçları",
        "yeni bir zorluk",
        """
        [Önceki durum: {previous_situation}]
        [Yapılan seçim: {previous_choice}]
        
        Bu bölümde:
        1. Seçimin sonuçlarını göster
        2. İlk mücadeleyi anlat
        3. Yeni bir zorluk ortaya çıkar
        """
    ),
    3: StoryStage(
        "Gelişme - Zorluklar",
        "Mücadelenin zorlaşması",
        "kritik bir an",
        """
        [Gelinen nokta: {current_situation}]
        [Karşılaşılan zorluk: {challenge}]
        
        Bu bölümde:
        1. Zorlukları artır
        2. İç çatışmayı derinleştir
        3. Kritik bir karar anına getir
        """
    ),
    4: StoryStage(
        "Doruk Nokta",
        "En büyük mücadele",
        "final kararı",
        """
        [Kritik an: {climax_situation}]
        [En büyük zorluk: {main_challenge}]
        
        Bu bölümde:
        1. En büyük mücadeleyi anlat
        2. Tüm zorlukları birleştir
        3. Final kararına hazırla
        """
    ),
    5: StoryStage(
        "Sonuç",
        "Hikayenin kapanışı",
        "final",
        """
        [Son durum: {final_situation}]
        [Kader anı: {final_challenge}]
        
        Bu bölümde:
        1. Son mücadeleyi tamamla
        2. Hikayeyi anlamlı bir sonuca bağla
        3. Dede Korkut'un öğüdüyle bitir
        """
    )
}

class ChoiceTemplate:
    def __init__(self, pattern, emotion, consequence):
        self.pattern = pattern
        self.emotion = emotion
        self.consequence = consequence

CHOICE_STRUCTURES = {
    "kahramanca": ChoiceTemplate(
        "[Eylem] için [hedef]e doğru [hareket]",
        "cesaret/yiğitlik",
        "büyük risk ama büyük onur"
    ),
    "akillica": ChoiceTemplate(
        "[Yöntem] ile [hedef]i [eylem]",
        "bilgelik/sabır",
        "güvenli ama zaman alıcı"
    ),
    "yaratici": ChoiceTemplate(
        "[Hedef] için [eylem]i göze almak",
        "yaratıcılık/sürpriz",
        "beklenmedik ama etkili"
    )
}

def get_stage_prompt(stage_num, context):
    """Hikaye aşamasına göre prompt oluştur"""
    if stage_num not in STORY_STRUCTURE:
        raise ValueError("Geçersiz hikaye aşaması")
        
    stage = STORY_STRUCTURE[stage_num]
    return stage.prompt_template.format(**context)

def get_choice_template(choice_type):
    """Seçenek tipine göre şablon döndür"""
    if choice_type not in CHOICE_STRUCTURES:
        raise ValueError("Geçersiz seçenek tipi")
        
    return CHOICE_STRUCTURES[choice_type]