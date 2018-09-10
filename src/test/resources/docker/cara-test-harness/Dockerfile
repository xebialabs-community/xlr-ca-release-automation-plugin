FROM fedora:25

MAINTAINER Benoit Moussaud

RUN dnf -y install procps net-tools pcre pcre-static python && \
    dnf clean all
RUN pip install --upgrade pip
RUN pip install flask
RUN mkdir /cara

ENV FLASK_APP=/cara/app.py
ENV FLASK_ENV=development

COPY cara /cara

VOLUME /cara

EXPOSE 5000

CMD flask run --host=0.0.0.0