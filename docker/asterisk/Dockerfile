FROM debian:bullseye-slim

# Установка Asterisk
RUN apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y \
    asterisk \
    asterisk-core-sounds-ru \
    asterisk-core-sounds-ru-wav \
    curl \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Создаем необходимые директории
RUN mkdir -p /var/lib/asterisk/agi-bin && \
    chmod 755 /var/lib/asterisk/agi-bin

# Копируем конфигурацию
COPY etc/* /etc/asterisk/

# Права на AGI скрипты
RUN chmod +x /var/lib/asterisk/agi-bin/* || true

EXPOSE 5060/udp 5060/tcp 10000-10099/udp 5038

CMD ["asterisk", "-f", "-vvvg", "-c"]
