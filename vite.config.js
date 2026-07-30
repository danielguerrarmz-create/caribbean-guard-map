import { defineConfig } from "vite";

export default defineConfig({
  // site/ is the website. The safety map is copied into site/mapa/app/ by
  // tools/build_site.py so the whole thing is navigable as one tree locally.
  // In production the map deploys separately, because the entire point is that
  // it does not sit behind anything heavier than itself.
  root: "site",

  server: {
    // Bound to 0.0.0.0 on purpose. This is a map for someone standing on a beach
    // holding a phone, and it cannot be judged in a desktop window. Vite prints a
    // LAN address; open that on a real phone on the same wifi.
    host: true,
    port: 5173,
    open: false
  },

  build: {
    outDir: "../dist",
    emptyOutDir: true,
    assetsInlineLimit: 0   // never inline the imagery; the load strategy depends
                           // on base.webp staying a separate deferred request
  }
});
