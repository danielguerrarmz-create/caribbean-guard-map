import type { Metadata } from "next";
import RichTextSection from "@/components/sections/RichTextSection";
import GalleryGrid from "@/components/sections/GalleryGrid";
import { swimClubContent } from "@/content/swim-club";

export const metadata: Metadata = {
  title: "Swim Club",
  description:
    "El Swim Club de Caribbean Guard ofrece natación en aguas abiertas y clases gratuitas de Swim School para la comunidad del Caribe Sur.",
};

export default function SwimClubPage() {
  return (
    <>
      <RichTextSection theme="light" html={swimClubContent.intro.html} image={swimClubContent.intro.image} />
      <GalleryGrid theme="white" images={swimClubContent.gallery} />
    </>
  );
}
