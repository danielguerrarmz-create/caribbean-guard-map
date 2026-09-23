import Link from "next/link";

const VARIANT_CLASSES = {
  primary: "bg-accent text-white hover:opacity-90",
  outline:
    "border-2 border-accent text-accent hover:bg-accent hover:text-white",
  inverse: "bg-white text-accent hover:bg-white/90",
} as const;

type ButtonBlockProps = {
  text: string;
  link: string;
  variant?: keyof typeof VARIANT_CLASSES;
  className?: string;
};

export default function ButtonBlock({
  text,
  link,
  variant = "primary",
  className = "",
}: ButtonBlockProps) {
  if (!text || !link) return null;

  const isExternal = /^https?:\/\//.test(link) || link.startsWith("mailto:");

  return (
    <Link
      href={link}
      target={isExternal ? "_blank" : undefined}
      rel={isExternal ? "noopener noreferrer" : undefined}
      className={`inline-block rounded-md px-6 py-3 text-sm font-semibold whitespace-nowrap transition-colors ${VARIANT_CLASSES[variant]} ${className}`}
    >
      {text}
    </Link>
  );
}
