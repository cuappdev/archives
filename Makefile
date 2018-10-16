vendor_clean:
	rm -rf vendor
	rm go.mod
	rm go.sum

vendor_init:
	export GO111MODULE=on
	go mod init
	go mod vendor

run:
	docker-compose up

test:
	gometalinter ./...  --vendor
	go test -race -v ./...

docs:
	godoc -http=:6060
