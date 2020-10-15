FROM node:4.6
WORKDIR /app
ADD . /app
RUN ls -ltrh
RUN echo " this is a test "
WORKDIR /app/basics
RUN echo "##### DEBUG LINE ######"
RUN ls -ltrh
RUN npm install
EXPOSE 3000
CMD npm start
