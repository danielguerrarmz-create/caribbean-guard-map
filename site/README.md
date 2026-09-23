This is a [Next.js](https://nextjs.org) project bootstrapped with [`create-next-app`](https://nextjs.org/docs/app/api-reference/cli/create-next-app).

## Getting Started

First, run the development server:

```bash
npm run dev
# or
yarn dev
# or
pnpm dev
# or
bun dev
```

Open [http://localhost:3000](http://localhost:3000) with your browser to see the result.

You can start editing the page by modifying `app/page.tsx`. The page auto-updates as you edit the file.

## Instagram feed (Behold.so)

The homepage Instagram feed (`src/components/sections/InstagramFeed.tsx`) is a live feed, not static embeds. It reads a Behold.so JSON feed URL from `NEXT_PUBLIC_BEHOLD_FEED_URL` at build/runtime. Until that variable is set, the component falls back to a link card pointing at instagram.com/caribbeanguard, so the site is never broken by a missing feed.

One-time setup (needs an Instagram login, so this step belongs to the site owner, not a developer):

1. Create a free account at [behold.so](https://behold.so) and connect the `@caribbeanguard` Instagram account.
2. Create a feed and copy its JSON feed URL (`https://feeds.behold.so/<FEED_ID>`).
3. Set `NEXT_PUBLIC_BEHOLD_FEED_URL` to that URL — locally in `.env.local`, and in the hosting provider's environment variables for production.
4. Redeploy (or restart `npm run dev`). The homepage should switch from the fallback card to the live photo grid automatically.

## Learn More

To learn more about Next.js, take a look at the following resources:

- [Next.js Documentation](https://nextjs.org/docs) - learn about Next.js features and API.
- [Learn Next.js](https://nextjs.org/learn) - an interactive Next.js tutorial.

You can check out [the Next.js GitHub repository](https://github.com/vercel/next.js) - your feedback and contributions are welcome!

## Deploy on Vercel

The easiest way to deploy your Next.js app is to use the [Vercel Platform](https://vercel.com/new?utm_medium=default-template&filter=next.js&utm_source=create-next-app&utm_campaign=create-next-app-readme) from the creators of Next.js.

Check out our [Next.js deployment documentation](https://nextjs.org/docs/app/building-your-application/deploying) for more details.
