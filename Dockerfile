# Static sites served by nginx, running as a non-root user on port 8080.
#   /            the AI Builders deck   (ai-builders/)
#   /websummit/  the Web Summit deck    (websummit/)
#   /images/     shared by both         (images/)
#   /fonts/      shared by both         (fonts/)
FROM nginxinc/nginx-unprivileged:1.27-alpine

COPY nginx/default.conf /etc/nginx/conf.d/default.conf
COPY nginx/security-headers.conf /etc/nginx/snippets/security-headers.conf

COPY ai-builders/index.html /usr/share/nginx/html/index.html
COPY websummit/ /usr/share/nginx/html/websummit/
COPY images/ /usr/share/nginx/html/images/
COPY fonts/ /usr/share/nginx/html/fonts/

EXPOSE 8080

HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
  CMD wget -q -O /dev/null http://127.0.0.1:8080/healthz || exit 1
