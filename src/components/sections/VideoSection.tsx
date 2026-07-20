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
            <video
              src={src}
              poster={poster}
              autoPlay={autoPlay}
              loop={loop}
              muted={muted || autoPlay}
              controls={controls}
              playsInline
              className="h-full w-full object-cover"
            />
          )}
        </div>
      </div>
    </section>
  );
}
