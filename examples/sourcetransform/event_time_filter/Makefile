TAG ?= stable
PUSH ?= false

.PHONY: image-push
image-push:
	docker buildx build -t "quay.io/numaio/numaflow-python/mapt-event-time-filter:${TAG}" --platform linux/amd64,linux/arm64 . --push

.PHONY: image
image:
	docker build -t "quay.io/numaio/numaflow-python/mapt-event-time-filter:${TAG}" .
	@if [ "$(PUSH)" = "true" ]; then docker push "quay.io/numaio/numaflow-python/mapt-event-time-filter:${TAG}"; fi

.PHONY: clean
clean:
	rm -rf ./dist
