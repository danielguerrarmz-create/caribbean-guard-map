import Image from "next/image";
import type { ButtonData, RichImage, Theme } from "@/lib/content-types";
import ButtonBlock from "./ButtonBlock";

type HeroSectionProps = {
  theme?: Theme;
  backgroundImage?: RichImage;
  overlayOpacity?: number;
  align?: "left" | "center";
  minHeightClassName?: string;
  heading: string;
  body?: string;
  button?: ButtonData;
};

export default function HeroSection({
  theme = "black",
  backgroundImage,
  overlayOpacity = 0.35,
  align = "center",
  minHeightClassName = "min-h-[70vh]",
  heading,
  body,
  button,
}: HeroSectionProps) {
  const hasBackgroundImage = Boolean(backgroundImage);

  return (
    <section
      className={`theme-${theme} relative flex items-center overflow-hidden bg-background ${minHeightClassName}`}
    >
      {backgroundImage && (
        <div className="absolute inset-0">
          <Image
            src={backgroundImage.url}
            alt={backgroundImage.alt}
            fill
            unoptimized
            priority
            referrerPolicy="no-referrer"
            className="object-cover"
          />
          <div
            className="absolute inset-0 bg-black"
            style={{ opacity: overlayOpacity }}
          />
        </div>
      )}

      <div
        className={`relative z-10 mx-auto flex w-full max-w-5xl flex-col gap-6 px-6 py-24 ${
          align === "center" ? "items-center text-center" : "items-start text-left"
        } ${hasBackgroundImage ? "text-white" : "text-foreground"}`}
      >
        <div className="rich-text" dangerouslySetInnerHTML={{ __html: heading }} />
        {body && (
          <div
            className="rich-text max-w-2xl text-lg opacity-90"
            dangerouslySetInnerHTML={{ __html: body }}
          />
        )}
        {button && (
          <ButtonBlock
            text={button.text}
            link={button.link}
            variant={hasBackgroundImage ? "inverse" : "primary"}
          />
        )}
      </div>
    </section>
  );
}
