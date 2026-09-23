"use client";

import { useState } from "react";
import type { AccordionItem, Theme } from "@/lib/content-types";

type AccordionProps = {
  theme?: Theme;
  items: AccordionItem[];
  allowMultiple?: boolean;
};

export default function Accordion({
  theme = "white",
  items,
  allowMultiple = false,
}: AccordionProps) {
  const [openItems, setOpenItems] = useState<Set<number>>(new Set());

  const toggle = (index: number) => {
    setOpenItems((prev) => {
      const next = allowMultiple ? new Set(prev) : new Set<number>();
      if (prev.has(index)) {
        next.delete(index);
      } else {
        next.add(index);
      }
      return next;
    });
  };

  return (
    <section className={`theme-${theme} bg-background text-foreground`}>
      <div className="mx-auto max-w-3xl px-6 py-16 md:py-24">
        <div className="flex flex-col divide-y divide-foreground/10 border-y border-foreground/10">
          {items.map((item, i) => {
            const isOpen = openItems.has(i);
            return (
              <div key={item.title + i}>
                <button
                  type="button"
                  className="flex w-full items-center justify-between gap-4 py-5 text-left"
                  aria-expanded={isOpen}
                  onClick={() => toggle(i)}
                >
                  <span className="text-lg font-semibold">{item.title}</span>
                  <span
                    className={`shrink-0 text-2xl leading-none text-accent transition-transform ${
                      isOpen ? "rotate-45" : ""
                    }`}
                    aria-hidden="true"
                  >
                    +
                  </span>
                </button>
                <div
                  className={`grid transition-[grid-template-rows] duration-300 ${
                    isOpen ? "grid-rows-[1fr]" : "grid-rows-[0fr]"
                  }`}
                >
                  <div className="overflow-hidden">
                    <div
                      className="rich-text pb-6 text-foreground/80"
                      dangerouslySetInnerHTML={{ __html: item.contentHtml }}
                    />
                  </div>
                </div>
              </div>
            );
          })}
        </div>
      </div>
    </section>
  );
}
