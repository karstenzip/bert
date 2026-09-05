FROM oven/bun:1-alpine AS base

WORKDIR /usr/src/app

ENV NODE_ENV=production

FROM base AS builder

COPY package.json bun.lock ./
RUN bun ci

COPY . .
RUN bun run build

FROM base AS runner

COPY --from=builder --chown=bun /usr/src/app/.output ./

USER bun
EXPOSE 3000/tcp

CMD ["bun", "run", "server/index.mjs"]
