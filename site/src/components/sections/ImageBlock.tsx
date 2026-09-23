import Image from "next/image";

type ImageBlockProps = {
  url: string;
  alt: string;
  className?: string;
  priority?: boolean;
};

export default function ImageBlock({
  url,
  alt,
  className = "",
  priority = false,
}: ImageBlockProps) {
  return (
    <div className={`relative overflow-hidden ${className}`}>
      <Image
        src={url}
        alt={alt}
        fill
        unoptimized
        priority={priority}
        referrerPolicy="no-referrer"
        className="object-cover"
      />
    </div>
  );
}
