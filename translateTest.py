from argostranslate import package, translate
package.install_from_path('translate-ru_en-1_0.argosmodel')
installed_languages = translate.get_installed_languages()
print([str(lang) for lang in installed_languages])

translation = installed_languages[0].get_translation(installed_languages[1])
print(translation)
print(translation.translate("Привет!"))
