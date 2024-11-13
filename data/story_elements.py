STORY_ELEMENTS = {
    "Boğaç Han": {
        "introduction": {
            "title": "Boğaç Han'ın Doğuşu",
            "setting": "Oğuz boyunun av meydanı",
            "initial_situation": "Bayındır Han'ın toy meydanında azgın bir boğa ortaya çıkar",
            "challenge": "Azgın boğayla yüzleşme",
            "choices": {
                "1": {
                    "text": "Boğayla yiğitçe güreşmek",
                    "result": "kahramanca_confrontation",
                    "emoji": "⚔️"
                },
                "2": {
                    "text": "Boğayı akıl ve kuvvetle alt etmek",
                    "result": "strategic_victory",
                    "emoji": "🤔"
                },
                "3": {
                    "text": "Boğadan kaçıp fırsat kollamak",
                    "result": "tactical_retreat",
                    "emoji": "🏃"
                }
            }
        },
        "development": {
            "kahramanca_confrontation": {
                "title": "Boğayla Mücadele",
                "situation": "Boğayla göğüs göğüse çarpışma",
                "challenge": "Boğanın gücüyle başa çıkma",
                "choices": {
                    "1": {
                        "text": "Boğayı alnından yakalayıp devirmek",
                        "result": "direct_victory",
                        "emoji": "💪"
                    },
                    "2": {
                        "text": "Boğayı yorup zayıf düşürmek",
                        "result": "tactical_victory",
                        "emoji": "⏳"
                    }
                }
            },
            "strategic_victory": {
                "title": "Akıllı Savaşçı",
                "situation": "Boğanın zayıf noktasını keşfetme",
                "challenge": "Doğru anı kollama",
                "choices": {
                    "1": {
                        "text": "Ani bir hamleyle saldırmak",
                        "result": "surprise_victory",
                        "emoji": "⚡"
                    },
                    "2": {
                        "text": "Boğayı çevrede oyalamak",
                        "result": "tire_out",
                        "emoji": "🎯"
                    }
                }
            },
            "tactical_retreat": {
                "title": "Geri Çekilme",
                "situation": "Güvenli bir mesafeden boğayı gözlemleme",
                "challenge": "Uygun fırsatı yakalama",
                "choices": {
                    "1": {
                        "text": "Ani bir baskınla şaşırtmak",
                        "result": "surprise_victory",
                        "emoji": "🎭"
                    },
                    "2": {
                        "text": "Yardım çağırmak",
                        "result": "seek_help",
                        "emoji": "🤝"
                    }
                }
            }
        },
        "conclusion": {
            "direct_victory": {
                "title": "Kahramanın Zaferi",
                "ending": "Boğaç Han adını alıp Oğuz'un yiğidi olma",
                "final_text": "Dedem Korkut geldi, kopuz çaldı, boy boyladı. Dedi: 'Yiğidim, sen boğayı yendin, bundan sonra adın Boğaç Han olsun!'"
            },
            "tactical_victory": {
                "title": "Akıllı Yiğidin Zaferi",
                "ending": "Hem gücü hem aklıyla nam salma",
                "final_text": "Dedem Korkut kopuzunu eline aldı, dedi: 'Hem güçlü hem akıllı yiğidim, adın dillere destan olsun!'"
            },
            "surprise_victory": {
                "title": "Beklenmedik Zafer",
                "ending": "Kurnazlığıyla destanlara konu olma",
                "final_text": "Dedem Korkut sözü açtı: 'Yiğidim, sen ki düşmanını şaşırttın, bundan böyle adın dilden dile dolaşsın!'"
            },
            "seek_help": {
                "title": "Alçakgönüllü Kahraman",
                "ending": "Birlik ve beraberliğin gücünü gösterme",
                "final_text": "Dedem Korkut dedi: 'Oğul, sen ki yalnız güce değil, birliğe de değer verdin. Adın ve namın daim olsun!'"
            }
        }
    },
    "Deli Dumrul": {
        "introduction": {
            "title": "Deli Dumrul'un Meydan Okuması",
            "setting": "Kuru çayın üstündeki köprü",
            "initial_situation": "Deli Dumrul köprüsünden geçenlerden haraç alır",
            "challenge": "Azrail'le karşılaşma",
            "choices": {
                "1": {
                    "text": "Azrail'e meydan okumak",
                    "result": "brave_challenge",
                    "emoji": "⚔️"
                },
                "2": {
                    "text": "Azrail'le pazarlık yapmak",
                    "result": "negotiation",
                    "emoji": "🤝"
                },
                "3": {
                    "text": "Tövbe edip af dilemek",
                    "result": "repentance",
                    "emoji": "🙏"
                }
            }
        },
        "development": {
            "brave_challenge": {
                "title": "Azrail'le Yüzleşme",
                "situation": "Azrail'le mücadele",
                "challenge": "Ölümle dans",
                "choices": {
                    "1": {
                        "text": "Can için savaşmak",
                        "result": "fight_for_life",
                        "emoji": "⚔️"
                    },
                    "2": {
                        "text": "Başkasının canını istemek",
                        "result": "seek_another_soul",
                        "emoji": "🔄"
                    }
                }
            },
            "negotiation": {
                "title": "Pazarlık",
                "situation": "Azrail'le anlaşma arayışı",
                "challenge": "Ölümden kaçış yolu bulma",
                "choices": {
                    "1": {
                        "text": "Can karşılığı can teklif etmek",
                        "result": "soul_exchange",
                        "emoji": "🔄"
                    },
                    "2": {
                        "text": "Allah'a yakarış",
                        "result": "divine_plea",
                        "emoji": "🙏"
                    }
                }
            }
        },
        "conclusion": {
            "fight_for_life": {
                "title": "Son Mücadele",
                "ending": "Eşinin aşkıyla hayatta kalma",
                "final_text": "Dedem Korkut der: Deli Dumrul ve eşi, gerçek aşkın gücüyle ölümü yendiler."
            },
            "seek_another_soul": {
                "title": "Fedakarlık",
                "ending": "Sevginin gücünü anlama",
                "final_text": "Dedem Korkut der: Deli Dumrul, can için can ararken sevginin değerini anladı."
            },
            "soul_exchange": {
                "title": "Aşkın Zaferi",
                "ending": "Gerçek sevginin gücü",
                "final_text": "Dedem Korkut der: Deli Dumrul'un eşi, aşkı uğruna canını vermeye razı oldu."
            },
            "divine_plea": {
                "title": "İlahi Af",
                "ending": "Allah'ın merhametine sığınma",
                "final_text": "Dedem Korkut der: Allah, Deli Dumrul'un tövbesini kabul eyledi."
            }
        }
    }
}

def get_character_info(character_name):
    """Karakter bilgilerini getir"""
    if character_name not in STORY_ELEMENTS:
        raise ValueError(f"Karakter bulunamadı: {character_name}")
    
    character = STORY_ELEMENTS[character_name]
    return {
        "title": character["introduction"]["title"],
        "setting": character["introduction"]["setting"],
        "initial_situation": character["introduction"]["initial_situation"]
    }

def get_story_stage(character_name, stage, previous_choice=None):
    """Hikayenin belirli bir aşamasını getir"""
    if character_name not in STORY_ELEMENTS:
        raise ValueError(f"Karakter bulunamadı: {character_name}")
    
    character = STORY_ELEMENTS[character_name]
    
    if stage == "introduction":
        return character["introduction"]
    elif stage == "development":
        # Önceki seçimin sonucunu kullan
        choice_result = character["introduction"]["choices"][previous_choice]["result"]
        return character["development"][choice_result]
    elif stage == "conclusion":
        # Development aşamasındaki son seçimin sonucunu kullan
        current_development = character["development"][previous_choice]
        last_choice = current_development["choices"]["1"]["result"]  # Varsayılan olarak ilk sonucu al
        return {
            "title": character["conclusion"][last_choice]["title"],
            "ending": character["conclusion"][last_choice]["ending"],
            "final_text": character["conclusion"][last_choice]["final_text"]
        }
    else:
        raise ValueError("Geçersiz hikaye aşaması")

def get_available_choices(character_name, stage, previous_choice=None):
    """Mevcut aşamadaki seçenekleri getir"""
    story_stage = get_story_stage(character_name, stage, previous_choice)
    return story_stage.get("choices", {})

def get_story_context(character_name, stage, previous_choice=None):
    """Hikaye bağlamını getir"""
    story_stage = get_story_stage(character_name, stage, previous_choice)
    return {
        "title": story_stage.get("title", ""),
        "setting": story_stage.get("setting", ""),
        "situation": story_stage.get("situation", ""),
        "challenge": story_stage.get("challenge", ""),
        "initial_situation": story_stage.get("initial_situation", ""),
        "ending": story_stage.get("ending", ""),
        "final_text": story_stage.get("final_text", "")
    }