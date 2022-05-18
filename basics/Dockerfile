FROM ubuntu:latest as coverage
RUN sleep 10
RUN echo "Run coverage"

FROM alpine:latest as unittest
RUN sleep 10
RUN echo "Run unit tests"

FROM node:4.6 as finalartifact
RUN sleep 10
RUN echo "produce artifact"

WORKDIR /app
ADD . /app

RUN npm install
EXPOSE 3000
CMD npm start
