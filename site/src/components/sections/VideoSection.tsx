"use client";

import { useRef, useState } from "react";
import type { Theme } from "@/lib/content-types";

type VideoSectionProps = {
  theme?: Theme;
  title?: string;
  src?: string;
  poster?: string;
  autoPlay?: boolean;
  loop?: boolean;
  muted?: boolean;
  controls?: boolean;
};

export default function VideoSection({
  theme = "white",
  title,
  src,
  poster,
  autoPlay = false,
  loop = false,
  muted = false,
  controls = true,
}: VideoSectionProps) {
  const videoRef = useRef<HTMLVideoElement>(null);
  const [started, setStarted] = useState(autoPlay);

  return (
    <section className={`theme-${theme} bg-background text-foreground`}>
      <div className="mx-auto max-w-5xl px-6 py-16 md:py-24">
        {title && (
          <h2 className="mb-8 text-center text-2xl font-semibold tracking-wide uppercase">
            {title}
          </h2>
        )}
        <div className="relative aspect-video overflow-hidden rounded-lg bg-black">
          {src && (
            <>
              <video
                ref={videoRef}
                src={src}
                poster={poster}
                autoPlay={autoPlay}
                loop={loop}
                muted={muted || autoPlay}
                controls={controls && started}
                playsInline
                className="h-full w-full object-cover"
                onPlay={() => setStarted(true)}
              />
              {controls && !started && (
                <button
                  type="button"
                  onClick={() => videoRef.current?.play()}
                  aria-label="Reproducir video"
                  className="absolute inset-0 flex items-center justify-center bg-black/10 transition hover:bg-black/20"
                >
                  <span className="flex h-16 w-16 items-center justify-center rounded-full bg-white/90 shadow-lg">
                    <svg viewBox="0 0 24 24" className="ml-1 h-7 w-7 fill-black">
                      <path d="M8 5v14l11-7z" />
                    </svg>
                  </span>
                </button>
              )}
            </>
          )}
        </div>
      </div>
    </section>
  );
}
