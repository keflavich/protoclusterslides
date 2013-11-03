CURRENT_BRANCH = $(shell git name-rev --name-only HEAD)
ifndef CURRENT_BRANCH
CURRENT_BRANCH = $(error Could not get current branch.)
endif

DATE=$(shell date)

BUILDDIR=build

deploy: clean
	ghp-import build/
	git push
	#git checkout gh-pages
	#-cp build/* .
	#-git add *.html
	#-git commit -m 'Automatic build commit on $(DATE).'
	#git checkout ${CURRENT_BRANCH}
	#git push

clean: 
	echo "Clean, I think"
