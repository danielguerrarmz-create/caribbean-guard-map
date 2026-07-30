import { defineConfig } from "vite";

export default defineConfig({
  // web/ is the site root. index.html sits there and references img/ and data/
  // with relative paths, which is also how it will sit on Cloudflare Pages, so
  // dev and production resolve identically.
  root: "web",

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
