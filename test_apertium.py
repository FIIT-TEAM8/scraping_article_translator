import apertium

translator = apertium.Translator("en", "spa")

print(translator.translate("Hello world, Hello dogs!"))