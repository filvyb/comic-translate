from typing import Any

from .base import TraditionalTranslation
from ..utils.textblock import TextBlock


class DeepLTranslation(TraditionalTranslation):
    """Translation engine using DeepL API."""

    def __init__(self):
        self.source_lang_code = None
        self.target_lang_code = None
        self.api_key = None
        self.client = None
        self.target_lang = None

    def initialize(self, settings: Any, source_lang: str, target_lang: str) -> None:

        import deepl

        self.target_lang = target_lang

        raw_src = self.get_language_code(source_lang)
        raw_tgt = self.get_language_code(target_lang)
        self.source_lang_code = self.preprocess_source_language_code(raw_src)
        self.target_lang_code = self.preprocess_language_code(raw_tgt)

        credentials = settings.get_credentials(settings.ui.tr("DeepL"))
        self.api_key = credentials.get('api_key', '')

        self.client = deepl.DeepLClient(self.api_key)

    def translate(self, blk_list: list[TextBlock]) -> list[TextBlock]:
        texts_to_translate = []
        block_indices = []

        for i, blk in enumerate(blk_list):
            text = self.preprocess_text(blk.text, self.source_lang_code)
            if text.strip():
                texts_to_translate.append(text)
                block_indices.append(i)
            else:
                blk.translation = ''

        if not texts_to_translate:
            return blk_list

        results = self.client.translate_text(
            texts_to_translate,
            source_lang=self.source_lang_code,
            target_lang=self.target_lang_code,
            split_sentences='off',
            model_type='prefer_quality_optimized'
        )

        for idx, result in zip(block_indices, results):
            blk_list[idx].translation = result.text

        return blk_list 
    
    def preprocess_source_language_code(self, lang_code: str) -> str:
        if 'zh' in lang_code.lower():
            return 'ZH'
        return lang_code.upper()

    def preprocess_language_code(self, lang_code: str) -> str:
        if lang_code == 'zh-CN':
            return 'ZH-HANS'
        if lang_code == 'zh-TW':
            return 'ZH-HANT'
        if lang_code == 'en':
            return 'EN-US'
        if lang_code == 'pt':
            return 'PT-PT' 

        # fallback: e.g. 'fr' → 'FR', 'de' → 'DE'
        return lang_code.upper()