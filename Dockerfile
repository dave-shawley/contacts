FROM python:3.8-alpine AS builder
RUN mkdir /source
WORKDIR /source
COPY setup.cfg /source/
COPY setup.py  /source/
COPY contacts  /source/contacts/
RUN apk --update add libpq postgresql-dev musl-dev gcc
RUN pip install wheel \
 && python setup.py bdist_wheel \
 && mv dist/*.whl /tmp/
RUN pip download psycopg2-binary \
 && tar xfz psycopg2-binary*.tar.gz \
 && cd psycopg2-binary* \
 && python setup.py bdist_wheel \
 && ls dist/ \
 && mv dist/*.whl /tmp/


FROM python:3.8-alpine
EXPOSE 8000
CMD ["contacts-api"]

COPY --from=builder /tmp/*.whl /tmp/
RUN apk --update add libpq \
 && pip install /tmp/psycopg2*.whl \
 && pip install /tmp/contacts*.whl \
 && rm -f /var/cache/apk/* \
 && rm -fR /root/.cache
