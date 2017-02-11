import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tutorial_project.settings')

import django

django.setup()

from tutorial_app.models import Definition, Word, UserProfile, Language

def add_lang(name, views=0):
	l = Language.objects.get_or_create(name=name)[0]
	l.views = views
	return l 

def add_word(lang, name, views=0):
	w = Word.objects.get_or_create(language=lang, name=name)[0]
	w.views = views
	w.save()
	return w

def add_def(word, definition, likes=0, dislikes=0):
	d = Definition.objects.get_or_create(word=word, definition=definition)[0]
	d.likes = likes
	d.dislikes = dislikes
	d.save()
	return d



def populate():
	python_lang = add_lang('Python')

	database_word = add_word(lang=python_lang, name='database')

	add_def(word=database_word, definition="Official Python Tutorial")
	
	add_def(word=database_word, definition="un Official Python Tutorial")
	
	add_def(word=database_word, definition="new Official Python Tutorial")

	jaca_lang = add_lang('Python')

	skatch_word = add_word(lang=java_lang, name='database')

	add_def(word=database_word, definition="Official Python Tutorial")
	
	add_def(word=database_word, definition="Official Python Tutorial")
	
	add_def(word=database_word, definition="Official Python Tutorial")

	ruby_lang = add_lang('Python')

	database_word = add_word(lang=ruby_lang, name='database')

	add_def(word=database_word, definition="Official Python Tutorial")
	
	add_def(word=database_word, definition="Official Python Tutorial")
	
	add_def(word=database_word, definition="Official Python Tutorial")

	
	for l in  Language.objects.all():
		for w in word.objects.filter(language=l):
			for d in definition.objects.filter(word=w):
				print "- {0} - {1}".format(str(l), str(w), str(d))

if __name__=='__main__':

	print "Starting  population script..."
	populate()
