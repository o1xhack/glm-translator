import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from utils import ArgumentParser, LOG
from translator import PDFTranslator, TranslationConfig

if __name__ == "__main__":
    argument_parser = ArgumentParser()
    args = argument_parser.parse_arguments()

    config = TranslationConfig()
    config.initialize(args)    

    translator = PDFTranslator(api_key=config.api_key, model_name=config.model_name)
    translator.translate_pdf(
        config.input_file,
        config.output_file_format,
        config.source_language,
        config.target_language,
        getattr(config, 'translation_style', '标准'),
        pages=3
    )

