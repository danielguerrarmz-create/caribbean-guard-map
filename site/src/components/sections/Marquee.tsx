import type { Theme } from "@/lib/content-types";

type MarqueeProps = {
  theme?: Theme;
  text: string;
  speed?: number;
};

export default function Marquee({ theme = "bright", text, speed = 20 }: MarqueeProps) {
  const repeated = Array.from({ length: 6 });

  return (
    <section className={`theme-${theme} overflow-hidden bg-background py-6`}>
      <div className="flex w-max animate-marquee" style={{ animationDuration: `${speed}s` }}>
        {[0, 1].map((copy) => (
          <div key={copy} className="flex shrink-0 items-center" aria-hidden={copy === 1}>
            {repeated.map((_, i) => (
              <span
                key={i}
                className="mx-6 flex items-center gap-6 text-3xl font-semibold whitespace-nowrap text-foreground md:text-5xl"
              >
                {text}
                <span className="text-accent" aria-hidden="true">
                  &bull;
                </span>
              </span>
            ))}
          </div>
        ))}
      </div>
    </section>
  );
}
