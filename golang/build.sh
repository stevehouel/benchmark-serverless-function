go get github.com/aws/aws-lambda-go/lambda
go get github.com/aws/aws-lambda-go/events
GOOS=linux GOARCH=amd64 go build -o bin/handler handler.go
cd bin
zip deploy-package.zip handler