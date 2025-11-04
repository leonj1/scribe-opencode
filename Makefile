start:
	docker compose up -d

stop:
	docker compose down

restart: stop start

.PHONY: start stop restart