#!/usr/bin/make
# Makefile readme (ru): <http://linux.yaroslavl.ru/docs/prog/gnu_make_3-79_russian_manual.html>
# Makefile readme (en): <https://www.gnu.org/software/make/manual/html_node/index.html#SEC_Contents>

SHELL = /bin/sh

.PHONY : help \
		 dev \
		 pull

.DEFAULT_GOAL : help
.SILENT : dev

help: ## Show this help
	@printf "\033[33m%s:\033[0m\n" 'Available commands'
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z0-9_-]+:.*?## / {printf "  \033[32m%-11s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)

dev: ## Run develop container
	docker run --rm -v "$$(pwd)/ha_conf:/config:rw" -v "$$(pwd)/custom_components:/config/custom_components" -p 8080:8123 homeassistant/home-assistant

pull: ## Get latest Home Assistant container
	docker pull homeassistant/home-assistant