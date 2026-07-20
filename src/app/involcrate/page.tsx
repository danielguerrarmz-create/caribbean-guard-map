import type { Metadata } from "next";
import RichTextSection from "@/components/sections/RichTextSection";
import GalleryGrid from "@/components/sections/GalleryGrid";
import { involcrateContent } from "@/content/involcrate";

export const metadata: Metadata = {
  title: "Involúcrate",
  description:
    "Involúcrate con Caribbean Guard: únete al Swim Club, Lifesaving Club o Freediving Club, o contáctanos para colaborar con la comunidad del Caribe Sur.",
};

export default function InvolcratePage() {
  return (
    <>
      <RichTextSection theme="light" html={involcrateContent.intro.html} />
      <GalleryGrid theme="light" images={involcrateContent.gallery} />
      <RichTextSection theme="light" html={involcrateContent.contact.html} />
    </>
  );
}
