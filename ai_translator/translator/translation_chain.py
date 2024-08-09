from zhipuai import ZhipuAI
from utils import LOG
import pandas as pd

class TranslationChain:
    def __init__(self, api_key: str, model_name: str = "glm-4"):
        self.client = ZhipuAI(api_key=api_key)
        self.model_name = model_name

    def run(self, content, source_language: str, target_language: str, translation_style: str) -> (str, bool):
        if isinstance(content, pd.DataFrame):
            # Handle DataFrame (table) translation
            translated_content = self.translate_table(content, source_language, target_language, translation_style)
        else:
            # Handle text translation
            translated_content = self.translate_text(content, source_language, target_language, translation_style)
        
        return translated_content, True

    def translate_text(self, text: str, source_language: str, target_language: str, translation_style: str) -> str:
        messages = [
            {"role": "system", "content": f"You are a translation expert. Translate from {source_language} to {target_language} in the style of {translation_style}. Maintain the original format and structure."},
            {"role": "user", "content": text}
        ]

        try:
            response = self.client.chat.completions.create(
                model=self.model_name,
                messages=messages
            )
            
            result = response.choices[0].message.content
            return result

        except Exception as e:
            LOG.error(f"An error occurred during text translation: {e}")
            return ""

    def translate_table(self, df: pd.DataFrame, source_language: str, target_language: str, translation_style: str) -> pd.DataFrame:
        translated_df = df.copy()
        for col in df.columns:
            col_content = df[col].astype(str).tolist()
            col_text = "\n".join(col_content)
            translated_text = self.translate_text(col_text, source_language, target_language, translation_style)
            translated_content = translated_text.split("\n")
            
            # Ensure the translated content has the same length as the original
            if len(translated_content) != len(df):
                LOG.warning(f"Translation length mismatch for column {col}. Adjusting...")
                if len(translated_content) > len(df):
                    translated_content = translated_content[:len(df)]
                else:
                    translated_content.extend([""] * (len(df) - len(translated_content)))
            
            translated_df[col] = translated_content
        return translated_df
        
  