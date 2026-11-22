// Vite: builds the review GUI into dist/, which `ontology-builder serve` serves (plan 0002).
// In `npm run dev`, /api goes to a running `ontology-builder serve` on its default port; the
// proxy sets the Host and Origin headers to the server's own, so its local-only guards pass.
import react from "@vitejs/plugin-react";
import { defineConfig } from "vite";

const apiPort = process.env.ONTOLOGY_BUILDER_PORT ?? "8765";

export default defineConfig({
  plugins: [react()],
  server: {
    host: "127.0.0.1",
    proxy: {
      "/api": {
        target: `http://127.0.0.1:${apiPort}`,
        changeOrigin: true,
        headers: { origin: `http://127.0.0.1:${apiPort}` },
      },
    },
  },
  build: { outDir: "dist", emptyOutDir: true },
});
