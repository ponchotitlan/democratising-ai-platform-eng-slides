# Static sites served by nginx, running as a non-root user on port 8080.
# One image per deck, picked with --build-arg DECK=<folder> (ai-builders or websummit):
#   /         the chosen deck  (<DECK>/index.html)
#   /images/  shared by both   (images/)
#   /fonts/   shared by both   (fonts/)
FROM nginxinc/nginx-unprivileged:1.27-alpine

COPY nginx/default.conf /etc/nginx/conf.d/default.conf
COPY nginx/security-headers.conf /etc/nginx/snippets/security-headers.conf

ARG DECK=ai-builders
COPY ${DECK}/index.html /usr/share/nginx/html/index.html
COPY images/ /usr/share/nginx/html/images/
COPY fonts/ /usr/share/nginx/html/fonts/

EXPOSE 8080

HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
  CMD wget -q -O /dev/null http://127.0.0.1:8080/healthz || exit 1
