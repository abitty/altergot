from coins.models import Coin
import os
from django.conf import settings
from django.core.management.base import BaseCommand, CommandError

class Command(BaseCommand):
	help = 'Deletes all unused images from media/upload folder'
	imagedir = os.path.join(settings.BASE_DIR, 'media/uploads/')

	def add_arguments(self, parser):
		parser.add_argument('--dry-run', 
            action='store_true',
            dest='dryrun',
            default=False,
            help='check for unused files without deleting them')
		
	def get_used_media(self):
		cn = Coin.objects.all()
		used_images = []
		for c in cn:
			if c.avers:
				used_images.append(os.path.split(c.avers.url)[1])
			if c.revers:
				used_images.append(os.path.split(c.revers.url)[1])
		return used_images 
		
	def get_all_media(self):
		media = []
		for fn in os.listdir(self.imagedir):
			fullfn = os.path.join(self.imagedir,fn)
			if os.path.isfile(fullfn):
				media.append(fn)
		return media
		
	def get_unused_media(self):
		used_media = self.get_used_media()
		print (len(used_media), " used images found")
		all_media = self.get_all_media()
		print (len(all_media)," total files")
		return [x for x in all_media if x not in used_media]
		

	def handle(self, *args, **options):
		dryrun = False
		if options['dryrun']:
			dryrun = True
		unused = self.get_unused_media()
		if dryrun:
			if len(unused):
				print(len(unused), " files to be deleted")
				for fn in unused:
					print(fn)
			else:
				print ("no unused images was found")
		else:
			for fn in unused:
				os.remove(os.path.join(self.imagedir,fn))
			if len(unused):
				print (len(unused)," fileas were deleted")
