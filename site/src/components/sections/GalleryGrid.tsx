"use client";

import Image from "next/image";
import { useEffect, useState } from "react";
import type { RichImage, Theme } from "@/lib/content-types";

type GalleryGridProps = {
  theme?: Theme;
  images: RichImage[];
};

export default function GalleryGrid({ theme = "white", images }: GalleryGridProps) {
  const [activeIndex, setActiveIndex] = useState<number | null>(null);
  const hasMultiple = images.length > 1;

  useEffect(() => {
    if (activeIndex === null) return;

    document.body.style.overflow = "hidden";
    const onKeyDown = (e: KeyboardEvent) => {
      if (e.key === "Escape") setActiveIndex(null);
      if (e.key === "ArrowRight") {
        setActiveIndex((i) => (i === null ? i : (i + 1) % images.length));
      }
      if (e.key === "ArrowLeft") {
        setActiveIndex((i) => (i === null ? i : (i - 1 + images.length) % images.length));
      }
    };
    window.addEventListener("keydown", onKeyDown);

    return () => {
      document.body.style.overflow = "";
      window.removeEventListener("keydown", onKeyDown);
    };
  }, [activeIndex, images.length]);

  const active = activeIndex !== null ? images[activeIndex] : null;

  return (
    <section className={`theme-${theme} bg-background`}>
      <div className="mx-auto max-w-6xl px-6 py-16 md:py-24">
        <div className="grid grid-cols-2 gap-3 sm:grid-cols-3">
          {images.map((image, i) => (
            <button
              key={image.url}
              type="button"
              onClick={() => setActiveIndex(i)}
              className="group relative aspect-square overflow-hidden rounded-lg"
              aria-label={`Ver imagen ${i + 1}`}
            >
              <Image
                src={image.url}
                alt={image.alt}
                fill
                unoptimized
                referrerPolicy="no-referrer"
                className="object-cover transition-transform duration-300 group-hover:scale-105"
              />
            </button>
          ))}
        </div>
      </div>

      {active && (
        <div
          className="fixed inset-0 z-50 flex items-center justify-center bg-black/90 p-4"
          onClick={() => setActiveIndex(null)}
        >
          <button
            type="button"
            className="absolute top-4 right-4 text-3xl leading-none text-white"
            aria-label="Cerrar"
            onClick={() => setActiveIndex(null)}
          >
            &times;
          </button>

          {hasMultiple && (
            <button
              type="button"
              className="absolute left-4 text-4xl text-white/80 hover:text-white"
              aria-label="Anterior"
              onClick={(e) => {
                e.stopPropagation();
                setActiveIndex((i) => (i === null ? i : (i - 1 + images.length) % images.length));
              }}
            >
              &#8249;
            </button>
          )}

          <div className="relative h-[80vh] w-full max-w-4xl" onClick={(e) => e.stopPropagation()}>
            <Image
              src={active.url}
              alt={active.alt}
              fill
              unoptimized
              referrerPolicy="no-referrer"
              className="object-contain"
            />
          </div>

          {hasMultiple && (
            <button
              type="button"
              className="absolute right-4 text-4xl text-white/80 hover:text-white"
              aria-label="Siguiente"
              onClick={(e) => {
                e.stopPropagation();
                setActiveIndex((i) => (i === null ? i : (i + 1) % images.length));
              }}
            >
              &#8250;
            </button>
          )}
        </div>
      )}
    </section>
  );
}
