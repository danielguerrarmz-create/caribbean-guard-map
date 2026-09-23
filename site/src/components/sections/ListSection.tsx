"use client";

import { useRef } from "react";
import type { ButtonData, ListItem, ListLayout, Theme } from "@/lib/content-types";
import ButtonBlock from "./ButtonBlock";
import ImageBlock from "./ImageBlock";

type ListSectionProps = {
  theme?: Theme;
  title?: string;
  layout: ListLayout;
  items: ListItem[];
  sectionButton?: ButtonData | null;
};

function ListItemCard({ item, className = "" }: { item: ListItem; className?: string }) {
  return (
    <div className={`flex flex-col gap-4 ${className}`}>
      {item.image && (
        <ImageBlock url={item.image.url} alt={item.title} className="aspect-[4/3] rounded-lg" />
      )}
      <div className="flex flex-1 flex-col gap-2">
        <h3 className="text-lg font-semibold">{item.title}</h3>
        <div
          className="rich-text-compact line-clamp-5 text-sm text-foreground/80"
          dangerouslySetInnerHTML={{ __html: item.descriptionHtml }}
        />
        {item.button?.text && item.button?.link && (
          <ButtonBlock
            text={item.button.text}
            link={item.button.link}
            variant="outline"
            className="mt-2 self-start"
          />
        )}
      </div>
    </div>
  );
}

function CarouselArrowButton({
  direction,
  onClick,
}: {
  direction: "left" | "right";
  onClick: () => void;
}) {
  return (
    <button
      type="button"
      onClick={onClick}
      aria-label={direction === "left" ? "Anterior" : "Siguiente"}
      className={`absolute top-1/2 z-10 hidden h-12 w-12 -translate-y-1/2 items-center justify-center rounded-full bg-accent text-white shadow-md transition-opacity hover:opacity-90 md:flex ${
        direction === "left" ? "-left-6" : "-right-6"
      }`}
    >
      <svg viewBox="0 0 24 24" className="h-5 w-5 fill-current" aria-hidden="true">
        {direction === "left" ? (
          <path d="M15.41 7.41 14 6l-6 6 6 6 1.41-1.41L10.83 12z" />
        ) : (
          <path d="M8.59 16.59 10 18l6-6-6-6-1.41 1.41L13.17 12z" />
        )}
      </svg>
    </button>
  );
}

export default function ListSection({
  theme = "white",
  title,
  layout,
  items,
  sectionButton,
}: ListSectionProps) {
  const scrollRef = useRef<HTMLDivElement>(null);

  const scrollByCard = (direction: "left" | "right") => {
    const el = scrollRef.current;
    if (!el) return;
    const amount = el.clientWidth * 0.9 * (direction === "left" ? -1 : 1);
    el.scrollBy({ left: amount, behavior: "smooth" });
  };

  return (
    <section className={`theme-${theme} bg-background text-foreground`}>
      <div className="mx-auto max-w-6xl px-6 py-16 md:py-24">
        {title && (
          <div
            className="mb-10 text-center text-2xl font-semibold tracking-wide uppercase"
            dangerouslySetInnerHTML={{ __html: title }}
          />
        )}

        {layout === "carousel" ? (
          <div className="relative">
            <CarouselArrowButton direction="left" onClick={() => scrollByCard("left")} />
            <div
              ref={scrollRef}
              className="no-scrollbar flex snap-x snap-mandatory gap-6 overflow-x-auto pb-4"
            >
              {items.map((item) => (
                <ListItemCard
                  key={item.title}
                  item={item}
                  className="w-[85%] shrink-0 snap-start sm:w-[380px]"
                />
              ))}
            </div>
            <CarouselArrowButton direction="right" onClick={() => scrollByCard("right")} />
          </div>
        ) : (
          <div className="grid gap-x-8 gap-y-12 sm:grid-cols-2 lg:grid-cols-3">
            {items.map((item) => (
              <ListItemCard key={item.title} item={item} />
            ))}
          </div>
        )}

        {sectionButton?.text && sectionButton?.link && (
          <div className="mt-12 flex justify-center">
            <ButtonBlock text={sectionButton.text} link={sectionButton.link} />
          </div>
        )}
      </div>
    </section>
  );
}
