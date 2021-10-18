FROM ubuntu:20.04
ENV DEBIAN_FRONTEND noninteractive

RUN apt-get -qq -y update \
    && apt-get -q -y dist-upgrade \
    && apt-get -q -y install locales libreoffice libreoffice-writer psmisc curl \
    libreoffice-impress libreoffice-common fonts-opensymbol hyphen-fr hyphen-de \
    hyphen-en-us hyphen-it hyphen-ru fonts-dejavu fonts-dejavu-core fonts-dejavu-extra \
    fonts-droid-fallback fonts-dustin fonts-f500 fonts-fanwood fonts-freefont-ttf \
    fonts-liberation fonts-lmodern fonts-lyx fonts-sil-gentium fonts-texgyre \
    fonts-tlwg-purisa python3-pip python3-uno python3-lxml python3-icu unoconv \
    && apt-get -qq -y autoremove \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/* \
    && localedef -i en_US -c -f UTF-8 -A /usr/share/locale/locale.alias en_US.UTF-8

WORKDIR /app

RUN mkdir /app/templates
RUN mkdir /app/rendered

ENV LANG C.UTF-8
ENV LANGUAGE C.UTF-8
ENV LC_ALL C.UTF-8

RUN groupadd -g 1000 -r app \
    && useradd -m -u 1000 -d /tmp -s /bin/false -g app app

COPY requirements.txt /app
RUN pip3 install --no-cache-dir -q -r /app/requirements.txt

COPY . /app

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "7000"]
