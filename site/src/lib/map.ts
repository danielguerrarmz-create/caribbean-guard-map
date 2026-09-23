// The coastal safety map is a separate static deployment (see ../web in the
// caribbean-guard-map repo), so the site links out to it rather than routing.
// Override per environment with NEXT_PUBLIC_MAP_URL, e.g. http://127.0.0.1:5174/
// while running the map locally.
export const MAP_URL =
  process.env.NEXT_PUBLIC_MAP_URL ?? "https://web-five-beta-p7wt9cgwmf.vercel.app/";
