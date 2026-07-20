import type { ButtonData, RichImage, Theme } from "@/lib/content-types";
import ButtonBlock from "./ButtonBlock";
import ImageBlock from "./ImageBlock";

type RichTextSectionProps = {
  theme?: Theme;
  html: string[];
  image?: RichImage;
  imagePosition?: "left" | "right";
  buttons?: ButtonData[];
  columns?: 1 | 2;
};

export default function RichTextSection({
  theme = "white",
  html,
  image,
  imagePosition = "right",
  buttons = [],
  columns = 1,
}: RichTextSectionProps) {
  const buttonVariant = theme === "bright" || theme === "black" ? "inverse" : "primary";

  const textBlocks = (
    <div
      className={
        columns === 2 && !image
          ? "grid gap-x-12 gap-y-8 md:grid-cols-2"
          : "flex flex-col gap-8"
      }
    >
      {html.map((block, i) => (
        <div key={i} className="rich-text" dangerouslySetInnerHTML={{ __html: block }} />
      ))}
    </div>
  );

  return (
    <section className={`theme-${theme} bg-background text-foreground`}>
      <div className="mx-auto max-w-6xl px-6 py-16 md:py-24">
        {image ? (
          <div className="grid items-center gap-12 md:grid-cols-2">
            <div className={imagePosition === "left" ? "md:order-2" : ""}>
              {textBlocks}
              {buttons.length > 0 && (
                <div className="mt-8 flex flex-wrap gap-4">
                  {buttons.map((btn) => (
                    <ButtonBlock key={btn.link + btn.text} text={btn.text} link={btn.link} variant={buttonVariant} />
                  ))}
                </div>
              )}
            </div>
            <ImageBlock
              url={image.url}
              alt={image.alt}
              className={`aspect-[4/3] rounded-lg ${imagePosition === "left" ? "md:order-1" : ""}`}
            />
          </div>
        ) : (
          <div className={columns === 1 ? "mx-auto max-w-3xl" : ""}>
            {textBlocks}
            {buttons.length > 0 && (
              <div className="mt-8 flex flex-wrap gap-4">
                {buttons.map((btn) => (
                  <ButtonBlock key={btn.link + btn.text} text={btn.text} link={btn.link} />
                ))}
              </div>
            )}
          </div>
        )}
      </div>
    </section>
  );
}
