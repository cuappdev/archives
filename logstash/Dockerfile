# https://github.com/elastic/logstash-docker
FROM docker.elastic.co/logstash/logstash:latest
USER root
COPY mysql-connector-java-5.1.44-bin.jar /opt/
# Add your logstash plugins setup here
RUN logstash-plugin install logstash-input-jdbc
# Example: RUN logstash-plugin install logstash-filter-json
RUN logstash-plugin install logstash-filter-aggregate
