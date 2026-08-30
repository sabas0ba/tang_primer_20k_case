PYTHON ?= python
PODMAN ?= podman
IMAGE ?= sabas0ba/tang-primer-dev

.PHONY: test release check container-build container-check

test:
	$(PYTHON) -m unittest discover -s tests -v

release:
	$(PYTHON) build_release.py

check: test release

container-build:
	$(PODMAN) build --file Containerfile --tag $(IMAGE) .

container-check:
	$(PODMAN) run --rm --volume "$(CURDIR):/workspace" $(IMAGE) make check
