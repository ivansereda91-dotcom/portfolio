#!/bin/bash
# Сайт-портфолио на ivansereda.fr: bash /opt/portfolio/setup.sh  (повторный запуск — обновление)
set -e
APP=/opt/portfolio
WWW=/var/www/portfolio
DOMAIN=ivansereda.fr

export DEBIAN_FRONTEND=noninteractive
apt-get install -y -q python3-pil >/dev/null

echo "== Собираю страницы =="
python3 "$APP/build.py"
mkdir -p "$WWW/img"
cp -r "$APP/site/." "$WWW/"

echo "== Загружаю фото (первый раз — пару минут) =="
python3 "$APP/images.py" "$WWW/img" || echo "Часть фото не загрузилась — запусти setup.sh ещё раз"

if ! grep -q "^$DOMAIN {" /etc/caddy/Caddyfile; then
  cat >> /etc/caddy/Caddyfile <<CADDY

$DOMAIN {
	root * $WWW
	encode zstd gzip
	header /img/* Cache-Control "public, max-age=2592000"
	file_server
	handle_errors {
		rewrite * /404.html
		file_server
	}
}

www.$DOMAIN {
	redir https://$DOMAIN{uri} permanent
}
CADDY
fi
caddy validate --config /etc/caddy/Caddyfile --adapter caddyfile >/dev/null
systemctl reload caddy
echo
echo "Готово: https://$DOMAIN"
